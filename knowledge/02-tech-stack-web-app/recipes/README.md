# Recipes — Pattern thực chiến

## Khác kiến thức tổng quát thế nào

| Knowledge tổng quát (các folder khác) | Recipes (folder này) |
|---|---|
| Học để hiểu | Đọc để làm |
| "Frontend là gì" | "Web tĩnh → fullstack: làm thế nào, prompt copy-paste sẵn" |
| Đọc theo flow logic | Đọc theo task |

## Recipes có sẵn

| Recipe | Khi nào đọc |
|---|---|
| [`static-to-fullstack.md`](static-to-fullstack.md) | App đang là web tĩnh (hardcode data, không có API thực) → cần thành fullstack |
| [`blog-admin-cms.md`](blog-admin-cms.md) | Cần thêm admin panel CRUD cho blog (auth + DB + UI admin) |

## Mỗi recipe có gì

- **Khi nào dùng** — trigger cụ thể.
- **Prerequisites** — kiến thức cần biết trước (link tới knowledge folder).
- **Decision tree** — quyết theo stack.
- **Code mẫu** — copy được, không phải pseudocode.
- **Prompt copy-paste** — đưa cho Claude làm hộ.
- **⚠️ Cấm** — pattern không nên làm.

## Cách dùng kết hợp với SKILL `/audit-webapp`

1. Học viên chạy `/audit-webapp`.
2. SKILL phát hiện gaps trong app.
3. Mỗi gap → link tới recipe phù hợp trong folder này.
4. Học viên đọc recipe → copy prompt → Claude làm.

## Khi nào nên thêm recipe mới?

Khi cùng 1 pattern xuất hiện ở > 3 học viên / dự án — đáng đóng gói thành recipe.

Ví dụ recipe có thể thêm trong tương lai:
- `add-payment-stripe.md` — Tích hợp Stripe.
- `add-image-upload.md` — Upload ảnh lên R2/S3/Vercel Blob.
- `add-email-sending.md` — Gửi email qua Resend / SendGrid.
- `add-search.md` — Search functionality (Algolia / Postgres full-text).
- `add-realtime.md` — Realtime với WebSocket / Liveblocks.
