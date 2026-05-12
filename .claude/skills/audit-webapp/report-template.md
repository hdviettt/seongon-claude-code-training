# Report Template — Audit Web App

Format bắt buộc cho output của SKILL `/audit-webapp`.

---

## 🔍 Audit Report — <tên app từ package.json hoặc folder>

**Buổi**: <buổi mấy nếu LESSON_NOTES.md có ghi>
**Ngày audit**: <YYYY-MM-DD>

---

## Stack hiện tại

| Tầng | Có gì | Status |
|---|---|---|
| **Frontend** | <framework + version + thư viện UI> | ✅ |
| **Backend** | <Next API routes / Express / không có> | ✅/❌ |
| **Database** | <Postgres + Neon / SQLite / không có> | ✅/❌ |
| **Auth** | <NextAuth + Google / không có> | ✅/❌ |
| **Deployment** | <Vercel / Railway / local-only> | ✅/❌ |

---

## Đối chiếu với tiêu chí giảng viên

(Đọc từ `LESSON_NOTES.md`)

| Tiêu chí | Trạng thái | Ghi chú |
|---|---|---|
| <tiêu chí 1> | ✅ | <ghi chú> |
| <tiêu chí 2> | ❌ | <lý do thiếu> |
| <tiêu chí 3> | ⚠️ | <có một phần> |
| ... | | |

---

## Gaps + Action Plan

### 🔴 Critical (làm trước)

#### Gap 1: <tiêu đề>

**Vấn đề:** <1-2 câu mô tả>
**Tác động:** <vì sao quan trọng>
**Đọc trước:** [`<path>`](<path>)
**Prompt copy-paste cho Claude:**
```
<prompt cụ thể, học viên copy vào Claude và Enter>
```

#### Gap 2: ...

### 🟡 High (nên làm sau Critical)

#### Gap N: ...
(format tương tự)

### 🟢 Medium (polish, có thời gian thì làm)

#### Gap M: ...
(format tương tự)

---

## Thứ tự khuyến nghị

1. <action 1 — Critical đầu tiên>
2. <action 2>
3. <action 3>
...

Sau mỗi action, **commit Git** rồi mới làm action tiếp theo.

---

## Sẵn sàng làm action nào?

Trả lời "1" / "2" / ... để tôi bắt đầu giúp bạn từng bước.

---

## Ví dụ filled-in report

(Cho học viên tham khảo)

### 🔍 Audit Report — chipchip-travel-tracker

**Buổi**: 3 (BTVN buổi 2 follow-up)
**Ngày audit**: 2026-05-12

### Stack hiện tại

| Tầng | Có gì | Status |
|---|---|---|
| **Frontend** | Next.js 14 + Tailwind + shadcn/ui | ✅ |
| **Backend** | Không có — data hardcode trong `app/page.tsx` | ❌ |
| **Database** | Không có | ❌ |
| **Auth** | Không có | ❌ |
| **Deployment** | Vercel — URL: chipchip.vercel.app | ✅ |

### Đối chiếu với tiêu chí giảng viên

| Tiêu chí | Trạng thái | Ghi chú |
|---|---|---|
| Có frontend | ✅ | UI đẹp, responsive OK |
| Backend thực | ❌ | Hardcode `expenses = [...]` ở `app/page.tsx:24` |
| Database thật | ❌ | Không có file DB config |
| Endpoint POST | ❌ | Form submit chỉ `console.log` |
| Deploy live | ✅ | chipchip.vercel.app |
| Form → DB → reload thấy | ❌ | Refresh là mất data |

### Gaps + Action Plan

#### 🔴 Critical

##### Gap 1: Không có backend + database

**Vấn đề:** Mọi data đang hardcode trong component. Form submit không lưu đi đâu.
**Tác động:** Đây không phải fullstack thật sự. Refresh là mất data.
**Đọc trước:** [`recipes/static-to-fullstack.md`](../../knowledge/02-tech-stack-web-app/recipes/static-to-fullstack.md) + [`database/hosted-providers.md`](../../knowledge/02-tech-stack-web-app/database/hosted-providers.md)
**Prompt copy-paste cho Claude:**
```
Tôi đang có Next.js 14 app track chi phí du lịch, deploy Vercel. 
Hiện hardcode data trong app/page.tsx.

Hãy thêm:
1. Postgres database trên Neon (vì tôi dùng Vercel).
2. Drizzle ORM với schema: trips (id, name, budget, currency, startDate, endDate), 
   expenses (id, tripId FK, category, amount, paidBy, paidAt, note).
3. API routes:
   - /api/trips (GET, POST), /api/trips/:id (GET, PUT, DELETE)
   - /api/trips/:id/expenses (GET, POST), /api/expenses/:id (PUT, DELETE)
4. Refactor app/page.tsx fetch từ /api/trips thay vì hardcode.
5. Form thêm expense submit thật → DB.
6. Tạo .env.example.
7. Hướng dẫn tôi tạo Neon project, copy DATABASE_URL, set env trên Vercel.

Bắt đầu bằng lên PLAN.md trước.
```

#### 🟡 High

##### Gap 2: Không có auth cho admin (chia tiền)

**Vấn đề:** Ai cũng vào URL được, sửa expense của người khác.
**Tác động:** Trip có nhiều người → cần phân quyền owner vs viewer.
**Đọc trước:** [`security/auth.md`](../../knowledge/02-tech-stack-web-app/security/auth.md)
**Prompt copy-paste cho Claude:**
```
Thêm auth cho app: NextAuth + Google OAuth + email magic link.
Schema users (id, email, name).
Schema trip_members (trip_id, user_id, role: owner/member).
Chỉ owner mới edit/delete được expense. Member chỉ thêm expense của mình.
Update API routes check auth + permission.
```

#### 🟢 Medium

##### Gap 3: Form chưa có validation

**Vấn đề:** User gõ số âm vào amount, app crash.
**Đọc trước:** [`knowledge/02-tech-stack-web-app/security/`](../../knowledge/02-tech-stack-web-app/security/)
**Prompt:**
```
Add Zod validation cho form thêm expense. Amount > 0, currency trong [VND, USD, EUR],
category required. Validate cả client và server.
```

### Thứ tự khuyến nghị

1. Gap 1 — Thêm DB + API + refactor (~2-3 giờ).
2. Test: form submit → reload thấy data.
3. Gap 2 — Auth + permission (~1-2 giờ).
4. Gap 3 — Validation (~30 phút).

Sau mỗi gap: commit Git, deploy lại Vercel, test live.

### Sẵn sàng làm action nào?

Trả lời "1" / "2" / "3" để tôi bắt đầu hỗ trợ.
