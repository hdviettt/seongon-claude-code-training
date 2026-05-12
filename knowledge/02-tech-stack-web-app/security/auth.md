# Upgrade Path: Thêm Authentication

## Khi nào bạn cần auth

- Có **admin area** (CRUD bài viết, sản phẩm) → cần phân biệt admin vs public.
- App cá nhân hoá (mỗi user thấy data riêng).
- Cần lưu user profile, history.

Web app public-read-only thuần (như landing page) **không cần auth.**

## Decision tree

### Bạn dùng stack gì?

```
Next.js → NextAuth (Auth.js)
Vite + React → Lucia, Clerk, hoặc Supabase Auth
Stack khác → tuỳ
```

### Bạn cần loại login gì?

| Loại | Pick |
|---|---|
| Chỉ "admin login" (1-2 người, không phải public) | **Email + password** đơn giản, hoặc **email magic link** |
| User public, đăng ký được | **OAuth (Google + Email)** |
| Enterprise, SSO | **Clerk Organizations** hoặc **WorkOS** |
| Cực nhanh, không muốn maintain | **Clerk** (đẹp sẵn, drop-in) |

## Recipe 1 — Admin-only auth cho Blog (Next.js + NextAuth)

**Scenario phổ biến cho học viên:** blog có admin CRUD, chỉ bạn được vào admin.

### Bước 1 — Cài

```bash
bun add next-auth@beta @auth/drizzle-adapter
```

### Bước 2 — Tạo `auth.ts` ở root

```typescript
import NextAuth from "next-auth"
import Google from "next-auth/providers/google"

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [Google],
  callbacks: {
    authorized: async ({ auth, request }) => {
      // Chỉ cho phép email admin truy cập admin routes
      const isAdmin = auth?.user?.email === process.env.ADMIN_EMAIL
      const isOnAdmin = request.nextUrl.pathname.startsWith('/admin')
      if (isOnAdmin && !isAdmin) return false
      return true
    },
  },
})
```

### Bước 3 — Tạo route handler

`app/api/auth/[...nextauth]/route.ts`:
```typescript
import { handlers } from "@/auth"
export const { GET, POST } = handlers
```

### Bước 4 — Tạo middleware

`middleware.ts` ở root:
```typescript
export { auth as middleware } from "@/auth"
```

### Bước 5 — Setup Google OAuth

1. Vào https://console.cloud.google.com.
2. Create project → "OAuth consent screen" → "External".
3. "Credentials" → "Create Credentials" → "OAuth client ID" → Web application.
4. Authorized redirect URIs:
   - Dev: `http://localhost:3000/api/auth/callback/google`
   - Prod: `https://yourapp.vercel.app/api/auth/callback/google`
5. Copy Client ID + Secret vào `.env.local`:
   ```
   AUTH_SECRET=<chạy: openssl rand -base64 32>
   AUTH_GOOGLE_ID=<client id>
   AUTH_GOOGLE_SECRET=<client secret>
   ADMIN_EMAIL=your-email@gmail.com
   ```

### Bước 6 — Thêm Login/Logout button

`app/components/AuthButton.tsx`:
```typescript
import { auth, signIn, signOut } from "@/auth"

export async function AuthButton() {
  const session = await auth()
  return session ? (
    <form action={async () => { 'use server'; await signOut() }}>
      <button>Sign out ({session.user?.email})</button>
    </form>
  ) : (
    <form action={async () => { 'use server'; await signIn('google') }}>
      <button>Sign in with Google</button>
    </form>
  )
}
```

### Bước 7 — Bảo vệ admin routes

Mọi page trong `app/admin/*` đã auto-protected bởi middleware. Trong page:

```typescript
import { auth } from "@/auth"
import { redirect } from "next/navigation"

export default async function AdminPage() {
  const session = await auth()
  if (session?.user?.email !== process.env.ADMIN_EMAIL) redirect('/')
  
  return <AdminDashboard />
}
```

### Bước 8 — Update `.env.example`

```
AUTH_SECRET=
AUTH_GOOGLE_ID=
AUTH_GOOGLE_SECRET=
ADMIN_EMAIL=
```

## Recipe 2 — User auth public (đăng ký được)

Tương tự Recipe 1 nhưng bỏ check `ADMIN_EMAIL`. User nào login cũng được.

Thêm:
- Drizzle adapter để lưu users + sessions vào DB.
- Trang `/dashboard` sau khi login.
- Logic phân quyền nếu cần.

Prompt cho Claude:
```
Setup user auth cho app Next.js của tôi:
- Provider: Google OAuth + email magic link.
- Lưu users vào DB (đang dùng Drizzle + Postgres).
- Trang /dashboard sau khi login.
- Mỗi user chỉ thấy data riêng của họ (filter theo user_id).
```

## Recipe 3 — Clerk (ship cực nhanh, không cần code auth)

Khi bạn muốn skip toàn bộ phần phức tạp:

```bash
bun add @clerk/nextjs
```

`middleware.ts`:
```typescript
import { clerkMiddleware } from "@clerk/nextjs/server"
export default clerkMiddleware()
```

`.env.local`:
```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=...
CLERK_SECRET_KEY=...
```

Pricing: free tier 10,000 MAU. $25/tháng cho 10k+.

Trade-off: lock-in Clerk, customize UI khó hơn.

## ⚠️ Cấm

- **Cấm hardcode password** trong code.
- **Cấm so sánh password không hash.** Luôn `bcrypt.compare()`.
- **Cấm gửi password qua email** plain.
- **Cấm để CORS `*`** cho API có auth.
- **Cấm để JWT secret hardcode** — luôn trong env.

## Tip thực chiến

- **Admin auth + 1 email cụ thể** = pattern đơn giản nhất cho học viên. Đừng phức tạp hoá lúc đầu.
- **Test login flow trên cả dev và production** trước khi báo "done".
- **Lưu `AUTH_SECRET` khác nhau giữa dev và production.**

## Prompt cho Claude làm hộ

```
Tôi có Next.js 14 app với blog (admin có thể CRUD bài viết). 
Hiện chưa có auth. Hãy:

1. Setup NextAuth v5 với Google OAuth.
2. Chỉ 1 email cụ thể (admin@gmail.com) được truy cập /admin/*.
3. Middleware bảo vệ tất cả route /admin/*.
4. Thêm login/logout button trên header.
5. Update .env.example.
6. Hướng dẫn tôi tạo Google OAuth credentials.
```

## Kiến thức liên quan

- [`security/`](../security/)
- [`recipes/blog-admin-cms.md`](../recipes/blog-admin-cms.md) — Sau khi có auth, build admin CRUD.
