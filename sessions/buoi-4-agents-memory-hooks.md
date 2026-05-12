# Buổi 4 — Kỹ năng sử dụng Claude Code

## Mục tiêu buổi học

- Build được team sub-agents để chia việc song song.
- Hiểu cơ chế Memory (CLAUDE.md, MEMORY.md) và setup chuẩn.
- Biết khi nào nên (và không nên) dùng Hooks.

## Thời lượng

3 giờ.

## Outline

### Phần 1 — Chữa BTVN buổi 3 (20 phút)

Review workspace với SKILLs học viên đã build:
- Case study tốt: GSC Performance skill kết nối Google Search Console MCP, SEO workspace 11 skills + SerpAPI integration.
- Lỗi phổ biến nhất: tạo skill nhưng đặt SAI folder (không nằm trong `.claude/skills/<ten>/`). Skill phải nằm đúng folder để được nhận.

### Phần 2 — Sub-agents (50 phút)

**Mục tiêu:** Học viên hiểu sub-agents và build được 2-3 agents.

Tham chiếu:
- [`knowledge/04-agents-memory-hooks/sub-agents/`](../knowledge/04-agents-memory-hooks/sub-agents/)

Cover:
- Định nghĩa: sub-agent = đồng nghiệp ảo có context riêng.
- 3 hệ quả của dùng sub-agent: song song + giảm token + tăng chất lượng.
- Cấu trúc 1 sub-agent: file `.md` trong `.claude/agents/` + frontmatter.
- Diagram: agent chính dispatch task sang 3 sub-agents (SEO research / Ads research / Web builder).

Hands-on:
- Build 1 sub-agent đại diện vai trò công việc của học viên (ví dụ: SEO-specialist, content-writer).
- Tạo SKILL gọi sub-agent đó.

### Phần 3 — Memory (40 phút)

**Mục tiêu:** Học viên setup được CLAUDE.md cho project + biết tắt auto-memory.

Tham chiếu:
- [`knowledge/04-agents-memory-hooks/memory/`](../knowledge/04-agents-memory-hooks/memory/)

Cover:
- Memory = thông tin Claude tự load mỗi session mới.
- 2 cơ chế: `CLAUDE.md` (manual) + `MEMORY.md` (auto).
- Hệ thống phân cấp: user CLAUDE.md + project CLAUDE.md + folder con CLAUDE.md.
- `/init` để Claude tự tạo CLAUDE.md.
- Khuyến nghị **tắt auto-memory** (`/memory` → off). Lý do: khó kiểm soát, dễ noise.

Hands-on:
- Mở 1 project học viên đã build → chạy `/init` → review CLAUDE.md → edit.

### Giải lao (10 phút)

### Phần 4 — Hooks (40 phút)

**Mục tiêu:** Học viên hiểu hooks là gì, khi nào dùng, khi nào KHÔNG dùng.

Tham chiếu:
- [`knowledge/04-agents-memory-hooks/hooks/`](../knowledge/04-agents-memory-hooks/hooks/)

Cover:
- Hook = script tự chạy ở 1 event.
- Như automation: trigger → action.
- 10+ event hỗ trợ: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `PreCompact`/`PostCompact`, `SubagentStart`/`SubagentStop`, `SessionEnd`, `FileChanged`.
- 4 ví dụ thực chiến:
  - Load format template trước khi tạo `.md`.
  - Refresh Google token khi hết hạn.
  - Backup chat trước compact.
  - Cắt file Excel trước khi đọc.

**Nguyên tắc nhấn mạnh:**
- Chỉ làm hook cho workflow **100% deterministic**.
- Workflow càng hẹp, càng cụ thể, càng hay gặp → càng nên có hook.
- Nếu giải được bằng SKILL hoặc CLAUDE.md → dùng cái đó, không dùng hook.

### Phần 5 — Tổng kết (20 phút)

Recap:
- **Sub-agents** giải bài toán delegation + context bloat.
- **Memory (CLAUDE.md)** giải bài toán lặp context.
- **Hooks** giải bài toán automation deterministic.
- 3 thứ này phát huy giá trị khi đã có workflow ổn — đừng làm khi mới học.

## BTVN

Xem [`exercises/btvn-4-team-agents.md`](../exercises/btvn-4-team-agents.md).

## Slide

`slides/2_Buổi 4 Claude Code cho SEO & Ads.pdf`
