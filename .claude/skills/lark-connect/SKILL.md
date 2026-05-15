---
name: lark-connect
description: This skill should be used when the user asks to "connect Lark", "kết nối Lark", "setup Lark MCP", "Lark bot", "/lark-connect", "Lark integration", "Feishu setup", "Lark Open Platform", or wants to authenticate Claude Code with their Lark Custom App so Claude can send messages, manage tasks, read/write Lark Docs, Sheets, Bitable, or Calendar via the bot identity. Walks non-technical users through Lark Developer Console custom-app creation, configures the official @larksuiteoapi/lark-mcp server via .mcp.json wrapper, and verifies the connection by smoke-testing the tools list. Uses tenant_access_token (bot mode) — no OAuth browser flow required. End deliverable — .env with LARK_APP_ID + LARK_APP_SECRET + LARK_DOMAIN, .mcp.json pointing to lark-mcp wrapper, and a verified smoke test confirming Claude can call Lark tools as the bot.
---

# lark-connect

Skill kết nối Lark/Feishu cho Claude Code qua official MCP server, dùng **tenant_access_token (bot mode)**. Setup ~5-7 phút, không cần OAuth browser flow.

Bot có thể:
- Gửi message vào group bot là member
- Quản lý Bitable / Sheets / Docs shared
- Schedule calendar event (bot-owned)
- Tạo task

Bot KHÔNG thể (cần OAuth user mode, hiện có bug với Larksuite — skill này không cover):
- Đọc personal docs/calendar của user
- Send message dưới danh nghĩa user

## Khi nào dùng skill này

User nói một trong các pattern:
- `/lark-connect` — setup lần đầu
- "kết nối Lark", "setup Lark MCP", "Lark bot"
- "Claude gửi message qua Lark được không"
- "tích hợp Lark vào project"

KHÔNG dùng skill này khi:
- User cần OAuth user mode (đọc data cá nhân) — hiện không support
- User chỉ cần webhook URL gửi message (đơn giản hơn, không cần MCP)
- User đã có `.mcp.json` working — gọi lại sẽ overwrite

## Default settings

| Setting | Default | Override khi |
|---|---|---|
| Domain | `https://open.larksuite.com` (Larksuite — gồm VN) | User dùng Feishu (China) → `https://open.feishu.cn` |
| Token mode | `tenant_access_token` (bot) | KHÔNG override — skill chỉ support mode này |
| Tools preset | default (~17 tools: im, bitable, docx, sheets) | User cần custom → set `LARK_TOOLS=tool1,tool2` |
| MCP config scope | Project (`.mcp.json` ở root) | User muốn user-scope → manual edit `~/.claude.json` |
| Language | Tiếng Việt | User chỉ nói tiếng Anh |

## Pre-conditions

- [ ] Node.js ≥18 installed (`node --version`)
- [ ] npm/npx accessible (`npx --version`)
- [ ] Python 3.10+ (cho wrapper script)
- [ ] Lark account (Larksuite — gồm Vietnam users)
- [ ] Internet (npm registry + Lark API)

KHÔNG cần browser (tenant mode bypass OAuth flow).

## Pipeline — 6 bước

Theo thứ tự, không skip.

### Step 1 — Pre-check environment

```bash
node --version    # cần ≥ 18
npx --version
python --version  # cần ≥ 3.10
```

Validate:
- Node.js < 18 → báo user upgrade (download nodejs.org hoặc dùng nvm)
- npx không có → cài Node.js (npm + npx ship cùng)

Smoke test lark-mcp accessible:
```bash
npx -y @larksuiteoapi/lark-mcp --version
```

Lần đầu npx download package ~50MB (~30-60 giây). Báo user "Đang tải lark-mcp lần đầu, chờ chút". Lần sau dùng cache.

### Step 2 — Walkthrough Lark Open Platform

Đọc `references/lark-platform-setup.md` để guide chi tiết. Hỏi user 1 câu:

```
Bạn đã có Lark Custom App + App ID/Secret chưa?
- Có → cung cấp LARK_APP_ID và LARK_APP_SECRET
- Chưa → mình hướng dẫn tạo (~5 phút)
```

**Nếu CHƯA**: walk through 6 sub-steps (chi tiết trong references/lark-platform-setup.md):
1. Vào https://open.larksuite.com → Login Lark account
2. Developer Console → **Create Custom App**
3. App name + icon → CREATE
4. **Credentials & Basic Info** → copy **App ID** + **App Secret**
5. **Permissions & Scopes** → enable scopes default (im:message, im:chat, docx:document, sheets:spreadsheet, bitable:app, calendar:calendar, task:task, contact:user.base:readonly)
6. **Version Management** → Submit for Release → Self-approve

Tenant mode KHÔNG cần OAuth consent screen, redirect URLs, Bot capability — bypass mọi config phức tạp.

Wait user xác nhận đã có credentials → Step 3.

### Step 3 — Write credentials vào .env

