# BENCHMARK.md — Lab #17: Multi-Memory Agent Benchmark Report

**Generated:** 2026-04-24 12:04:29

---

## 1. Benchmark Summary — 10 Multi-Turn Conversations

| # | Scenario | Group | Turns | No-Memory Result | With-Memory Result | Pass? |
|---|----------|-------|------:|------------------|-------------------|-------|
| 1 | Recall user name after 6 turns | profile_recall | 6 | Xin lỗi, tôi không có khả năng nhớ thông tin từ cuộc trò chu... | Có, bạn tên là Linh! Nếu bạn có bất kỳ câu hỏi nào hoặc cần ... | Pass |
| 2 | Allergy conflict update | conflict_update | 3 | Nếu bạn dị ứng với đậu nành, bạn nên tránh tất cả các sản ph... | Bạn đã chia sẻ rằng bạn dị ứng đậu nành, không phải sữa bò. ... | Pass |
| 3 | Programming language preference | profile_recall | 3 | Nếu bạn mới bắt đầu với việc phát triển web bằng Python, tôi... | Nếu bạn đang tìm kiếm một web framework phù hợp, tôi khuyên ... | Fail |
| 4 | Recall previous debug lesson | episodic_recall | 3 | Tôi không có khả năng nhớ lại các cuộc trò chuyện trước đó, ... | Có, trong lần trước bạn đã gặp lỗi kết nối Docker container ... | Fail |
| 5 | Learning style preference | profile_recall | 3 | Để học deep learning hiệu quả, bạn có thể thử những cách sau... | Để học deep learning hiệu quả theo phong cách hands-on, bạn ... | Pass |
| 6 | FAQ knowledge retrieval — ML concept | semantic_retrieval | 2 | Overfitting và underfitting là hai vấn đề phổ biến trong việ... | Chắc chắn rồi! Dưới đây là sự khác nhau giữa overfitting và ... | Pass |
| 7 | Docker guide retrieval | semantic_retrieval | 2 | Để các container trong Docker Compose kết nối với nhau, bạn ... | Trong Docker Compose, các container có thể kết nối với nhau ... | Pass |
| 8 | Token budget trimming (long conversation) | trim_budget | 8 | Chúng ta đã thảo luận về một số khái niệm quan trọng trong h... | Chắc chắn rồi! Dưới đây là tóm tắt những chủ đề mà chúng ta ... | Pass |
| 9 | Multi-fact profile update | conflict_update | 4 | Tôi không có khả năng nhớ thông tin từ cuộc trò chuyện trước... | Hiện tại, tôi biết rằng bạn tên Minh, 25 tuổi, sống ở Hà Nội... | Pass |
| 10 | Cross-session episodic recall | episodic_recall | 3 | Xin lỗi, nhưng tôi không có khả năng nhớ được thông tin từ c... | Có, bạn đã deploy thành công project API Gateway với FastAPI... | Pass |

**Overall Pass Rate:** 8/10 (80%)

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
> Xin lỗi, tôi không có khả năng nhớ thông tin từ cuộc trò chuyện trước. Tuy nhiên, bạn đã giới thiệu mình là Linh. Nếu bạn cần trợ giúp về điều gì, hãy cho tôi biết nhé!

**With-memory response:**
> Có, bạn tên là Linh! Nếu bạn có bất kỳ câu hỏi nào hoặc cần trợ giúp, hãy cho tôi biết nhé!

**Result:** PASS (keyword `Linh` found)

### Scenario 2: Allergy conflict update
**Group:** conflict_update | **Turns:** 3 | **Expected keyword:** `đậu nành`

**Description:** Agent must update allergy fact (recency wins) and confirm the correction.

**Setup turns:**
- User: Tôi dị ứng sữa bò.
- User: Bạn gợi ý bữa sáng phù hợp cho tôi nhé.

**Test turn:** À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò. Tôi dị ứng gì vậy?

**No-memory response:**
> Nếu bạn dị ứng với đậu nành, bạn nên tránh tất cả các sản phẩm chứa đậu nành, bao gồm đậu hũ, sữa đậu nành, và các loại thực phẩm chế biến từ đậu nành. Dị ứng đậu nành có thể gây ra các phản ứng dị ứng như mẩn ngứa, khó thở, hoặc các vấn đề tiêu hóa. Nếu bạn có bất kỳ triệu chứng nào không rõ ràng, 

**With-memory response:**
> Bạn đã chia sẻ rằng bạn dị ứng đậu nành, không phải sữa bò. Nếu bạn cần gợi ý bữa sáng không chứa đậu nành, hãy cho tôi biết để tôi có thể giúp bạn với những lựa chọn phù hợp!

**Result:** PASS (keyword `đậu nành` found)

### Scenario 3: Programming language preference
**Group:** profile_recall | **Turns:** 3 | **Expected keyword:** `Python`

**Description:** Agent should recommend Python-based framework knowing user preference.

**Setup turns:**
- User: Tôi rất thích Python và không thích Java.
- User: Tôi cần tìm hiểu về web framework.

**Test turn:** Gợi ý cho tôi một web framework phù hợp.

