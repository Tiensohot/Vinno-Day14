#!/usr/bin/env python3
"""
Script để convert output từ NotebookLM sang JSONL format cho golden_set.jsonl
"""

import json
import sys
from pathlib import Path

def convert_notebooklm_to_jsonl(input_file: str, output_file: str = "data/golden_set.jsonl"):
    """
    Convert JSON array từ NotebookLM sang JSONL format với ground_truth_doc_ids
    
    Args:
        input_file: Đường dẫn file JSON từ NotebookLM
        output_file: Đường dẫn file JSONL output
    """
    try:
        # Đọc file JSON từ NotebookLM
        print(f"📖 Đang đọc file: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
            # Nếu là JSON array
            if content.startswith('['):
                test_cases = json.loads(content)
            # Nếu là JSON object
            elif content.startswith('{'):
                test_cases = [json.loads(content)]
            else:
                print("❌ File không phải JSON hợp lệ")
                return False
        
        print(f"✅ Đã đọc {len(test_cases)} test cases")
        
        # Convert sang JSONL
        print(f"🔄 Đang convert sang JSONL format...")
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, case in enumerate(test_cases, 1):
                # Đảm bảo có các trường bắt buộc
                if 'id' not in case:
                    case['id'] = i
                
                if 'question' not in case or 'expected_answer' not in case:
                    print(f"⚠️  Case {i} thiếu 'question' hoặc 'expected_answer', bỏ qua")
                    continue
                
                # Thêm ground_truth_doc_ids
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
        
        print(f"✅ Đã tạo file: {output_file}")
        
        # Kiểm tra số lượng
        with open(output_file, 'r', encoding='utf-8') as f:
            count = sum(1 for _ in f)
        
        print(f"📊 Tổng cộng: {count} test cases")
        
        if count >= 50:
            print("✅ Đạt yêu cầu tối thiểu 50 test cases!")
            return True
        else:
            print(f"⚠️  Chỉ có {count} cases, cần ít nhất 50")
            return False
            
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {input_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Lỗi JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def validate_jsonl(jsonl_file: str):
    """Validate file JSONL"""
    print(f"\n🔍 Đang validate file: {jsonl_file}")
    
    try:
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                try:
                    case = json.loads(line)
                    
                    # Kiểm tra các trường bắt buộc
                    required_fields = ['id', 'question', 'expected_answer', 'ground_truth_doc_ids']
                    missing = [field for field in required_fields if field not in case]
                    
                    if missing:
                        print(f"⚠️  Case {i} thiếu: {missing}")
                    
                except json.JSONDecodeError:
                    print(f"❌ Case {i} không phải JSON hợp lệ")
        
        print("✅ Validation hoàn thành!")
        
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file: {jsonl_file}")

if __name__ == "__main__":
    # Nếu có argument từ command line
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "data/golden_set.jsonl"
    else:
        # Mặc định
        input_file = "data/testcases_from_notebooklm.json"
        output_file = "data/golden_set.jsonl"
    
    print("=" * 60)
    print("🚀 Convert NotebookLM output sang JSONL format")
    print("=" * 60)
    
    # Convert
    success = convert_notebooklm_to_jsonl(input_file, output_file)
    
    # Validate
    if success:
        validate_jsonl(output_file)
    
    print("=" * 60)
