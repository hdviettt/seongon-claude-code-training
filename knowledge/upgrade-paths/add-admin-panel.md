# Upgrade Path: Thêm Admin Panel (CRUD)

## Khi nào bạn cần

- Có blog → cần admin tạo / sửa / xoá bài viết.
- Có site bán hàng → cần admin quản lý sản phẩm, đơn hàng.
- Có dashboard → cần admin update data.

## Prerequisites

- **Phải có auth trước.** Đọc [`add-auth.md`](add-auth.md) nếu chưa có.
- Phải có DB. Đọc [`add-database.md`](add-database.md) nếu chưa có.

## Cấu trúc admin panel chuẩn

```
app/
├── (public)/                  ← group routes public
│   ├── page.tsx               ← homepage
│   └── posts/
│       └── [id]/page.tsx      ← public post detail
├── admin/                      ← group routes admin (protected)
│   ├── layout.tsx              ← admin layout với sidebar
│   ├── page.tsx                ← admin dashboard
│   ├── posts/
│   │   ├── page.tsx            ← list posts (admin view)
│   │   ├── new/page.tsx        ← form tạo post
│   │   └── [id]/edit/page.tsx  ← form sửa post
│   └── ...
├── api/
│   ├── posts/                  ← public read
│   │   └── route.ts
│   └── admin/                  ← admin-only mutate
│       └── posts/
│           ├── route.ts        ← POST tạo
│           └── [id]/route.ts   ← PUT, DELETE
└── ...
```

Quy tắc:
- **Public routes**: ai cũng xem được (GET only).
- **Admin routes**: chỉ admin (POST/PUT/DELETE).
- API admin **bắt buộc check auth** ở mọi endpoint.

## Recipe: Blog admin CRUD

### Bước 1 — Schema DB (nếu chưa có)

`db/schema.ts`:
```typescript
import { pgTable, serial, text, timestamp, boolean } from 'drizzle-orm/pg-core'

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  slug: text('slug').notNull().unique(),
  content: text('content').notNull(),
  excerpt: text('excerpt'),
  coverImage: text('cover_image'),
  published: boolean('published').default(false),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
})
```

Run migration:
```bash
bun drizzle-kit generate
bun drizzle-kit migrate
```

### Bước 2 — API admin routes

`app/api/admin/posts/route.ts`:
```typescript
import { auth } from '@/auth'
import { db } from '@/db'
import { posts } from '@/db/schema'

export async function POST(request: Request) {
  // Check auth
  const session = await auth()
  if (session?.user?.email !== process.env.ADMIN_EMAIL) {
    return new Response('Unauthorized', { status: 401 })
  }

  const body = await request.json()
  const [newPost] = await db.insert(posts).values({
    title: body.title,
    slug: slugify(body.title),
    content: body.content,
    excerpt: body.excerpt,
    published: body.published ?? false,
  }).returning()

  return Response.json(newPost)
}

function slugify(text: string) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')
}
```

`app/api/admin/posts/[id]/route.ts`:
```typescript
import { auth } from '@/auth'
import { db } from '@/db'
import { posts } from '@/db/schema'
import { eq } from 'drizzle-orm'

async function requireAdmin() {
  const session = await auth()
  if (session?.user?.email !== process.env.ADMIN_EMAIL) {
    throw new Error('Unauthorized')
  }
}

export async function PUT(request: Request, { params }: { params: { id: string } }) {
  await requireAdmin()
  const body = await request.json()
  const [updated] = await db.update(posts)
    .set({ ...body, updatedAt: new Date() })
    .where(eq(posts.id, Number(params.id)))
    .returning()
  return Response.json(updated)
}

export async function DELETE(request: Request, { params }: { params: { id: string } }) {
  await requireAdmin()
  await db.delete(posts).where(eq(posts.id, Number(params.id)))
  return new Response(null, { status: 204 })
}
```

### Bước 3 — Admin layout với sidebar

`app/admin/layout.tsx`:
```typescript
import Link from 'next/link'
import { auth } from '@/auth'
import { redirect } from 'next/navigation'

export default async function AdminLayout({ children }: { children: React.ReactNode }) {
  const session = await auth()
  if (session?.user?.email !== process.env.ADMIN_EMAIL) redirect('/')

  return (
    <div className="flex min-h-screen">
      <aside className="w-64 border-r p-4">
        <h2 className="font-bold mb-4">Admin</h2>
        <nav className="space-y-2">
          <Link href="/admin" className="block">Dashboard</Link>
          <Link href="/admin/posts" className="block">Posts</Link>
        </nav>
      </aside>
      <main className="flex-1 p-8">{children}</main>
    </div>
  )
}
```

