# Session 01 — Tech stack cho non-tech

## Đối tượng

Marketer, quản lý, người làm content/sale — không lập trình. Đã dùng hoặc sắp dùng Claude Code.

## Thesis

Non-tech dùng Claude Code không cần biết code, nhưng phải biết đủ để:
1. Đọc được Claude đang làm gì.
2. Chặn được khi Claude sắp phá.
3. Nói được idea bằng ngôn ngữ Claude hiểu.

Buổi học dạy **đọc bản đồ**, không dạy lập trình.

## Outcome (đo được khi buổi học kết thúc)

Học viên có thể:
- [ ] Vẽ lại diagram 3 tầng (Request flow / Security / Deployment) từ trí nhớ.
- [ ] Đọc 1 repo lạ và trả lời: stack là gì, deploy ở đâu, DB ở đâu.
- [ ] Nhận diện được 4 danger zones và biết khi nào phải dừng Claude.
- [ ] Giao việc cho Claude theo pattern feature → user story → acceptance.

## Cấu trúc (3 tiếng)

| Time | Phần | Mục tiêu | Format |
|---|---|---|---|
| 0:00-0:15 | Hook | Tạo niềm tin "tôi cũng làm được" | Video case study |
| 0:15-0:50 | Mental model 3 tầng | Diagram làm xương sống | Slide + ví dụ Shopee/Facebook |
| 0:50-1:10 | Vocabulary 20 từ | Cheatsheet take-home | In giấy |
| 1:10-1:20 | Giải lao | | |
| 1:20-1:50 | Đọc 1 dự án thật | "À hóa ra dễ thế" moment | Hands-on |
| 1:50-2:20 | Danger zones | Pattern dừng-tay | Demo video |
| 2:20-2:50 | Hands-on: build tool nhỏ | Áp dụng feature → user story | Live coding với Claude |
| 2:50-3:00 | Q&A + take-home | | |

## Materials cần chuẩn bị

- [ ] **Cheatsheet A4** — 3 tầng + 20 từ vựng + 4 danger zones (xem `handouts/cheatsheet.md` — chưa viết)
- [ ] **Slide deck** — ~30 slide max (xem `slides/` — chưa viết)
- [ ] **1 repo mẫu** đơn giản (Next.js + Postgres) để học viên đọc (xem `demos/sample-project/` — chưa setup)
- [ ] **Video "Claude sắp xóa DB"** — quay sẵn, đừng demo live (xem `demos/danger-demo.md` — chưa viết)
- [ ] **Bài tập hands-on** — form thu lead → Google Sheet (xem `exercises/form-thu-lead.md` — chưa viết)

## Cái sẽ trip up học viên

**Họ confuse "frontend" với "thiết kế đẹp"** và "backend" với "logic phức tạp".

Pre-empt từ slide đầu:
- Frontend = cái user **thấy + click** (đẹp hay xấu không liên quan).
- Backend = cái xử lý **sau khi user click** (đơn giản hay phức tạp không liên quan).

## Trạng thái

Draft — chưa có content. Việt sẽ guide từng phần.
