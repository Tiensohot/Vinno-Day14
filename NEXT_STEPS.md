# 📋 Các bước tiếp theo sau khi có Golden Answer

Bạn đã tạo xong `data/answer/golden_answer.json` với 50+ test cases. Dưới đây là các bước tiếp theo:

---

## 🔄 Bước 1: Convert sang JSONL format

File `golden_answer.json` là JSON array, nhưng hệ thống cần format **JSONL** (mỗi dòng là 1 JSON object).

### Chạy lệnh này:

```bash
python data/convert_notebooklm_to_jsonl.py data/answer/golden_answer.json data/golden_set.jsonl
```

Hoặc tạo script convert nhanh:

```python
import json

# Đọc file JSON
with open('data/answer/golden_answer.json', 'r', encoding='utf-8') as f:
    test_cases = json.load(f)

# Convert sang JSONL
with open('data/golden_set.jsonl', 'w', encoding='utf-8') as f:
    for case in test_cases:
        # Thêm ground_truth_doc_ids nếu chưa có
        if 'ground_truth_doc_ids' not in case:
            case['ground_truth_doc_ids'] = [
                "19_2014_TT-BTP_249771",
                "63_2010_ND-CP_106929"
            ]
        f.write(json.dumps(case, ensure_ascii=False) + '\n')

print(f"✅ Converted {len(test_cases)} test cases to JSONL")
```

---

## ✅ Bước 2: Validate định dạng

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

## 🚀 Bước 3: Chạy Benchmark

Sau khi validate thành công, chạy:

```bash
python main.py
```

Điều này sẽ:
1. Đọc `data/golden_set.jsonl`
2. Chạy Agent trên mỗi test case
3. Tính toán RAGAS metrics (Faithfulness, Relevancy)
4. Chạy Multi-Judge evaluation
5. Tạo file `reports/summary.json` và `reports/benchmark_results.json`

---

## 📊 Bước 4: Phân tích kết quả

Sau khi `main.py` chạy xong, bạn sẽ có:

- `reports/summary.json` - Tóm tắt kết quả
- `reports/benchmark_results.json` - Chi tiết từng test case

Xem kết quả:

```bash
# Windows
type reports\summary.json

# Linux/Mac
cat reports/summary.json
```

---

## 📝 Bước 5: Điền Failure Analysis

Dựa trên kết quả benchmark, điền file `analysis/failure_analysis.md`:

1. **Tổng quan Benchmark** - Số cases, tỉ lệ pass/fail
2. **Phân nhóm lỗi** - Hallucination, Incomplete, Tone Mismatch, v.v.
3. **Phân tích 5 Whys** - Chọn 3 case tệ nhất và phân tích nguyên nhân gốc rễ
4. **Kế hoạch cải tiến** - Đề xuất cách fix

---

## 🔧 Bước 6: Tối ưu Agent (Optional)

Nếu kết quả không tốt, bạn có thể:

1. **Cải tiến Chunking** - Thay đổi chunk_size, overlap
2. **Cập nhật System Prompt** - Nhấn mạnh vào việc chỉ trả lời dựa trên context
3. **Thêm Reranking** - Sắp xếp lại chunks theo relevance
4. **Cải tiến Retriever** - Dùng embedding model tốt hơn

Sau đó chạy lại `python main.py` để so sánh (Regression Testing).

---

## 📋 Checklist hoàn thành

- [ ] Convert `golden_answer.json` → `golden_set.jsonl`
- [ ] Chạy `python check_lab.py` để validate
- [ ] Chạy `python main.py` để benchmark
- [ ] Xem kết quả trong `reports/`
- [ ] Điền `analysis/failure_analysis.md`
- [ ] (Optional) Tối ưu Agent và chạy lại
- [ ] Commit file vào Git
- [ ] Nộp bài

---

## 🎯 Lệnh nhanh (Copy-paste)

```bash
# 1. Convert sang JSONL
python -c "
import json
with open('data/answer/golden_answer.json', 'r', encoding='utf-8') as f:
    cases = json.load(f)
with open('data/golden_set.jsonl', 'w', encoding='utf-8') as f:
    for case in cases:
        if 'ground_truth_doc_ids' not in case:
            case['ground_truth_doc_ids'] = ['19_2014_TT-BTP_249771', '63_2010_ND-CP_106929']
        f.write(json.dumps(case, ensure_ascii=False) + '\n')
print(f'✅ Converted {len(cases)} cases')
"

# 2. Validate
python check_lab.py

# 3. Benchmark
python main.py

# 4. Xem kết quả
type reports\summary.json
```

---

## ⚠️ Lưu ý quan trọng

1. **Trước khi nộp bài**, chạy `python check_lab.py` để đảm bảo định dạng đúng
2. **File `.env` không được push** lên GitHub (chứa API Key)
3. **File `data/golden_set.jsonl` phải có** trước khi chạy `main.py`
4. **Nộp bài cần có:**
   - Source code hoàn chỉnh
   - `reports/summary.json` + `reports/benchmark_results.json`
   - `analysis/failure_analysis.md` (đã điền đầy đủ)
   - `analysis/reflections/reflection_[Tên_SV].md` (cá nhân)

