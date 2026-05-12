# 03 — Mở rộng năng lực Claude Code

## Khi nào học viên cần folder này

- Dùng Claude Code 1 thời gian, muốn nó làm việc **nhanh hơn**, **lặp lại được**.
- Có 1 quy trình thường xuyên (research, viết content, phân tích từ khoá) muốn đóng gói thành lệnh dùng nhanh.
- Cần Claude truy cập dữ liệu ngoài: Google Search Console, SerpAPI, WordPress, Figma, Google Ads...
- Đã nghe đến "SKILLs", "MCP", "CLI" mà chưa rõ.

## Tóm tắt

Có 4 cách mở rộng Claude Code:

1. **Commands** — lệnh hệ thống có sẵn (`/compact`, `/init`, `/model`...).
2. **SKILLs** — kỹ năng bạn tự xây cho Claude Code, gọi bằng `/`.
3. **MCP / API / CLI** — kết nối Claude với thế giới ngoài.
4. **Sub-agents** — đồng nghiệp ảo có context riêng (xem folder `04-`).

Folder này focus 3 cái đầu.

## Sub-folders

| Folder | Nội dung |
|---|---|
| [`commands/`](commands/) | Các lệnh `/` hệ thống có sẵn: `/compact`, `/init`, `/model`, `/effort`, `/powerup` |
| [`skills/`](skills/) | SKILLs cơ bản + cấu trúc + ví dụ research-skill |
| [`ket-noi-ngoai/`](ket-noi-ngoai/) | API vs MCP vs CLI: khác nhau ở đâu, dùng cái nào khi nào |

## Files trong skills/

- `skills/README.md` — SKILLs là gì, khi nào nên build.
- `skills/cau-truc.md` — Cấu trúc 1 SKILL: `SKILL.md` + file đi kèm.
- `skills/examples/research-skill/` — Ví dụ SKILL hoàn chỉnh có script Python.

## Prerequisites

- Đã setup Claude Code (`knowledge/01-setup-claude-code/`).
- Đã hiểu cơ bản về tech stack (`knowledge/02-tech-stack-web-app/`).

## Khoá học liên quan

Buổi 3: [`sessions/buoi-3-mo-rong.md`](../../sessions/buoi-3-mo-rong.md)
