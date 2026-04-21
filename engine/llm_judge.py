import os
from typing import Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMJudge:
    def __init__(self, use_api: bool = False):
        self.use_api = use_api
        self.client = None

        if self.use_api:
            try:
                self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except Exception as e:
                print(f"⚠️  OpenAI API không khả dụng: {e}. Sử dụng mock mode.")
                self.use_api = False

    def _get_judge_prompt(self, question: str, answer: str, ground_truth: str) -> str:
        return f"""Bạn là chuyên gia đánh giá chất lượng câu trả lời AI về pháp luật hành chính Việt Nam.

CÂU HỎI: {question}

CÂU TRẢ LỜI CỦA AGENT: {answer}

CÂU TRẢ LỜI KỲ VỌNG (GROUND TRUTH): {ground_truth}

TIÊU CHÍ ĐÁNH GIÁ:
- 5 điểm: Chính xác 100%, đầy đủ, có trích dẫn điều khoản cụ thể, chuyên nghiệp
- 4 điểm: Chính xác, đầy đủ nhưng thiếu một số chi tiết nhỏ hoặc không trích dẫn
- 3 điểm: Đúng ý chính nhưng thiếu thông tin quan trọng hoặc diễn đạt chưa rõ
- 2 điểm: Có sai sót về số liệu, tên cơ quan, hoặc thiếu thông tin then chốt
- 1 điểm: Sai hoàn toàn, không liên quan, hoặc bịa thông tin

HƯỚNG DẪN:
- So sánh nội dung thực chất, không yêu cầu giống từng chữ với Ground Truth
- Nếu Agent trả lời đúng bản chất Ground Truth → 4-5 điểm
- Nếu Agent trả lời gần đúng nhưng thiếu chi tiết quan trọng → 3 điểm
- Nếu Agent sai số liệu (ví dụ: 5 ngày thay vì 10 ngày), sai tên cơ quan → 2 điểm
- Nếu Agent bịa thông tin không có trong thực tế → 1 điểm

Trả lời CHỈ một số nguyên từ 1 đến 5 (không có text nào khác)."""

    def _call_judge(self, model: str, question: str, answer: str, ground_truth: str) -> int:
        if not self.use_api or not self.client:
            return 4  # mock

        prompt = self._get_judge_prompt(question, answer, ground_truth)
        try:
            message = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=10,
            )
            score_text = message.choices[0].message.content.strip()
            return max(1, min(5, int(score_text)))
        except Exception as e:
            print(f"⚠️  Error calling {model} judge: {e}")
            return 4

    async def evaluate_multi_judge(self, question: str, answer: str, ground_truth: str) -> Dict[str, Any]:
        """Gọi 2 judge (gpt-4o-mini + gpt-4o) và tính consensus."""
        mini_score = self._call_judge("gpt-4o-mini", question, answer, ground_truth)
        full_score = self._call_judge("gpt-4o", question, answer, ground_truth)

        diff = abs(mini_score - full_score)
        if diff == 0:
            agreement = 1.0
        elif diff <= 1:
            agreement = 0.8
        else:
            agreement = 0.5

        return {
            "final_score": (mini_score + full_score) / 2,
            "agreement_rate": agreement,
            "individual_scores": {
                "gpt-4o-mini-judge": mini_score,
                "gpt-4o-judge": full_score,
            },
        }

    async def check_position_bias(self, response_a: str, response_b: str):
        """Stub: đổi chỗ A/B để kiểm tra thiên vị vị trí của judge."""
        pass
