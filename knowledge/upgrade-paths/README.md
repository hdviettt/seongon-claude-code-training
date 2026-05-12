# Upgrade Paths — Đường nâng cấp web app

## Khi nào học viên cần folder này

- Đã build 1 web app (theo BTVN buổi 2) nhưng **chưa thực sự fullstack**.
- Có note từ giảng viên về tính năng cần thêm, không biết bắt đầu từ đâu.
- Muốn upgrade từ trạng thái A → B nhưng cần decision tree cụ thể.

## Khác `02-tech-stack-web-app/` thế nào?

| `02-tech-stack/` | `upgrade-paths/` |
|---|---|
| Kiến thức tổng quát | Recipe cụ thể |
| "Frontend là gì" | "Bạn đang là web tĩnh, cần làm gì để có backend" |
| Đọc để hiểu | Đọc để làm |

→ Cần làm thực tế thì đọc folder này. Cần học thì đọc `02-tech-stack/`.

## Các path

| Path | Khi nào dùng |
|---|---|
| [`static-to-fullstack.md`](static-to-fullstack.md) | Bạn đang là web tĩnh (hardcode data, không có API thực) → cần thành fullstack thật |
| [`add-database.md`](add-database.md) | Cần thêm DB. Decision tree: Vercel→Neon, Railway→Postgres built-in, etc |
| [`add-auth.md`](add-auth.md) | Cần thêm authentication (login user / admin) |
| [`add-admin-panel.md`](add-admin-panel.md) | Cần CRUD admin (cho blog, e-commerce, etc) |
| [`add-deployment.md`](add-deployment.md) | App chạy local OK rồi, cần deploy public |

## Cách dùng kết hợp

1. Đọc `LESSON_NOTES.md` ở root — note giảng viên có gì.
2. Chạy SKILL `/audit-webapp` để Claude tự audit repo bạn.
3. Claude sẽ chỉ bạn đọc đường nâng cấp nào trong folder này.
4. Làm theo decision tree.
