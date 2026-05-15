---
name: google-connect
description: This skill should be used when the user asks to "connect Google", "kết nối Google", "setup Google OAuth", "đăng nhập Google", "/google-connect", "Google Sheets không kết nối được", "GOOGLE_REFRESH_TOKEN expired", "lỗi 401 Google", "invalid_grant", or wants to authenticate Claude Code with their Google account to read/write Google Sheets, Google Docs, or Google Drive. Walks non-technical users step-by-step through Google Cloud Console OAuth setup, runs the OAuth browser flow, writes credentials to .env, installs an auto-refresh hook so future token expiries recover automatically, and runs a smoke test to verify the connection works. End deliverable — a working .env with GOOGLE_CLIENT_ID + GOOGLE_CLIENT_SECRET + GOOGLE_REFRESH_TOKEN, an installed PostToolUse hook, and a verified smoke test.
---

# google-connect

Skill kết nối Google OAuth cho Claude Code — designed cho non-tech. Sau khi chạy xong, học viên có thể yêu cầu Claude đọc/ghi Google Sheets, Docs, Drive mà không gặp lỗi auth.

## Khi nào dùng skill này

User nói một trong các pattern:
- `/google-connect` — setup lần đầu
- "kết nối Google", "setup Google OAuth", "đăng nhập Google"
- "Google Sheets không kết nối được", "lỗi đọc Sheets"
- "GOOGLE_REFRESH_TOKEN expired", "invalid_grant", "lỗi 401 Google"
- Setup repo mới có dùng Google APIs

KHÔNG dùng skill này khi:
- User chỉ cần đọc 1 public Sheet (dùng URL export CSV nhanh hơn)
- User đã có `.env` working + hook installed (skill đã chạy thành công trước đó — gọi lại sẽ overwrite)
- User muốn dùng Google service account (skill này là OAuth user flow — service account cần skill khác)
- User cần **Google Ads / DV360 / SA360 / CM360** — các API marketing này cần credentials BỔ SUNG ngoài OAuth scope (xem `references/scopes-explained.md` mục "Lưu ý: 1 số Google API cần credentials BỔ SUNG"). Skill cover OAuth scope flow only.

## Default settings

| Setting | Default | Override khi |
|---|---|---|
| Scopes | spreadsheets + drive + documents | User cần thêm scope (gmail, calendar) — sửa `scripts/oauth_refresh.py` |
| `.env` path | Project root (`./.env`) | User dùng `.env.local` hoặc khác — sửa path trong scripts |
| Hook path | `.claude/hooks/google_token_refresh.py` | Không override — Claude Code convention |
| OAuth port | 8080 | Port bị chiếm — sửa trong `scripts/oauth_refresh.py` |
| Language | Tiếng Việt | User chỉ nói tiếng Anh |

## Pre-conditions

Trước khi chạy skill, verify:
- [ ] Python 3.8+ installed (`python --version`)
- [ ] Pip packages: `google-auth`, `google-auth-oauthlib`, `google-api-python-client` (skill sẽ tự cài nếu thiếu)
- [ ] Account Google của user (Gmail account để OAuth)
- [ ] Browser default available (skill mở browser cho OAuth flow)

Skill sẽ check pre-conditions ở Step 1. Fail → báo user + dừng.

## Pipeline — 7 bước

Theo thứ tự, không skip. Skill enforce mỗi bước done mới sang bước sau.

### Step 1 — Pre-check environment

```bash
python --version
python -m pip list | grep -E "google-auth|google-api-python-client"
```

Validate:
- Python ≥ 3.8 → PASS
- Packages installed → PASS, không thì cài: `python -m pip install google-auth google-auth-oauthlib google-api-python-client`

Nếu user trên Windows/PowerShell, dùng `python -m pip` thay vì `pip` để tránh PATH issue.

### Step 2 — Walkthrough Google Cloud Console setup

Đây là bước user struggle nhất. Đọc `references/google-cloud-setup.md` để guide chi tiết với screenshot description.

Skill hỏi user 1 câu duy nhất:
```
Bạn đã có Google Cloud project + OAuth credentials chưa?
- Có → cung cấp GOOGLE_CLIENT_ID và GOOGLE_CLIENT_SECRET
- Chưa → mình hướng dẫn tạo (mất ~5 phút)
```

