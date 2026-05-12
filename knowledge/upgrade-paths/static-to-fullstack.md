# Upgrade Path: Web tĩnh → Fullstack thật sự

## Dấu hiệu bạn đang là web tĩnh (chưa fullstack)

Check 1 trong các dấu hiệu sau:
- Data hiển thị trên trang **hardcode** trong file `.tsx`/`.html` (ví dụ: array `posts = [{...}, {...}]` viết thẳng trong component).
- Form gửi xong **không lưu** đi đâu, hoặc chỉ `console.log()`.
- Không có folder `api/`, `routes/`, hoặc `app/api/` (Next.js).
- Không có file kết nối database (`db.ts`, `prisma/`, `drizzle/`).
- Không có file `.env.example` (hoặc có nhưng rỗng).
- Deploy URL có nhưng F12 → Network → không có request nào tới `/api/*`.

→ Đó là web tĩnh, không phải fullstack.

## Để thành fullstack thật sự, cần thêm 3 thứ

```
┌─────────────────────────────────────────────────┐
│ Bạn đã có:                                      │
│ ✓ Frontend (UI)                                 │
├─────────────────────────────────────────────────┤
│ Bạn cần thêm:                                   │
│ + Backend (API routes)                          │
│ + Database (lưu data thật)                      │
│ + Endpoint POST/PUT/DELETE (write data)         │
└─────────────────────────────────────────────────┘
```

## Decision tree

### Bước 1 — Bạn đang dùng framework gì?

```
package.json có "next" → Next.js → SANG BƯỚC 2A
package.json có "vite" + "react" → Vite/React → SANG BƯỚC 2B
HTML thuần / chỉ index.html → SANG BƯỚC 2C
```

### Bước 2A — Next.js: thêm API routes (cùng repo)

**Đây là path đơn giản nhất.** Next.js cho phép backend chung repo với frontend.

Folder cần tạo:
```
app/
├── api/
│   ├── posts/
│   │   ├── route.ts        ← GET, POST, /api/posts
│   │   └── [id]/
│   │       └── route.ts    ← GET, PUT, DELETE /api/posts/:id
│   └── ...
├── lib/
│   └── db.ts               ← kết nối database
└── ...
```

Prompt cho Claude:
```
Tôi đang có Next.js app, hiện hardcode data. Hãy:
1. Thêm Postgres database (đề xuất hosted phù hợp với deploy của tôi).
2. Setup Drizzle ORM với schema tương ứng với data đang hardcode.
3. Tạo API routes /api/posts (GET, POST) và /api/posts/:id (GET, PUT, DELETE).
4. Refactor component fetch từ API thay vì hardcode.
5. Tạo .env.example.
```

Sau đó đọc:
- [`add-database.md`](add-database.md) — chọn DB phù hợp.
- [`add-deployment.md`](add-deployment.md) — deploy lại với DB.

### Bước 2B — Vite/React: cần BE service riêng

Vite/React thuần không có backend builtin. Bạn cần thêm 1 service backend riêng.

**Options:**
1. **Migrate sang Next.js** (recommended cho người mới) — gộp FE và BE lại.
2. **Giữ Vite, thêm BE Node service** — phức tạp hơn, 2 service phải deploy.
3. **Dùng Supabase / Firebase** — backend được cung cấp sẵn, FE gọi thẳng.

**Khuyến nghị cho học viên non-tech:** **migrate sang Next.js**.

Prompt:
```
Tôi đang có Vite + React app. Hãy migrate sang Next.js 14 App Router 
để có backend cùng repo. Giữ nguyên UI, chỉ đổi framework.

Sau khi migrate, làm theo flow của Next.js để thêm API + DB.
```

### Bước 2C — HTML thuần: rebuild từ đầu với framework

Web HTML thuần không scale được lên fullstack. Cần rebuild với framework có sẵn structure.

Prompt:
```
Tôi có 1 trang HTML thuần với UI thế này: [mô tả]. Hãy rebuild thành 
Next.js app:
1. Giữ nguyên design và content.
2. Thêm Postgres database + Drizzle ORM.
3. Có CRUD cho [resource cụ thể: bài viết / sản phẩm / etc].
4. Tạo .env.example.
```

## Sau khi có backend + database

Bạn vẫn cần check:

- [ ] Có ít nhất 1 endpoint **POST** (tạo data mới) — không chỉ GET.
- [ ] Form trên UI **submit thật** vào API → DB.
- [ ] Refresh trang, data vẫn còn (không mất).
- [ ] F12 → Network → thấy request `/api/*` khi tương tác.
- [ ] Có thể truy cập từ 2 trình duyệt khác nhau, cùng thấy data như nhau.

5 tiêu chí trên = web app thực sự fullstack.

## Tip cuối

Khi nâng cấp, **đừng làm 1 lần tất cả.** Tách:
1. Setup DB + 1 endpoint GET đơn giản → test.
2. Thêm POST → test (form submit lưu được).
3. Thêm PUT/DELETE → test.
4. Thêm auth nếu cần (xem [`add-auth.md`](add-auth.md)).
5. Deploy lại (xem [`add-deployment.md`](add-deployment.md)).

Mỗi bước commit Git riêng → revert dễ khi sai.

## Kiến thức liên quan

- [`knowledge/02-tech-stack-web-app/backend.md`](../02-tech-stack-web-app/backend.md)
- [`knowledge/02-tech-stack-web-app/database.md`](../02-tech-stack-web-app/database.md)
- [`add-database.md`](add-database.md) — decision cụ thể về DB.
