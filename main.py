import asyncio
import json
import os
import time
from engine.runner import BenchmarkRunner
from agent.main_agent import MainAgent
from agent.agent_v2 import AgentV2
from engine.llm_judge import LLMJudge


class ExpertEvaluator:
    async def score(self, _case, _resp):
        return {
            "faithfulness": 0.9,
            "relevancy": 0.8,
            "retrieval": {"hit_rate": 1.0, "mrr": 0.5},
        }


def load_documents(doc_dir: str = "data/processed/md") -> dict:
    """Load tất cả file .md trong thư mục thành dict {doc_id: content}."""
    doc_store = {}
    if not os.path.isdir(doc_dir):
        print(f"⚠️  Thư mục tài liệu không tồn tại: {doc_dir}")
        return doc_store
    for fname in os.listdir(doc_dir):
        if fname.endswith(".md"):
            doc_id = fname[:-3]  # bỏ .md
            fpath = os.path.join(doc_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                doc_store[doc_id] = f.read()
    print(f"📚 Đã load {len(doc_store)} tài liệu: {list(doc_store.keys())}")
    return doc_store


async def run_benchmark_with_results(
    agent_version: str,
    use_api: bool = True,
    agent=None,
    doc_store: dict = None,
):
    print(f"🚀 Khởi động Benchmark cho {agent_version}...")
    print(f"📡 Sử dụng API: {'Có (Groq + OpenAI)' if use_api else 'Không (Mock mode)'}")
    print(f"📖 RAG context: {'Có (' + str(len(doc_store)) + ' tài liệu)' if doc_store else 'Không'}")

    if not os.path.exists("data/golden_set.jsonl"):
        print("❌ Thiếu data/golden_set.jsonl. Hãy chạy 'python data/synthetic_gen.py' trước.")
        return None, None

    with open("data/golden_set.jsonl", "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f if line.strip()]

    if not dataset:
        print("❌ File data/golden_set.jsonl rỗng.")
        return None, None

    judge = LLMJudge(use_api=use_api)
    runner = BenchmarkRunner(agent, ExpertEvaluator(), judge, doc_store=doc_store)
    results = await runner.run_all(dataset)

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "pass")
    summary = {
        "metadata": {
            "version": agent_version,
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "metrics": {
            "avg_score": sum(r["judge"]["final_score"] for r in results) / total,
            "hit_rate": sum(r["ragas"]["retrieval"]["hit_rate"] for r in results) / total,
            "agreement_rate": sum(r["judge"]["agreement_rate"] for r in results) / total,
        },
    }
    return results, summary


async def run_benchmark(version, use_api: bool = True, agent=None, doc_store=None):
    _, summary = await run_benchmark_with_results(
        version, use_api=use_api, agent=agent, doc_store=doc_store
    )
    return summary


async def main():
    use_api = True

    # Load tài liệu pháp luật cho RAG
    doc_store = load_documents()

    # V1: MainAgent baseline — không có RAG, không có system prompt
    v1_summary = await run_benchmark(
        "Agent_V1_Base",
        use_api=use_api,
        agent=MainAgent(),
        doc_store=None,
    )

    # V2: AgentV2 tối ưu — có RAG + system prompt chuyên nghiệp + temperature thấp
    v2_results, v2_summary = await run_benchmark_with_results(
        "Agent_V2_Optimized",
        use_api=use_api,
        agent=AgentV2(),
        doc_store=doc_store,
    )

    if not v1_summary or not v2_summary:
        print("❌ Không thể chạy Benchmark. Kiểm tra lại data/golden_set.jsonl.")
        return

    v1_score = v1_summary["metrics"]["avg_score"]
    v2_score = v2_summary["metrics"]["avg_score"]
    delta = v2_score - v1_score

    print("\n📊 --- KẾT QUẢ SO SÁNH (REGRESSION) ---")
    print(f"V1 Score: {v1_score:.2f}  (passed {v1_summary['metadata']['passed']}/{v1_summary['metadata']['total']})")
    print(f"V2 Score: {v2_score:.2f}  (passed {v2_summary['metadata']['passed']}/{v2_summary['metadata']['total']})")
    print(f"Delta: {'+' if delta >= 0 else ''}{delta:.2f}")

    os.makedirs("reports", exist_ok=True)
    with open("reports/summary.json", "w", encoding="utf-8") as f:
        json.dump(
            {"v1": v1_summary, "v2": v2_summary, "delta": round(delta, 4)},
            f,
            ensure_ascii=False,
            indent=2,
        )
    with open("reports/benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(v2_results, f, ensure_ascii=False, indent=2)

    if delta > 0:
        print("✅ QUYẾT ĐỊNH: CHẤP NHẬN BẢN CẬP NHẬT (APPROVE)")
    else:
        print("❌ QUYẾT ĐỊNH: TỪ CHỐI (BLOCK RELEASE)")


if __name__ == "__main__":
    asyncio.run(main())
