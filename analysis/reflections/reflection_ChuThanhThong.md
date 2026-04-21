# Reflection - Member 1

## 1. Đóng góp của tôi

### Phần nào bạn chịu trách nhiệm?
- [x] Tạo Golden Dataset (50 test cases)
- [x] Phát triển Multi-Judge Consensus Engine
- [x] Phát triển Async Runner
- [ ] Phát triển Retrieval Evaluator (Hit Rate, MRR)
- [ ] Phân tích Failure Analysis
- [ ] Tối ưu Agent

### Chi tiết công việc:
- Tạo file `data/synthetic_gen.py` để generate 50 test cases từ golden_answer.json
- Cập nhật `engine/llm_judge.py` để sử dụng 2 API key (Groq + OpenAI) thay vì mock
- Cập nhật `engine/runner.py` để chạy benchmark song song với asyncio
- Cập nhật `main.py` để khởi tạo Judge với use_api=True
- Điều chỉnh temperature và prompt để cải tiến Multi-Judge consensus
- Commit: "Implement Multi-Judge Consensus Engine with Groq + OpenAI"

---

## 2. Bài học rút ra

### Kiến thức kỹ thuật:
- **Retrieval Evaluation:** Hiểu được Hit Rate (100%) cho thấy retriever hoạt động tốt, nhưng Judge Score thấp (2.74) chỉ ra vấn đề ở Generation stage
- **Multi-Judge Consensus:** Học được cách so sánh 2 model khác nhau (Groq vs OpenAI) để tính Agreement Rate (91.8%), giúp xác thực chất lượng đánh giá
- **Async Programming:** Sử dụng asyncio.gather() để chạy 50 test cases song song, giảm thời gian từ 150s xuống ~30s
- **Failure Analysis:** Phân tích 5 Whys giúp xác định nguyên nhân gốc rễ - prompt chưa tối ưu, không yêu cầu câu trả lời chi tiết

### Kỹ năng mềm:
- Làm việc nhóm: Phối hợp tốt để cập nhật code mà không xung đột
- Gặp phải vấn đề: Ban đầu Judge Score quá thấp (2.74), phải debug từng bước
- Cách giải quyết: Kiểm tra từng component (Agent, Retriever, Judge) để tìm ra vấn đề

---

## 3. Thách thức gặp phải

### Vấn đề kỹ thuật:

1. **Vấn đề:** Judge Score quá thấp (2.74/5.0)
   - **Nguyên nhân:** Temperature quá thấp (0.1) → Judge quá khắt khe
   - **Giải pháp:** Tăng temperature từ 0.1 → 0.3, cải tiến prompt với rubric chi tiết
   - **Kết quả:** Cải tiến nhưng vẫn còn thấp, phát hiện ra vấn đề thực sự ở Agent

2. **Vấn đề:** Agent không nhận được context
   - **Nguyên nhân:** `runner.py` không truyền context vào `agent.query()`
   - **Giải pháp:** Thêm `context=test_case.get("context", "")` vào runner
   - **Kết quả:** Thành công, Agent bây giờ nhận được context đúng

3. **Vấn đề:** 2 Judge (Groq vs OpenAI) cho điểm rất khác nhau
   - **Nguyên nhân:** Groq model khác biệt, prompt không rõ ràng
   - **Giải pháp:** Chuẩn hóa prompt, thêm rubric chi tiết (5 điểm, 4 điểm, v.v.)
   - **Kết quả:** Agreement Rate tăng từ 80% → 91.8%

### Vấn đề nhóm:
- Gặp khó khăn: Không có, phối hợp tốt
- Cách giải quyết: Giao tiếp rõ ràng qua Git commits

---

## 4. Kế hoạch cải tiến

### Nếu làm lại, bạn sẽ làm gì khác?
- Sẽ kiểm tra từng component (Agent, Retriever, Judge) từ đầu thay vì giả định
- Sẽ dành thời gian hơn cho việc cải tiến prompt thay vì chỉ điều chỉnh temperature
- Sẽ viết unit test cho từng component để debug nhanh hơn

### Ứng dụng trong tương lai:
- Kiến thức về Multi-Judge Consensus có thể áp dụng cho các hệ thống evaluation khác
- Muốn học thêm về Semantic Chunking và Reranking Layer để cải tiến Retrieval

---

## 5. Đánh giá tự thân

### Mức độ hoàn thành:
- [x] Hoàn thành 100% công việc được giao
- [ ] Hoàn thành 80-90% công việc
- [ ] Hoàn thành 60-80% công việc
- [ ] Hoàn thành < 60% công việc

### Chất lượng công việc:
- [x] Rất tốt (9-10/10)
- [ ] Tốt (7-8/10)
- [ ] Trung bình (5-6/10)
- [ ] Cần cải tiến (< 5/10)

### Đóng góp cho nhóm:
- [x] Rất tích cực, giúp nhóm hoàn thành sớm
- [ ] Tích cực, hoàn thành công việc đúng hạn
- [ ] Bình thường, hoàn thành công việc nhưng chậm
- [ ] Cần cải tiến, không hoàn thành đúng hạn

---

## 6. Lời cảm ơn

Cảm ơn những người đã giúp đỡ:
- Member 2: Giúp kiểm tra logic Multi-Judge
- Member 3: Hỗ trợ debug khi gặp lỗi API

---

**Ngày hoàn thành:** 21/04/2026
**Ký tên:** Member 1
