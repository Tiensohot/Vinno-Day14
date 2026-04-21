# 📋 Hướng dẫn Generate Test Case bằng NotebookLM

## 🎯 Mục tiêu
Tạo **50+ test cases** chất lượng cao từ các tài liệu pháp luật Việt Nam để đánh giá AI Agent.

---

## 📤 Bước 1: Upload tài liệu vào NotebookLM

1. Truy cập: https://notebooklm.google.com
2. Tạo Notebook mới
3. Upload 2 file markdown từ `data/processed/md/`:
   - `19_2014_TT-BTP_249771.md` (Quy định về Thủ tục hành chính)
   - `63_2010_ND-CP_106929.md` (Về kiểm soát thủ tục hành chính)

---

## 🔧 Bước 2: Prompt cho NotebookLM

Dán prompt này vào NotebookLM và chạy:

```
Bạn là một chuyên gia tạo test case cho hệ thống AI Evaluation. 
Dựa trên các tài liệu pháp luật được cung cấp, hãy tạo 50 câu hỏi-đáp chất lượng cao theo yêu cầu sau:

## YÊUCẦU CHUNG:
- Mỗi câu hỏi phải có câu trả lời rõ ràng, có thể trích dẫn từ tài liệu
- Câu trả lời phải chứa thông tin cụ thể, không mơ hồ
- Phải bao gồm tất cả 5 loại câu hỏi dưới đây

## PHÂN BỐ 50 CASES:

### 1. FACT-CHECK (15 cases) - Kiểm tra thông tin cơ bản
Định nghĩa: Câu hỏi yêu cầu trích xuất thông tin trực tiếp từ tài liệu
Độ khó: EASY
Ví dụ:
- "Thông tư 167/2012/TT-BTC có áp dụng cho hoạt động kiểm soát thủ tục hành chính nào?"
- "Cơ sở dữ liệu quốc gia hoạt động bao nhiêu giờ trong ngày?"

Yêu cầu: Tạo 15 câu hỏi tương tự, mỗi câu trích xuất 1 thông tin cụ thể từ tài liệu

### 2. REASONING (15 cases) - Yêu cầu suy luận
Định nghĩa: Câu hỏi yêu cầu giải thích LÝ DO hoặc MỐI LIÊN HỆ giữa các thông tin
Độ khó: MEDIUM
Ví dụ:
- "Tại sao Cục Kiểm soát thủ tục hành chính phải đề nghị điều chỉnh dữ liệu trong 10 ngày?"
- "Việc hạch toán tương tự chứng khoán có đồng nghĩa với việc coi tài sản mã hóa là chứng khoán không? Giải thích."

Yêu cầu: Tạo 15 câu hỏi yêu cầu giải thích nguyên nhân, lý do, hoặc mối liên hệ

### 3. MULTI-HOP (10 cases) - Kết hợp nhiều thông tin
Định nghĩa: Câu hỏi yêu cầu kết hợp thông tin từ 2-3 đoạn khác nhau trong tài liệu
Độ khó: HARD
Ví dụ:
- "Nếu dữ liệu thủ tục hành chính không chính xác, Cục Kiểm soát phải làm gì và trong bao lâu?"
- "Kế hoạch kiểm tra của Bộ Tư pháp được phê duyệt khi nào và phải gửi tới các địa phương trong bao lâu?"

Yêu cầu: Tạo 10 câu hỏi yêu cầu kết hợp thông tin từ nhiều phần của tài liệu

### 4. ADVERSARIAL (5 cases) - Lừa Agent (Prompt Injection)
Định nghĩa: Câu hỏi cố tình sai lệch hoặc yêu cầu thông tin KHÔNG CÓ trong tài liệu
Độ khó: HARD
Ví dụ:
- "Thông tư 167/2012/TT-BTC có áp dụng cho tài sản mã hóa ở nước ngoài không?" 
  → Câu trả lời đúng: "Không, tài liệu không đề cập đến tài sản mã hóa ở nước ngoài"
- "Ai là người phê duyệt kế hoạch kiểm tra của các tỉnh?"
  → Câu trả lời đúng: "Tài liệu không cung cấp thông tin này"

Yêu cầu: Tạo 5 câu hỏi mà Agent phải trả lời "Tôi không biết" hoặc "Tài liệu không đề cập"

### 5. EDGE-CASE (5 cases) - Trường hợp biên
Định nghĩa: Câu hỏi về các trường hợp đặc biệt, ngoại lệ, hoặc điều kiện cụ thể
Độ khó: MEDIUM
Ví dụ:
- "Trong trường hợp kiểm tra đột xuất, tổ chức được kiểm tra có phải gửi báo cáo trước không?"
- "Khi Cơ sở dữ liệu quốc gia được sửa chữa, phải làm gì?"

Yêu cầu: Tạo 5 câu hỏi về các trường hợp đặc biệt hoặc ngoại lệ

## OUTPUT FORMAT:

Trả lời theo format JSON dưới đây (CHÍNH XÁC):

[
  {
    "id": 1,
    "question": "Câu hỏi cụ thể?",
    "expected_answer": "Câu trả lời chi tiết từ tài liệu",
    "type": "fact-check|reasoning|multi-hop|adversarial|edge-case",
    "difficulty": "easy|medium|hard",
    "source_section": "Tên phần/điều trong tài liệu"
  },
  ...
]

## TIÊU CHÍ CHẤT LƯỢNG:
✅ Mỗi câu hỏi phải rõ ràng, không mơ hồ
✅ Câu trả lời phải có thể trích dẫn từ tài liệu (hoặc rõ ràng không có)
✅ Phải bao gồm đủ 5 loại câu hỏi
✅ Phân bố: 15 fact-check, 15 reasoning, 10 multi-hop, 5 adversarial, 5 edge-case
✅ Không lặp lại câu hỏi
✅ Độ khó tăng dần trong mỗi loại

Bắt đầu tạo 50 test cases ngay!
```

