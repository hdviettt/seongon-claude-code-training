---
name: lark-connect
description: This skill should be used when the user asks to "connect Lark", "kết nối Lark", "setup Lark MCP", "đăng nhập Lark", "/lark-connect", "Lark integration", "Feishu setup", "Lark Open Platform", or wants to authenticate Claude Code with their Lark account so Claude can send messages, manage tasks, read/write Lark Docs, Sheets, Bitable, or Calendar. Walks non-technical users through Lark Developer Console custom-app creation, installs the official @larksuiteoapi/lark-mcp server, configures .mcp.json for Claude Code, runs the OAuth browser flow via lark-mcp login, and verifies the connection by smoke-testing a tool call. End deliverable — a working .mcp.json pointing to lark-mcp, .env with LARK_APP_ID + LARK_APP_SECRET, cached OAuth tokens, and a verified smoke test confirming Claude can call Lark tools.
---

# lark-connect

Skill kết nối Lark/Feishu cho Claude Code qua official MCP server. Sau khi chạy xong, học viên có thể yêu cầu Claude gửi message Lark, đọc/ghi Bitable, quản lý task, schedule calendar mà không gặp lỗi auth.

## Khi nào dùng skill này

User nói một trong các pattern:
- `/lark-connect` — setup lần đầu
- "kết nối Lark", "setup Lark MCP", "đăng nhập Lark", "Lark integration"
- "Feishu setup", "Lark Open Platform"
- "Claude gửi message qua Lark được không"

KHÔNG dùng skill này khi:
- User chỉ cần gửi 1 message qua Lark webhook (dùng webhook URL trực tiếp, không cần MCP)
- User đã có `.mcp.json` working + `lark-mcp login` đã chạy (skill đã chạy thành công — gọi lại sẽ overwrite)
- User muốn build Lark bot có UI riêng (skill này là MCP integration cho Claude Code, không phải build bot)

## Default settings

| Setting | Default | Override khi |
|---|---|---|
| Domain | `https://open.larksuite.com` (Lark Suite — international, gồm VN) | User dùng Feishu (China) → `https://open.feishu.cn` |
| Token mode | `user_access_token` (truy cập resource cá nhân) | User chỉ cần bot capability → `tenant_access_token` |
| OAuth | Enabled | User chỉ cần bot — disable `--oauth` |
| Tools preset | `default` (gồm IM + Calendar + Docs + Bitable) | User cần custom — truyền `-t tool1,tool2` |
| MCP config scope | Project (`.mcp.json` ở root) | User muốn user-scope → `~/.claude.json` |
| Language | Tiếng Việt | User chỉ nói tiếng Anh |

## Pre-conditions

- [ ] Node.js ≥18 installed (`node --version`)
- [ ] npm/npx accessible (`npx --version`)
- [ ] Lark account (Larksuite hoặc Feishu)
- [ ] Browser default available
- [ ] Internet (Lark API + npm registry)

Skill check pre-conditions ở Step 1. Fail → báo user fix + dừng.

## Pipeline — 7 bước

Theo thứ tự, không skip.

### Step 1 — Pre-check environment

```bash
node --version    # cần ≥ 18
npx --version
```

Validate:
- Node.js < 18 → báo user upgrade (download nodejs.org hoặc dùng nvm)
- npx không có → cài Node.js (npm + npx ship cùng)

Run smoke check lark-mcp accessible:
```bash
npx -y @larksuiteoapi/lark-mcp --version
```

Lần đầu chạy npx sẽ download package (~30-60 giây). Báo user "Đang tải lark-mcp lần đầu, chờ chút".

### Step 2 — Walkthrough Lark Open Platform

Đọc `references/lark-platform-setup.md` để guide chi tiết. Hỏi user 1 câu:

```
Bạn đã có Lark Custom App + App ID/Secret chưa?
- Có → cung cấp LARK_APP_ID và LARK_APP_SECRET
- Chưa → mình hướng dẫn tạo (~5-7 phút)
```

**Nếu CHƯA**: walk through 7 sub-steps (chi tiết trong references/lark-platform-setup.md):
1. Vào https://open.larksuite.com (hoặc https://open.feishu.cn cho FS) → Login Lark account
2. Click **Developer Console** → **Create Custom App**
3. App name + icon → CREATE
4. Vào **Credentials & Basic Info** → copy **App ID** + **App Secret**
5. Vào **Permissions & Scopes** → enable scopes default (im:message, docx:document, sheets:spreadsheet, calendar:calendar, task:task, contact:contact, offline_access)
6. Vào **Events & Callbacks** → để trống (không cần cho MCP usage)
7. Vào **Version Management** → Submit for Release → Self-approve (Custom App tự duyệt được)

