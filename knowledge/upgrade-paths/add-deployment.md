# Upgrade Path: Deploy lên Production

## Khi nào bạn cần

- App chạy local OK rồi (`bun run dev` ra UI ngon).
- Cần URL public, ai cũng truy cập được.
- Cần deploy lại sau khi thêm DB / auth.

## Decision tree

### Bạn dùng stack gì?

```
Next.js → Vercel (default) hoặc Railway
Vite + React (SPA) → Cloudflare Pages, Vercel, hoặc Netlify
Next.js + Postgres + custom worker → Railway (mọi thứ 1 chỗ)
App có cron / queue / long-running → Railway hoặc Fly.io
Static site (Astro, Next SSG, HTML) → Cloudflare Pages (free, fast)
```

### Stack của bạn có DB không?

```
Có DB → 
  Vercel: app trên Vercel + DB trên Neon
  Railway: app + DB cùng Railway (built-in Postgres)
Không DB →
  Vercel hoặc Cloudflare Pages
```

## Recipe 1 — Deploy Next.js lên Vercel (KHÔNG DB)

Use case: landing page, blog static, portfolio.

### Bước 1 — Push code lên GitHub

```bash
gh repo create my-app --public --source=. --remote=origin --push
```

(Hoặc nhờ Claude làm.)

### Bước 2 — Connect Vercel

1. https://vercel.com → đăng nhập bằng GitHub.
2. "Add New Project" → chọn repo.
3. Vercel tự detect Next.js, default config OK.
4. Click "Deploy".

### Bước 3 — URL live

Sau ~1 phút, Vercel hiện URL dạng `my-app.vercel.app`. Done.

### Bước 4 — Mỗi lần push code lên main, Vercel auto-deploy.

## Recipe 2 — Deploy Next.js + Postgres lên Vercel + Neon

Use case: blog có admin CRUD, e-commerce, app có DB.

### Bước 1 — Setup Neon

1. https://neon.tech → create project.
2. Copy connection string.

### Bước 2 — Setup Vercel project (như Recipe 1)

### Bước 3 — Thêm env variable trên Vercel

1. Vercel dashboard → Project → Settings → Environment Variables.
2. Add:
   - `DATABASE_URL` = (Neon connection string)
   - `AUTH_SECRET` = (chạy `openssl rand -base64 32`)
   - `AUTH_GOOGLE_ID`, `AUTH_GOOGLE_SECRET` (nếu có Google OAuth)
   - `ADMIN_EMAIL`
3. Apply cho cả 3 env: Production, Preview, Development.

### Bước 4 — Update Google OAuth redirect URLs

Trong Google Cloud Console:
- Authorized redirect URIs thêm: `https://my-app.vercel.app/api/auth/callback/google`.

### Bước 5 — Run migration trên Neon

Local terminal:
```bash
DATABASE_URL="<neon connection string>" bun drizzle-kit migrate
```

Hoặc chạy 1 lần qua Neon SQL editor.

### Bước 6 — Re-deploy

Vercel auto-deploy khi push code. Hoặc trigger manual: dashboard → Deployments → "Redeploy".

### Bước 7 — Test

- Mở URL → trang load không lỗi.
- Login admin → vào /admin → tạo post → public xem được.

## Recipe 3 — Deploy Next.js + Postgres lên Railway

Use case: bạn muốn 1 nhà cho cả app + DB. Đơn giản hơn Vercel+Neon.

### Bước 1 — Tạo Railway project

1. https://railway.app → New Project → Deploy from GitHub.
2. Chọn repo.
3. Railway tự detect Next.js.

### Bước 2 — Add Postgres service

1. Trong project Railway → "+" → "Database" → "Postgres".
2. Railway tạo DB, tự cấp `DATABASE_URL` cho app service.

### Bước 3 — Add env variables

Project Settings → Variables:
- `AUTH_SECRET`
- `AUTH_GOOGLE_ID`, `AUTH_GOOGLE_SECRET`
- `ADMIN_EMAIL`

(`DATABASE_URL` đã auto-set bởi Railway.)

### Bước 4 — Setup domain

Railway → Settings → Public Networking → "Generate Domain". URL dạng `my-app.up.railway.app`.

Hoặc custom domain: add domain, Railway cho DNS records, bạn config ở Cloudflare.

### Bước 5 — Run migration

Trong code, thêm script tự migrate khi start (cẩn thận production):

`package.json`:
```json
{
  "scripts": {
    "start": "bun drizzle-kit migrate && next start"
  }
}
```

Hoặc chạy manual:
```bash
railway run bun drizzle-kit migrate
```

### Bước 6 — Test

Mở URL Railway → test flow.

## Recipe 4 — Deploy Vite/React SPA lên Cloudflare Pages

