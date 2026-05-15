# Lark Scopes & Tools — Tenant Mode

Scope = quyền truy cập API. Skill `lark-connect` chỉ support **tenant_access_token (bot mode)**. Đọc khi muốn hiểu mỗi scope cho phép gì hoặc thêm scope mới.

## Contents
- [8 Scope default (skill bật sẵn)](#8-scope-default-skill-bật-sẵn)
- [Thêm scope](#thêm-scope)
- [Preset tools lark-mcp](#preset-tools-lark-mcp)
- [Custom tool selection](#custom-tool-selection)
- [Tenant mode limitations](#tenant-mode-limitations)
- [Security note](#security-note)

---

## 8 Scope default (skill bật sẵn)

### `im:message`
Gửi/đọc message Lark. Core cho automation messaging.

### `im:chat`
Quản lý chat (create group, add member, list groups bot là member).

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
Read basic info của user (name, email). Cần để identify users trong API responses.

**KHÔNG cần `offline_access`** (chỉ áp dụng cho OAuth user mode, skill không dùng).

---

## Thêm scope

### Step 1: Lark Console

https://open.larksuite.com → Developer Console → app → **Permissions & Scopes**

### Step 2: Add Permission

Click **Add Permission**, search keyword (vd "mail"). Lark hiển thị scope match.

### Step 3: Save + Re-release

Sau khi add:
1. Click **Save Changes**
2. Vào **Version Management**
3. **Create Version** (vd v1.0.1)
4. **Submit for Release** → Self-approve

### Step 4: Restart Claude Code

MCP server cache tools metadata. Quit CC hoàn toàn → mở lại → tool mới available.

---

## Preset tools lark-mcp

Default skill bật `default` preset (17 tools):

| Module | Tools cover |
|---|---|
| **im (messaging)** | im_v1_chat_create, im_v1_chat_list, im_v1_chatMembers_get, im_v1_message_create, im_v1_message_list |
| **bitable** | bitable_v1_app_create, bitable_v1_appTable_create, bitable_v1_appTableField_list, bitable_v1_appTable_list, bitable_v1_appTableRecord_create, bitable_v1_appTableRecord_search, bitable_v1_appTableRecord_update |
| **docx** | docx_v1_document_rawContent, docx_builtin_import |
| **drive** | drive_v1_permissionMember_create |
| **wiki** | wiki_v2_space_getNode |
| **contact** | contact_v3_user_batchGetId |

lark-mcp có 200+ tool nhưng default preset = 17 phổ biến nhất. Custom select để thêm tool khác.

---

## Custom tool selection

Set `LARK_TOOLS` trong `.env`:

```env
LARK_TOOLS=im.v1.message.create,preset.calendar.default,preset.docx.default
```

Cú pháp:
- Tool đơn: `<module>.<version>.<resource>.<action>` (vd `im.v1.message.create`)
- Preset: `preset.<group>.<variant>` (vd `preset.calendar.default`)

Comma-separated, không space.

Lợi ích custom:
- Giảm số tool Claude phải scan → faster
- Bảo mật — exclude destructive tools (vd `*.delete`)

Full tool list: https://github.com/larksuite/lark-openapi-mcp

---

## Tenant mode limitations

Tenant mode = bot acts as ITSELF. KHÔNG act AS user.

**Tenant mode CÓ THỂ**:
- Gửi message vào group bot là member
- Quản lý Bitable / Sheets / Docs shared với bot
- Schedule calendar event (bot-owned calendar)
- Tạo task assigned to bot
- List + manage chat group members

**Tenant mode KHÔNG THỂ** (cần user_access_token, skill không support):
- Đọc personal docs/calendar của user
- Send message dưới danh nghĩa user
- Read 1-1 chat của user khác
- Access "My Drive" của user

Phù hợp use case SEONGON: gửi notification, automation Bitable client SEO, schedule calendar group, manage shared docs. KHÔNG phù hợp nếu cần personal automation cá nhân.

---

## Common scopes ngoài 8 default

| Scope | Purpose | Khi nào cần |
|---|---|---|
| `mail:mail` | Lark Mail — đọc/gửi mail | Workflow mail automation |
| `drive:drive` | Drive — list/upload/download | File management |
| `vc:meeting` | Video Conference — schedule meeting | Meeting bot |
| `wiki:wiki` | Lark Wiki — read/write wiki | Knowledge base |
| `okr:objective` | OKR — list/update | Performance tracking |
| `attendance:attendance` | Attendance | HR automation |
| `helpdesk:ticket` | Helpdesk — tickets | Customer support |

Full list: https://open.larksuite.com/document/server-docs/application-v6/scope

---

## Security note

- Scope càng rộng = bot càng quyền lực
- KHÔNG enable wildcard scope (`*:*`)
- KHÔNG share App Secret — mỗi user/team tạo app riêng
- Rotate App Secret định kỳ — Console → Credentials → "Regenerate Secret"
- `.env` trong `.gitignore` (skill auto-handle)
- App Secret leak → revoke ngay tại Console
