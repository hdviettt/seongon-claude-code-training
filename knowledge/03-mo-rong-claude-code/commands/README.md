# Commands — Lệnh hệ thống có sẵn

**Commands** = các lệnh được xây sẵn bởi Claude Code. Gọi bằng `/`.

Khác với **SKILLs** (cũng dùng `/`) — Commands là của Claude Code, SKILLs là do bạn tự build.

## Các command thường dùng

### `/clear` — Bắt đầu mới

Xoá cuộc trò chuyện hiện tại, bắt đầu session mới với context trống.

Khi nào dùng: chuyển sang task khác hoàn toàn, muốn Claude quên context cũ.

### `/compact` — Nén context

Khi cuộc trò chuyện quá dài (>50 tin nhắn), context nặng → Claude trả lời chậm và kém chất lượng. `/compact` tóm tắt cuộc trò chuyện trước, giữ thông tin quan trọng, giải phóng context.

**Khi nào dùng:**
- Sau 1 task dài, muốn tiếp tục task tiếp theo.
- Khi Claude bắt đầu chậm.
- Trước khi rời máy lâu — quay lại đỡ tốn token.

**Khi nào KHÔNG dùng:**
- Đang trong giữa 1 task quan trọng cần đủ context.

### `/init` — Tạo CLAUDE.md tự động

Claude đọc cấu trúc folder hiện tại, tự tạo file `CLAUDE.md` tóm tắt project: stack, structure, conventions.

File này sẽ được load mỗi lần bạn mở Claude Code trong folder → không phải lặp lại thông tin.

**Khi nào dùng:** mỗi khi bắt đầu làm việc với 1 project mới.

### `/model` — Đổi model

Claude Code có 3 model:
- **Opus 4.7** — mạnh nhất, đắt nhất. Dùng cho task khó: planning, debug phức tạp, research sâu.
- **Sonnet 4.6** — cân bằng, mặc định. Dùng cho task hàng ngày.
- **Haiku 4.5** — nhanh và rẻ. Dùng cho task lặp lại, simple.

**Tips:**
- Bắt đầu task lớn → đổi sang Opus.
- Thực thi từng bước → Sonnet đủ.
- Lặp đi lặp lại 1 thao tác đơn giản → Haiku.

### `/effort` — Điều chỉnh nỗ lực suy luận

Thang: `low → medium → high → xhigh → max`.

Effort càng cao = Claude suy nghĩ kỹ hơn = chậm hơn, tốn token hơn, kết quả tốt hơn.

**Tips:**
- Plan mode + Opus + xhigh → cho task chiến lược, kế hoạch lớn.
- Sonnet + high → mặc định khi thực thi.

### `/config` → ngôn ngữ

Đổi ngôn ngữ ưu tiên của Claude Code (giao tiếp với bạn).

Khi bạn muốn Claude luôn trả lời tiếng Việt:
1. Gõ `/config`.
2. Tìm "Output language" hoặc tương đương.
3. Đổi sang Vietnamese.

### `/login` — Đăng nhập lại

Khi session hết hạn hoặc bạn muốn đổi account.

### `/resume` — Quay lại cuộc trò chuyện trước

Nếu lỡ đóng terminal, mở lại Claude Code, gõ `/resume` để tiếp tục cuộc cũ.

### `/agents` — Quản lý sub-agents

Xem, tạo, sửa sub-agents (xem `knowledge/04-agents-memory-hooks/sub-agents/`).

### `/plan` — Bật Plan Mode

Yêu cầu Claude lên kế hoạch chi tiết trước khi thực thi. Xem `knowledge/01-setup-claude-code/giao-dien/` mục "Plan Mode".

Variant: `/ultraplan` — plan kỹ hơn nữa, dùng cho task siêu lớn.

### `/usage` — Xem usage hiện tại

Hiện số token đã dùng, chi phí ước tính, quota còn lại của plan.

### `/memory` — Quản lý memory

Xem các file memory mà Claude đang auto-load. Tắt auto-memory nếu cần (khuyến nghị tắt — xem `knowledge/04-agents-memory-hooks/memory/`).

### `/powerup` — Hướng dẫn các tính năng

Claude hướng dẫn từng tính năng chính của Claude Code: `@`, plan mode, undo, tasks, MCP, skills, hooks, agents, remote-control, model.

Tips: gõ "Hướng dẫn tôi về /powerup bằng tiếng Việt" → Claude giải thích từng cái.

## Tips chung

- **Học commands theo nhu cầu**, không học tất cả 1 lúc.
- Bắt đầu chỉ với: `/clear`, `/compact`, `/model`, `/plan`, `/init`. Đủ 90% công việc hàng ngày.
- Khi không nhớ commands gì, gõ `/` → Claude list ra cho chọn.

## Tiếp theo

- Để tự xây lệnh riêng (SKILLs), đọc [`skills-co-ban.md`](skills-co-ban.md).
- Để kết nối Claude với hệ thống ngoài, đọc [`ket-noi-ben-ngoai.md`](ket-noi-ben-ngoai.md).