Wait user xác nhận đã có credentials → Step 3.

### Step 3 — Write credentials vào .env

Validate format LARK_APP_ID:
- Lark Suite: bắt đầu `cli_` (vd `cli_a1b2c3d4e5`)
- Feishu: bắt đầu `cli_`
- Format invalid → báo user copy nhầm → ask lại

Skill validate App Secret không trống + ≥30 chars (Lark secrets typically 40+ chars).

Ghi `.env` (preserve existing vars):
```env
LARK_APP_ID=cli_xxxx
LARK_APP_SECRET=xxxx
LARK_DOMAIN=https://open.larksuite.com
```

Nếu `.env` không tồn tại, copy từ `assets/env.template`.

### Step 4 — Write `.mcp.json` config

Tạo hoặc patch `.mcp.json` ở project root. Pattern dùng wrapper script để load credentials từ `.env`:

```json
{
  "mcpServers": {
    "lark-mcp": {
      "command": "python",
      "args": [".claude/skills/lark-connect/scripts/lark_mcp_runner.py"]
    }
  }
}
```

Wrapper `lark_mcp_runner.py` đọc `.env` → spawn `npx -y @larksuiteoapi/lark-mcp mcp` với args đúng. Lợi ích:
- Credentials KHÔNG hardcode trong `.mcp.json` → safe commit lên git
- Switch domain/mode bằng sửa `.env`, không sửa config

Nếu `.mcp.json` đã tồn tại với mcpServers khác → MERGE, không overwrite.

### Step 5 — Run OAuth login

```bash
npx -y @larksuiteoapi/lark-mcp login -a <LARK_APP_ID> -s <LARK_APP_SECRET>
```

Script sẽ:
1. Mở browser tới Lark OAuth consent page
2. User login Lark account → approve scopes
3. Lark redirect về local callback → token cached vào `~/.lark-mcp/`
4. Print "Login successful"

Skill báo user: "Browser sẽ mở. Login Lark, approve permissions. Sau đó quay lại đây — token được lark-mcp tự lưu, không cần copy."

Wait exit code 0 → Step 6.

### Step 6 — Smoke test

Restart Claude Code session để load MCP (skill báo user manual restart hoặc dùng /restart command).

Sau restart, verify lark-mcp tools available:
```bash
python .claude/skills/lark-connect/scripts/smoke_test.py
```

Smoke test sẽ:
1. Check `~/.lark-mcp/` có token cached
2. Spawn lark-mcp server bằng wrapper
3. Send 1 JSON-RPC `tools/list` request
4. Verify response có tools (vd `im.v1.message.create`)

Output `OK — lark-mcp ready với N tools` → Step 7.

### Step 7 — Report

```
Lark MCP setup hoàn tất.

.env có:
  - LARK_APP_ID
  - LARK_APP_SECRET
  - LARK_DOMAIN

.mcp.json có entry "lark-mcp" trỏ tới wrapper script
OAuth token cached tại ~/.lark-mcp/

Test ngay bằng cách hỏi Claude:
  "Gửi message qua Lark cho group X: 'Test from Claude'"
  "List 5 file Bitable gần nhất của tôi"
  "Tạo task Lark 'Review proposal' deadline mai"

Nếu Claude báo không thấy tool Lark → restart Claude Code (close + reopen)
```

## Decision points

| Step | Hỏi user khi | Auto-proceed khi |
|---|---|---|
| 1 (pre-check) | Node.js <18 hoặc npx fail | Node + npx OK |
| 2 (Lark Platform) | User chưa có Custom App | User confirm "đã có" |
| 3 (.env) | LARK_APP_ID fail format | Format match `cli_` prefix |
| 4 (.mcp.json) | Existing `.mcp.json` có conflict server name | No conflict |
| 5 (OAuth login) | `lark-mcp login` exit ≠ 0 | Exit 0 + token cached |
| 6 (smoke test) | `tools/list` fail hoặc empty | ≥1 tool returned |
| 7 (report) | N/A | — |

## Recovery

Khi step fail:
1. Đọc stderr — script in error cụ thể
2. Tra `references/troubleshooting.md` mục tương ứng
3. Fix root cause, KHÔNG workaround
4. Retry step từ đầu sau khi fix

