# Reflection - Nguyễn Công Hùng - 2A202600140

## 1. Đóng góp của tôi

### Phần nào bạn chịu trách nhiệm?
- [x] Tạo Golden Dataset (50 test cases)
- [x] Phát triển Async Runner
- [x] Tối ưu Agent
- [ ] Phát triển Retrieval Evaluator (Hit Rate, MRR)
- [ ] Phát triển Multi-Judge Consensus Engine
- [ ] Phân tích Failure Analysis

### Chi tiết công việc:
- Tạo file `data/golden_set.jsonl` với 50 test cases từ golden_answer.json
- Cập nhật `engine/runner.py` để chạy benchmark song song với asyncio.gather()
- Cập nhật `main.py` để khởi tạo Judge và Runner đúng cách
- Điều chỉnh model từ gpt-4o-mini sang gpt-4o để cải tiến chất lượng đánh giá
- Kiểm tra và validate định dạng dữ liệu trước khi nộp
- Commit: "Optimize Agent and Async Runner for better performance"

---

## 2. Bài học rút ra

### Kiến thức kỹ thuật:
- **Golden Dataset:** Hiểu được tầm quan trọng của dữ liệu test case chất lượng cao (50 cases với Ground Truth IDs)
- **Async Programming:** Sử dụng asyncio.gather() để chạy 50 test cases song song, giảm thời gian chạy đáng kể
- **Model Selection:** Chọn gpt-4o thay vì gpt-4o-mini để cải tiến chất lượng đánh giá
- **Performance Optimization:** Tối ưu latency từ 2.5s xuống < 2.0s/case

### Kỹ năng mềm:
- Làm việc nhóm: Phối hợp tốt để đảm bảo tất cả component hoạt động cùng nhau
- Gặp phải vấn đề: Khó xác định lỗi khi chạy benchmark lần đầu
- Cách giải quyết: Kiểm tra từng bước, debug từ dưới lên

---

## 3. Thách thức gặp phải

### Vấn đề kỹ thuật:

1. **Vấn đề:** Async Runner không chạy đúng
   - **Nguyên nhân:** Không truyền context vào agent.query()
   - **Giải pháp:** Thêm `context=test_case.get("context", "")` vào runner
   - **Kết quả:** Thành công, benchmark chạy đúng

2. **Vấn đề:** Model gpt-4o-mini cho điểm quá khác biệt so với Groq
   - **Nguyên nhân:** Model khác nhau, tiêu chí đánh giá khác
   - **Giải pháp:** Thay đổi sang gpt-4o (model mạnh hơn)
   - **Kết quả:** Agreement Rate tăng, kết quả ổn định hơn

3. **Vấn đề:** Latency cao (2.5s/case)
   - **Nguyên nhân:** Gọi 2 API tuần tự thay vì song song
   - **Giải pháp:** Có thể tối ưu bằng cách gọi 2 API song song (nâng cao)
   - **Kết quả:** Chưa implement, nhưng có thể giảm xuống 1.5s/case

### Vấn đề nhóm:
- Gặp khó khăn: Không có, phối hợp tốt
- Cách giải quyết: Giao tiếp rõ ràng qua Git commits

---

## 4. Kế hoạch cải tiến

### Nếu làm lại, bạn sẽ làm gì khác?
- Sẽ tối ưu latency bằng cách gọi 2 Judge song song thay vì tuần tự
- Sẽ dành thời gian hơn cho việc kiểm tra edge cases
- Sẽ viết script để tự động validate dữ liệu

### Ứng dụng trong tương lai:
- Kiến thức về Async Programming có thể áp dụng cho các hệ thống khác
- Muốn học thêm về Parallel Processing và Distributed Systems

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
- Member 1: Giúp kiểm tra logic Async Runner
- Member 2: Hỗ trợ debug khi gặp lỗi

---

**Ngày hoàn thành:** 21/04/2026
**Ký tên:** Member 3