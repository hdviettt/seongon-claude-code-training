# Backend — Cái xử lý sau khi user click

## Định nghĩa 1 dòng

**Backend = phần của web app chạy ở server, xử lý logic sau khi user gửi request từ frontend.**

User không nhìn thấy backend trực tiếp. Nhưng mọi tác vụ "đăng ký", "thanh toán", "gửi email", "lưu data" đều do backend làm.

## Tại sao cần backend?

Frontend chỉ chạy trong trình duyệt của user — nó **không thể**:
- Lưu data lâu dài (đóng tab là mất).
- Giữ bí mật (mọi code frontend đều public, ai cũng xem được).
- Gọi API có authentication an toàn.
- Gửi email, xử lý thanh toán.

→ Cần 1 chương trình chạy trên server (máy chủ ở xa) để làm những việc này. Đó là backend.

## Cấu trúc 1 request đơn giản

```
User click "Đăng ký"
  ↓
Frontend gửi request tới Backend
  POST /api/register { email: "viet@gmail.com" }
  ↓
Backend nhận request:
  1. Kiểm tra email có hợp lệ không
  2. Kiểm tra email đã tồn tại trong DB chưa
  3. Tạo user mới trong DB
  4. Gửi email confirm
  5. Trả về kết quả cho Frontend
  ↓
Frontend hiển thị: "Đăng ký thành công!"
```

## API và Endpoint

- **API** (Application Programming Interface) = cách Frontend "nói chuyện" với Backend.
- **Endpoint** = 1 URL cụ thể trong API.

Ví dụ:
- `POST /api/register` — endpoint để đăng ký.
- `GET /api/users/123` — endpoint để lấy thông tin user có ID 123.
- `DELETE /api/posts/456` — endpoint để xoá post 456.

`GET / POST / PUT / DELETE` là **method** — loại request:
- `GET` — lấy data.
- `POST` — tạo mới.
- `PUT` / `PATCH` — sửa.
- `DELETE` — xoá.

## Ngôn ngữ và framework backend phổ biến

Backend có thể viết bằng nhiều ngôn ngữ. Mỗi ngôn ngữ có framework riêng:

### Node.js (JavaScript / TypeScript)
- Phổ biến nhất hiện nay vì cùng ngôn ngữ với frontend.
- Framework: **Express**, **Fastify**, **Hono**, hoặc **Next.js API routes** (gộp với frontend).

### Python
- Mạnh cho AI, ML, data processing.
- Framework: **FastAPI** (hiện đại), **Django**, **Flask**.

### Go
- Hiệu năng cao, dùng cho service cần throughput lớn.
- Framework: **Gin**, **chi**, **Echo**.

### Ruby
- Framework: **Ruby on Rails** (vẫn rất phổ biến cho startup).

### Java / Kotlin
- Enterprise, hệ thống lớn. Framework: Spring Boot.

## Khi build mới, chọn backend nào?

| Use case | Pick |
|---|---|
| Web app đơn giản, frontend dùng Next.js | **Next.js API routes** (cùng repo, dễ deploy) |
| API dùng cho nhiều client (web + mobile) | **Node + Hono** hoặc **Fastify** |
| Có nhiều xử lý AI / ML / data | **Python + FastAPI** |
| Realtime (chat, collab) | **Node + WebSocket / Socket.io** |
| Throughput cực cao | **Go** |

**Default an toàn:** Next.js API routes — không cần deploy thêm service riêng, code chung repo với frontend.

## ORM — không viết SQL thuần

ORM (Object-Relational Mapping) = thư viện giúp bạn nói chuyện với database bằng code thay vì SQL thuần.

Phổ biến:
- **Drizzle ORM** (TypeScript) — modern, nhẹ.
- **Prisma** (TypeScript) — phổ biến, dev UX tốt.
- **SQLAlchemy** (Python).
- **TypeORM**, **Sequelize**.

Default cho TypeScript: **Drizzle** hoặc **Prisma**.

## Backend khi audit dự án có sẵn

Đọc các file sau để biết backend đang dùng gì:
- `package.json` — Node.js project: tìm `express`, `fastify`, `hono`, `next`.
- `requirements.txt` / `pyproject.toml` — Python: tìm `fastapi`, `django`, `flask`.
- `go.mod` — Go project.
- Folder `routes/`, `api/`, `controllers/`, `app/api/` — đây là code backend.

Nói với Claude: "đọc backend của repo này và cho tôi biết stack đang dùng".

## Tip thực chiến

Khi giao Claude build backend:
- **Mô tả việc cần làm**, không mô tả endpoint cụ thể.
  - Tệ: "tạo cho tôi `POST /api/register` nhận email và mật khẩu, hash bcrypt..."
  - Tốt: "user đăng ký bằng email + password, lưu vào DB, gửi email confirm. Đề xuất API cho tôi."
- **Để Claude tự đề xuất ORM**, trừ khi repo đã có sẵn.
- **Khi audit dự án có sẵn**, luôn cho Claude đọc `package.json` trước.

## Backend không phải lúc nào cũng cần

- Trang tĩnh thuần (landing 1 page, blog SSG): **không cần backend**.
- App dùng BaaS như **Supabase** / **Firebase**: backend được cung cấp sẵn, bạn chỉ viết frontend gọi thẳng.

→ Hỏi Claude: "với idea này tôi có cần backend riêng không?" trước khi build.

## Tiếp theo

Đọc [`database.md`](database.md) — nơi backend lưu data.
