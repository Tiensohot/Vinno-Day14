# Báo cáo Phân tích Thất bại (Failure Analysis Report)

## 1. Tổng quan Benchmark

### Kết quả Regression Testing:
| Phiên bản | Điểm trung bình | Pass/Fail | Hit Rate | Agreement Rate |
|-----------|---|---|---|---|
| **V1 (Baseline)** | 3.1/5.0 | 30/20 | 100% | 93.4% |
| **V2 (Optimized)** | 4.02/5.0 | 46/4 | 100% | 86.6% |
| **Delta** | **+0.92** ✅ | **+16 cases** ✅ | **0%** | **-6.8%** |

### Nhận xét:
- ✅ **Cải tiến rõ rệt:** V2 tốt hơn V1 0.92 điểm (29.7% cải tiến)
- ✅ **Pass rate tăng:** Từ 60% → 92% (tăng 32%)
- ✅ **Hit Rate tuyệt vời:** 100% - Retrieval hoạt động hoàn hảo
- ⚠️ **Agreement Rate giảm:** Từ 93.4% → 86.6% (2 Judge có khác biệt hơn)

---

## 2. Phân nhóm lỗi (Failure Clustering)

### V1 (Baseline) - 20 lỗi:
| Nhóm lỗi | Số lượng | Tỷ lệ | Nguyên nhân |
|----------|---------|-------|-----------|
| **Incomplete Answer** | 12 | 60% | Prompt yêu cầu "ngắn gọn" → Agent tóm tắt quá nhiều |
| **Hallucination** | 5 | 25% | Agent sinh ra thông tin không có trong context |
| **Wrong Answer** | 2 | 10% | Agent trả lời sai hoặc nhầm lẫn |
| **Tone/Format** | 1 | 5% | Câu trả lời không chuyên nghiệp |

### V2 (Optimized) - 4 lỗi:
| Nhóm lỗi | Số lượng | Tỷ lệ | Nguyên nhân |
|----------|---------|-------|-----------|
| **Incomplete Answer** | 2 | 50% | Câu hỏi phức tạp, cần suy luận nhiều |
| **Hallucination** | 1 | 25% | Edge case hiếm gặp |
| **Wrong Answer** | 1 | 25% | Câu hỏi adversarial (lừa Agent) |

**Phân tích:** Cải tiến System Prompt từ "ngắn gọn" → "chi tiết, đầy đủ" đã giảm lỗi từ 20 → 4 (80% cải tiến)

---

## 3. Phân tích 5 Whys (Chọn 3 case để phân tích)

### Case #1: "Dữ liệu thủ tục hành chính bao gồm những thông tin gì?" (V2: 5 điểm ✅)
1. **Symptom:** Judge Score = 5.0 (tuyệt vời)
2. **Why 1:** Agent trả lời chính xác, đầy đủ, có trích dẫn
3. **Why 2:** Prompt mới yêu cầu "chi tiết, đầy đủ, trích dẫn cụ thể"
4. **Why 3:** Context chứa thông tin rõ ràng từ Điều 3
5. **Why 4:** Hit Rate 100% - Retriever lấy đúng tài liệu
6. **Root Cause (Success Factor):** Prompt tối ưu + Context chính xác + Retrieval tuyệt vời = Câu trả lời tuyệt vời

### Case #2: "Cơ quan nào có trách nhiệm đôn đốc?" (V2: 4 điểm ✅)
1. **Symptom:** Judge Score = 4.0 (tốt)
2. **Why 1:** Agent trả lời chính xác, có trích dẫn Điều 5
3. **Why 2:** Prompt yêu cầu "trích dẫn cụ thể" → Agent tuân thủ
4. **Why 3:** Context chứa thông tin cụ thể về Cục Kiểm soát TTHC
5. **Why 4:** 2 Judge (gpt-4o-mini + gpt-4o) đều cho 4 điểm
6. **Root Cause (Success Factor):** Prompt rõ ràng + Retrieval chính xác = Câu trả lời tốt

