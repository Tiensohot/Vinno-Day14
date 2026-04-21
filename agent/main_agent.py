import asyncio
import os
from typing import Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class MainAgent:
    """Agent dùng OpenAI API để sinh câu trả lời dựa trên context."""
    def __init__(self):
        self.name = "SupportAgent-v1"
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"

    def _call_llm(self, question: str, context: str = "") -> str:
        if context:
            prompt = (
                f"Dựa trên context sau, hãy trả lời câu hỏi:\n\n"
                f"Context: {context}\n\n"
                f"Câu hỏi: {question}\n\n"
                f"Hãy trả lời ngắn gọn, chính xác dựa trên context."
            )
        else:
            prompt = f"Hãy trả lời câu hỏi sau:\n\nCâu hỏi: {question}\n\nTrả lời ngắn gọn, chính xác."

        try:
            message = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500,
            )
            return message.choices[0].message.content
        except Exception as e:
            print(f"⚠️  Error calling OpenAI API: {e}")
            return f"Xin lỗi, tôi không thể trả lời câu hỏi này: {question}"

    async def query(self, question: str, context: str = "") -> Dict:
        answer = self._call_llm(question, context)
        return {
            "answer": answer,
            "contexts": [context] if context else [],
            "metadata": {
                "model": self.model,
                "tokens_used": len(answer.split()),
                "sources": ["openai-api"],
            },
        }

if __name__ == "__main__":
    agent = MainAgent()
    async def test():
        resp = await agent.query("Làm thế nào để đổi mật khẩu?")
        print(resp)
    asyncio.run(test())
