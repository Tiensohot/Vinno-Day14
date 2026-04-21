import asyncio
import os
from typing import Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEM_PROMPT = """Bạn là chuyên gia tư vấn pháp luật hành chính Việt Nam, chuyên về kiểm soát thủ tục hành chính.

Nguyên tắc bắt buộc:
1. CHỈ trả lời dựa trên nội dung tài liệu được cung cấp trong phần CONTEXT.
2. Trích dẫn cụ thể số điều, khoản liên quan (ví dụ: "Theo Điều 5 Khoản 2b...").
3. Nếu tài liệu không có thông tin cần thiết, trả lời đúng một câu: "Thông tin không có trong tài liệu được cung cấp."
4. Trả lời ngắn gọn, chính xác, đúng trọng tâm — không giải thích dài dòng.
5. Tuyệt đối không suy đoán, không thêm thông tin ngoài context."""


class AgentV2:
    """
    Agent V2 tối ưu: system prompt pháp luật chuyên nghiệp, temperature=0.1,
    max_tokens=1000, yêu cầu trích dẫn điều khoản từ context.
    """
    def __init__(self):
        self.name = "SupportAgent-v2"
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"

    def _call_llm(self, question: str, context: str = "") -> str:
        if context:
            user_prompt = (
                "CONTEXT (tài liệu pháp luật):\n"
                "---\n"
                f"{context}\n"
                "---\n\n"
                f"Câu hỏi: {question}\n\n"
                "Trả lời chính xác, ngắn gọn, có trích dẫn số điều/khoản cụ thể từ tài liệu trên."
            )
        else:
            user_prompt = (
                f"Câu hỏi: {question}\n\n"
                "Không có tài liệu tham khảo. Chỉ trả lời nếu bạn chắc chắn về thông tin pháp luật này."
            )

        try:
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=1000,
            )
            return message.choices[0].message.content
        except Exception as e:
            print(f"⚠️  Error calling OpenAI API (V2): {e}")
            return f"Xin lỗi, không thể trả lời câu hỏi này: {question}"

    async def query(self, question: str, context: str = "") -> Dict:
        answer = self._call_llm(question, context)
        return {
            "answer": answer,
            "contexts": [context] if context else [],
            "metadata": {
                "model": self.model,
                "tokens_used": len(answer.split()),
                "sources": ["openai-api-v2"],
            },
        }


if __name__ == "__main__":
    agent = AgentV2()

    async def test():
        resp = await agent.query(
            "Cơ sở dữ liệu quốc gia phải hoạt động bao nhiêu giờ mỗi ngày?",
            context="Điều 11: Cơ sở dữ liệu quốc gia phải bảo đảm hoạt động liên tục 24 giờ.",
        )
        print(resp)

    asyncio.run(test())