Common recovery:
| Failure | Fix |
|---|---|
| Step 1 — `node: command not found` | Install Node.js 18+ từ nodejs.org |
| Step 1 — `npx -y @larksuiteoapi/lark-mcp` timeout | Network slow → tăng timeout `npm config set fetch-retry-maxtimeout 60000` |
| Step 2 — User stuck Lark Platform | Đọc `references/lark-platform-setup.md` sub-step |
| Step 3 — App ID không bắt đầu `cli_` | Copy lại từ Lark Console → Credentials |
| Step 4 — `.mcp.json` conflict | Manual edit theo template `assets/mcp-config.template.json` |
| Step 5 — Browser không mở | Copy auth URL từ stderr → paste manual |
| Step 5 — "Invalid app credentials" | App chưa Release ở Version Management → quay lại Step 2 sub-step 7 |
| Step 6 — Tools list empty | Scopes chưa enable đúng → quay lại Step 2 sub-step 5 |
| Step 6 — Claude không thấy tool Lark | Chưa restart CC sau Step 5 → close + reopen Claude Code |

## Anti-patterns

- KHÔNG hardcode LARK_APP_ID/SECRET trong `.mcp.json` — luôn qua wrapper đọc `.env`
- KHÔNG commit `.env` lên git (skill check `.gitignore` có `.env` chưa, thêm nếu chưa)
- KHÔNG skip Step 2 sub-step 7 (Release) — app chưa Release sẽ fail OAuth với "App pending review"
- KHÔNG dùng custom domain ngoài 2 domain official (`open.larksuite.com` / `open.feishu.cn`)
- KHÔNG share App Secret với người khác — mỗi học viên tự tạo app riêng

## Common pitfalls

1. **Submit for Release vs Self-approve** — Custom App có thể self-approve (không cần admin Lark). Bypass nếu user nhầm tưởng cần admin permission.
2. **Lark Suite vs Feishu domain** — VN dùng `open.larksuite.com`, China dùng `open.feishu.cn`. User Vietnam thường nhầm vào Feishu domain → auth fail.
3. **Scopes thiếu** — enable không đủ scope → tool call fail 403. Default skill enable 7 scope common, nếu user cần thêm (gmail bridge, custom field Bitable) → đọc `references/scopes-and-tools.md`.
4. **Token expire** — lark-mcp tự refresh khi gọi. Khác Google, không cần PostToolUse hook.
5. **`npx` chậm lần đầu** — package ~50MB. User tưởng skill stuck → báo trước "đang download lần đầu".
6. **MCP không load sau restart** — Claude Code cache MCP startup. Nếu chỉnh `.mcp.json` mà skill không thấy → close hoàn toàn process CC + mở lại.
7. **`.mcp.json` syntax error** → silent fail. install.py validate JSON parse trước khi ghi.

## Skill files

| File | Purpose | Khi nào load |
|---|---|---|
| `references/lark-platform-setup.md` | Walkthrough Developer Console (7 sub-steps) | Step 2 |
| `references/troubleshooting.md` | 12+ common errors + fix | Khi step fail |
| `references/scopes-and-tools.md` | Token modes + 30+ scopes + preset tools | User muốn thêm/bớt scope |
| `references/mcp-explained.md` | MCP là gì, vì sao dùng MCP với Lark thay vì raw API | User hỏi about MCP |
| `scripts/install.py` | Orchestrator — write .env + .mcp.json + .gitignore | Step 3-4 |
| `scripts/lark_mcp_runner.py` | Wrapper — đọc .env, spawn lark-mcp với credentials | Runtime (MCP load) |
| `scripts/smoke_test.py` | Verify tools list non-empty | Step 6 |
| `assets/env.template` | Skeleton `.env` với 3 LARK vars | Step 3 |
| `assets/mcp-config.template.json` | `.mcp.json` template | Step 4 |

## Tiêu chí chất lượng (self-check)

Trước khi report Step 7:
- [ ] `.env` có LARK_APP_ID + LARK_APP_SECRET + LARK_DOMAIN, format valid
- [ ] `.mcp.json` ở project root, JSON parse OK, có entry "lark-mcp"
- [ ] `scripts/lark_mcp_runner.py` executable (Python script với shebang)
- [ ] `~/.lark-mcp/` tồn tại (token cached)
- [ ] Smoke test exit code 0, ≥1 tool returned
- [ ] `.gitignore` có `.env` (nếu git repo)

## Voice rules

- Tiếng Việt direct, imperative form
- KHÔNG technical jargon không giải thích (audience non-tech)
- Mỗi step có rationale ngắn để user hiểu WHY
- KHÔNG emoji
- Step phức tạp (Step 2 Lark Console) → trỏ về references chi tiết

## Sample timing

- Step 1 pre-check + npx download: 1-2 phút
- Step 2 Lark Platform setup (lần đầu): 5-7 phút
- Step 3 .env credentials: 1 phút
- Step 4 .mcp.json: 30 giây
- Step 5 OAuth login: 1-2 phút
- Step 6 restart CC + smoke test: 1 phút
- Step 7 report: 30 giây

**Total: 9-14 phút** lần đầu. Re-setup (vd đổi máy): ~3 phút (skip Step 2).
