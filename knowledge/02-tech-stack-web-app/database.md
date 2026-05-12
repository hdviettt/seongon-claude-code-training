# Database — Nơi lưu data

## Định nghĩa 1 dòng

**Database (DB) = nơi web app lưu trữ data lâu dài, an toàn, tổ chức được.**

Khi user đăng ký tài khoản, post bài, mua hàng — tất cả data đó được lưu vào DB.

## Tại sao không lưu thẳng vào file?

Lưu vào file (Excel, CSV, JSON) chỉ ổn với data nhỏ, 1 người dùng. Khi web app có nhiều user truy cập cùng lúc, lưu data vào file gây:
- **Conflict**: 2 user ghi cùng lúc → mất data.
- **Chậm**: tìm 1 user trong file 100k dòng tốn nhiều giây.
- **Khó query**: muốn lấy "tất cả user đăng ký trong tháng 5" rất khó với file thuần.

→ DB giải quyết tất cả những vấn đề này, bằng cách tổ chức data theo cấu trúc, có index, có transaction.

## 2 loại DB chính

### 1. Relational (SQL) — quan hệ bảng

Data được tổ chức thành **bảng**, có cột rõ ràng, các bảng quan hệ với nhau qua **khoá**.

Ví dụ — DB của 1 blog:

**Bảng `users`:**
| id | tên | email |
|---|---|---|
| 1 | Việt | viet@gmail.com |
| 2 | An | an@gmail.com |

**Bảng `posts`:**
| id | user_id | tiêu đề | nội dung |
|---|---|---|---|
| 1 | 1 | Hello world | ... |
| 2 | 1 | Bài 2 | ... |
| 3 | 2 | An viết bài | ... |

`user_id` ở bảng `posts` quan hệ tới `id` ở bảng `users` — đó là khoá ngoại (foreign key).

**DB SQL phổ biến:**
- **PostgreSQL** — default khuyến nghị, mạnh mẽ, miễn phí, open source.
- **MySQL** — phổ biến, đặc biệt với WordPress.
- **SQLite** — nhẹ, lưu trong 1 file, dùng cho app nhỏ hoặc local.

### 2. Document (NoSQL) — không bảng cố định

Data lưu dưới dạng **document** (giống JSON), không cần định nghĩa cột trước.

```json
{
    "tên": "Việt",
    "email": "viet@gmail.com",
    "posts": [
        {"tiêu đề": "Hello world", "nội dung": "..."},
        {"tiêu đề": "Bài 2", "nội dung": "..."}
    ]
}
```

Mỗi document có thể có cấu trúc khác nhau.

**DB NoSQL phổ biến:**
- **MongoDB** — phổ biến nhất.
- **Firebase Firestore** — của Google, BaaS.
- **DynamoDB** — của AWS.

## Khi nào chọn loại nào?

| Use case | Chọn |
|---|---|
| Web app có user, post, comment, order — data có quan hệ | **Postgres** (SQL) |
| App đơn giản, 1 user, lưu local | **SQLite** |
| Data schema thay đổi nhiều, không cố định | **MongoDB** |
| Cần BaaS toàn diện (auth + DB + storage) ship nhanh | **Supabase** (Postgres) hoặc **Firebase** (NoSQL) |
| Cần search semantic (RAG, vector) | **Postgres + pgvector** |
| Cache, session, rate limit | **Redis** |

**Default an toàn:** Postgres. 90% web app dùng Postgres là đủ.

## Hosted DB — không tự quản lý server

Bạn không cần tự setup Postgres trên máy server — dùng dịch vụ hosted:

- **Railway** — đơn giản, $5-10/tháng cho 1 app + DB.
- **Supabase** — Postgres + auth + storage + realtime.
- **Neon** — Postgres serverless, có "branch DB" như Git.
- **Vercel Postgres** — tích hợp Vercel.
- **PlanetScale** — MySQL.

Default cho người mới: **Railway** hoặc **Supabase**.

## Schema — cấu trúc bảng

**Schema** = mô tả cấu trúc bảng: có cột gì, kiểu data gì, có ràng buộc gì.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

- `PRIMARY KEY` — khoá chính, mỗi row có ID duy nhất.
- `NOT NULL` — không được để trống.
- `UNIQUE` — không được trùng.

Khi build với Claude, bạn không cần viết SQL — Claude sẽ tự viết. Bạn chỉ cần mô tả "lưu user với tên, email" — Claude lo phần còn lại.

## Migration — thay đổi DB an toàn

**Migration** = script thay đổi schema (thêm cột mới, đổi tên bảng, xoá ràng buộc...).

Tại sao cần migration?
- DB production có data thật — không thể xoá đi tạo lại.
- Cần thay đổi từng bước, có thể rollback nếu sai.

ORM (Drizzle, Prisma) tự sinh migration cho bạn. Quy trình:
1. Sửa schema trong code.
2. ORM generate migration file (SQL).
3. Apply migration lên DB.

**Quan trọng:** luôn backup DB trước khi migrate production.

## ⚠️ Danger zone

Đây là 3 hành động trên DB **không bao giờ được để Claude tự quyết**:

1. **`DROP TABLE`** — xoá cả bảng, mất hết data.
2. **`DELETE FROM ... WITHOUT WHERE`** — xoá tất cả row trong bảng.
3. **Migration trên production mà chưa backup.**

Khi Claude muốn làm 1 trong 3 việc trên, **luôn dừng lại**, đọc kỹ, xác nhận trước khi đồng ý.

## DB khi audit dự án có sẵn

Đọc các file:
- `package.json` — tìm `pg`, `mongodb`, `prisma`, `drizzle-orm`.
- `.env.example` — tìm `DATABASE_URL`, `POSTGRES_URL`, `MONGO_URI`.
- Folder `migrations/`, `drizzle/`, `prisma/migrations/`.

## Tip thực chiến

Khi build mới:
- Mô tả **data bạn cần lưu** (user, post, order...), không mô tả "tôi muốn dùng Postgres".
- Để Claude đề xuất schema, bạn review lại.
- Luôn dùng hosted DB cho production (Railway/Supabase) — đừng tự host nếu không có lý do.

## Tiếp theo

Đọc [`security.md`](security.md) — bảo mật ở tầng 2.
