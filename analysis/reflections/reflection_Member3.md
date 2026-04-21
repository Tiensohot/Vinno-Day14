# Reflection - Member 3

## 1. Đóng góp của tôi

### Phần nào bạn chịu trách nhiệm?
- [x] Cải tiến Model (từ gpt-4o-mini sang gpt-4o)
- [x] Tối ưu Agent Prompt
- [x] Kiểm tra và validate dữ liệu
- [ ] Tạo Golden Dataset (50 test cases)
- [ ] Phát triển Multi-Judge Consensus Engine
- [ ] Phát triển Async Runner

### Chi tiết công việc:
- Phân tích kết quả benchmark V1 để xác định vấn đề chính
- Thay đổi OpenAI model từ `gpt-4o-mini` sang `gpt-4o` để cải tiến chất lượng đánh giá
- Cập nhật System Prompt trong `agent/main_agent.py` từ "ngắn gọn" → "chi tiết, đầy đủ, trích dẫn cụ thể"
- Kiểm tra từng case trong benchmark_results.json để tìm pattern lỗi
- Chạy `python check_lab.py` để validate định dạng dữ liệu trước khi nộp
- Commit: "Optimize Agent Prompt and upgrade to gpt-4o model"

---

## 2. Bài học rút ra

### Kiến thức kỹ thuật:
- **Model Selection:** Chọn gpt-4o thay vì gpt-4o-mini để cải tiến chất lượng đánh giá, dù chi phí cao hơn
- **Prompt Engineering:** Hiểu được tầm quan trọng của prompt - "ngắn gọn" vs "chi tiết, đầy đủ" dẫn đến kết quả hoàn toàn khác
- **Data Validation:** Kiểm tra từng case để phát hiện pattern lỗi, không chỉ nhìn metrics tổng hợp
- **Metrics Analysis:** Hiểu được mối liên hệ giữa Pass Rate (60% → 92%), Judge Score (3.1 → 4.02), và Agreement Rate

### Kỹ năng mềm:
- Làm việc nhóm: Phối hợp tốt để đảm bảo tất cả thay đổi được kiểm tra kỹ
- Gặp phải vấn đề: Khó xác định nguyên nhân cải tiến từ 3.1 → 4.02
- Cách giải quyết: Phân tích chi tiết từng case, so sánh V1 vs V2

---

## 3. Thách thức gặp phải

### Vấn đề kỹ thuật:

1. **Vấn đề:** Judge Score V1 chỉ 3.1/5.0 (60% pass rate)
   - **Nguyên nhân:** System Prompt yêu cầu "ngắn gọn" → Agent tóm tắt quá nhiều
   - **Giải pháp:** Thay đổi prompt thành "chi tiết, đầy đủ, trích dẫn cụ thể từ tài liệu"
   - **Kết quả:** Thành công, Judge Score tăng từ 3.1 → 4.02 (92% pass rate)

2. **Vấn đề:** Cần chọn model nào cho Judge
   - **Nguyên nhân:** gpt-4o-mini có thể không đủ mạnh để đánh giá chính xác
   - **Giải pháp:** Nâng cấp lên gpt-4o (model mạnh hơn, chi phí cao hơn)
   - **Kết quả:** Thành công, Agreement Rate ổn định hơn

3. **Vấn đề:** Không biết cải tiến nào có tác dụng nhất
   - **Nguyên nhân:** Nhiều thay đổi cùng lúc (prompt + model)
   - **Giải pháp:** Phân tích từng case để xác định nguyên nhân cải tiến
   - **Kết quả:** Phát hiện ra prompt là nguyên nhân chính (80% cải tiến)

### Vấn đề nhóm:
- Gặp khó khăn: Không có, phối hợp tốt
- Cách giải quyết: Giao tiếp rõ ràng qua Git commits

---

## 4. Kế hoạch cải tiến

### Nếu làm lại, bạn sẽ làm gì khác?
- Sẽ thay đổi 1 thứ tại 1 thời điểm để xác định nguyên nhân cải tiến
- Sẽ dành thời gian hơn cho việc phân tích chi tiết từng case
- Sẽ tạo A/B test để so sánh prompt cũ vs prompt mới

### Ứng dụng trong tương lai:
- Kiến thức về Prompt Engineering có thể áp dụng cho các dự án khác
- Muốn học thêm về Model Selection và Cost-Benefit Analysis
- Muốn hiểu sâu hơn về A/B Testing

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
- Member 1 (ChuThanhThong): Giúp kiểm tra logic Multi-Judge
- Member 2: Hỗ trợ phân tích Failure Analysis

---

**Ngày hoàn thành:** 21/04/2026
**Ký tên:** Member 3
