# BENCHMARK.md — Lab #17: Multi-Memory Agent Benchmark Report

**Generated:** 2026-04-24 12:15:59

---

## 1. Benchmark Summary — 10 Multi-Turn Conversations

| # | Scenario | Group | Turns | No-Memory Result | With-Memory Result | Pass? |
|---|----------|-------|------:|------------------|-------------------|-------|
| 1 | Recall user name after 6 turns | profile_recall | 6 | Xin lỗi, tôi không có khả năng nhớ thông tin từ các cuộc trò... | Có chứ, tên bạn là Linh! Nếu có điều gì khác bạn muốn hỏi ho... | Pass |
| 2 | Allergy conflict update | conflict_update | 3 | Nếu bạn dị ứng đậu nành, bạn nên tránh tất cả các sản phẩm c... | Bạn đã chia sẻ rằng bạn dị ứng sữa bò. Nếu bạn cũng dị ứng đ... | Pass |
| 3 | Programming language preference | profile_recall | 3 | Nếu bạn mới bắt đầu với phát triển web và muốn có một framew... | Dựa trên sở thích của bạn với Python và kinh nghiệm của bạn ... | Pass |
| 4 | Recall previous debug lesson | episodic_recall | 3 | Tôi không có khả năng nhớ lại các cuộc trò chuyện trước đó, ... | Có, trong lần trước bạn đã gặp lỗi kết nối Docker container ... | Fail |
| 5 | Learning style preference | profile_recall | 3 | Để học deep learning hiệu quả theo cách hands-on, bạn có thể... | Để học deep learning hiệu quả theo phong cách hands-on, bạn ... | Pass |
| 6 | FAQ knowledge retrieval — ML concept | semantic_retrieval | 2 | Overfitting và underfitting là hai vấn đề phổ biến trong học... | Chắc chắn rồi! Dưới đây là sự khác nhau giữa overfitting và ... | Pass |
| 7 | Docker guide retrieval | semantic_retrieval | 2 | Trong Docker Compose, các container có thể kết nối với nhau ... | Các container trong Docker Compose có thể kết nối với nhau t... | Pass |
| 8 | Token budget trimming (long conversation) | trim_budget | 8 | Chắc chắn! Dưới đây là tóm tắt những nội dung chính mà chúng... | Chắc chắn rồi! Dưới đây là tóm tắt những gì chúng ta đã thảo... | Pass |
| 9 | Multi-fact profile update | conflict_update | 4 | Tôi không có khả năng ghi nhớ thông tin từ các cuộc trò chuy... | Chắc chắn rồi! Đây là những thông tin tôi nhớ về bạn:  - Tên... | Pass |
| 10 | Cross-session episodic recall | episodic_recall | 3 | Tôi không có khả năng nhớ lại thông tin từ các cuộc trò chuy... | Có, bạn đã deploy thành công project API Gateway lên Railway... | Pass |

**Overall Pass Rate:** 9/10 (90%)

---

## 2. Detailed Conversation Transcripts

### Scenario 1: Recall user name after 6 turns
**Group:** profile_recall | **Turns:** 6 | **Expected keyword:** `Linh`

**Description:** Agent should recall user name after several unrelated turns.

**Setup turns:**
- User: Xin chào, tôi tên là Linh.
- User: Hôm nay thời tiết đẹp quá nhỉ?
- User: Bạn có thể giới thiệu về machine learning không?
- User: Cảm ơn, rất hữu ích!
- User: Tôi đang học Python ở trường đại học.

**Test turn:** Bạn có nhớ tên tôi không?

**No-memory response:**
> Xin lỗi, tôi không có khả năng nhớ thông tin từ các cuộc trò chuyện trước. Tuy nhiên, bạn đã giới thiệu tên mình là Linh. Nếu bạn có câu hỏi hoặc cần hỗ trợ gì, hãy cho tôi biết nhé!

**With-memory response:**
> Có chứ, tên bạn là Linh! Nếu có điều gì khác bạn muốn hỏi hoặc chia sẻ, hãy cho tôi biết nhé!

**Result:** PASS (keyword `Linh` found)

