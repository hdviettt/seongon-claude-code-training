# Security — Bảo mật web app

> **Sub-file trong folder này:**
> - [`auth.md`](auth.md) — Authentication chi tiết (NextAuth, Clerk, OAuth, recipe admin-only auth).

## Định nghĩa 1 dòng

**Security = đảm bảo data và hành động trên web app không bị kẻ xấu lợi dụng.**

Bỏ qua security = sớm muộn cũng bị hack. Bị hack lần đầu có thể chỉ mất 1 ngày fix. Bị hack ở scale lớn = mất user, mất data, mất uy tín, có thể mất tiền lớn.

## 3 layer bảo mật bắt buộc

Mọi web app fullstack đều cần 3 layer này:

```
┌────────────────────────────────────────────┐
│ 1. Transport (kênh truyền)                 │
│    HTTPS / TLS — mã hoá data đi qua mạng   │
├────────────────────────────────────────────┤
│ 2. Authentication (định danh)              │
│    JWT / Session / OAuth                    │
├────────────────────────────────────────────┤
│ 3. Validation (kiểm tra input)             │
│    Sanitize + Rate limit                    │
└────────────────────────────────────────────┘
```

## 1. Transport — HTTPS / TLS

**HTTP** truyền data dạng plain text — ai chen vào giữa cũng đọc được. **HTTPS** mã hoá data → an toàn.

Nguyên tắc:
- **Mọi web app public-facing đều phải HTTPS.**
- Không bao giờ deploy app HTTP-only.

Hosting provider hiện đại (Vercel, Railway, Cloudflare) **tự bật HTTPS** — bạn không phải làm gì. Đó là 1 lý do để dùng họ thay vì tự host.

## 2. Authentication — User là ai?

Authentication = xác định **đây là user nào**.

### Các phương thức

**Email + Password**
- Cách truyền thống.
- Lưu password phải **hash** (bcrypt, argon2) — không bao giờ lưu plain text.

**Magic Link**
- User gõ email, hệ thống gửi link → click link là đăng nhập.
- UX tốt cho user, không cần nhớ password.
- Dùng dịch vụ: Resend, SendGrid để gửi mail.

**OAuth (Google, Facebook, GitHub login)**
- "Tiếp tục với Google" — user dùng tài khoản có sẵn.
- Tiện cho user, giảm friction đăng ký.

**SSO / SAML**
- Cho enterprise — user đăng nhập 1 lần dùng cho nhiều app trong tổ chức.

### Session vs JWT

Sau khi user đăng nhập, hệ thống cần "nhớ" user trong các request sau:

- **Session-based**: server tạo session ID, lưu cookie ở browser. Mỗi request browser gửi cookie kèm → server check session.
- **JWT (JSON Web Token)**: server tạo 1 token mã hoá, client lưu, gửi kèm mỗi request.

**Khi nào dùng cái nào:**
- Web app truyền thống → **Session** (an toàn hơn, dễ revoke).
- API dùng cho nhiều client (web + mobile) → **JWT**.

### Thư viện auth phổ biến

- **NextAuth / Auth.js** — default cho Next.js, drop-in OAuth providers.
- **Clerk** — BaaS, đẹp sẵn, free tier OK.
- **Supabase Auth** — đi kèm Supabase DB.
- **WorkOS** — cho enterprise SSO.
- **Lucia** — lightweight cho TypeScript.

**Default khuyến nghị:** NextAuth (nếu Next.js), Clerk (nếu cần ship cực nhanh).

## 3. Validation — Không tin user input

Mọi data đến từ user **đều phải kiểm tra trước khi xử lý**. Không tin bất cứ thứ gì client gửi lên.

### Input validation

- Validate cả ở client (UX tốt) và server (security).
- Dùng thư viện: **Zod**, **Yup**, **Valibot** (TypeScript).

Ví dụ với Zod:
```typescript
const schema = z.object({
    email: z.string().email(),
    age: z.number().min(0).max(150)
})
```

### Rate Limit

Giới hạn số request 1 user/IP có thể gửi trong khoảng thời gian.

Tại sao cần:
- Tránh brute force password.
- Tránh spam API.
- Tránh DOS attack (làm sập server bằng cách spam).

Quy tắc cơ bản:
- Auth endpoint: 5 lần / 15 phút / IP.
- API public: 60 req / phút / IP hoặc API key.
- Heavy endpoint (AI inference): 10 req / phút / user.

Thư viện: **Upstash Ratelimit**, **express-rate-limit**, hoặc dùng WAF của Cloudflare.

### Các attack phổ biến cần biết tên

- **SQL Injection** — kẻ xấu chèn câu SQL vào input. Cách phòng: dùng ORM (Drizzle, Prisma), không string-concat SQL.
- **XSS (Cross-Site Scripting)** — chèn JavaScript độc vào trang. Cách phòng: framework hiện đại (React, Next.js) tự escape. Tránh `dangerouslySetInnerHTML`.
- **CSRF (Cross-Site Request Forgery)** — site khác lừa user gửi request. Cách phòng: `SameSite=Lax` cookie, CSRF token.

## Environment variables — không hard-code secret

**Secret** = thông tin nhạy cảm: API key, DB password, JWT secret, OAuth client secret.

**KHÔNG BAO GIỜ:**
- Hard-code secret vào code.
- Commit secret lên Git (kể cả private repo).

**LUÔN:**
- Lưu secret trong file `.env` (không commit, đã có `.gitignore`).
- Trên production, set secret qua dashboard của hosting (Vercel, Railway).
- Code đọc qua `process.env.SECRET_NAME` hoặc tương đương.

File `.env.example` (có commit) chứa **tên biến** nhưng không có giá trị:
```
DATABASE_URL=
AUTH_SECRET=
GOOGLE_CLIENT_ID=
```

→ Người mới clone repo về biết cần set biến nào, nhưng không thấy secret thật.

## Security headers — set 1 lần, an toàn cả đời

Trong middleware của app, set các header sau:

```
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
```

Claude Code có thể set giúp bạn — chỉ cần nói "add security headers chuẩn cho Next.js app này".

## ⚠️ Danger zone

3 việc **KHÔNG BAO GIỜ** để Claude tự làm khi liên quan security:

1. **Tạo / xoá user trong DB production** mà bạn chưa review.
2. **Sửa file `.env`** — chỉ bạn được sửa.
3. **Disable auth middleware** "để test" — luôn dùng env riêng để test, đừng disable production.

## Tip thực chiến

Khi giao Claude build app có user:
1. Nói rõ phương thức auth (email + Google OAuth là phổ biến nhất).
2. Nói rõ ai là "admin" và quyền khác user thường.
3. Bắt buộc Claude dùng thư viện chuẩn (NextAuth, Clerk), không tự code crypto.
4. Yêu cầu Claude tạo file `.env.example` ngay từ đầu.

## Khi audit dự án có sẵn

Hỏi Claude:
> "Audit security của repo này: kiểm tra auth flow, validation, rate limit, secret leakage, security headers."

Claude sẽ scan code và list các gap.

## Tiếp theo

Đọc [`deployment.md`](deployment.md) — đưa code lên Internet.