**Nếu CHƯA**: walk through 6 sub-steps (chi tiết trong references/google-cloud-setup.md):
1. Vào https://console.cloud.google.com/projectcreate
2. Tạo project name (vd: "claude-seongon-{date}")
3. Enable 3 APIs: Sheets, Drive, Docs (https://console.cloud.google.com/apis/library)
4. Tạo OAuth consent screen (External, test user = email của user)
5. Tạo OAuth Client ID (Desktop app)
6. Download JSON → copy `client_id` + `client_secret`

Wait user xác nhận đã có credentials → Step 3.

### Step 3 — Write CLIENT_ID + CLIENT_SECRET vào .env

Kiểm tra `.env` tồn tại ở project root:
- Có → preserve các biến khác, chỉ append/update GOOGLE_CLIENT_ID + GOOGLE_CLIENT_SECRET
- Không → tạo mới từ `assets/env.template`

User paste GOOGLE_CLIENT_ID và GOOGLE_CLIENT_SECRET. Skill validate format:
- CLIENT_ID phải match regex `^\d+-[\w]+\.apps\.googleusercontent\.com$`
- CLIENT_SECRET phải bắt đầu `GOCSPX-`

Validate fail → báo user copy nhầm → ask lại.

### Step 4 — Run OAuth browser flow

Run `scripts/oauth_refresh.py`:
```bash
PYTHONUTF8=1 python .claude/skills/google-connect/scripts/oauth_refresh.py
```

Script sẽ:
1. Mở browser tới Google OAuth consent screen
2. User login Google account → grant 3 scopes
3. Google redirect về `http://localhost:8080` với authorization code
4. Script exchange code → refresh_token
5. Append `GOOGLE_REFRESH_TOKEN=<token>` vào `.env`

Skill báo user: "Browser sẽ mở. Login Google account, bấm Continue 2 lần, hoặc Allow tất cả permissions. Sau đó quay lại đây."

Wait script exit code 0 → Step 5. Exit code khác 0 → đọc `references/troubleshooting.md` mục tương ứng error.

### Step 5 — Install auto-refresh hook

Token có lifetime ~6 tháng. Khi expire, hook tự refresh không cần user can thiệp.

Run `scripts/install.py`:
```bash
python .claude/skills/google-connect/scripts/install.py
```

Script sẽ:
1. Copy `scripts/sources/oauth_refresh.py` → `.claude/skills/lib/oauth_refresh.py` (canonical location)
2. Copy `scripts/sources/google_token_refresh.py` → `.claude/hooks/google_token_refresh.py`
3. Patch `.claude/settings.local.json` thêm PostToolUse hook entry:
   ```json
   {
     "hooks": {
       "PostToolUse": [
         {
           "matcher": "Bash",
           "hooks": [{"type": "command", "command": "python .claude/hooks/google_token_refresh.py"}]
         }
       ]
     }
   }
   ```
4. Detect existing hooks → merge thay vì overwrite

Validate: file `.claude/hooks/google_token_refresh.py` tồn tại + settings.local.json có entry → Step 6.

### Step 6 — Smoke test

Verify connection thực sự work:
```bash
python .claude/skills/google-connect/scripts/smoke_test.py
```

Script sẽ:
1. Load `.env`
2. Refresh access token từ refresh_token
3. Gọi Google Sheets API list metadata 1 public sheet test
4. Print "OK — Google API hoạt động" nếu success

Smoke test fail → đọc `references/troubleshooting.md`. Common causes:
- Scopes chưa enable đúng → quay lại Step 2 enable APIs
- Refresh_token sai → quay lại Step 4 OAuth flow
- Network blocked → check firewall

### Step 7 — Report

Output cho user:
```
Google OAuth setup hoàn tất.

.env có 3 biến:
  - GOOGLE_CLIENT_ID
  - GOOGLE_CLIENT_SECRET
  - GOOGLE_REFRESH_TOKEN

Hook auto-refresh: .claude/hooks/google_token_refresh.py (active)
Smoke test: PASSED

Test ngay bằng cách hỏi Claude:
  "Đọc Google Sheet này giúp tôi: <URL>"
  "Liệt kê 10 file Google Drive gần nhất của tôi"

Nếu sau này gặp lỗi 401 / invalid_grant, hook sẽ tự mở browser cho bạn re-auth.
```

## Decision points

Tổng hợp các điểm skill phải dừng/hỏi user vs auto-proceed:

| Step | Hỏi user khi | Auto-proceed khi |
|---|---|---|
| 1 (pre-check) | Python <3.8 hoặc cài pip fail | Python + packages OK |
| 2 (Cloud Console) | User chưa có Cloud project | User confirm "đã có credentials" |
| 3 (.env) | CLIENT_ID/SECRET fail format validation | Format match regex |
| 4 (OAuth flow) | `oauth_refresh.py` exit code ≠ 0 | Exit code 0 + .env có GOOGLE_REFRESH_TOKEN |
| 5 (install hook) | `install.py` báo fail trên copy hoặc patch settings | Exit code 0 + 3 files đúng vị trí |
| 6 (smoke test) | Exit code ≠ 0 (401/403/network) | Exit code 0 |
| 7 (report) | N/A — luôn output | — |

## Recovery

Khi step fail, skill làm theo thứ tự:

1. **Đọc error message stderr** — script in ra error cụ thể (HTTP code, missing var, port conflict)
2. **Tra `references/troubleshooting.md`** mục tương ứng step — có 10+ common errors + fix
3. **Báo user fix root cause** — KHÔNG suggest workaround (vd: thay vì skip step, fix Cloud Console)
4. **Retry step** từ đầu sau khi user fix

Common recovery:
| Failure | Fix |
|---|---|
| Step 1 — `python` không tìm thấy | Cài Python 3.10+ từ python.org, tick "Add to PATH" |
| Step 2 — User stuck ở Cloud Console | Đọc `references/google-cloud-setup.md` sub-step tương ứng |
| Step 3 — Format CLIENT_ID sai | Quay lại Cloud Console → Credentials → click client → copy lại |
| Step 4 — "Access blocked" | Add email user vào Test users của OAuth consent screen |
| Step 4 — Port 8080 busy | Sửa `PORT = 8090` trong `oauth_refresh.py` |
| Step 5 — settings.local.json conflict | Manual edit theo template trong `troubleshooting.md` |
| Step 6 — 401/403 smoke test | Verify scopes đã grant + APIs enabled |

## Anti-patterns

- KHÔNG hard-code GOOGLE_CLIENT_ID hoặc CLIENT_SECRET trong scripts — luôn đọc từ `.env`
- KHÔNG commit `.env` lên git (skill check `.gitignore` có `.env` chưa, thêm nếu chưa)
- KHÔNG skip Step 5 (install hook) — không có hook, user phải re-run skill mỗi lần token expire
- KHÔNG share refresh_token với người khác — đây là credential riêng của user
- KHÔNG dùng service account thay user OAuth — service account flow khác hoàn toàn, cần skill riêng

## Common pitfalls

1. **Port 8080 bị chiếm** — script fail. Fix: kill process trên port 8080, hoặc sửa PORT trong `oauth_refresh.py`.
2. **OAuth consent screen "Access blocked"** — user chưa thêm chính email làm test user. Fix: vào OAuth consent screen → Test users → Add email user đang login.
3. **APIs chưa enable** — 401/403 ở smoke test. Fix: vào Cloud Console → APIs & Services → Library → enable Sheets, Drive, Docs.
4. **Sai client_secret** — paste nhầm trailing space. Fix: copy lại từ JSON, không từ display field.
5. **Browser không mở tự động** — Windows/WSL issue. Fix: copy URL từ stderr, paste manual vào browser.
6. **Settings.local.json đã có hook khác** — install.py phải MERGE, không overwrite. Đã handle.
7. **Token expire giữa session** — hook PostToolUse sẽ catch + auto-refresh. User chỉ cần retry lệnh Bash gần nhất.

## Skill files

| File | Purpose | Khi nào load |
|---|---|---|
| `references/google-cloud-setup.md` | Visual walkthrough Cloud Console (6 sub-steps) | Step 2 |
| `references/troubleshooting.md` | 10+ common errors + fixes | Khi step nào fail |
| `references/scopes-explained.md` | 3 scopes giải thích cho non-tech | User hỏi "scope là gì" / muốn thêm scope |
| `scripts/oauth_refresh.py` | Local copy — chạy OAuth flow ở Step 4 | Step 4 |
| `scripts/install.py` | Installer — deploy hook + lib + patch settings | Step 5 |
| `scripts/smoke_test.py` | Verify Google API works | Step 6 |
| `scripts/sources/oauth_refresh.py` | Source file to install at `.claude/skills/lib/` | Step 5 (deployed) |
| `scripts/sources/google_token_refresh.py` | Source hook to install at `.claude/hooks/` | Step 5 (deployed) |
| `assets/env.template` | Skeleton `.env` với 3 Google vars + comment | Step 3 (nếu .env không tồn tại) |

## Tiêu chí chất lượng (self-check)

Trước khi report Step 7:
- [ ] `.env` tồn tại ở project root, có 3 biến GOOGLE_*
- [ ] `.claude/hooks/google_token_refresh.py` tồn tại
- [ ] `.claude/skills/lib/oauth_refresh.py` tồn tại
- [ ] `.claude/settings.local.json` có entry PostToolUse với matcher "Bash"
- [ ] Smoke test exit code 0
- [ ] `.gitignore` có `.env` (nếu repo là git repo)

## Voice rules

- Tiếng Việt direct, imperative form
- KHÔNG dùng technical jargon mà không giải thích (audience non-tech)
- KHÔNG nói "Bạn cần phải...", thay bằng "Vào Cloud Console", "Click Enable"
- Mỗi step có rationale 1 dòng để user hiểu WHY, không chỉ HOW
- KHÔNG emoji
- Step nào user dễ stuck → có "Common pitfall" section ở cuối skill liên kết tới troubleshooting.md

## Sample timing

- Step 1 pre-check: 1 phút
- Step 2 Cloud Console setup (lần đầu): 5-7 phút
- Step 3 .env credentials: 1 phút
- Step 4 OAuth flow: 1-2 phút
- Step 5 install hook: 30 giây
- Step 6 smoke test: 30 giây
- Step 7 report: 30 giây

**Total: 8-12 phút** lần đầu setup. Subsequent re-runs (vd refresh token expire 6 tháng sau): ~2 phút (hook tự handle).
