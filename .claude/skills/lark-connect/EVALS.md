# EVALS — lark-connect (Tenant Mode)

3 scenarios để test skill có hoạt động đúng không. Chạy ở phiên Claude Code mới (fresh context).

## Eval 1: Golden path — Học viên setup lần đầu

**Tên scenario**: Repo trắng, học viên chưa có Lark Custom App

**Precondition**:
- Repo mới (không có `.env`, không có `.mcp.json`)
- Node.js 20+ installed (`node --version` ≥ 18)
- Python 3.10+ installed
- Học viên có Lark account (Lark Suite)

**User input**:
```
/lark-connect
```

**Expected behavior**:
1. Skill `lark-connect` triggered
2. Step 1: Pre-check Node.js + npx + Python. Lần đầu npx tải lark-mcp (báo user ~60s).
3. Step 2: Hỏi "Đã có Lark Custom App chưa?" → CHƯA → walkthrough 6 sub-steps từ `references/lark-platform-setup.md`
4. Step 3: User paste APP_ID + SECRET → skill validate format (regex `cli_` prefix, secret ≥30 chars) → verify app identity via API call → ghi `.env`
5. Step 4: Run `install.py` → patch `.mcp.json` với entry "lark-mcp" trỏ tới wrapper script
6. Step 5: Báo user restart CC + run `smoke_test.py` → tools/list returns ≥10 tools (typically 17)
7. Step 6: Report files created + app_name verified + cách test bằng "List nhóm chat Lark"

**Pass criteria**:
- [ ] `.env` ở project root có LARK_APP_ID + LARK_APP_SECRET + LARK_DOMAIN + LARK_TOKEN_MODE=tenant_access_token
- [ ] App identity verified — skill báo "App detected: <app_name>" sau Step 3
- [ ] `.mcp.json` ở project root có entry "lark-mcp" với command "python"
- [ ] `.gitignore` có `.env`
- [ ] Smoke test exit 0 với ≥10 tools
- [ ] Sau restart CC, Claude load lark-mcp tools (call "list Lark chats" work)
- [ ] Tổng thời gian end-to-end ≤12 phút (lần đầu)
- [ ] Skill KHÔNG mention OAuth, browser flow, redirect URL — tenant mode bypass

---

## Eval 2: Edge case — Học viên đã có Lark Custom App

**Tên scenario**: Returning user — App đã có, chỉ cần setup MCP integration

**Precondition**:
- Repo mới (không có `.env`)
- Học viên có sẵn LARK_APP_ID + LARK_APP_SECRET từ app cũ
- App đã Released ở Lark Console

**User input**:
```
/lark-connect

Tôi đã có Lark Custom App rồi, App ID là cli_xxxxxxx, Secret là xxxxxx.
```

**Expected behavior**:
1. Skill triggered
2. Step 1: Pre-check OK
3. Step 2: User confirm "đã có credentials" → SKIP walkthrough 6 sub-steps Lark Platform
4. Step 3: Skill validate format App ID + Secret → verify identity via API → ghi `.env`
5. Step 4-6: như Eval 1

**Pass criteria**:
- [ ] Skill DETECT user đã có credentials, KHÔNG force walk through Lark Console
- [ ] Format validation vẫn enforce
- [ ] Tổng thời gian end-to-end ≤4 phút (skip Lark Platform setup)
- [ ] All deliverables như Eval 1

---

## Eval 3: Anti-pattern — Bot chưa được add vào group nào

**Tên scenario**: Setup thành công nhưng bot là member của 0 chats — skill phải educate user về membership requirement

**Precondition**:
- Eval 1 hoặc 2 đã pass (setup complete)
- Bot chưa được add vào group Lark nào

**User input** (trong Claude Code session đã restart):
```
List các nhóm chat Lark mà bot đang ở
```

**Expected behavior**:
1. Claude call MCP tool `im_v1_chat_list`
2. lark-mcp return empty list (`items: []`)
3. Claude báo user: "Bot hiện không có chat nào. Để bot thấy chats, anh cần add bot làm member của group đó: vào group → Settings → Add Members → search bot name → Add"
4. KHÔNG fabricate fake chats hoặc fail silently
5. Suggest user check Bot capability + invite bot vào group test trước

**Pass criteria**:
- [ ] Skill (qua Claude + MCP) return empty list correctly (không error 401/403)
- [ ] Claude diagnose đúng — "0 chats vì bot chưa là member", không phải "API fail"
- [ ] Recommendation cụ thể về cách add bot vào group
- [ ] User được hướng dẫn check Bot capability ở Lark Console (Step 5 sub-step trong setup)

---

## Cách chạy evals

### Manual test

1. Tạo 1 repo trống test (vd `~/test-lark-connect/`)
2. Copy `.claude/skills/lark-connect/` từ workspace vào repo test
3. Mở phiên Claude Code mới ở repo test
4. Chạy Eval 1/2/3 theo precondition
5. Tick Pass criteria

### Cleanup giữa các evals

Để re-run scenario, xoá:
- `.env`
- `.mcp.json`
- `.gitignore` line `.env` (nếu test fresh)

Restart Claude Code session (quit + mở lại).

---

## Eval results log

| Date | Skill version | Eval 1 | Eval 2 | Eval 3 | Notes |
|---|---|---|---|---|---|
| 2026-05-15 | v0.2 (tenant only) | TESTED partial | NOT TESTED | NOT TESTED | Direct API test (curl) work — 23 chats listed cho "Trợ lý SEONGON" app. Skill end-to-end via Claude+MCP pending fresh CC test. |
