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
- Phân tích kết quả benchmark: Agent V2 đạt Judge Score 4.02/5.0, cải thiện 29.7% so với V1 (3.1/5.0)
- Commit: "Implement Retrieval Evaluator and Failure Analysis"

---

## 2. Bài học rút ra

### Kiến thức kỹ thuật:
- **Retrieval Evaluation:** Hit Rate 100% cho thấy retriever hoạt động tuyệt vời, nhưng cần kết hợp với Generation metrics để đánh giá toàn bộ hệ thống
- **Failure Analysis:** Phân tích 5 Whys giúp xác định các case thất bại (4/50) tập trung ở câu hỏi ngoài phạm vi tài liệu
- **Prompt Engineering:** Tối ưu prompt giúp nâng Judge Score từ 3.1 (V1) lên 4.02 (V2), cải thiện 29.7%
- **Metrics Interpretation:** Hiểu được mối liên hệ giữa Hit Rate (100%), Judge Score (4.02/5.0), và Agreement Rate (86.6%)

### Kỹ năng mềm:
- Làm việc nhóm: Phối hợp tốt với Member 1 để debug vấn đề
- Gặp phải vấn đề: Khó xác định nguyên nhân Judge Score thấp ban đầu
- Cách giải quyết: Phân tích từng case trong benchmark_results.json để tìm pattern

---

## 3. Thách thức gặp phải

### Vấn đề kỹ thuật:

1. **Vấn đề:** Agent V1 có Judge Score thấp (3.1/5.0)
   - **Nguyên nhân:** Chưa kiểm tra chi tiết câu trả lời của Agent
   - **Giải pháp:** Phân tích benchmark_results.json, so sánh agent_response với expected_answer
   - **Kết quả:** Phát hiện Agent trả lời không đầy đủ, thiếu trích dẫn cụ thể

2. **Vấn đề:** 4/50 test cases bị fail (score thấp)
   - **Nguyên nhân:** Câu hỏi nằm ngoài phạm vi tài liệu, Agent trả lời "Thông tin không có trong tài liệu"
   - **Giải pháp:** Cập nhật failure_analysis.md với phân tích các case fail thực tế
   - **Kết quả:** Xác định được pattern: câu hỏi về đối tượng không được điều chỉnh bởi văn bản

3. **Vấn đề:** Prompt cần cải tiến
   - **Nguyên nhân:** "Trả lời ngắn gọn" → Agent tóm tắt quá nhiều
   - **Giải pháp:** Thay đổi thành "Trả lời chi tiết, đầy đủ, trích dẫn cụ thể"
   - **Kết quả:** Judge Score tăng từ 3.1 → 4.02 (+29.7%), Agreement Rate 86.6%

### Vấn đề nhóm:
- Gặp khó khăn: Không có, phối hợp tốt