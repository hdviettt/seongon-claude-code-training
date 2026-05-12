# Best Practice — Dùng Claude Code hiệu quả

## Mindset cốt lõi

> **Việc gì Claude Code cũng làm được.**

Người mới thường tự giới hạn: "tôi không biết code, làm sao bảo Claude X được". Đó là tư duy sai. Đúng là:

> "Tôi không cần biết code. Tôi mô tả vấn đề rõ ràng, Claude tự nghĩ cách. Nếu sai, tôi sửa mô tả, không sửa code."

Với mindset này, bạn sẽ:
- Giao việc lớn hơn (không chỉ "viết hàm này").
- Trao quyền hơn cho Claude (Plan Mode, Opus xhigh).
- Đo lường output thay vì process.

## 2 chỉ số đo "dùng tốt"

Sau khi có mindset đúng, bạn tối ưu:

### 1. Lãng phí tối thiểu

**Token = tiền.** Mỗi tin nhắn tốn token, mỗi context dài tốn token. Lãng phí token = lãng phí tiền.

Cách giảm lãng phí:

- **Dùng `/compact` định kỳ** khi cuộc trò chuyện dài.
- **Tách sub-agent cho task con** — sub-agent có context riêng, không kế thừa noise.
- **Đặt thông tin lặp lại vào `CLAUDE.md`** — không phải gõ lại mỗi session.
- **Đúng model cho đúng task** — Opus chỉ cho task khó, Sonnet cho hàng ngày, Haiku cho lặp.
- **Đúng effort cho đúng task** — xhigh chỉ khi cần.
- **Đừng cho Claude đọc 10,000 dòng Excel khi chỉ cần 200 dòng đầu.**

### 2. Chất lượng tối đa

Cách tăng chất lượng:

- **Plan Mode cho task lớn.** Để Claude lên kế hoạch trước, bạn review, rồi mới làm.
- **Cho Claude đủ context** — không úp mở, không "tôi nghĩ bạn hiểu".
- **Cho Claude đọc tài liệu liên quan** trước khi giao task.
- **Yêu cầu Claude self-check** — "trước khi đưa cho tôi, check lại checklist Y".
- **Iterate, không one-shot.** Output đầu tiên thường chưa hoàn hảo — feedback → Claude refine.

## 10 quy tắc thực hành

### 1. Bắt đầu mọi project bằng `/init` hoặc tự viết `CLAUDE.md`

Không có CLAUDE.md → Claude đoán mò → tốn token + sai context.

### 2. Plan Mode cho task lớn

Bạn không thể nhớ ra mọi yêu cầu. Plan Mode buộc bạn nghĩ đủ trước khi Claude bắt đầu.

```
Bật plan mode: Shift + Tab (2 lần) hoặc /plan
```

### 3. Một task lớn → tách thành sub-agents

Web app, research nhiều mặt, đa kênh marketing → dispatch sang sub-agents. Đừng để 1 agent ôm hết.

### 4. Workflow lặp → SKILL

Làm việc gì >5 lần với cùng quy trình → đóng gói thành SKILL.

### 5. Workflow deterministic → Hook

Mỗi lần tạo file `.md` cần format X → hook.

### 6. Đừng micromanage

Tệ: "viết function Y, tham số Z, trả về W, dùng thư viện..."
Tốt: "user cần làm việc X, output cần đạt Y. Bạn tự đề xuất stack."

Micromanage = Claude không phát huy được intelligence.

### 7. Đo bằng output, không đo bằng process

Đừng so sánh "Claude viết bao nhiêu dòng code". So sánh "tôi đã giao task gì, output có đạt yêu cầu không".

### 8. Cẩn thận với danger zone

4 hành động luôn dừng lại review trước khi để Claude làm:
- Migration DB.
- Deploy production.
- Force push / reset hard.
- Sửa `.env`.

### 9. Audit định kỳ

Tháng 1 lần:
- Xem các SKILL còn dùng không, có cái nào nên gộp hay xoá?
- `CLAUDE.md` còn relevant không?
- Hook nào đang chạy mà không cần thiết?

### 10. Tự hỏi "việc này nên dùng Claude Code không?"

Không phải mọi việc cần Claude Code. Việc 30 giây gõ thẳng vẫn nhanh hơn giao Claude. Việc đơn giản 1 phút → Haiku đủ, không cần Opus.

## Anti-patterns thường gặp

### Anti-pattern 1 — "Hỏi để cho biết"

```
Bạn: "Claude, lập trình là gì?"
Claude: <trả lời dài>
```

→ Tốn token Claude Code. Câu này nên hỏi Claude.ai (web app) hoặc đọc tài liệu.

Claude Code dành cho **hành động + làm việc với file** — không phải Q&A thuần.

### Anti-pattern 2 — Mô tả chi tiết code thay vì mục tiêu

```
Bạn: "tạo function tên là `register()` nhận tham số email kiểu string, hash password bằng bcrypt, lưu vào table users với cột id BIGINT..."
```

→ Bạn đang code thay Claude. Hãy mô tả MỤC TIÊU:
```
"User đăng ký bằng email + password. Lưu vào DB. Có gửi email confirm."
```

### Anti-pattern 3 — One-shot mọi task

```
Bạn: "Build cho tôi website + admin + payment + analytics + multi-language. Đi."
Claude: <làm nửa vời, sai chỗ này chỗ kia>
```

→ Tách. Build website trước. Test. Rồi mới thêm admin. Mỗi feature 1 PR.

### Anti-pattern 4 — Không review Claude làm gì

```
Bạn: "OK làm đi."
Claude: <approve hết>
Bạn: <không xem diff, không xem log>
```

→ 2 tuần sau phát hiện Claude xoá nhầm file. Quá muộn.

**Luôn xem Claude đang làm gì.** Plan Mode + approval = bạn vẫn control.

### Anti-pattern 5 — Đổ lỗi cho Claude

```
Bạn: "Claude làm hỏng mất rồi"
```

→ Thật ra: bạn approve mọi action mà không đọc, không có Plan Mode, không có Git để rollback.

Lỗi không phải ở Claude. Lỗi ở quy trình.

## Quy trình chuẩn cho 1 task

```
1. Nghĩ rõ mục tiêu (1-2 câu).
2. Mở Claude Code trong folder đúng.
3. /plan → mô tả task → Claude lên plan.
4. Review plan, edit nếu cần.
5. Approve → Claude thực thi.
6. Review từng action quan trọng (Yes / Yes don't ask / No).
7. Test output thực tế.
8. Commit changes vào Git.
9. /compact nếu task xong, cuộc trò chuyện sẽ tiếp tục.
```

## Tóm tắt

- **Mindset đúng**: việc gì Claude Code cũng làm được, bạn không cần biết code.
- **Tối ưu 2 chỉ số**: lãng phí tối thiểu (token), chất lượng tối đa (output).
- **10 quy tắc thực hành** + **5 anti-pattern cần tránh**.
- **Quy trình chuẩn 9 bước** cho mỗi task.

## Tiếp theo

[`alternatives.md`](alternatives.md) — Khi Claude Code đắt, xem alternatives.