Use case: SPA không cần SEO, dashboard sau login.

### Bước 1 — Build local thử

```bash
bun run build
```

Đảm bảo có folder `dist/` output.

### Bước 2 — Push lên GitHub

```bash
gh repo create my-app --public --source=. --remote=origin --push
```

### Bước 3 — Connect Cloudflare Pages

1. Cloudflare dashboard → Pages → "Create a project" → "Connect to Git".
2. Chọn repo.
3. Build settings:
   - Framework preset: Vite.
   - Build command: `bun run build`.
   - Build output: `dist`.

### Bước 4 — Deploy

Cloudflare build và deploy. URL: `my-app.pages.dev`.

## Domain & DNS

### Mua domain
- **Namecheap, GoDaddy** — truyền thống.
- **Cloudflare** — recommend, $10/năm, miễn phí WHOIS privacy.

### Setup DNS với Cloudflare

1. Trên dashboard hosting (Vercel/Railway), add custom domain.
2. Hosting cho bạn DNS records (CNAME hoặc A).
3. Vào Cloudflare DNS → add records.
4. Đợi 5 phút - vài giờ → domain live.

### HTTPS

Mọi hosting hiện đại (Vercel, Railway, Cloudflare) **auto bật HTTPS**. Bạn không phải làm gì.

## Monitoring sau deploy

### Logs

- Vercel: Dashboard → Project → Deployments → click deploy → Functions / Build logs.
- Railway: Dashboard → Project → Service → Logs.
- Cloudflare: Dashboard → Pages → Functions → Logs.

### Error tracking

Cài Sentry:
```bash
bunx @sentry/wizard@latest -i nextjs
```

Free tier 5,000 errors/tháng. Đủ cho học viên.

### Uptime monitoring

- **BetterStack** — free tier 10 monitor.
- **Cronitor** — free tier OK.

Add monitor cho URL chính → email/SMS alert khi down.

## Cách check deployment thật sự thành công

Checklist:
- [ ] URL load được trên trình duyệt private (incognito).
- [ ] F12 → Console không có error đỏ.
- [ ] Network tab → các API call đều 200 OK.
- [ ] Tạo data mới qua admin → public xem được.
- [ ] Logout / login lại → vẫn hoạt động.
- [ ] Test trên điện thoại (responsive OK).
- [ ] Refresh trang nhiều lần → data persist (không mất).

## Lỗi phổ biến khi deploy

### "500 Internal Server Error"

90% là **thiếu env variable**. Check Vercel/Railway dashboard → Variables → đảm bảo:
- `DATABASE_URL` set đúng.
- `AUTH_SECRET` set.
- OAuth credentials set.

### "Database connection error"

- `DATABASE_URL` sai format.
- DB chưa whitelist IP (Neon thường không cần, Railway tự handle).
- Migration chưa chạy (chạy `drizzle-kit migrate`).

### "OAuth redirect_uri_mismatch"

- Google Console: thêm redirect URI prod (`https://yourapp.com/api/auth/callback/google`).

### "Function timeout"

- Vercel free tier: 10s timeout cho serverless function. Function quá chậm.
- Optimize query DB, hoặc upgrade Vercel Pro (60s timeout).

## Prompt cho Claude làm hộ

```
Tôi có Next.js 14 app với Drizzle + Postgres + NextAuth (Google OAuth). 
Code đang local. Hãy:

1. Setup deploy lên [Vercel + Neon | Railway].
2. Tạo .env.example đầy đủ.
3. Hướng dẫn tôi:
   - Tạo Neon project (nếu Vercel) hoặc add Postgres service Railway.
   - Set env variables trên dashboard hosting.
   - Update Google OAuth redirect URIs cho domain production.
   - Run migration trên DB production.
4. Sau deploy, hướng dẫn tôi check 5 tiêu chí thành công.
```

## ⚠️ Cấm

- **Cấm commit secret** vào Git (`.env`, OAuth keys, DB password).
- **Cấm chạy migration prod** mà chưa backup.
- **Cấm push thẳng vào main** không qua review (cho dự án team).

## Tóm tắt

| Stack | Hosting recommend | DB recommend |
|---|---|---|
| Next.js không DB | Vercel | — |
| Next.js + Postgres | Vercel + Neon, hoặc Railway | Neon hoặc Railway Postgres |
| Vite + React SPA | Cloudflare Pages | — (gọi API ngoài) |
| App có cron/worker | Railway | Railway Postgres |
| Static site | Cloudflare Pages | — |

## Kiến thức liên quan

- [`knowledge/02-tech-stack-web-app/deployment.md`](../02-tech-stack-web-app/deployment.md)
- [`knowledge/02-tech-stack-web-app/source-control.md`](../02-tech-stack-web-app/source-control.md)
- [`add-database.md`](add-database.md)
