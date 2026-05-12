# 04 — Agents, Memory, Hooks

## Khi nào học viên cần folder này

- Đã quen SKILLs, muốn nâng cấp workflow lên cấp tự động hoá cao hơn.
- Cần Claude làm nhiều task song song.
- Muốn Claude "nhớ" thông tin giữa các session (project context, voice, conventions).
- Muốn Claude tự động chạy script ở các thời điểm nhất định (trước commit, sau khi tạo file, etc).

## Tóm tắt

3 tính năng advanced của Claude Code:

### Sub-agents
Đồng nghiệp ảo của Claude Code, có **context riêng** (không chia sẻ với agent chính). Dùng để chia việc song song và tiết kiệm token.

### Memory
Cơ chế Claude tự load thông tin khi bắt đầu session mới. 2 cơ chế chính: `CLAUDE.md` (manual) và `MEMORY.md` (auto).

### Hooks
Script tự chạy ở 1 event nhất định (trước/sau khi gọi tool, khi compact, khi end session). Như automation cho chính Claude Code.

## Sub-folders

| Folder | Nội dung |
|---|---|
| [`sub-agents/`](sub-agents/) | Tạo và dùng sub-agents (đồng nghiệp ảo có context riêng) |
| [`memory/`](memory/) | CLAUDE.md, MEMORY.md, hệ thống phân cấp memory |
| [`hooks/`](hooks/) | Hooks: trigger + action, các event hỗ trợ, nguyên tắc dùng |

## Prerequisites

- Đã hiểu SKILLs (`knowledge/03-mo-rong-claude-code/skills/`).
- Đã dùng Claude Code ít nhất 1-2 tuần (3 tính năng này phát huy hiệu quả với workflow đã có).

## Khoá học liên quan

Buổi 4: [`sessions/buoi-4-agents-memory-hooks.md`](../../sessions/buoi-4-agents-memory-hooks.md)
