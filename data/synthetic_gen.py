import json
import asyncio
import os
from typing import List, Dict
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

async def generate_qa_from_text(text: str, num_pairs: int = 5) -> List[Dict]:
    """
    Sử dụng Groq API để tạo các cặp (Question, Expected Answer, Context)
    từ đoạn văn bản cho trước.
    Yêu cầu: Tạo ít nhất 1 câu hỏi 'lừa' (adversarial) hoặc cực khó.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("⚠️  GROQ_API_KEY không được tìm thấy. Sử dụng dữ liệu mẫu từ golden_answer.json")
        return await load_golden_answer()
    
    client = Groq(api_key=api_key)
    
    prompt = f"""Bạn là một chuyên gia tạo test case cho hệ thống AI Evaluation.
Dựa trên đoạn văn bản sau, hãy tạo {num_pairs} câu hỏi-đáp chất lượng cao:

Văn bản:
{text[:1000]}

Yêu cầu:
1. Tạo {num_pairs} câu hỏi khác nhau
2. Mỗi câu hỏi phải có câu trả lời rõ ràng từ văn bản
3. Bao gồm các loại: fact-check, reasoning, multi-hop, adversarial, edge-case
4. Độ khó: easy, medium, hard
5. Trả lời CHÍNH XÁC theo format JSON dưới đây (không có text khác):

[
  {{
    "question": "Câu hỏi?",
    "expected_answer": "Câu trả lời chi tiết",
    "type": "fact-check|reasoning|multi-hop|adversarial|edge-case",
    "difficulty": "easy|medium|hard",
    "source_section": "Tên phần"
  }}
]"""

    try:
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        response_text = message.choices[0].message.content.strip()
        
        # Parse JSON từ response
        try:
            qa_pairs = json.loads(response_text)
            if not isinstance(qa_pairs, list):
                qa_pairs = [qa_pairs]
        except json.JSONDecodeError:
            print(f"⚠️  Không thể parse JSON từ API response. Sử dụng dữ liệu mẫu.")
            return await load_golden_answer()
        
        return qa_pairs
    except Exception as e:
        print(f"⚠️  Lỗi gọi Groq API: {e}. Sử dụng dữ liệu mẫu từ golden_answer.json")
        return await load_golden_answer()

async def load_golden_answer() -> List[Dict]:
    """
    Load dữ liệu từ file golden_answer.json nếu API không khả dụng
    """
    try:
        with open("data/answer/golden_answer.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Không tìm thấy file data/answer/golden_answer.json")
        return []

async def main():
    print("🚀 Bắt đầu tạo Golden Dataset...")
    
    # Nếu file golden_set.jsonl đã tồn tại, hỏi có muốn tạo lại không
    if os.path.exists("data/golden_set.jsonl"):
        print("⚠️  File data/golden_set.jsonl đã tồn tại.")
        print("Sử dụng dữ liệu từ golden_answer.json...")
        qa_pairs = await load_golden_answer()
    else:
        # Tạo dữ liệu mới từ API
        raw_text = "AI Evaluation là một quy trình kỹ thuật nhằm đo lường chất lượng của AI Agent..."
        qa_pairs = await generate_qa_from_text(raw_text, num_pairs=50)
    
    if not qa_pairs:
        print("❌ Không có dữ liệu để tạo golden_set.jsonl")
        return
    
    # Ghi vào file JSONL
    os.makedirs("data", exist_ok=True)
    with open("data/golden_set.jsonl", "w", encoding="utf-8") as f:
        for i, pair in enumerate(qa_pairs, 1):
            # Đảm bảo có các trường bắt buộc
            if "id" not in pair:
                pair["id"] = i
            if "ground_truth_doc_ids" not in pair:
                pair["ground_truth_doc_ids"] = [
                    "19_2014_TT-BTP_249771",
                    "63_2010_ND-CP_106929"
                ]
            if "type" not in pair:
                pair["type"] = "fact-check"
            if "difficulty" not in pair:
                pair["difficulty"] = "easy"
            
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")
    
    print(f"✅ Tạo thành công {len(qa_pairs)} test cases")
    print(f"📁 Lưu vào: data/golden_set.jsonl")

if __name__ == "__main__":
    asyncio.run(main())
