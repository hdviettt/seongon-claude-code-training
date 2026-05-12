# Lesson Notes — Note giảng viên

File này được **giảng viên Việt** update mỗi buổi học. Học viên `git pull` về để Claude Code có context buổi hôm nay.

---

## Buổi <N> — <ngày YYYY-MM-DD>

### Bối cảnh

<1-3 đoạn ngắn về tình hình thực tế buổi học:
- Học viên đã nộp BTVN gì?
- Quan sát chung — pattern lặp lại?
- Buổi hôm nay focus gì?>

### Tiêu chí "đạt yêu cầu" cho buổi này

Đây là source of truth khi Claude Code audit. Học viên dùng SKILL `/audit-webapp`, Claude sẽ đối chiếu với checklist này.

- [ ] <Tiêu chí 1 — cụ thể, đo được>
- [ ] <Tiêu chí 2>
- [ ] <Tiêu chí 3>
- [ ] ...

### Pattern lỗi thường gặp + Cách fix

Khi học viên có dấu hiệu này → Claude nên đề xuất action này.

| Pattern lỗi | Cách phát hiện | Đọc |
|---|---|---|
| Web tĩnh, hardcode data | `package.json` có `next` nhưng không có `pg`/`drizzle`/`prisma` + có array data trong `.tsx` | [`knowledge/02-tech-stack-web-app/recipes/static-to-fullstack.md`](knowledge/02-tech-stack-web-app/recipes/static-to-fullstack.md) |
| Thiếu admin auth | Có `/admin` route nhưng không có `middleware.ts` hoặc `auth.ts` | [`knowledge/02-tech-stack-web-app/security/auth.md`](knowledge/02-tech-stack-web-app/security/auth.md) |
| Deploy nhưng API 404 | URL live OK nhưng F12 → Network gọi `/api/*` ra 404 | DB chưa setup hoặc env chưa set — đọc [`add-database.md`](knowledge/02-tech-stack-web-app/database/hosted-providers.md) |

### Note cá nhân (optional)

Nếu giảng viên có note riêng cho 1 vài học viên cụ thể, ghi ở đây. Claude sẽ đọc và áp dụng khi audit repo của họ.

- **<tên/email học viên>**: <note cụ thể, vd: "stack hiện đại nhưng UI chưa responsive, focus UX trước">.
- ...

---

## Buổi 3 — Follow-up BTVN buổi 2 (Web app fullstack)

### Bối cảnh

Sau BTVN buổi 2, nhiều học viên đã build website nhưng:
- Có người làm **web tĩnh** (hardcode data, không có backend).
- Có người **fullstack hòm hòm** nhưng thiếu auth, deploy lỗi, hoặc DB chưa thật.
- Có người làm tốt, cần polish thêm.

Buổi hôm nay: hướng dẫn từng người nâng cấp về đúng tiêu chí "fullstack thật sự".

### Tiêu chí "đạt yêu cầu" cho buổi này

Web app phải tick **TẤT CẢ** tiêu chí Critical:

#### Critical (phải đủ — không phải thì chưa đạt)

- [ ] **Frontend hiển thị được**, UI có nội dung (không chỉ "Hello World").
- [ ] **Backend thực**: có folder `app/api/` (Next.js) hoặc service riêng (Node/Python). KHÔNG chỉ hardcode JSON trong component.
- [ ] **Database thật**: Postgres / SQLite / Mongo. Có file schema/migration. KHÔNG chỉ file `.json` static.
- [ ] **Có ít nhất 1 endpoint write** (POST/PUT/DELETE), không chỉ GET.
- [ ] **Form trên UI submit thật** → API → DB. Refresh trang thấy data persist.
- [ ] **Deploy live**, URL public ai cũng truy cập được (Vercel / Railway / Cloudflare).
- [ ] **Mở từ 2 trình duyệt khác nhau** cùng thấy data như nhau.

#### High (nên có)

- [ ] `.env.example` đầy đủ, không leak secret.
- [ ] `README.md` mô tả: project gì, cách chạy local, cách deploy.
- [ ] Form input có validation cơ bản (required, type check).
- [ ] Nếu có admin area → có auth bảo vệ.

#### Medium (polish)

- [ ] Mobile responsive.
- [ ] Loading + empty states.
- [ ] Error handling (không show stack trace).

### Pattern lỗi thường gặp + Cách fix

| Pattern lỗi | Cách phát hiện | Action |
|---|---|---|
| **Hardcode data trong component** | Array `const posts = [...]` ở `.tsx`, không có `db/`, không có `fetch('/api/...')` | Đọc [`static-to-fullstack.md`](knowledge/02-tech-stack-web-app/recipes/static-to-fullstack.md). Setup DB + API routes. |
| **Form submit chỉ `console.log`** | Form `onSubmit` không có `fetch` với POST | Tạo API route POST, refactor form gọi API. Sau đó verify: refresh thấy data. |
| **DB chỉ là file JSON** | `data/posts.json` được import vào component | Setup DB thật: Postgres + Neon nếu Vercel, Postgres Railway nếu Railway. |
| **Deploy nhưng API 404** | Production URL load OK, nhưng action lỗi | Check env vars trên dashboard hosting (`DATABASE_URL`, `AUTH_SECRET`). |
| **Admin area không có auth** | Có `/admin` page, ai cũng vào được | Đọc [`add-auth.md`](knowledge/02-tech-stack-web-app/security/auth.md). Setup NextAuth + check email admin. |
| **Push secret lên Git** | File `.env` có trong commit history | **KHẨN**: rotate tất cả secret. Add `.env` vào `.gitignore`. Force-push xoá history nếu repo còn private. |

### Recipe khuyến nghị mặc định

Cho học viên chưa biết chọn stack gì, recommend:

**Stack default cho buổi này:**
- Frontend: Next.js 14 (App Router) + Tailwind + shadcn/ui
- Backend: Next.js API routes (cùng repo)
- DB: Postgres
  - Nếu deploy Vercel → DB trên **Neon**
  - Nếu deploy Railway → **Postgres built-in Railway**
- ORM: Drizzle
- Auth (nếu cần): NextAuth v5 + Google OAuth
- Deploy: Vercel hoặc Railway

### Quy trình audit cho học viên

1. Học viên clone repo training về máy.
2. `cd` vào repo training, hoặc mở Claude Code song song.
3. Trong Claude Code, gõ:
   ```
   /audit-webapp
   ```
   Hoặc nói tự nhiên:
   ```
   Đọc LESSON_NOTES.md của khoá. Audit repo web app tôi đang có 
   ở folder ../my-webapp. Đưa ra action plan nâng cấp.
   ```
4. Claude đọc:
   - `LESSON_NOTES.md` (file này).
   - Repo học viên.
   - Knowledge base.
5. Claude ra report theo `report-template.md`.
6. Học viên chọn action → Claude làm từng bước.

### Deadline buổi này

Cuối buổi, học viên phải có repo đạt **tất cả tiêu chí Critical**. High và Medium làm sau cũng được.

### Form nộp

[Link form SEONGON]