Validate format LARK_APP_ID:
- Match regex `^cli_[a-zA-Z0-9]{12,20}$` (vd `cli_a7e3876125b95010`)
- Format invalid → báo user copy nhầm → ask lại

Validate App Secret ≥30 chars (Lark secrets typically 32+ chars).

Verify app identity bằng API call (catch user paste nhầm app khác):
```bash
TOKEN=$(curl -s -X POST 'https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d '{"app_id":"<id>","app_secret":"<secret>"}' | python -c "import json,sys; print(json.load(sys.stdin).get('tenant_access_token',''))")

curl -s "https://open.larksuite.com/open-apis/application/v6/applications/<id>?lang=en_us" \
  -H "Authorization: Bearer $TOKEN" | python -c "import json,sys; d=json.load(sys.stdin); print(f\"App: {d['data']['app']['app_name']}\")"
```

Báo user "App detected: <name>" để xác nhận đúng app.

Lưu ý: tên app theo i18n — UI Console hiển thị tiếng Việt (vd "Trợ lý SEONGON") nhưng API trả primary name tiếng Anh. Cùng app, khác language. Verify bằng App ID match là chính xác.

Ghi `.env` (preserve existing vars):
```env
LARK_APP_ID=cli_xxxx
LARK_APP_SECRET=xxxx
LARK_DOMAIN=https://open.larksuite.com
LARK_TOKEN_MODE=tenant_access_token
```

Nếu `.env` không tồn tại, copy từ `assets/env.template`.

### Step 4 — Write `.mcp.json` config

Run `install.py` để patch `.mcp.json`:
```bash
python .claude/skills/lark-connect/scripts/install.py
```

Script sẽ:
- Validate `.env` (re-check format)
- Patch `.mcp.json` thêm entry "lark-mcp" trỏ tới `lark_mcp_runner.py`
- Ensure `.gitignore` có `.env`
- MERGE với `.mcp.json` có sẵn (không overwrite mcpServers khác)

Pattern wrapper script tách credentials khỏi MCP config:
- `.env` (gitignored) chứa LARK_APP_ID/SECRET
- `.mcp.json` (commit OK) trỏ tới `lark_mcp_runner.py`
- Runner load `.env` runtime, spawn lark-mcp với `--domain` + `--token-mode tenant_access_token` args

**`--domain https://open.larksuite.com` BẮT BUỘC** — lark-mcp default đi Feishu, sai cho user Larksuite (Vietnam). Wrapper inject flag này tự động.

### Step 5 — Restart Claude Code + smoke test

Skill báo user: "Đóng Claude Code hoàn toàn rồi mở lại (KHÔNG chỉ reload — phải kill process). MCP servers load lúc CC start, không reload runtime."

Sau restart, run smoke test:
```bash
python .claude/skills/lark-connect/scripts/smoke_test.py --verbose
```

Smoke test sẽ:
1. Validate `.env` có 3 biến
2. Spawn lark-mcp via wrapper
3. Send JSON-RPC `tools/list` request
4. Verify ≥10 tools returned (typically 17 default preset)

Smoke test fail → đọc `references/troubleshooting.md`. Common causes:
- Scopes chưa approve trong Lark Console
- App chưa Released → quay lại Step 2 sub-step 6
- npx timeout → tăng `npm config set fetch-timeout 60000`

### Step 6 — Report

```
Lark MCP setup hoàn tất (tenant mode).

App detected: <app_name từ Lark API>
.env có:
  - LARK_APP_ID
  - LARK_APP_SECRET
  - LARK_DOMAIN

.mcp.json có entry "lark-mcp" trỏ tới wrapper script
Smoke test: PASSED (N tools available)

Test ngay trong Claude Code:
  "List các nhóm chat Lark bot đang ở"
  "Send message qua Lark cho group X: 'Test'"
  "List 5 Bitable apps bot có access"

Lưu ý:
- Bot chỉ thấy chat nó là MEMBER. Add bot vào group muốn bot access (trong app group: tap name → Settings → Add Members → search bot name).
- Để test ngay, vào Lark Console → app → Bot → Add to Groups → chọn group.
```

## Decision points

| Step | Hỏi user khi | Auto-proceed khi |
|---|---|---|
| 1 (pre-check) | Node.js <18 hoặc npx fail | Node + npx OK |
| 2 (Lark Platform) | User chưa có Custom App | User confirm "đã có" |
| 3 (.env) | App ID/Secret fail format hoặc app identity fail verify | Format + identity OK |
| 4 (.mcp.json) | `.mcp.json` parse error | No conflict |
| 5 (smoke test) | `tools/list` fail hoặc returns <10 tools | ≥10 tools |
| 6 (report) | N/A | — |

## Recovery

Khi step fail:
1. Đọc stderr — script in error cụ thể
2. Tra `references/troubleshooting.md` mục tương ứng
3. Fix root cause
4. Retry step từ đầu

