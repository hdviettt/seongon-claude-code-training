# Buổi 5 — Tự động hoá Claude Code

## Mục tiêu buổi học

- Biết cách dùng Claude Code khi không ở máy tính (remote control + GitHub).
- Hệ thống hoá best practice sau 4 buổi.
- Biết alternatives khi Claude Code quá đắt hoặc không phù hợp.

## Thời lượng

3 giờ.

## Outline

### Phần 1 — Chữa BTVN buổi 4 (20 phút)

Review team agents học viên đã build. Đánh giá:
- Sub-agents có description rõ không?
- SKILLs gọi từ sub-agents có hợp lý không?
- Khi giao nhiệm vụ lớn, Claude có dispatch đúng sub-agent không?

### Phần 2 — Remote Control (45 phút)

**Mục tiêu:** Học viên dùng được Claude Code từ điện thoại.

Tham chiếu:
- [`knowledge/05-tu-dong-hoa/remote-control.md`](../knowledge/05-tu-dong-hoa/remote-control.md)

Cover:
- 2 cách kết nối từ điện thoại:
  - `/remote-control` — cần máy tính bật.
  - GitHub repo — không cần máy tính.
- So sánh khi nào dùng cách nào.
- Setup notification để nhận alert khi Claude cần input.

Demo:
- Gõ `/remote-control` trên máy → kết nối app Claude trên điện thoại → giao task → xem Claude làm trên máy.
- Tạo session mới từ điện thoại với GitHub repo.

### Phần 3 — Best Practice (50 phút)

**Mục tiêu:** Hệ thống hoá những gì đã học sau 4 buổi thành mindset + 10 quy tắc.

Tham chiếu:
- [`knowledge/05-tu-dong-hoa/best-practice.md`](../knowledge/05-tu-dong-hoa/best-practice.md)

Cover:
- **Mindset cốt lõi:** "Việc gì Claude Code cũng làm được."
- 2 chỉ số đo: **lãng phí tối thiểu + chất lượng tối đa**.
- 10 quy tắc thực hành (CLAUDE.md ngay đầu, Plan Mode, sub-agents cho task lớn, SKILL cho lặp, hook cho deterministic, không micromanage, đo output không đo process, cẩn thận danger zone, audit định kỳ, hỏi "có cần Claude không").
- 5 anti-patterns cần tránh (hỏi để biết, mô tả code thay vì mục tiêu, one-shot, không review, đổ lỗi).
- Quy trình chuẩn 9 bước cho 1 task.

### Giải lao (10 phút)

### Phần 4 — Alternatives (35 phút)

**Mục tiêu:** Học viên biết khi nào nên xem xét tool khác.

Tham chiếu:
- [`knowledge/05-tu-dong-hoa/alternatives.md`](../knowledge/05-tu-dong-hoa/alternatives.md)

Cover:
- 4 alternatives chính: Codex, Antigravity, Cursor, OpenCode.
- Bảng so sánh: vendor, model, pricing, strength, khi nào dùng.
- Pattern khuyến nghị theo persona (1 người / team / hạn ngân sách).
- Migration giữa các tool (CLAUDE.md → AGENTS.md / Cursor rules; MCP standard cross-tool).

Nhấn mạnh: **học workflow** (SKILLs, agents, hooks, CLAUDE.md), không học tool. Workflow chuyển được, tool có thể thay.

### Phần 5 — Kết thúc khoá (20 phút)

Recap toàn khoá:
- Buổi 1 — Setup, hiểu Claude Code là gì.
- Buổi 2 — Hiểu tech stack web app.
- Buổi 3 — Mở rộng với Commands, SKILLs, kết nối ngoài.
- Buổi 4 — Sub-agents, Memory, Hooks.
- Buổi 5 — Remote control, best practice, alternatives.

Bước tiếp theo cho học viên:
- Apply 10 quy tắc trong best practice vào project thật.
- Build 1 SKILL cho việc làm nhiều nhất hằng ngày.
- Audit workspace 1 lần/tháng.

Q&A.

## Slide

`slides/3_Buổi 5 Claude Code cho SEO & Ads.pdf`

## Sau khoá học

Học viên có thể:
- Tự host repo này clone về máy để tham khảo bất cứ lúc nào.
- Hỏi Claude Code dựa trên `knowledge/` thay vì hỏi giảng viên.
- Đóng góp lại knowledge (mở PR) khi học được pattern mới.