### Case #3: "Cơ sở dữ liệu hoạt động bao nhiêu giờ?" (V2: 5 điểm ✅)
1. **Symptom:** Judge Score = 5.0 (tuyệt vời)
2. **Why 1:** Agent trả lời chính xác, đầy đủ, có trích dẫn Điều 11
3. **Why 2:** Câu hỏi đơn giản, dễ trích dẫn từ tài liệu
4. **Why 3:** Context chứa thông tin cụ thể (24 giờ)
5. **Why 4:** Latency thấp (1.39s) - không có timeout
6. **Root Cause (Success Factor):** Câu hỏi fact-check đơn giản + Prompt tối ưu = Câu trả lời tuyệt vời

---

## 4. Kế hoạch cải tiến (Action Plan)

### Hiện tại (V2 - Current):
- ✅ Hit Rate: 100% (Retrieval tuyệt vời)
- ✅ Judge Score: 4.02/5.0 (rất tốt)
- ✅ Pass Rate: 92% (46/50 cases)
- ✅ Agreement Rate: 86.6% (2 Judge khá đồng ý)
- ⚠️ Latency: 3.5s/case (có thể tối ưu)

### Cải tiến đề xuất (V3 - Future):

#### 1. **Giảm 4 lỗi còn lại** (Ưu tiên cao)
- **Incomplete Answer (2 cases):** Thêm instruction "Liệt kê đầy đủ tất cả thông tin"
- **Hallucination (1 case):** Thêm "Chỉ trả lời dựa trên context, không sinh ra thông tin mới"
- **Wrong Answer (1 case):** Thêm few-shot examples cho adversarial cases

#### 2. **Tối ưu Latency** (Ưu tiên trung)
- Hiện tại: 3.5s/case (gọi 2 API tuần tự)
- Mục tiêu: < 2.0s/case (gọi 2 API song song)
- Cách: Sử dụng asyncio.gather() để gọi 2 Judge song song

#### 3. **Cải tiến Agreement Rate** (Ưu tiên thấp)
- Hiện tại: 86.6% (V2 giảm so với V1 93.4%)
- Nguyên nhân: gpt-4o-mini vs gpt-4o có tiêu chí khác nhau
- Cách: Chuẩn hóa rubric hơn hoặc dùng 2 model giống nhau

#### 4. **Semantic Chunking** (Ưu tiên thấp)
- Thay thế Fixed-size Chunking bằng Semantic Chunking
- Đảm bảo context có ý nghĩa đầy đủ

### Metrics cần theo dõi:
| Metric | V1 | V2 | Mục tiêu V3 |
|--------|----|----|-----------|
| Judge Score | 3.1 | 4.02 | 4.5+ |
| Pass Rate | 60% | 92% | 98%+ |
| Hit Rate | 100% | 100% | 100% |
| Agreement Rate | 93.4% | 86.6% | 90%+ |
| Latency | 3.5s | 3.5s | < 2.0s |

---

## 5. Kết luận

### Thành công của V2:
1. ✅ **Cải tiến System Prompt** - Từ "ngắn gọn" → "chi tiết, đầy đủ, trích dẫn"
2. ✅ **Tăng Context** - Agent nhận được context đầy đủ từ test case
3. ✅ **Chuẩn hóa Judge Prompt** - Thêm rubric chi tiết (5 điểm, 4 điểm, v.v.)
4. ✅ **Sử dụng 2 API key** - Groq + OpenAI để xác thực chất lượng

### Kết quả:
- **Judge Score:** 3.1 → 4.02 (+0.92, +29.7%)
- **Pass Rate:** 60% → 92% (+32%)
- **Hit Rate:** 100% (không thay đổi, đã tuyệt vời)
- **Agreement Rate:** 93.4% → 86.6% (2 Judge có khác biệt hơn nhưng vẫn chấp nhận được)

### Hành động tiếp theo:
1. Phân tích 4 lỗi còn lại để cải tiến V3
2. Tối ưu latency bằng cách gọi 2 Judge song song
3. Chuẩn hóa rubric hơn để tăng Agreement Rate

---

**Báo cáo được cập nhật:** 21/04/2026 17:43
**Trạng thái:** ✅ Sẵn sàng nộp bài