Common recovery:
| Failure | Fix |
|---|---|
| Step 1 — `node: command not found` | Install Node.js 18+ từ nodejs.org |
| Step 1 — npx timeout | `npm config set fetch-timeout 60000` |
| Step 2 — Stuck Lark Platform | Đọc `references/lark-platform-setup.md` sub-step |
| Step 3 — App ID không match `cli_` prefix | Copy lại từ Lark Console → Credentials |
| Step 3 — App identity verify fail (wrong app) | Re-check anh paste đúng credentials chưa |
| Step 4 — `.mcp.json` parse error | Validate `python -c "import json; json.load(open('.mcp.json'))"` → fix syntax |
| Step 5 — Tools list empty | Scopes chưa approve → Lark Console → Permissions |
| Step 5 — Claude không thấy tool Lark | Quit CC process hoàn toàn (KHÔNG chỉ reload window), mở lại |

## Anti-patterns

- KHÔNG hardcode LARK_APP_ID/SECRET trong `.mcp.json` — luôn qua wrapper đọc `.env`
- KHÔNG commit `.env` lên git (skill check `.gitignore` có `.env` chưa, thêm nếu chưa)
- KHÔNG skip Step 2 sub-step 6 (Release) — app chưa Release sẽ fail authenticate
- KHÔNG dùng custom domain ngoài 2 domain official (`open.larksuite.com` / `open.feishu.cn`)
- KHÔNG share App Secret — mỗi học viên/team tự tạo app riêng
- KHÔNG override `LARK_TOKEN_MODE=user_access_token` — skill chỉ support tenant mode

## Common pitfalls

1. **Lark Suite vs Feishu domain** — VN dùng `open.larksuite.com`. Wrapper inject `--domain` flag tự động, nhưng user phải tạo app đúng region (app Feishu không cross-platform Larksuite).
2. **App identity confusion** — Console UI hiển thị tên i18n (Vietnamese), API trả primary name (English). Cùng app, khác language. Verify bằng App ID match, không bằng tên.
3. **Bot không thấy chat nào** — bot chỉ list được chat nó là MEMBER. Webhook subscription ≠ membership. Add bot vào group qua Settings → Add Members.
4. **`npx` chậm lần đầu** — package ~50MB. User tưởng skill stuck → báo trước "Đang tải lần đầu".
5. **MCP không load sau restart** — Claude Code cache MCP startup. Phải QUIT process hoàn toàn (Ctrl+Q / Cmd+Q), KHÔNG chỉ close window hoặc /restart.
6. **App chưa Release** → authenticate fail. Bắt buộc Submit for Release + Self-approve ở Version Management.
7. **Scopes thiếu** → tool call fail 403. Default 8 scope đủ most use cases. Custom: đọc `references/scopes-and-tools.md`.

## Skill files

| File | Purpose | Khi nào load |
|---|---|---|
| `references/lark-platform-setup.md` | Walkthrough Developer Console (6 sub-steps) | Step 2 |
| `references/troubleshooting.md` | 10+ common errors per step + fix | Khi step fail |
| `references/scopes-and-tools.md` | 8 default scopes + cách thêm scope | User muốn customize |
| `references/mcp-explained.md` | MCP là gì + so sánh với raw API approach | User hỏi about MCP |
| `scripts/install.py` | Orchestrator — validate .env + patch .mcp.json + ensure .gitignore | Step 4 |
| `scripts/lark_mcp_runner.py` | Wrapper runtime — đọc .env + spawn lark-mcp với args | Runtime (MCP load) |
| `scripts/smoke_test.py` | Verify tools/list non-empty | Step 5 |
| `assets/env.template` | Skeleton `.env` với 4 LARK vars | Step 3 |
| `assets/mcp-config.template.json` | `.mcp.json` template | Step 4 |

## Tiêu chí chất lượng (self-check)

Trước khi report Step 6:
- [ ] `.env` có LARK_APP_ID + LARK_APP_SECRET + LARK_DOMAIN + LARK_TOKEN_MODE, format valid
- [ ] App identity verified via API (báo user tên app match)
- [ ] `.mcp.json` ở project root, JSON parse OK, có entry "lark-mcp"
- [ ] `.gitignore` có `.env` (nếu git repo)
- [ ] Smoke test exit 0, ≥10 tools returned
- [ ] User đã restart Claude Code (skill nhắc explicit)

## Voice rules

- Tiếng Việt direct, imperative form
- KHÔNG technical jargon không giải thích (audience non-tech)
- Mỗi step có rationale ngắn user hiểu WHY
- KHÔNG emoji
- Step phức tạp (Step 2) → trỏ về references chi tiết

## Sample timing

- Step 1 pre-check + npx download: 1-2 phút
- Step 2 Lark Platform setup (lần đầu): 5-7 phút
- Step 3 .env + verify identity: 1 phút
- Step 4 install.py: 30 giây
- Step 5 restart + smoke test: 1 phút
- Step 6 report: 30 giây

**Total: 8-12 phút** lần đầu. Re-setup (đổi máy): ~3 phút (skip Step 2).
