# 02 — Tech stack cho web app

## Khi nào học viên cần folder này

- Muốn build 1 web app (blog, landing page, dashboard, e-commerce).
- Đang đọc code của 1 dự án có sẵn, không hiểu các thành phần.
- Cần quyết định "dùng công nghệ gì cho idea này?"
- Cần nâng cấp app hiện tại theo note giảng viên — xem `recipes/`.

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

## Sub-folders

Mỗi folder là 1 mảnh kiến thức tự đủ, có `README.md` overview + file con cho sub-topic.

| Folder | Nội dung |
|---|---|
| [`lap-trinh-co-ban/`](lap-trinh-co-ban/) | Nền tảng: biến, hàm, kiểu dữ liệu, thư viện |
| [`frontend/`](frontend/) | Cái user thấy: HTML/CSS/JS, React/Next, Tailwind |
| [`backend/`](backend/) | Cái xử lý: API, runtime, ORM |
| [`database/`](database/) | Nơi lưu data: Postgres, hosted providers, migrations |
| [`security/`](security/) | Auth, validation, rate limit, env vars |
| [`deployment/`](deployment/) | Đưa code lên Internet: Vercel/Railway, CI/CD, monitoring |
| [`source-control/`](source-control/) | Git, GitHub, branch, commit |
| [`recipes/`](recipes/) | Recipe thực chiến: static-to-fullstack, blog admin CMS |

## Thứ tự đọc

Học mới từ đầu: 1 → 2 → 3 → 4 → 5 → 6 → 7.
Nâng cấp app có sẵn: vào thẳng `recipes/`.

## Prerequisites

- Đã setup được Claude Code (`knowledge/01-setup-claude-code/`).

## 4 quy tắc khi giao việc tech stack cho Claude Code

1. **Mô tả mục tiêu rõ ràng, không mô tả công nghệ.** Tệ: "làm cho tôi 1 trang Next.js". Tốt: "làm cho tôi 1 trang landing giới thiệu khoá học X, có form thu email".

2. **Để Claude Code quyết stack nếu bạn không có lý do cố định.**

3. **Khi audit dự án có sẵn, hỏi Claude đọc `package.json` trước.**

4. **Mỗi tầng có 1 quyết định. Tổng 3-5 quyết định cho 1 web app.** Không quá phức tạp.

## Khoá học liên quan

Buổi 2: [`sessions/buoi-2-tech-stack.md`](../../sessions/buoi-2-tech-stack.md)
