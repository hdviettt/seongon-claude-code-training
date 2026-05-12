# 02 — Tech stack cho web app

## Khi nào học viên cần folder này

- Muốn build 1 web app (blog, landing page, dashboard, công cụ nội bộ, e-commerce).
- Đang đọc code của 1 dự án có sẵn, không hiểu các thành phần.
- Cần quyết định "dùng công nghệ gì cho idea này?"
- Nghe Claude Code nói "frontend", "backend", "deploy" mà không biết những từ này nghĩa gì.

## Tóm tắt

**Tech stack** = danh sách công nghệ để xây 1 sản phẩm.

Mọi web app đều có cấu trúc 3 tầng:

```
┌──────────────────────────────────────────────────────────┐
│ Tầng 1 — Luồng request                                   │
│ Frontend (cái user thấy) → Backend (xử lý) → Database    │
├──────────────────────────────────────────────────────────┤
│ Tầng 2 — Security                                        │
│ HTTPS, Authentication, Validation                        │
├──────────────────────────────────────────────────────────┤
│ Tầng 3 — Deployment                                      │
│ Source code → Git → CI/CD → Hosting                      │
└──────────────────────────────────────────────────────────┘
```

Khi build 1 web app với Claude Code, bạn cần biết đủ về cả 3 tầng để **giao việc đúng** — không cần biết viết code, nhưng phải biết "frontend là gì, backend là gì" để Claude hiểu bạn muốn làm gì.

## Files trong folder

Đọc theo thứ tự:

1. [`lap-trinh-co-ban.md`](lap-trinh-co-ban.md) — Nền tảng: biến, hàm, kiểu dữ liệu. Đọc nếu bạn chưa biết gì về lập trình.
2. [`frontend.md`](frontend.md) — Tầng 1: cái user thấy.
3. [`backend.md`](backend.md) — Tầng 1: cái xử lý sau khi user click.
4. [`database.md`](database.md) — Tầng 1: nơi lưu data.
5. [`security.md`](security.md) — Tầng 2: bảo mật.
6. [`deployment.md`](deployment.md) — Tầng 3: đưa code lên Internet.
7. [`source-control.md`](source-control.md) — Tầng 3: Git và GitHub.

## Prerequisites

- Đã setup được Claude Code (xem `knowledge/01-setup-claude-code/`).

## 4 quy tắc khi giao việc tech stack cho Claude Code

1. **Mô tả mục tiêu rõ ràng, không mô tả công nghệ.** Tệ: "làm cho tôi 1 trang Next.js". Tốt: "làm cho tôi 1 trang landing giới thiệu khoá học X, có form thu email".

2. **Để Claude Code quyết stack nếu bạn không có lý do cố định.** Khi build mới, nói "đề xuất stack phù hợp" thay vì bắt buộc.

3. **Khi audit dự án có sẵn, hỏi Claude đọc `package.json` / `requirements.txt` trước.** Đó là nơi Claude biết stack hiện tại.

4. **Mỗi tầng có 1 quyết định. Tổng 3-5 quyết định cho 1 web app.** Không quá phức tạp.

## Khoá học liên quan

Buổi 2 của khoá: [`sessions/buoi-2-tech-stack.md`](../../sessions/buoi-2-tech-stack.md)
