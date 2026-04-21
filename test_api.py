#!/usr/bin/env python3
"""
Script test API Groq
"""

import asyncio
import os
from dotenv import load_dotenv
from agent.main_agent import MainAgent
from engine.llm_judge import LLMJudge

load_dotenv()

async def test_agent():
    """Test Agent API"""
    print("=" * 60)
    print("🧪 Test Agent API")
    print("=" * 60)
    
    agent = MainAgent()
    
    # Test 1: Câu hỏi đơn giản
    print("\n📝 Test 1: Câu hỏi đơn giản")
    question = "Cơ sở dữ liệu quốc gia hoạt động bao nhiêu giờ mỗi ngày?"
    context = "Cơ sở dữ liệu quốc gia về thủ tục hành chính phải bảo đảm hoạt động liên tục 24 giờ trong tất cả các ngày."
    
    print(f"Câu hỏi: {question}")
    print(f"Context: {context}")
    
    response = await agent.query(question, context)
    print(f"Câu trả lời: {response['answer']}")
    print(f"Metadata: {response['metadata']}")
    
    # Test 2: Câu hỏi phức tạp
    print("\n📝 Test 2: Câu hỏi phức tạp")
    question2 = "Tại sao cần thực hiện đánh giá tác động của thủ tục hành chính?"
    context2 = "Việc đánh giá tác động nhằm làm rõ sự cần thiết, tính hợp lý, tính hợp pháp và các chi phí tuân thủ thủ tục hành chính."
    
    print(f"Câu hỏi: {question2}")
    print(f"Context: {context2}")
    
    response2 = await agent.query(question2, context2)
    print(f"Câu trả lời: {response2['answer']}")
    print(f"Metadata: {response2['metadata']}")

async def test_judge():
    """Test Judge API"""
    print("\n" + "=" * 60)
    print("🧪 Test Judge API")
    print("=" * 60)
    
    judge = LLMJudge()
    
    # Test 1: Câu trả lời tốt
    print("\n📝 Test 1: Câu trả lời tốt")
    question = "Cơ sở dữ liệu quốc gia hoạt động bao nhiêu giờ mỗi ngày?"
    answer = "Cơ sở dữ liệu quốc gia hoạt động liên tục 24 giờ trong tất cả các ngày."
    ground_truth = "Bảo đảm hoạt động liên tục 24 (hai mươi tư) giờ trong tất cả các ngày."
    
    print(f"Câu hỏi: {question}")
    print(f"Câu trả lời: {answer}")
    print(f"Ground Truth: {ground_truth}")
    
    result = await judge.evaluate_multi_judge(question, answer, ground_truth)
    print(f"Kết quả: {result}")
    
    # Test 2: Câu trả lời tệ
    print("\n📝 Test 2: Câu trả lời tệ")
    question2 = "Cơ sở dữ liệu quốc gia hoạt động bao nhiêu giờ mỗi ngày?"
    answer2 = "Tôi không biết."
    ground_truth2 = "Bảo đảm hoạt động liên tục 24 giờ trong tất cả các ngày."
    
    print(f"Câu hỏi: {question2}")
    print(f"Câu trả lời: {answer2}")
    print(f"Ground Truth: {ground_truth2}")
    
    result2 = await judge.evaluate_multi_judge(question2, answer2, ground_truth2)
    print(f"Kết quả: {result2}")

async def main():
    print("\n🚀 Bắt đầu test API Groq\n")
    
    # Test Agent
    await test_agent()
    
    # Test Judge
    await test_judge()
    
    print("\n" + "=" * 60)
    print("✅ Test hoàn thành!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