### Scenario 2: Allergy conflict update
**Group:** conflict_update | **Turns:** 3 | **Expected keyword:** `đậu nành`

**Description:** Agent must update allergy fact (recency wins) and confirm the correction.

**Setup turns:**
- User: Tôi dị ứng sữa bò.
- User: Bạn gợi ý bữa sáng phù hợp cho tôi nhé.

**Test turn:** À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò. Tôi dị ứng gì vậy?

**No-memory response:**
> Nếu bạn dị ứng đậu nành, bạn nên tránh tất cả các sản phẩm chứa đậu nành, bao gồm sữa đậu nành, đậu phụ, và các sản phẩm chế biến từ đậu nành như tương miso và nước tương. Dị ứng đậu nành là một phản ứng miễn dịch với protein có trong đậu nành, và triệu chứng có thể bao gồm phát ban, ngứa, khó thở h

**With-memory response:**
> Bạn đã chia sẻ rằng bạn dị ứng sữa bò. Nếu bạn cũng dị ứng đậu nành, tôi sẽ lưu thông tin đó để hỗ trợ bạn tốt hơn trong tương lai. Nếu bạn cần gợi ý về bữa sáng không chứa cả sữa bò và đậu nành, hãy cho tôi biết nhé!

**Result:** PASS (keyword `đậu nành` found)

### Scenario 3: Programming language preference
**Group:** profile_recall | **Turns:** 3 | **Expected keyword:** `Python`

**Description:** Agent should recommend Python-based framework knowing user preference.

**Setup turns:**
- User: Tôi rất thích Python và không thích Java.
- User: Tôi cần tìm hiểu về web framework.

**Test turn:** Gợi ý cho tôi một web framework phù hợp.

**No-memory response:**
> Nếu bạn mới bắt đầu với phát triển web và muốn có một framework dễ sử dụng, tôi gợi ý bạn thử **Flask**. Flask rất nhẹ nhàng và linh hoạt, cho phép bạn dễ dàng xây dựng các ứng dụng web nhỏ và sau đó mở rộng chúng nếu cần. Nó có tài liệu hướng dẫn rõ ràng và cộng đồng hỗ trợ lớn, điều này sẽ giúp bạ

**With-memory response:**
> Dựa trên sở thích của bạn với Python và kinh nghiệm của bạn về web framework, tôi gợi ý bạn nên thử **Flask**. Đây là một micro-framework rất dễ sử dụng, cho phép bạn nhanh chóng xây dựng ứng dụng web mà không cần phải cấu hình quá nhiều.

**Lý do nên chọn Flask**:
- **Dễ học**: Flask có cú pháp rõ 

**Result:** PASS (keyword `Python` found)

### Scenario 4: Recall previous debug lesson
**Group:** episodic_recall | **Turns:** 3 | **Expected keyword:** `service name`

**Description:** Agent recalls Docker debugging episode from earlier in the session.

**Setup turns:**
- User: Hôm trước tôi bị lỗi kết nối Docker container, cuối cùng phải dùng docker service name thay vì localhost.
- User: Bài học là luôn dùng service name trong Docker Compose.

**Test turn:** Tôi lại bị lỗi kết nối trong Docker, bạn có nhớ kinh nghiệm trước đó không?

**No-memory response:**
> Tôi không có khả năng nhớ lại các cuộc trò chuyện trước đó, nhưng tôi có thể giúp bạn với vấn đề kết nối hiện tại trong Docker. Bạn có thể mô tả chi tiết về lỗi bạn đang gặp phải không? Ví dụ, bạn đang cố gắng kết nối từ container nào đến container nào, và thông báo lỗi cụ thể là gì?

**With-memory response:**
> Có, trong lần trước bạn đã gặp lỗi kết nối Docker container và đã phải sử dụng tên dịch vụ thay vì `localhost`. Bạn có thể cung cấp thêm chi tiết về lỗi lần này không? Ví dụ như thông báo lỗi cụ thể hay cấu hình Docker của bạn? Tôi sẽ cố gắng giúp bạn!

**Result:** FAIL (keyword `service name` not found)

