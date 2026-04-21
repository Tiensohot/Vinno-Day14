#!/usr/bin/env python3
"""
Script để convert golden_answer.json sang golden_set.jsonl
"""

import json
import sys

def convert():
    print("=" * 60)
    print("🔄 Convert golden_answer.json → golden_set.jsonl")
    print("=" * 60)
    
    try:
        # Đọc file JSON
        print("\n📖 Đang đọc data/answer/golden_answer.json...")
        with open('data/answer/golden_answer.json', 'r', encoding='utf-8') as f:
            test_cases = json.load(f)
        
        print(f"✅ Đã đọc {len(test_cases)} test cases")
        
        # Convert sang JSONL
        print("\n🔄 Đang convert sang JSONL format...")
        with open('data/golden_set.jsonl', 'w', encoding='utf-8') as f:
            for i, case in enumerate(test_cases, 1):
                # Đảm bảo có ID
                if 'id' not in case:
                    case['id'] = i
                
                # Thêm ground_truth_doc_ids nếu chưa có
                if 'ground_truth_doc_ids' not in case:
                    case['ground_truth_doc_ids'] = [
                        "19_2014_TT-BTP_249771",
                        "63_2010_ND-CP_106929"
                    ]
                
                # Thêm metadata nếu chưa có
                if 'metadata' not in case:
                    case['metadata'] = {
                        'difficulty': case.get('difficulty', 'medium'),
                        'type': case.get('type', 'fact-check'),
                        'category': 'legal'
                    }
                
                # Ghi vào JSONL
                f.write(json.dumps(case, ensure_ascii=False) + '\n')
        
        print(f"✅ Đã tạo file: data/golden_set.jsonl")
        
        # Kiểm tra số lượng
        with open('data/golden_set.jsonl', 'r', encoding='utf-8') as f:
            count = sum(1 for _ in f)
        
        print(f"\n📊 Tổng cộng: {count} test cases")
        
        if count >= 50:
            print("✅ Đạt yêu cầu tối thiểu 50 test cases!")
        else:
            print(f"⚠️  Chỉ có {count} cases, cần ít nhất 50")
        
        print("\n" + "=" * 60)
        print("✅ Conversion hoàn thành!")
        print("=" * 60)
        print("\n📝 Bước tiếp theo:")
        print("1. Chạy: python check_lab.py")
        print("2. Chạy: python main.py")
        print("=" * 60)
        
        return True
        
    except FileNotFoundError as e:
        print(f"❌ Lỗi: Không tìm thấy file {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Lỗi JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

if __name__ == "__main__":
    success = convert()
    sys.exit(0 if success else 1)
