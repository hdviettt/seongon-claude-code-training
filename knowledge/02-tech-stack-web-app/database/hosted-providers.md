# Upgrade Path: Thêm Database

## Quyết định 1 — Bạn cần loại data gì?

| Loại data | DB phù hợp |
|---|---|
| User, post, order, comment — có quan hệ rõ | **Postgres** (SQL) — 90% case |
| Document fluid, schema thay đổi nhiều | MongoDB |
| Cần search semantic (RAG, AI) | Postgres + pgvector |
| App nhỏ, 1 user, local | SQLite |

**Default cho học viên: Postgres.** Phần dưới giả định bạn dùng Postgres.

## Quyết định 2 — Deploy ở đâu? → Chọn DB hosted theo nó

Đây là phần quan trọng nhất.

### Bạn deploy app trên **Vercel**?

→ Vercel **không có Postgres built-in tốt**. Dùng provider riêng:

**Option A — Neon (Recommended)**
- Postgres serverless.
- Free tier rộng (0.5GB storage).
- Branch DB như Git (preview deploy có DB riêng).
- Pricing: free → $19/tháng cho 10GB.
- Setup: https://neon.tech → tạo project → copy connection string.

**Option B — Supabase**
- Postgres + Auth + Storage + Realtime trong 1 service.
- Free tier: 500MB DB, 1GB storage, 50,000 active user/tháng.
- Pricing: free → $25/tháng.
- Khi nào pick Supabase thay Neon: bạn muốn auth + storage cùng nhà.

**Option C — Vercel Postgres**
- Tích hợp sẵn trong dashboard Vercel.
- Pricing: $20/tháng cho Hobby, $100/tháng cho Pro.
- Đắt hơn Neon, ít linh hoạt.
- Pick khi bạn muốn tất cả trong 1 dashboard.

**Khuyến nghị mặc định: Neon.**

### Bạn deploy app trên **Railway**?

→ Railway **có Postgres built-in** — cực tiện.

- Click "Add Postgres" trong dashboard project Railway.
- Railway tự cấp `DATABASE_URL` cho app.
- Free tier: $5 credit/tháng (đủ cho dev).
- Pricing: pay-as-you-go từ $5/tháng.

**Khuyến nghị mặc định: Postgres của Railway luôn — không cần provider khác.**

### Bạn deploy trên **Cloudflare Pages / Workers**?

→ Cloudflare có:
- **D1** — SQLite distributed (cho data nhỏ).
- **Hyperdrive + Neon** — Postgres qua Cloudflare connection pooling.

Pick D1 nếu app nhẹ. Pick Neon qua Hyperdrive nếu cần Postgres.

### Bạn chưa deploy / deploy chỗ khác?

Đọc [`deployment/platforms.md`](../deployment/platforms.md) trước, hoặc:
- Test local: SQLite (file `.db` trong project).
- Production: Postgres + Neon.

## Quyết định 3 — ORM nào?

Đa số stack Next.js / Node:

| ORM | Pick khi |
|---|---|
| **Drizzle** | Default. Lightweight, SQL-first, types tốt. |
| **Prisma** | Bạn đã quen, hoặc team đã dùng. Dev UX tốt hơn, bundle nặng hơn. |

**Default: Drizzle.**

Python:
- **SQLAlchemy** — default.

## Setup từng bước (Next.js + Postgres + Drizzle + Neon)

### Bước 1 — Tạo DB trên Neon

1. https://neon.tech → đăng ký.
2. Create project → ghi nhớ "Connection string".
3. Lưu vào `.env.local`:
   ```
   DATABASE_URL=postgresql://user:pass@ep-xxx.aws.neon.tech/neondb?sslmode=require
   ```

### Bước 2 — Cài Drizzle

```bash
bun add drizzle-orm postgres
bun add -D drizzle-kit
```

### Bước 3 — Define schema

`db/schema.ts`:
```typescript
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core'

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  content: text('content').notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
})
```

### Bước 4 — Setup Drizzle config

`drizzle.config.ts`:
```typescript
import type { Config } from 'drizzle-kit'

export default {
  schema: './db/schema.ts',
  out: './drizzle',
  dialect: 'postgresql',
  dbCredentials: { url: process.env.DATABASE_URL! },
} satisfies Config
```

### Bước 5 — Generate + run migration

```bash
bun drizzle-kit generate    # tạo SQL migration
bun drizzle-kit migrate     # apply lên DB
```

### Bước 6 — Tạo DB client để dùng trong app

`db/index.ts`:
```typescript
import { drizzle } from 'drizzle-orm/postgres-js'
import postgres from 'postgres'

const client = postgres(process.env.DATABASE_URL!)
export const db = drizzle(client)
```

### Bước 7 — Dùng trong API route

`app/api/posts/route.ts`:
```typescript
import { db } from '@/db'
import { posts } from '@/db/schema'

export async function GET() {
  const allPosts = await db.select().from(posts)
  return Response.json(allPosts)
}

export async function POST(request: Request) {
  const body = await request.json()
  const [newPost] = await db.insert(posts).values(body).returning()
  return Response.json(newPost)
}
```

### Bước 8 — Update `.env.example`

```
DATABASE_URL=
```

Commit `.env.example`, KHÔNG commit `.env.local`.

## Prompt cho Claude làm hộ

```
Tôi có Next.js 14 app, deploy trên Vercel. Hãy setup database cho tôi:

1. Database: Postgres trên Neon (recommended cho Vercel).
2. ORM: Drizzle.
3. Schema cần có: <mô tả data, vd: posts với id, title, content, createdAt>.
4. Tạo API routes /api/posts (GET, POST) và /api/posts/:id (GET, PUT, DELETE).
5. Tạo .env.example.
6. Hướng dẫn tôi tạo Neon project và lấy connection string.

Sau khi xong, test bằng cách insert 1 post và list ra.
```

Claude sẽ làm step by step, hỏi bạn khi cần input (connection string).

## Khi đã có DB rồi, cần migrate sang loại khác?

Hiếm khi cần. Nếu thật sự cần (ví dụ từ SQLite local → Postgres production):

1. Export data hiện tại ra JSON.
2. Setup DB mới.
3. Viết script import JSON → DB mới.
4. Update `DATABASE_URL` trong env.

Đừng tự làm — bảo Claude:
```
Tôi đang dùng SQLite, muốn migrate sang Postgres trên Neon. 
Hãy lên kế hoạch + script migration. Tôi sẽ backup trước khi chạy.
```

## ⚠️ Cấm

- **Cấm commit DB password** vào Git. Luôn dùng `.env`.
- **Cấm chạy `DROP TABLE`** trên production mà chưa backup.
- **Cấm chạy migration** trên production mà chưa test trên dev.

## Tóm tắt

| Bạn đang... | Pick |
|---|---|
| Deploy trên Vercel | Postgres + Neon |
| Deploy trên Railway | Postgres built-in của Railway |
| Deploy trên Cloudflare | D1 (nhẹ) hoặc Neon qua Hyperdrive |
| Chưa deploy | SQLite local cho dev → Neon cho production |
| Stack Next.js | Drizzle ORM |
| Stack Python | SQLAlchemy |

## Kiến thức liên quan

- [`database/`](../database/)
- [`deployment/platforms.md`](../deployment/platforms.md)
