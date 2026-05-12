# INDEX — Bản đồ kiến thức

Tra cứu nhanh: chủ đề nào ở đâu.

## Theo topic

### Setup & giao diện
- [Cài Claude Code trên Windows](knowledge/01-setup-claude-code/cai-dat/windows.md)
- [Cài Claude Code trên Mac](knowledge/01-setup-claude-code/cai-dat/mac.md)
- [Giao diện cơ bản: commands, @, plan mode, approval](knowledge/01-setup-claude-code/giao-dien/)
- [Troubleshooting khi setup](knowledge/01-setup-claude-code/cai-dat/troubleshooting.md)

### Lập trình & web app
- [Tech stack tổng quan](knowledge/02-tech-stack-web-app/README.md)
- [Lập trình cơ bản: biến, hàm, dữ liệu](knowledge/02-tech-stack-web-app/lap-trinh-co-ban/)
- [Frontend](knowledge/02-tech-stack-web-app/frontend/)
- [Backend](knowledge/02-tech-stack-web-app/backend/)
- [Database](knowledge/02-tech-stack-web-app/database/)
  - [Hosted providers (Neon, Supabase, Railway)](knowledge/02-tech-stack-web-app/database/hosted-providers.md)
- [Security](knowledge/02-tech-stack-web-app/security/)
  - [Authentication chi tiết](knowledge/02-tech-stack-web-app/security/auth.md)
- [Deployment](knowledge/02-tech-stack-web-app/deployment/)
  - [Platforms chi tiết (Vercel/Railway/CF)](knowledge/02-tech-stack-web-app/deployment/platforms.md)
- [Source control (Git/Github)](knowledge/02-tech-stack-web-app/source-control/)
- **Recipes thực chiến:**
  - [Tổng quan recipes](knowledge/02-tech-stack-web-app/recipes/)
  - [Web tĩnh → fullstack](knowledge/02-tech-stack-web-app/recipes/static-to-fullstack.md)
  - [Blog admin CMS (auth + CRUD)](knowledge/02-tech-stack-web-app/recipes/blog-admin-cms.md)

### Mở rộng Claude Code
- [Commands hệ thống](knowledge/03-mo-rong-claude-code/commands/)
- [SKILLs là gì, khi nào dùng](knowledge/03-mo-rong-claude-code/skills/)
- [Cấu trúc 1 SKILL](knowledge/03-mo-rong-claude-code/skills/cau-truc.md)
- [Kết nối Claude với thế giới ngoài: API, MCP, CLI](knowledge/03-mo-rong-claude-code/ket-noi-ngoai/)
- [Ví dụ SKILL: research](knowledge/03-mo-rong-claude-code/skills/examples/research-skill/)

### Agents, Memory, Hooks
- [Sub-agents](knowledge/04-agents-memory-hooks/sub-agents/)
- [Memory: CLAUDE.md và MEMORY.md](knowledge/04-agents-memory-hooks/memory/)
- [Hooks](knowledge/04-agents-memory-hooks/hooks/)

### Tự động hoá & alternatives
- [Remote control: dùng CC trên điện thoại](knowledge/05-tu-dong-hoa/remote-control.md)
- [Best practice: mindset dùng Claude Code](knowledge/05-tu-dong-hoa/best-practice.md)
- [Khi Claude Code đắt: alternatives](knowledge/05-tu-dong-hoa/alternatives.md)

### Agents có sẵn trong repo
- [`giang-vien`](.claude/agents/giang-vien.md) — Giảng viên ảo. Giải đáp khái niệm, giải thích dễ hiểu.
- [`tro-ly`](.claude/agents/tro-ly.md) — Trợ lý ảo. Hỗ trợ build sản phẩm, plan + execute từng bước.

### SKILLs có sẵn trong repo
- [`/audit-webapp`](.claude/skills/audit-webapp/SKILL.md) — Audit web app học viên dựa trên LESSON_NOTES.md

### File giảng viên update
- [`LESSON_NOTES.md`](LESSON_NOTES.md) — Note cho buổi học hiện tại + tiêu chí audit

## Theo buổi học

| Buổi | Topic chính | Outline |
|---|---|---|
| 1 | Setup Claude Code | [sessions/buoi-1-setup.md](sessions/buoi-1-setup.md) |
| 2 | Tech stack web app | [sessions/buoi-2-tech-stack.md](sessions/buoi-2-tech-stack.md) |
| 3 | Commands, SKILLs, kết nối ngoài | [sessions/buoi-3-mo-rong.md](sessions/buoi-3-mo-rong.md) |
| 4 | Sub-agents, memory, hooks | [sessions/buoi-4-agents-memory-hooks.md](sessions/buoi-4-agents-memory-hooks.md) |
| 5 | Remote control, alternatives | [sessions/buoi-5-tu-dong-hoa.md](sessions/buoi-5-tu-dong-hoa.md) |

## Bài tập về nhà

| Sau buổi | BTVN | File |
|---|---|---|
| 1 | Bài học lập trình cho non-tech | [exercises/btvn-1-lap-trinh-cho-non-tech.md](exercises/btvn-1-lap-trinh-cho-non-tech.md) |
| 2 | Web app full-stack | [exercises/btvn-2-web-app-fullstack.md](exercises/btvn-2-web-app-fullstack.md) |
| 3 | Workspace với SKILLs | [exercises/btvn-3-workspace-skills.md](exercises/btvn-3-workspace-skills.md) |
| 4 | Team sub-agents | [exercises/btvn-4-team-agents.md](exercises/btvn-4-team-agents.md) |
