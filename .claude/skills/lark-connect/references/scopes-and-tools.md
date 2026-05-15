# Lark Scopes & Tools — Giải thích

Scope = quyền truy cập API. Token mode = bot vs user. Tools = function lark-mcp expose cho Claude.

## Contents
- [2 Token modes — chọn cái nào](#2-token-modes--chọn-cái-nào)
- [9 Scope default (skill bật sẵn)](#9-scope-default-skill-bật-sẵn)
- [Thêm scope](#thêm-scope)
- [Preset tools lark-mcp](#preset-tools-lark-mcp)
- [Custom tool selection](#custom-tool-selection)
- [Security note](#security-note)

---

## 2 Token modes — chọn cái nào

Lark có 2 loại token:

### `tenant_access_token` (Bot mode)

**Đại diện cho**: App (bot), không phải user cụ thể.
**Quyền**: Mọi resource owned bởi bot, hoặc shared explicit với bot.
**Setup**: Đơn giản — không cần OAuth flow.
**Hạn chế**: Không truy cập được data cá nhân user (vd "My Drive" của user).

**Use case**:
- Bot trong group reply automation
- Workflow không touch personal data
- Schedule task gửi message hàng ngày

### `user_access_token` (User mode) — DEFAULT của skill

**Đại diện cho**: User cụ thể (người login OAuth).
**Quyền**: Mọi resource user có access.
**Setup**: OAuth flow (Step 5 của skill).
**Lợi**: Access personal data — calendar, my drive, my tasks.

**Use case** (phần lớn audience SEONGON):
- Đọc Bitable cá nhân
- Schedule meeting calendar
- Quản lý task list cá nhân
- Send message với danh nghĩa user

**Default skill dùng `user_access_token`** vì phù hợp hầu hết use case marketing/operations.

Switch sang tenant mode: sửa `.env`:
```env
LARK_TOKEN_MODE=tenant_access_token
```

Wrapper script `lark_mcp_runner.py` đọc biến này → spawn lark-mcp với `--token-mode` tương ứng.

---

## 9 Scope default (skill bật sẵn)

### `im:message`
Gửi/đọc message Lark. Core cho automation messaging.

### `im:chat`
Quản lý chat (create group, add member, list groups).

### `docx:document`
Đọc/ghi Lark Docs. Read content, append paragraph, replace text.

### `sheets:spreadsheet`
Đọc/ghi Lark Sheets. Get cell values, batch update, create sheet.

### `bitable:app`
Đọc/ghi Bitable (Airtable-like). List records, create record, filter.

### `calendar:calendar`
Quản lý calendar — list events, create event, update, delete.

### `task:task`
Quản lý Lark Tasks — list, create, complete, assign.

### `contact:user.base:readonly`
Read basic info của user (name, email). Cần để identify "current user" trong API calls.

### `offline_access`
**BẮT BUỘC** cho `user_access_token`. Cho phép refresh token khi access token expire.

---

## Thêm scope

Nếu cần thêm scope (Mail, Drive nâng cao, custom Bitable):

### Step 1: Vào Lark Console

https://open.larksuite.com → Developer Console → app của bạn → **Permissions & Scopes**

### Step 2: Search + Add

Click **Add Permission**, search keyword (vd "mail"). Lark hiển thị scope match.

### Step 3: Save + Re-release

Sau khi add scope, click **Save Changes**. Sau đó:
1. Vào **Version Management**
2. **Create Version** new (vd v1.0.1)
3. **Submit for Release** → Self-approve

### Step 4: Re-run OAuth login

User phải re-grant với scopes mới:
```bash
npx -y @larksuiteoapi/lark-mcp login -a <id> -s <secret>
```

Browser sẽ hiện scopes mới để user approve.

---

## Preset tools lark-mcp

lark-mcp ship 50+ tools, group thành presets:

| Preset | Tools cover | Khi nào dùng |
|---|---|---|
| `preset.im.default` | Send/receive message, manage chat | Bot automation, notification |
| `preset.calendar.default` | List/create/update events | Schedule assistant |
| `preset.docx.default` | Read/write Docs content | Content automation, copy text |
| `preset.sheets.default` | Read/write Sheets cells | Data automation, batch update |
| `preset.bitable.default` | Bitable CRUD | Database-like operations |
| `preset.task.default` | Task management | Productivity automation |
| `preset.contact.default` | User info lookup | Identify users, get profile |

Default skill bật `default` (gồm tất cả 7 preset trên).

---

## Custom tool selection

Nếu muốn limit tools (vd chỉ messaging, không cần calendar), set `LARK_TOOLS` trong `.env`:

```env
LARK_TOOLS=im.v1.message.create,im.v1.chat.list,preset.calendar.default
```

Cú pháp:
- Tool đơn: `<module>.<version>.<resource>.<action>` (vd `im.v1.message.create`)
- Preset: `preset.<group>.<variant>` (vd `preset.calendar.default`)

Comma-separated, không space.

Lợi ích custom:
- Giảm số tool Claude phải scan → faster
- Bảo mật — exclude destructive tools (vd `*.delete`)

---

## Security note

- Scope càng rộng = token càng quyền lực
- KHÔNG enable `*:*` scope (wildcard) cho production
- KHÔNG share App Secret — mỗi user/team tạo app riêng
- Rotate App Secret định kỳ — Console → Credentials → "Regenerate Secret"
- Token cache tại `~/.lark-mcp/` — KHÔNG commit
- `.env` trong `.gitignore` (skill auto-handle)

---

## Common scopes ngoài 9 default

| Scope | Purpose | Khi nào cần |
|---|---|---|
| `mail:mail` | Gmail-like — đọc/gửi mail trong Lark Mail | Workflow mail automation |
| `drive:drive` | My Drive — list/upload/download file | File management |
| `vc:meeting` | Video Conference — schedule/join meeting | Meeting bot |
| `wiki:wiki` | Lark Wiki — read/write wiki pages | Knowledge base |
| `okr:objective` | OKR — list/update OKR | Performance tracking |
| `attendance:attendance` | Attendance — punch in/out | HR automation |

Full list: https://open.larksuite.com/document/scope-list