### Scenario 5: Learning style preference
**Group:** profile_recall | **Turns:** 3 | **Expected keyword:** `hands-on`

**Description:** Agent suggests hands-on approach based on stored learning preference.

**Setup turns:**
- User: Tôi thích học kiểu hands-on, không thích đọc lý thuyết nhiều.
- User: Tôi đang học data science.

**Test turn:** Gợi ý cho tôi cách học deep learning hiệu quả.

**No-memory response:**
> Để học deep learning hiệu quả theo cách hands-on, bạn có thể tham khảo các phương pháp sau:

1. **Khóa học trực tuyến**: Tham gia các khóa học có tính thực hành cao từ các nền tảng như Coursera (Andrew Ng's Deep Learning Specialization), Udacity (Deep Learning Nanodegree), hoặc Fast.ai. Những khóa h

**With-memory response:**
> Để học deep learning hiệu quả theo phong cách hands-on, bạn có thể thực hiện những bước sau:

1. **Chọn Framework**: Bắt đầu với một framework phổ biến như TensorFlow hoặc PyTorch. Cả hai đều có tài liệu phong phú và cộng đồng hỗ trợ tốt.

2. **Thực hành qua dự án**: Tạo các dự án nhỏ để áp dụng kiế

**Result:** PASS (keyword `hands-on` found)

### Scenario 6: FAQ knowledge retrieval — ML concept
**Group:** semantic_retrieval | **Turns:** 2 | **Expected keyword:** `overfitting`

**Description:** Agent retrieves ML knowledge from semantic memory to explain concepts.

**Setup turns:**
- User: Tôi đang nghiên cứu về AI.

**Test turn:** Giải thích sự khác nhau giữa overfitting và underfitting.

**No-memory response:**
> Overfitting và underfitting là hai vấn đề phổ biến trong học máy khi xây dựng mô hình.

1. **Overfitting (Quá khớp)**: Xảy ra khi mô hình quá phức tạp và học rất kỹ các chi tiết và nhiễu trong dữ liệu huấn luyện. Mặc dù mô hình có thể đạt được độ chính xác cao trên dữ liệu huấn luyện, nhưng nó thườn

**With-memory response:**
> Chắc chắn rồi! Dưới đây là sự khác nhau giữa overfitting và underfitting trong machine learning:

### Overfitting
- **Định nghĩa**: Overfitting xảy ra khi mô hình học quá kỹ các đặc điểm và nhiễu trong dữ liệu huấn luyện, dẫn đến hiệu suất kém khi áp dụng cho dữ liệu mới. Mô hình này có thể đạt được

**Result:** PASS (keyword `overfitting` found)

### Scenario 7: Docker guide retrieval
**Group:** semantic_retrieval | **Turns:** 2 | **Expected keyword:** `service`

**Description:** Agent retrieves Docker networking info from semantic memory.

**Setup turns:**
- User: Tôi cần deploy ứng dụng bằng Docker.

**Test turn:** Làm sao để các container trong Docker Compose kết nối với nhau?

**No-memory response:**
> Trong Docker Compose, các container có thể kết nối với nhau dễ dàng thông qua tên dịch vụ (service name) mà bạn đã định nghĩa trong file `docker-compose.yml`. Dưới đây là các bước để thiết lập và kết nối các container:

1. **Tạo file `docker-compose.yml`**: Đầu tiên, bạn cần tạo một file có tên là `

**With-memory response:**
> Các container trong Docker Compose có thể kết nối với nhau thông qua tên dịch vụ (service name) được định nghĩa trong file `docker-compose.yml`. Mỗi dịch vụ sẽ được Docker tạo một DNS name tương ứng, cho phép các container giao tiếp với nhau mà không cần phải sử dụng địa chỉ IP.

Ví dụ, nếu bạn có m

**Result:** PASS (keyword `service` found)

### Scenario 8: Token budget trimming (long conversation)
**Group:** trim_budget | **Turns:** 8 | **Expected keyword:** `neural`

**Description:** Agent handles long conversation with token budget management.

**Setup turns:**
- User: Hãy giải thích chi tiết về neural networks.
- User: Tiếp tục giải thích về backpropagation.
- User: Gradient descent hoạt động thế nào?
- User: Batch normalization là gì?
- User: Dropout regularization hoạt động ra sao?
- User: So sánh Adam và SGD optimizer.
- User: Transfer learning là gì?

**Test turn:** Tóm tắt lại những gì chúng ta đã thảo luận.

**No-memory response:**
> Chắc chắn! Dưới đây là tóm tắt những nội dung chính mà chúng ta đã thảo luận:

1. **Neural Networks**:
   - Là mô hình tính toán lấy cảm hứng từ cấu trúc não người, gồm lớp đầu vào, lớp ẩn và lớp đầu ra.
   - Mỗi nơ-ron thực hiện phép toán tổng trọng số và áp dụng hàm kích hoạt.
   - Huấn luyện mạng

**With-memory response:**
> Chắc chắn rồi! Dưới đây là tóm tắt những gì chúng ta đã thảo luận:

1. **Neural Networks**:
   - Cấu trúc cơ bản gồm lớp đầu vào, lớp ẩn và lớp đầu ra.
   - Hoạt động dựa trên việc truyền thông tin qua các lớp và tối ưu hóa trọng số thông qua backpropagation.

2. **Backpropagation**:
   - Là thuật t

**Result:** PASS (keyword `neural` found)

### Scenario 9: Multi-fact profile update
**Group:** conflict_update | **Turns:** 4 | **Expected keyword:** `VinAI`

**Description:** Agent updates workplace fact (FPT → VinAI) and recalls all other facts.

**Setup turns:**
- User: Tôi tên Minh, 25 tuổi, sống ở Hà Nội.
- User: Tôi làm software engineer ở FPT.
- User: À không, tôi vừa chuyển sang VinAI rồi.

**Test turn:** Bạn nhớ gì về tôi?

**No-memory response:**
> Tôi không có khả năng ghi nhớ thông tin từ các cuộc trò chuyện trước. Tuy nhiên, tôi biết rằng bạn tên Minh, 25 tuổi, sống ở Hà Nội và vừa chuyển sang làm việc tại VinAI. Bạn có muốn chia sẻ thêm về bản thân không?

**With-memory response:**
> Chắc chắn rồi! Đây là những thông tin tôi nhớ về bạn:

- Tên bạn là Minh, 25 tuổi, và bạn sống ở Hà Nội.
- Bạn là software engineer và trước đây làm việc tại FPT, nhưng hiện tại bạn đã chuyển sang VinAI.

Nếu có thông tin nào bạn muốn thêm hoặc cập nhật, hãy cho tôi biết nhé!

**Result:** PASS (keyword `VinAI` found)

### Scenario 10: Cross-session episodic recall
**Group:** episodic_recall | **Turns:** 3 | **Expected keyword:** `health check`

**Description:** Agent recalls deployment episode and lessons learned.

**Setup turns:**
- User: Tôi vừa hoàn thành project API Gateway, dùng FastAPI và đã deploy thành công lên Railway.
- User: Bài học lớn nhất là cần setup health check endpoint trước khi deploy.

**Test turn:** Tôi sắp deploy project mới, bạn có nhớ kinh nghiệm deploy trước đó của tôi không?

**No-memory response:**
> Tôi không có khả năng nhớ lại thông tin từ các cuộc trò chuyện trước. Tuy nhiên, nếu bạn chia sẻ kinh nghiệm và bài học bạn đã học từ dự án trước, tôi có thể giúp bạn áp dụng chúng cho project mới hoặc cung cấp thêm thông tin và mẹo hữu ích cho việc deploy!

**With-memory response:**
> Có, bạn đã deploy thành công project API Gateway lên Railway và đã học được rằng việc thiết lập health check endpoint là rất quan trọng trước khi triển khai. Nếu bạn cần tư vấn hoặc hỗ trợ cụ thể cho project mới này, hãy cho tôi biết chi tiết hơn về nó nhé!

**Result:** PASS (keyword `health check` found)

---

## 3. Token Usage Analysis

| # | Scenario | No-Memory Tokens | With-Memory Tokens | Difference |
|---|----------|----------------:|-----------------:|----------:|
| 1 | Recall user name after 6 turns | 671 | 1668 | +997 |
| 2 | Allergy conflict update | 633 | 1380 | +747 |
| 3 | Programming language preference | 569 | 1566 | +997 |
| 4 | Recall previous debug lesson | 352 | 1234 | +882 |
| 5 | Learning style preference | 869 | 1735 | +866 |
| 6 | FAQ knowledge retrieval — ML concept | 366 | 1258 | +892 |
| 7 | Docker guide retrieval | 968 | 1622 | +654 |
| 8 | Token budget trimming (long conversation) | 6962 | 7636 | +674 |
| 9 | Multi-fact profile update | 277 | 1282 | +1005 |
| 10 | Cross-session episodic recall | 302 | 1216 | +914 |

---

## 4. Test Group Coverage

| Test Group | Scenarios | Passed | Rate |
|------------|----------:|-------:|-----:|
| profile_recall | 3 | 3 | 100% |
| conflict_update | 2 | 2 | 100% |
| episodic_recall | 2 | 1 | 50% |
| semantic_retrieval | 2 | 2 | 100% |
| trim_budget | 1 | 1 | 100% |

---

## 5. Reflection — Privacy & Limitations

### 5.1 PII/Privacy Risks

1. **Long-term Profile Memory** stores personally identifiable information (PII) directly:
   - User name, age, location, workplace, allergies, preferences
   - This is the **most sensitive memory type** because it contains explicit identity data
2. **Episodic Memory** may inadvertently store sensitive task details (e.g., proprietary code, internal system names)
3. **Semantic Memory** risk is lower since it stores domain knowledge, not user data

### 5.2 Most Sensitive Memory

**Long-term Profile Memory** is the most sensitive because:
- Contains direct PII (name, location, health data like allergies)
- Persists across sessions (long-lived)
- If breached, provides a complete user profile that can be used for identity theft

### 5.3 Deletion, TTL, and Consent

Our implementation supports **GDPR right-to-be-forgotten**:
- Each memory backend has a `delete(user_id)` method
- To fully delete a user's data, all 4 backends must be cleared:
  - `short_term.clear()` — removes conversation buffer
  - `long_term.delete(user_id)` — removes profile JSON file
  - `episodic.delete(user_id)` — removes episode JSONL file
  - `semantic.delete(source)` — removes user-contributed knowledge
- **Recommended TTL policy:**
  - Profile preferences: 90 days
  - Profile facts: 30 days
  - Episodes: 7 days
  - Short-term: session-only (auto-cleared)
- **Consent**: Agent should explicitly ask user before storing PII (opt-in model)

### 5.4 Technical Limitations

1. **LLM Fact Extraction Accuracy**: The LLM-based extractor may miss implicit facts or hallucinate facts not stated by the user. JSON parsing can fail on malformed LLM output.
2. **Semantic Search Quality**: Depends on embedding model quality. Short or ambiguous queries may retrieve irrelevant chunks. No re-ranking mechanism.
3. **No Real-time Sync**: Multiple agent instances cannot share memory state in real-time (no pub/sub). Dict-based profile store is single-process only.
4. **Token Budget Estimation**: tiktoken provides accurate counts for OpenAI models but the budget allocation between memory types is static (not adaptive).
5. **Episodic Retrieval**: Keyword-based matching is simplistic compared to embedding-based similarity. May miss semantically related but lexically different episodes.
6. **Conflict Resolution**: Simple recency-wins policy may be too aggressive — no user confirmation before overwriting important facts (e.g., medical data).
7. **Scale Limitations**: JSON/JSONL persistence does not scale beyond ~10K users. Production deployment would need Redis + PostgreSQL.

### 5.5 What Would Help Most?

- **Long-term profile** helps the agent the most — it enables personalization without repeating preferences each session
- **Episodic memory** has the highest risk if retrieved incorrectly — wrong past experience could lead to incorrect advice
- **Federated forgetting** is needed in multi-agent systems — deletion must propagate to all agents with a copy of the data
