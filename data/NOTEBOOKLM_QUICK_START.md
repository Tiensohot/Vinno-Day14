# 🚀 Quick Start: Generate Test Cases với NotebookLM

## 📋 Tóm tắt quy trình

```
1. Upload 2 file markdown vào NotebookLM
   ↓
2. Chạy prompt tạo 50 test cases
   ↓
3. Copy output JSON
   ↓
4. Chạy script convert sang JSONL
   ↓
5. Validate và chạy benchmark
```

---

## 🎯 Bước 1: Chuẩn bị tài liệu

Bạn cần upload 2 file này vào NotebookLM:
- `data/processed/md/19_2014_TT-BTP_249771.md`
- `data/processed/md/63_2010_ND-CP_106929.md`

---

## 📝 Bước 2: Prompt cho NotebookLM

**Dán prompt này vào NotebookLM:**

```
Bạn là một chuyên gia tạo test case cho hệ thống AI Evaluation. 
Dựa trên các tài liệu pháp luật được cung cấp, hãy tạo 50 câu hỏi-đáp chất lượng cao theo yêu cầu sau:

## YÊUCẦU CHUNG:
- Mỗi câu hỏi phải có câu trả lời rõ ràng, có thể trích dẫn từ tài liệu
- Câu trả lời phải chứa thông tin cụ thể, không mơ hồ
- Phải bao gồm tất cả 5 loại câu hỏi dưới đây

## PHÂN BỐ 50 CASES:

### 1. FACT-CHECK (15 cases) - Kiểm tra thông tin cơ bản
Độ khó: EASY
Ví dụ:
- "Cơ sở dữ liệu quốc gia hoạt động bao nhiêu giờ trong ngày?"
- "Kinh phí thực hiện kiểm soát thủ tục hành chính tại các tỉnh do ngân sách nào chi trả?"

### 2. REASONING (15 cases) - Yêu cầu suy luận
Độ khó: MEDIUM
Ví dụ:
- "Tại sao Cục Kiểm soát thủ tục hành chính phải đề nghị điều chỉnh dữ liệu trong 10 ngày?"
- "Giải thích lý do tại sao việc hạch toán tương tự chứng khoán không đồng nghĩa với việc coi tài sản mã hóa là chứng khoán?"

### 3. MULTI-HOP (10 cases) - Kết hợp nhiều thông tin
Độ khó: HARD
Ví dụ:
- "Nếu dữ liệu thủ tục hành chính không chính xác, Cục Kiểm soát phải làm gì và trong bao lâu?"
- "Kế hoạch kiểm tra của Bộ Tư pháp được phê duyệt khi nào và phải gửi tới các địa phương trong bao lâu?"

### 4. ADVERSARIAL (5 cases) - Lừa Agent
Độ khó: HARD
Ví dụ:
- "Thông tư 167/2012/TT-BTC có áp dụng cho tài sản mã hóa ở nước ngoài không?" 
  → Câu trả lời: "Tài liệu không cung cấp thông tin này"
- "Ai là người phê duyệt kế hoạch kiểm tra của các tỉnh?"
  → Câu trả lời: "Tài liệu không đề cập rõ ràng"

### 5. EDGE-CASE (5 cases) - Trường hợp biên
Độ khó: MEDIUM
Ví dụ:
- "Trong trường hợp kiểm tra đột xuất, tổ chức được kiểm tra có phải gửi báo cáo trước không?"
- "Khi Cơ sở dữ liệu quốc gia được sửa chữa, phải làm gì?"

## OUTPUT FORMAT (CHÍNH XÁC):

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

Bắt đầu tạo 50 test cases ngay!
```

---

## 📥 Bước 3: Copy output

1. NotebookLM sẽ trả lại JSON array
2. Copy toàn bộ output (từ `[` đến `]`)
3. Tạo file `data/testcases_from_notebooklm.json`
4. Dán output vào file này

---

## 🔄 Bước 4: Convert sang JSONL

Chạy lệnh này:

```bash
python data/convert_notebooklm_to_jsonl.py
```

Hoặc nếu file input có tên khác:

```bash
python data/convert_notebooklm_to_jsonl.py data/your_file.json data/golden_set.jsonl
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

## 📊 Ví dụ output

Xem file `data/example_testcases.json` để hiểu format chính xác.

---

## 🚀 Chạy benchmark

Sau khi có `data/golden_set.jsonl`:

```bash
python main.py
```

---

## 💡 Troubleshooting

### ❌ "JSON không hợp lệ"
- Kiểm tra file có bắt đầu bằng `[` và kết thúc bằng `]` không
- Dùng https://jsonlint.com để validate

### ❌ "Chỉ có 30 cases, cần 50"
- Chạy prompt lần 2 với yêu cầu "Tạo thêm 20 cases"
- Hoặc edit file `data/golden_set.jsonl` thêm cases

### ❌ "Thiếu ground_truth_doc_ids"
- Script convert sẽ tự thêm nếu chưa có
- Kiểm tra lại file output

---

## 📝 Checklist

- [ ] Upload 2 file markdown vào NotebookLM
- [ ] Chạy prompt tạo 50 test cases
- [ ] Copy output JSON vào `data/testcases_from_notebooklm.json`
- [ ] Chạy `python data/convert_notebooklm_to_jsonl.py`
- [ ] Chạy `python check_lab.py` để validate
- [ ] Kiểm tra `data/golden_set.jsonl` có 50+ dòng
- [ ] Chạy `python main.py` để benchmark
- [ ] Commit file vào Git

---

## 📚 Tài liệu thêm

- Xem `data/TESTCASE_GENERATION_PROMPT.md` để hiểu chi tiết hơn
- Xem `data/example_testcases.json` để xem ví dụ format
- Xem `data/HARD_CASES_GUIDE.md` để hiểu các loại test case khó

