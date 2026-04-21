#!/usr/bin/env python3
"""
Script để fix ground_truth_doc_ids dựa trên source_section
"""

import json
import re

def extract_doc_id_from_source(source_section: str) -> list:
    """
    Trích xuất Document ID từ source_section
    
    Ví dụ:
    - "Điều 3 Thông tư 19/2014/TT-BTP" → ["19_2014_TT-BTP_249771"]
    - "Điều 5 Nghị định 63/2010/NĐ-CP" → ["63_2010_ND-CP_106929"]
    - "Điều 7 Thông tư 19/2014/TT-BTP" → ["19_2014_TT-BTP_249771"]
    """
    
    if not source_section:
        return ["19_2014_TT-BTP_249771", "63_2010_ND-CP_106929"]
    
    # Mapping từ source_section đến doc_id
    if "19/2014/TT-BTP" in source_section or "Thông tư 19/2014" in source_section:
        return ["19_2014_TT-BTP_249771"]
    elif "63/2010/NĐ-CP" in source_section or "Nghị định 63/2010" in source_section:
        return ["63_2010_ND-CP_106929"]
    else:
        # Nếu không xác định được, trả về cả hai
        return ["19_2014_TT-BTP_249771", "63_2010_ND-CP_106929"]

def fix_ground_truth_doc_ids():
    print("=" * 60)
    print("🔧 Fix ground_truth_doc_ids dựa trên source_section")
    print("=" * 60)
    
    try:
        # Đọc file golden_answer.json
        print("\n📖 Đang đọc data/answer/golden_answer.json...")
        with open('data/answer/golden_answer.json', 'r', encoding='utf-8') as f:
            test_cases = json.load(f)
        
        print(f"✅ Đã đọc {len(test_cases)} test cases")
        
        # Fix ground_truth_doc_ids
        print("\n🔧 Đang fix ground_truth_doc_ids...")
        fixed_count = 0
        
        for case in test_cases:
            source_section = case.get('source_section', '')
            doc_ids = extract_doc_id_from_source(source_section)
            
            # Cập nhật ground_truth_doc_ids
            case['ground_truth_doc_ids'] = doc_ids
            fixed_count += 1
            
            # Debug: in ra một số cases
            if fixed_count <= 5 or fixed_count > len(test_cases) - 3:
                print(f"  Case {case['id']}: {source_section[:50]}... → {doc_ids}")
        
        print(f"\n✅ Đã fix {fixed_count} test cases")
        
        # Lưu lại file
        print("\n💾 Đang lưu file...")
        with open('data/answer/golden_answer.json', 'w', encoding='utf-8') as f:
            json.dump(test_cases, f, ensure_ascii=False, indent=2)
        
        print("✅ Đã lưu data/answer/golden_answer.json")
        
        # Convert sang JSONL
        print("\n🔄 Đang convert sang JSONL format...")
        with open('data/golden_set.jsonl', 'w', encoding='utf-8') as f:
            for case in test_cases:
                # Thêm metadata nếu chưa có
                if 'metadata' not in case:
                    case['metadata'] = {
                        'difficulty': case.get('difficulty', 'medium'),
                        'type': case.get('type', 'fact-check'),
                        'category': 'legal'
                    }
                
                f.write(json.dumps(case, ensure_ascii=False) + '\n')
        
        print("✅ Đã tạo data/golden_set.jsonl")
        
        # Thống kê
        print("\n📊 Thống kê:")
        doc_19_count = sum(1 for c in test_cases if "19_2014_TT-BTP_249771" in c.get('ground_truth_doc_ids', []))
        doc_63_count = sum(1 for c in test_cases if "63_2010_ND-CP_106929" in c.get('ground_truth_doc_ids', []))
        both_count = sum(1 for c in test_cases if len(c.get('ground_truth_doc_ids', [])) > 1)
        
        print(f"  - Cases từ Thông tư 19/2014/TT-BTP: {doc_19_count}")
        print(f"  - Cases từ Nghị định 63/2010/NĐ-CP: {doc_63_count}")
        print(f"  - Cases từ cả 2 document: {both_count}")
        
        print("\n" + "=" * 60)
        print("✅ Fix hoàn thành!")
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
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    success = fix_ground_truth_doc_ids()
    sys.exit(0 if success else 1)