---

## 📥 Bước 3: Copy output từ NotebookLM

1. NotebookLM sẽ trả lại JSON array
2. Copy toàn bộ output
3. Dán vào file `data/testcases_from_notebooklm.json`

---

## 🔄 Bước 4: Convert sang JSONL format

Chạy script Python này để convert:

```python
import json

# Đọc file JSON từ NotebookLM
with open('data/testcases_from_notebooklm.json', 'r', encoding='utf-8') as f:
    test_cases = json.load(f)

# Convert sang JSONL và thêm ground_truth_doc_ids
with open('data/golden_set.jsonl', 'w', encoding='utf-8') as f:
    for i, case in enumerate(test_cases, 1):
        case['id'] = i
        case['ground_truth_doc_ids'] = [
            "19_2014_TT-BTP_249771",
            "63_2010_ND-CP_106929"
        ]
        case['metadata'] = {
            'difficulty': case.get('difficulty', 'medium'),
            'type': case.get('type', 'fact-check'),
            'category': 'legal'
        }
        f.write(json.dumps(case, ensure_ascii=False) + '\n')

print(f"✅ Converted {len(test_cases)} test cases to JSONL format")
```

---

## ✅ Bước 5: Validate

Chạy lệnh kiểm tra:

```bash
python check_lab.py
```

Nó sẽ kiểm tra:
- ✅ Có 50+ test cases
- ✅ Mỗi case có `ground_truth_doc_ids`
- ✅ Format JSON hợp lệ
- ✅ Không có trường bắt buộc bị thiếu

---

## 💡 Tips để NotebookLM tạo test case tốt

1. **Nếu output không đủ 50 cases:** Chạy prompt lần 2 với yêu cầu "Tạo thêm 10 cases loại [type] khác"
2. **Nếu câu trả lời quá ngắn:** Yêu cầu "Mở rộng câu trả lời, thêm chi tiết từ tài liệu"
3. **Nếu có lỗi format:** Copy output vào https://jsonlint.com để kiểm tra
4. **Nếu muốn chỉnh sửa:** Có thể edit file `data/golden_set.jsonl` trực tiếp

---

## 📊 Checklist hoàn thành

- [ ] Upload 2 file markdown vào NotebookLM
- [ ] Chạy prompt tạo 50 test cases
- [ ] Copy output JSON
- [ ] Chạy script convert sang JSONL
- [ ] Chạy `python check_lab.py` để validate
- [ ] Kiểm tra `data/golden_set.jsonl` có 50+ dòng
- [ ] Commit file vào Git

---

## 🚀 Lệnh nhanh

```bash
# Sau khi có golden_set.jsonl, chạy benchmark
python data/synthetic_gen.py  # Nếu cần
python main.py               # Chạy evaluation
python check_lab.py          # Kiểm tra định dạng
```

