# Default Checklist: Web App thực sự Fullstack

Dùng làm fallback khi `LESSON_NOTES.md` không có.

## Tiêu chí cốt lõi (Critical — phải đủ để gọi "fullstack")

- [ ] Có frontend (UI hiển thị thật, không phải file `.txt`).
- [ ] Có backend thực — API route hoặc service riêng — KHÔNG chỉ hardcode JSON trong component.
- [ ] Có database thật (Postgres, SQLite, Mongo) — KHÔNG chỉ file JSON.
- [ ] Có ít nhất 1 endpoint **write** (POST/PUT/DELETE), không chỉ GET.
- [ ] Form trên UI submit thật → API → DB → reload thấy data.
- [ ] Deploy live, có URL public ai cũng truy cập được.
- [ ] Refresh tab, data vẫn còn.
- [ ] Mở từ 2 trình duyệt khác nhau, cùng thấy data.

## Tiêu chí High (nên có để gọi "production-ready")

- [ ] Có `.env.example` đầy đủ.
- [ ] Secret KHÔNG có trong Git history (`.env` đã gitignore từ đầu).
- [ ] Có README mô tả: project là gì, cách chạy local, cách deploy.
- [ ] Có ít nhất 1 form input → validation (client + server).
- [ ] Auth có middleware/guard cho route nhạy cảm (admin, dashboard).
- [ ] Mobile responsive (hoặc note rõ "desktop only").

## Tiêu chí Medium (polish)

- [ ] Có rate limit cho endpoint nhạy cảm.
- [ ] Có error handling — không show stack trace cho user.
- [ ] Loading states cho async actions.
- [ ] Empty states ("Chưa có post nào").
- [ ] Image optimization (next/image, hoặc width/height fix).

## Đặc biệt cho từng loại app

### Blog cá nhân/doanh nghiệp
- [ ] Public xem được list bài + chi tiết bài.
- [ ] Admin login được, CRUD post.
- [ ] Bài có support markdown hoặc rich text.
- [ ] Bài có cover image (lưu storage, không hardcode URL).

### Site bán hàng
- [ ] List sản phẩm + chi tiết.
- [ ] Giỏ hàng (cart) — persist trong session/DB.
- [ ] Checkout flow (kể cả không tích hợp payment real).
- [ ] Admin: CRUD sản phẩm, xem đơn hàng.

### Mini-tool / Generator
- [ ] Form input.
- [ ] Process logic chạy được.
- [ ] Output hiển thị.
- [ ] (Optional) Lưu history vào DB cho user xem lại.

### Dashboard kéo data từ nền tảng thứ 3
- [ ] Có auth (vì có data nhạy cảm).
- [ ] Kết nối thật với platform (API/MCP/CLI).
- [ ] Cache data hợp lý (không gọi API mỗi lần load).
- [ ] Refresh button.

### Chatbot AI
- [ ] Có UI chat thật (input + message list).
- [ ] Kết nối Claude API / OpenAI API.
- [ ] Lưu history vào DB.
- [ ] Stream response (UX tốt hơn loading 5s).

## Cách check cụ thể

### Check "không hardcode data"

Tìm trong code các pattern:
- `const posts = [{...}, {...}]` ở component → ❌ hardcode.
- `posts.json` file static được import → ⚠️ static data, không phải DB.
- `fetch('/api/posts')` → ✅ gọi API.
- `await db.select().from(posts)` → ✅ query DB.

### Check "có write endpoint"

Tìm trong `app/api/` (Next.js) hoặc tương đương:
- File `route.ts` chỉ có `GET` → ❌ read-only.
- File `route.ts` có `POST` / `PUT` / `DELETE` → ✅.

### Check "có DB thật"

- `package.json` có: `pg`, `postgres`, `prisma`, `drizzle-orm`, `mongodb`, `mongoose` → ✅.
- Chỉ có: `lowdb`, hoặc đọc/ghi file JSON → ⚠️ không phải DB thật cho production.

### Check "deploy live"

- Repo có `vercel.json` / `railway.json` → có thể đã setup.
- README có "Live URL: ..." → mở thử URL đó.
- Repo không có gì → chưa deploy.

### Check "form submit thật"

Đọc form component:
- `onSubmit` chỉ `console.log` hoặc `alert` → ❌.
- `onSubmit` có `fetch('/api/...', { method: 'POST' })` → ✅.

## Khi đối chiếu, dùng format:

```markdown
| Tiêu chí | Trạng thái | Ghi chú |
|---|---|---|
| Frontend có | ✅ | Next.js 14 + Tailwind |
| Backend thực | ❌ | Hardcode posts ở `app/page.tsx:12`, không có `/api` |
| Database | ❌ | Chỉ có `data/posts.json`, chưa setup DB |
| Endpoint write | ❌ | Chỉ có GET (do chưa có backend) |
| ... |
```
