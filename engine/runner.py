import asyncio
import time
from typing import List, Dict

class BenchmarkRunner:
    def __init__(self, agent, evaluator, judge, doc_store: Dict[str, str] = None):
        self.agent = agent
        self.evaluator = evaluator
        self.judge = judge
        self.doc_store = doc_store or {}

    async def run_single_test(self, test_case: Dict) -> Dict:
        start_time = time.perf_counter()

        # Build context from ground_truth_doc_ids if not provided in test_case
        context = test_case.get("context", "")
        if not context and self.doc_store:
            doc_ids = test_case.get("ground_truth_doc_ids", [])
            relevant_docs = [self.doc_store[doc_id] for doc_id in doc_ids if doc_id in self.doc_store]
            context = "\n\n---\n\n".join(relevant_docs)

        response = await self.agent.query(test_case["question"], context=context)
        latency = time.perf_counter() - start_time

        ragas_scores = await self.evaluator.score(test_case, response)

        judge_result = await self.judge.evaluate_multi_judge(
            test_case["question"],
            response["answer"],
            test_case["expected_answer"]
        )

        return {
            "test_case": test_case["question"],
            "agent_response": response["answer"],
            "latency": latency,
            "ragas": ragas_scores,
            "judge": judge_result,
            "status": "fail" if judge_result["final_score"] < 3 else "pass"
        }

    async def run_all(self, dataset: List[Dict], batch_size: int = 5) -> List[Dict]:
        """Chạy song song bằng asyncio.gather với giới hạn batch_size để không bị Rate Limit."""
        results = []
        for i in range(0, len(dataset), batch_size):
            batch = dataset[i:i + batch_size]
            tasks = [self.run_single_test(case) for case in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
        return results
