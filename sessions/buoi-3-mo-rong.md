# Buổi 3 — Mở rộng năng lực Claude Code

## Mục tiêu buổi học

- Biết các commands hệ thống thường dùng.
- Build được SKILL cơ bản.
- Hiểu API / MCP / CLI: khác nhau ở đâu, khi nào dùng.

## Thời lượng

3 giờ.

## Outline

### Phần 1 — Commands (30 phút)

**Mục tiêu:** Học viên dùng được 5-7 command hệ thống chính.

Tham chiếu:
- [`knowledge/03-mo-rong-claude-code/commands/`](../knowledge/03-mo-rong-claude-code/commands/)

Demo:
- `/compact` — giảm context khi cuộc trò chuyện dài.
- `/init` — tạo CLAUDE.md tự động.
- `/model` & `/effort` — đổi model và effort.
- `/config language` — đổi ngôn ngữ ưu tiên.
- `/powerup` — hướng dẫn tất cả tính năng chính.

### Phần 2 — SKILLs (45 phút)

**Mục tiêu:** Học viên build được 1 SKILL đơn giản.

Tham chiếu:
- [`knowledge/03-mo-rong-claude-code/skills/`](../knowledge/03-mo-rong-claude-code/skills/)
- [`knowledge/03-mo-rong-claude-code/skills/cau-truc.md`](../knowledge/03-mo-rong-claude-code/skills/cau-truc.md)

Cover:
- SKILL khác Commands: tự xây vs xây sẵn.
- Bản chất SKILL = chỉ dẫn đóng gói để dùng lại.
- Cấu trúc: folder `.claude/skills/<ten>/SKILL.md` + file đi kèm.
- 2 cấp: project vs user.
- Cách đánh giá SKILL tốt: chỉ dẫn cụ thể + tiêu chí chất lượng.

Hands-on bài tập:
- Tự thiết kế 1 SKILL `/research` với:
  - Bước nghiên cứu của riêng học viên.
  - Nguồn ưu tiên.
  - Giới hạn số nguồn.
  - Format output.
- Lưu ở cấp project.

### Giải lao (10 phút)

### Phần 3 — Cài SKILL người khác đã build (15 phút)

Tham khảo 4 repo SKILLs công khai:
- `ui-ux-pro-max` — design UI.
- `claude-ads` — chạy Ads.
- `claude-seo` — SEO workflows.
- `marketing-skills` — marketing chung.

Cách cài: gửi URL Github cho Claude, bảo nó setup vào `.claude/skills/`.

### Phần 4 — Kết nối Claude với thế giới ngoài (40 phút)

Tham chiếu:
- [`knowledge/03-mo-rong-claude-code/ket-noi-ngoai/`](../knowledge/03-mo-rong-claude-code/ket-noi-ngoai/)

#### API (10 phút)
- Định nghĩa.
- Ví dụ: SerpAPI, DataForSEO, Google Ads API.
- Setup API thành SKILL — xem ví dụ `examples/research-skill/`.

#### MCP (15 phút)
- Định nghĩa: API = 1 tác vụ, MCP = bộ tác vụ.
- MCP servers phổ biến: WordPress, Playwright, Netlify, Figma, Google Ads.

#### CLI (10 phút)
- Định nghĩa: lệnh terminal của 1 platform.
- Ví dụ: gh, railway, vercel, netlify.

#### So sánh API vs MCP vs CLI (5 phút)
Bảng so sánh trong knowledge file.

### Phần 5 — Tổng kết (10 phút)

Recap. Nhấn mạnh: SKILLs + API/MCP/CLI = mở rộng đáng kể năng lực Claude Code.

## BTVN

Xem [`exercises/btvn-3-workspace-skills.md`](../exercises/btvn-3-workspace-skills.md).
