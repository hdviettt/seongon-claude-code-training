# Buổi 2 — 'Code' trong Claude Code (Tech Stack Web App)

## Mục tiêu buổi học

- Hiểu nền tảng của lập trình để dùng Claude Code hiệu quả.
- Nắm được kiến trúc 1 ứng dụng web (web app).
- Xây được 1 full-stack web app.

## Thời lượng

3 giờ.

## Outline

### Phần 1 — Chữa BTVN buổi 1 (15 phút)

Review các artifact học viên nộp: bài học lập trình cho non-tech (.ipynb), chat history.

### Phần 2 — Lập trình cơ bản (45 phút)

**Mục tiêu:** Hiểu các khái niệm cốt lõi để đọc code Claude viết.

Tham chiếu kiến thức:
- [`knowledge/02-tech-stack-web-app/lap-trinh-co-ban/`](../knowledge/02-tech-stack-web-app/lap-trinh-co-ban/)

Cover:
- Lập trình = con người dùng ngôn ngữ lập trình để hướng dẫn máy tính.
- Ngôn ngữ lập trình → ngôn ngữ máy tính.
- 4 khái niệm: Biến, Hàm, Toán tử, Control flow.
- Các kiểu dữ liệu: string, int, boolean, list, object.
- Thư viện (library).

Ví dụ minh hoạ: hàm `cộng(x, y)` viết bằng pseudocode tiếng Việt.

### Giải lao (10 phút)

### Phần 3 — Tech Stack tổng quan (30 phút)

**Mục tiêu:** Hiểu diagram 3 tầng của 1 web app.

Tham chiếu kiến thức:
- [`knowledge/02-tech-stack-web-app/README.md`](../knowledge/02-tech-stack-web-app/README.md)

Vẽ diagram 3 tầng:
1. Request flow: Frontend → Backend → Database
2. Security: HTTPS, Auth, Validation
3. Deployment: Source → Git → CI/CD → Hosting

### Phần 4 — Đi sâu từng tầng (60 phút)

**Mục tiêu:** Học viên biết khi nào dùng cái nào.

Cover (mỗi mảnh 8-10 phút):

#### Tầng 1 — Request flow

- [`frontend.md`](../knowledge/02-tech-stack-web-app/frontend/) — HTML/CSS/JS, React/Next.js, Tailwind, shadcn/ui.
- [`backend.md`](../knowledge/02-tech-stack-web-app/backend/) — Node/Python/Go, API, endpoints, ORM.
- [`database.md`](../knowledge/02-tech-stack-web-app/database/) — SQL vs NoSQL, Postgres mặc định, hosted DB.

#### Tầng 2 — Security

- [`security.md`](../knowledge/02-tech-stack-web-app/security/) — HTTPS, Auth (session/JWT/OAuth), Validation, rate limit, env vars.

#### Tầng 3 — Deployment

- [`deployment.md`](../knowledge/02-tech-stack-web-app/deployment/) — Vercel/Railway/Cloudflare, CI/CD, domain, monitoring.
- [`source-control.md`](../knowledge/02-tech-stack-web-app/source-control/) — Git, GitHub, branch, commit, PR.

### Phần 5 — Tổng kết (10 phút)

Tóm tắt diagram 3 tầng. Recap: với 1 idea bất kỳ, hỏi Claude:
> "Tôi muốn build X. Đề xuất stack 3 tầng cho tôi, kèm lý do."

## BTVN

Xem [`exercises/btvn-2-web-app-fullstack.md`](../exercises/btvn-2-web-app-fullstack.md).

## Slide

- `slides/4_Buổi 1 Claude Code cho SEO & Ads.pdf` (cuối file, từ trang 70)
- `slides/1_Buổi 2 Claude Code cho SEO & Ads.pdf`

## Khuyến nghị stack cho học viên BTVN

Default:
- **Frontend:** Next.js + Tailwind + shadcn/ui
- **Backend:** Next.js API routes
- **Database:** Postgres (Supabase hoặc Railway)
- **Auth:** NextAuth + Google OAuth
- **Hosting:** Vercel (nếu không DB phức tạp) hoặc Railway
- **Source control:** GitHub (public repo cho BTVN)