**No-memory response:**
> Nếu bạn mới bắt đầu với việc phát triển web bằng Python, tôi khuyên bạn nên thử **Flask**. Đây là một framework nhẹ, dễ học và rất linh hoạt. Với Flask, bạn có thể nhanh chóng tạo ra một ứng dụng web cơ bản và mở rộng nó sau này khi bạn cần thêm tính năng.

Flask cũng có tài liệu hướng dẫn rất tốt v

**With-memory response:**
> Nếu bạn đang tìm kiếm một web framework phù hợp, tôi khuyên bạn nên thử **Flask**. Đây là một lựa chọn tuyệt vời cho những người mới bắt đầu với web development vì nó nhẹ, dễ hiểu và dễ dàng mở rộng. Bạn có thể nhanh chóng xây dựng các ứng dụng nhỏ và sau đó mở rộng chúng khi cần.

Nếu bạn muốn phát

**Result:** FAIL (keyword `Python` not found)

### Scenario 4: Recall previous debug lesson
**Group:** episodic_recall | **Turns:** 3 | **Expected keyword:** `service name`

**Description:** Agent recalls Docker debugging episode from earlier in the session.

**Setup turns:**
- User: Hôm trước tôi bị lỗi kết nối Docker container, cuối cùng phải dùng docker service name thay vì localhost.
- User: Bài học là luôn dùng service name trong Docker Compose.

**Test turn:** Tôi lại bị lỗi kết nối trong Docker, bạn có nhớ kinh nghiệm trước đó không?

**No-memory response:**
> Tôi không có khả năng nhớ lại các cuộc trò chuyện trước đó, nhưng tôi có thể giúp bạn với vấn đề kết nối trong Docker. Bạn có thể mô tả rõ hơn về lỗi mà bạn gặp phải? Ví dụ như thông báo lỗi cụ thể hoặc cấu hình của bạn?

**With-memory response:**
> Có, trong lần trước bạn đã gặp lỗi kết nối Docker container và đã phải sử dụng tên dịch vụ thay vì `localhost`. Bạn có thể cung cấp thêm chi tiết về lỗi lần này không? Ví dụ như thông báo lỗi cụ thể hoặc cấu hình Docker của bạn? Tôi sẽ giúp bạn phân tích và tìm giải pháp!

**Result:** FAIL (keyword `service name` not found)

### Scenario 5: Learning style preference
**Group:** profile_recall | **Turns:** 3 | **Expected keyword:** `hands-on`

**Description:** Agent suggests hands-on approach based on stored learning preference.

**Setup turns:**
- User: Tôi thích học kiểu hands-on, không thích đọc lý thuyết nhiều.
- User: Tôi đang học data science.

**Test turn:** Gợi ý cho tôi cách học deep learning hiệu quả.

**No-memory response:**
> Để học deep learning hiệu quả, bạn có thể thử những cách sau:

1. **Khóa học trực tuyến**: Tham gia các khóa học như Coursera (Andrew Ng), edX, hoặc Udacity. Các khóa học này thường có phần thực hành rất tốt.

2. **Thực hành với thư viện phổ biến**: Làm quen với TensorFlow hoặc PyTorch. Bắt đầu bằng

**With-memory response:**
> Để học deep learning hiệu quả theo phong cách hands-on, bạn có thể thực hiện những bước sau:

1. **Chọn Framework**: Bắt đầu với một framework phổ biến như TensorFlow hoặc PyTorch. Cả hai đều có tài liệu và cộng đồng hỗ trợ mạnh mẽ.

2. **Khóa Học Online**: Tham gia các khóa học thực hành như:
   - 

**Result:** PASS (keyword `hands-on` found)

### Scenario 6: FAQ knowledge retrieval — ML concept
**Group:** semantic_retrieval | **Turns:** 2 | **Expected keyword:** `overfitting`

**Description:** Agent retrieves ML knowledge from semantic memory to explain concepts.

**Setup turns:**
- User: Tôi đang nghiên cứu về AI.

**Test turn:** Giải thích sự khác nhau giữa overfitting và underfitting.

**No-memory response:**
> Overfitting và underfitting là hai vấn đề phổ biến trong việc huấn luyện mô hình học máy.

1. **Overfitting (Quá khớp)**: 
   - Xảy ra khi mô hình học quá nhiều từ dữ liệu huấn luyện, dẫn đến việc nó hoạt động rất tốt trên tập dữ liệu huấn luyện nhưng lại kém trên dữ liệu chưa thấy (tập kiểm tra). 


**With-memory response:**
> Chắc chắn rồi! Dưới đây là sự khác nhau giữa overfitting và underfitting trong machine learning:

### Overfitting
- **Định nghĩa**: Overfitting xảy ra khi mô hình học quá kỹ các đặc điểm và nhiễu trong dữ liệu huấn luyện, khiến nó hoạt động rất tốt trên dữ liệu huấn luyện nhưng kém trên dữ liệu mới 

**Result:** PASS (keyword `overfitting` found)

### Scenario 7: Docker guide retrieval
**Group:** semantic_retrieval | **Turns:** 2 | **Expected keyword:** `service`

**Description:** Agent retrieves Docker networking info from semantic memory.