### Bước 4 — Form tạo post

`app/admin/posts/new/page.tsx`:
```typescript
'use client'
import { useRouter } from 'next/navigation'

export default function NewPostPage() {
  const router = useRouter()

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const form = new FormData(e.currentTarget)
    const res = await fetch('/api/admin/posts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: form.get('title'),
        content: form.get('content'),
        excerpt: form.get('excerpt'),
        published: form.get('published') === 'on',
      })
    })
    if (res.ok) router.push('/admin/posts')
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-2xl">
      <input name="title" placeholder="Title" required className="w-full p-2 border rounded" />
      <input name="excerpt" placeholder="Excerpt" className="w-full p-2 border rounded" />
      <textarea name="content" placeholder="Content (markdown OK)" rows={20} required
        className="w-full p-2 border rounded" />
      <label className="flex items-center gap-2">
        <input type="checkbox" name="published" />
        Published
      </label>
      <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">
        Create
      </button>
    </form>
  )
}
```

### Bước 5 — Danh sách post + nút edit/delete

`app/admin/posts/page.tsx`:
```typescript
import { db } from '@/db'
import { posts } from '@/db/schema'
import Link from 'next/link'

export default async function AdminPostsPage() {
  const all = await db.select().from(posts).orderBy(posts.createdAt)

  return (
    <div>
      <div className="flex justify-between mb-6">
        <h1 className="text-2xl font-bold">Posts</h1>
        <Link href="/admin/posts/new" className="px-4 py-2 bg-blue-500 text-white rounded">
          + New Post
        </Link>
      </div>

      <table className="w-full border-collapse">
        <thead>
          <tr className="border-b">
            <th className="text-left p-2">Title</th>
            <th className="text-left p-2">Status</th>
            <th className="text-left p-2">Created</th>
            <th className="text-left p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {all.map(post => (
            <tr key={post.id} className="border-b">
              <td className="p-2">{post.title}</td>
              <td className="p-2">{post.published ? 'Published' : 'Draft'}</td>
              <td className="p-2">{new Date(post.createdAt).toLocaleDateString()}</td>
              <td className="p-2 space-x-2">
                <Link href={`/admin/posts/${post.id}/edit`}>Edit</Link>
                <DeleteButton id={post.id} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

// Component DeleteButton tách ra cho gọn (cần 'use client')
```

## UI components khuyến nghị

Thay vì viết HTML/CSS thô, dùng **shadcn/ui**:

```bash
bunx shadcn@latest init
bunx shadcn@latest add button input textarea table form dialog
```

Sau đó components có sẵn, đẹp, accessible.

## Upload ảnh cho post

Nếu post có cover image:

### Option A — Public folder (đơn giản, dev only)

Lưu vào `public/uploads/`. **Không scale lên production.**

### Option B — Cloudflare R2 / S3 / Vercel Blob

Production storage. Recommend:
- **Vercel Blob** — tích hợp Vercel, đắt nhưng tiện.
- **Cloudflare R2** — rẻ, S3-compatible.
- **Supabase Storage** — nếu đã dùng Supabase.

Prompt cho Claude:
```
Thêm upload ảnh cho admin tạo post. Dùng Vercel Blob storage. 
Upload từ form, lưu URL vào DB.
```

## Prompt cho Claude làm hộ

```
Tôi có Next.js 14 app blog với public read-only. Hãy add admin panel:

1. Schema: posts có title, slug, content, excerpt, coverImage, published, 
   createdAt, updatedAt.
2. API admin routes: /api/admin/posts (POST), /api/admin/posts/:id 
   (PUT, DELETE). Mỗi route check auth, chỉ admin (env ADMIN_EMAIL) 
   được access.
3. UI admin: /admin với sidebar, /admin/posts (list), /admin/posts/new 
   (form tạo), /admin/posts/:id/edit (form sửa).
4. Dùng shadcn/ui cho UI.
5. Bảo vệ /admin/* qua middleware.
6. Test flow: tạo post → publish → public xem được.
```

## ⚠️ Cấm

- **Cấm API admin không check auth** — kể cả 1 endpoint cũng phải check.
- **Cấm hardcode admin email** — luôn dùng env.
- **Cấm cho công khai DELETE endpoint** không qua auth.

## Kiến thức liên quan

- [`add-auth.md`](add-auth.md) — Phải có auth trước.
- [`add-database.md`](add-database.md) — Phải có DB trước.
- [`knowledge/02-tech-stack-web-app/security.md`](../02-tech-stack-web-app/security.md)
