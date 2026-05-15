# EVALS — lark-connect

3 scenarios để test skill có hoạt động đúng không. Chạy ở phiên Claude Code mới (fresh context).

## Eval 1: Golden path — Học viên setup lần đầu

**Tên scenario**: Repo trắng, học viên chưa có Lark Custom App

**Precondition**:
- Repo mới (không có `.env`, không có `.mcp.json`)
- Node.js 20+ installed (`node --version` ≥ 18)
- Python 3.10+ installed
- Học viên có Lark account (Lark Suite hoặc Feishu)

**User input**:
```
/lark-connect
```

**Expected behavior**:
1. Skill `lark-connect` triggered
2. Step 1: Pre-check Node.js + npx + Python. Lần đầu npx tải lark-mcp (báo user chờ ~60s).
3. Step 2: Hỏi "Đã có Lark Custom App chưa?" → CHƯA → walkthrough 7 sub-steps từ `references/lark-platform-setup.md`
4. Step 3: User paste APP_ID + SECRET → skill validate format (regex `cli_` prefix, secret ≥30 chars) → ghi `.env`
5. Step 4: Run `install.py` → patch `.mcp.json` với entry "lark-mcp" trỏ tới wrapper script
6. Step 5: Run `npx lark-mcp login -a $X -s $Y` → browser mở → user authorize → token cached `~/.lark-mcp/`
7. Step 6: User restart Claude Code. Sau restart, skill run `smoke_test.py` → tools/list returns ≥10 tools
8. Step 7: Report files created + cách test bằng "Gửi Lark cho group X"

**Pass criteria**:
- [ ] `.env` ở project root có LARK_APP_ID + LARK_APP_SECRET + LARK_DOMAIN
- [ ] `.mcp.json` ở project root có entry "lark-mcp" với command "python"
- [ ] `~/.lark-mcp/` tồn tại với token cached
- [ ] `.gitignore` có `.env`
- [ ] Smoke test exit 0 với ≥10 tools
- [ ] Sau restart CC, Claude tự load lark-mcp tools
- [ ] Tổng thời gian end-to-end ≤15 phút (lần đầu)

---

## Eval 2: Edge case — Học viên đã có Lark Custom App từ trước

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
3. Step 2: User confirm "đã có credentials" → SKIP walkthrough 7 sub-steps Lark Platform
4. Step 3: Skill validate format App ID + Secret từ user input → ghi `.env`
5. Step 4-7: như Eval 1

**Pass criteria**:
- [ ] Skill DETECT user đã có credentials, KHÔNG force walk through Lark Console
- [ ] Format validation vẫn enforce
- [ ] Tổng thời gian end-to-end ≤6 phút (skip Lark Platform setup)
- [ ] All deliverables như Eval 1

---

## Eval 3: Anti-pattern — App chưa Released

**Tên scenario**: User paste credentials hợp lệ nhưng app chưa Released ở Lark Console → OAuth fail

**Precondition**:
- Repo mới
- Học viên có App ID + Secret nhưng quên bước 7 Release ở Lark Platform setup

**User input** (Step 5 sẽ fail):
Sau khi Step 1-4 done, Step 5 `npx lark-mcp login` returns "Invalid app credentials" hoặc "App pending review".

**Expected behavior**:
1. Skill Step 5 detect exit code ≠ 0
2. Đọc stderr error message
3. Match error pattern "Invalid app credentials" → reference troubleshooting.md Step 5 errors
4. Báo user CỤ THỂ: "App chưa Released. Vào Lark Console → Version Management → Submit for Release → Self-approve"
5. KHÔNG tiếp tục Step 6 smoke test (vì token sẽ không có)
6. Wait user fix → confirm → re-run Step 5

**Pass criteria**:
- [ ] Skill DETECT login fail (không silent proceed sang Step 6)
- [ ] Error message CỤ THỂ — chỉ ra Lark Console page cần vào (không generic "fix it")
- [ ] Step 6 KHÔNG chạy với credentials invalid
- [ ] Recovery instruction explicit + trỏ về `references/troubleshooting.md` mục đúng
- [ ] Sau khi user fix + re-run, pipeline tiếp tục từ Step 5

---

## Cách chạy evals

### Manual test

1. Tạo 1 repo trống test (vd `~/test-lark-connect/`)
2. Copy `.claude/skills/lark-connect/` từ workspace vào repo test
3. Mở phiên Claude Code mới ở repo test
4. Chạy Eval 1/2/3 theo precondition
5. Tick Pass criteria sau khi skill xong

### Cleanup giữa các evals

Để re-run scenario, xoá:
- `.env`
- `.mcp.json`
- `~/.lark-mcp/` (token cache)
- Restart Claude Code

Hoặc git stash để revert.

### Reset Lark Console (cho Eval 3 setup)

Để force "app pending" state cho Eval 3:
1. Vào Lark Console → app → Version Management
2. Click "Retract" version đang Released → app trở về Development mode
3. Run Step 5 → sẽ fail với "Invalid app credentials"

---

## Eval results log

| Date | Skill version | Eval 1 | Eval 2 | Eval 3 | Notes |
|---|---|---|---|---|---|
| 2026-05-15 | v0.1 | NOT TESTED | NOT TESTED | NOT TESTED | Initial release — pending manual test |