**Setup turns:**
- User: Tôi cần deploy ứng dụng bằng Docker.

**Test turn:** Làm sao để các container trong Docker Compose kết nối với nhau?

**No-memory response:**
> Để các container trong Docker Compose kết nối với nhau, bạn có thể sử dụng tên dịch vụ được định nghĩa trong tệp `docker-compose.yml`. Docker Compose tự động tạo một mạng cho các dịch vụ trong cùng một tệp `docker-compose.yml`, vì vậy chúng có thể giao tiếp với nhau thông qua tên dịch vụ.

Dưới đây 

**With-memory response:**
> Trong Docker Compose, các container có thể kết nối với nhau thông qua tên dịch vụ (service name) được định nghĩa trong file `docker-compose.yml`. Mỗi dịch vụ sẽ được Docker tạo một DNS name tương ứng mà các container khác có thể sử dụng để giao tiếp.

Dưới đây là hướng dẫn chi tiết:

1. **Định nghĩa

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
> Chúng ta đã thảo luận về một số khái niệm quan trọng trong học máy và mạng nơ-ron, bao gồm:

1. **Neural Networks (Mạng Nơ-ron)**: Là cấu trúc tính toán lấy cảm hứng từ não bộ con người, sử dụng các nơ-ron để xử lý và phân tích dữ liệu.

2. **Backpropagation (Truyền Ngược)**: Là thuật toán cho phép 

**With-memory response:**
> Chắc chắn rồi! Dưới đây là tóm tắt những chủ đề mà chúng ta đã thảo luận:

1. **Neural Networks**:
   - Là một cấu trúc tính toán lấy cảm hứng từ não người, bao gồm các nơ-ron được kết nối, cho phép học và mô hình hóa các mối quan hệ phức tạp trong dữ liệu.

2. **Backpropagation**:
   - Là thuật toá

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
> Tôi không có khả năng nhớ thông tin từ cuộc trò chuyện trước. Tuy nhiên, hiện tại tôi biết bạn tên Minh, 25 tuổi, sống ở Hà Nội và vừa chuyển sang làm việc tại VinAI. Nếu bạn muốn chia sẻ thêm, tôi rất sẵn lòng lắng nghe!

**With-memory response:**
> Hiện tại, tôi biết rằng bạn tên Minh, 25 tuổi, sống ở Hà Nội, và bạn là một software engineer làm việc tại VinAI. Nếu có thông tin nào khác mà bạn muốn tôi ghi nhớ hoặc nếu bạn có câu hỏi nào khác, hãy cho tôi biết nhé!

**Result:** PASS (keyword `VinAI` found)

### Scenario 10: Cross-session episodic recall
**Group:** episodic_recall | **Turns:** 3 | **Expected keyword:** `health check`

**Description:** Agent recalls deployment episode and lessons learned.

**Setup turns:**
- User: Tôi vừa hoàn thành project API Gateway, dùng FastAPI và đã deploy thành công lên Railway.
- User: Bài học lớn nhất là cần setup health check endpoint trước khi deploy.

**Test turn:** Tôi sắp deploy project mới, bạn có nhớ kinh nghiệm deploy trước đó của tôi không?

**No-memory response:**
> Xin lỗi, nhưng tôi không có khả năng nhớ được thông tin từ các cuộc trò chuyện trước đó. Tuy nhiên, nếu bạn cần chia sẻ kinh nghiệm hoặc có câu hỏi về việc deploy project mới, tôi rất sẵn lòng hỗ trợ! Bạn đang lên kế hoạch deploy project gì?

**With-memory response:**
> Có, bạn đã deploy thành công project API Gateway với FastAPI lên Railway. Bạn cũng đã chia sẻ rằng bài học lớn nhất là cần thiết lập health check endpoint trước khi deploy. 

Nếu bạn cần hỗ trợ cụ thể nào cho việc deploy project mới này, chẳng hạn như cấu hình, các bước cần thực hiện, hoặc bất kỳ th

**Result:** PASS (keyword `health check` found)

---

## 3. Token Usage Analysis

| # | Scenario | No-Memory Tokens | With-Memory Tokens | Difference |
|---|----------|----------------:|-----------------:|----------:|
| 1 | Recall user name after 6 turns | 668 | 1220 | +552 |
| 2 | Allergy conflict update | 617 | 985 | +368 |
| 3 | Programming language preference | 573 | 1114 | +541 |
| 4 | Recall previous debug lesson | 302 | 958 | +656 |
| 5 | Learning style preference | 610 | 1289 | +679 |
| 6 | FAQ knowledge retrieval — ML concept | 438 | 1349 | +911 |
| 7 | Docker guide retrieval | 975 | 1783 | +808 |
| 8 | Token budget trimming (long conversation) | 6488 | 6798 | +310 |
| 9 | Multi-fact profile update | 266 | 1227 | +961 |
| 10 | Cross-session episodic recall | 311 | 1249 | +938 |

---

## 4. Test Group Coverage

| Test Group | Scenarios | Passed | Rate |
|------------|----------:|-------:|-----:|
| profile_recall | 3 | 2 | 67% |
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
