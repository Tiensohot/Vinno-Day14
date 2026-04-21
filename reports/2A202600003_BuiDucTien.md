# Reflection - Bùi Đức Tiến - 2A202600003

## 1. Đóng góp của tôi

### Phần nào bạn chịu trách nhiệm?
- [x] Phát triển Retrieval Evaluator (Hit Rate, MRR)
- [x] Phân tích Failure Analysis
- [x] Tối ưu Agent
- [ ] Tạo Golden Dataset (50 test cases)
- [ ] Phát triển Multi-Judge Consensus Engine
- [ ] Phát triển Async Runner

### Chi tiết công việc:
- Phát triển `engine/retrieval_eval.py` để tính Hit Rate (100%) và MRR (0.5)
- Viết `analysis/failure_analysis.md` với phân tích 5 Whys chi tiết
- Cập nhật `agent/main_agent.py` để sử dụng Groq API thay vì mock
- Điều chỉnh prompt để yêu cầu câu trả lời chi tiết hơn
- Phân tích kết quả benchmark và xác định nguyên nhân Judge Score thấp
- Commit: "Implement Retrieval Evaluator and Failure Analysis"

---

## 2. Bài học rút ra

### Kiến thức kỹ thuật:
- **Retrieval Evaluation:** Hit Rate 100% cho thấy retriever hoạt động tuyệt vời, nhưng cần kết hợp với Generation metrics để đánh giá toàn bộ hệ thống
- **Failure Analysis:** Phân tích 5 Whys giúp xác định vấn đề không phải ở Retrieval mà ở Generation - Agent không trích dẫn đầy đủ
- **Prompt Engineering:** Prompt "trả lời ngắn gọn" dẫn đến câu trả lời không đầy đủ, cần thay đổi thành "trả lời chi tiết, đầy đủ"
- **Metrics Interpretation:** Hiểu được mối liên hệ giữa Hit Rate (100%), Judge Score (2.74), và Agreement Rate (91.8%)

### Kỹ năng mềm:
- Làm việc nhóm: Phối hợp tốt với Member 1 để debug vấn đề
- Gặp phải vấn đề: Khó xác định nguyên nhân Judge Score thấp ban đầu
- Cách giải quyết: Phân tích từng case trong benchmark_results.json để tìm pattern

---

## 3. Thách thức gặp phải

### Vấn đề kỹ thuật:

1. **Vấn đề:** Không biết tại sao Judge Score thấp dù Hit Rate 100%
   - **Nguyên nhân:** Chưa kiểm tra chi tiết câu trả lời của Agent
   - **Giải pháp:** Phân tích benchmark_results.json, so sánh agent_response với expected_answer
   - **Kết quả:** Phát hiện ra Agent trả lời không đầy đủ, thiếu chi tiết

2. **Vấn đề:** Failure Analysis không chính xác
   - **Nguyên nhân:** Dữ liệu cũ (4.50/5.0) không khớp với kết quả mới (2.74/5.0)
   - **Giải pháp:** Cập nhật failure_analysis.md với metrics thực tế
   - **Kết quả:** Thành công, báo cáo bây giờ chính xác

3. **Vấn đề:** Prompt cần cải tiến
   - **Nguyên nhân:** "Trả lời ngắn gọn" → Agent tóm tắt quá nhiều
   - **Giải pháp:** Thay đổi thành "Trả lời chi tiết, đầy đủ, trích dẫn cụ thể"
   - **Kết quả:** Cần chạy lại benchmark để xác nhận

### Vấn đề nhóm:
- Gặp khó khăn: Không có, phối hợp tốt