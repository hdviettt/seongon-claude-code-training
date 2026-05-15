# Troubleshooting — Lark MCP setup

12+ common errors per step. Đọc khi step trong pipeline fail.

## Contents
- [Step 1 errors (pre-check)](#step-1-errors-pre-check)
- [Step 2 errors (Lark Platform)](#step-2-errors-lark-platform)
- [Step 3 errors (.env)](#step-3-errors-env)
- [Step 4 errors (.mcp.json)](#step-4-errors-mcpjson)
- [Step 5 errors (OAuth login)](#step-5-errors-oauth-login)
- [Step 6 errors (smoke test)](#step-6-errors-smoke-test)
- [Runtime errors (sau setup)](#runtime-errors-sau-setup)

---

## Step 1 errors (pre-check)

### "node: command not found"

**Cause**: Node.js chưa cài hoặc không trong PATH.
**Fix**:
- Download Node.js 20 LTS tại https://nodejs.org → install với option "Add to PATH" tick
- Hoặc dùng nvm: `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash` rồi `nvm install 20`

### "npx: command not found"

**Cause**: Node.js cài cũ không có npx. npx ship với npm ≥5.2.
**Fix**: Upgrade Node.js lên 18+ (npx included).

### `npx -y @larksuiteoapi/lark-mcp` chậm hoặc timeout

**Cause**: Package ~50MB, network slow lần đầu download.
**Fix**: Tăng timeout npm:
```bash
npm config set fetch-retry-maxtimeout 60000
npm config set fetch-timeout 60000
```
Hoặc cài global 1 lần (lần sau npx dùng cache):
```bash
npm install -g @larksuiteoapi/lark-mcp
```

---

## Step 2 errors (Lark Platform)

### Không thấy "Create Custom App"

**Cause**: Account login vào sai region (Feishu vs Lark Suite).
**Fix**: Logout, vào đúng domain (https://open.larksuite.com cho Lark Suite VN).

### "Permission denied" khi enable scope

**Cause**: Account là member của workspace, không phải admin.
**Fix**:
- Custom App: bạn là creator → tự enable scope được (không cần admin workspace)
- Nếu vẫn fail → check email account dùng Lark Suite cá nhân, KHÔNG phải email workspace company.

### "App ID không hiện" sau khi tạo

**Cause**: Đang ở wrong tab.
**Fix**: Click app vừa tạo → menu trái → "Credentials & Basic Info".

---

## Step 3 errors (.env)

### "LARK_APP_ID format invalid"

**Cause**: Paste nhầm hoặc copy thiếu prefix.
**Format đúng**: `cli_` + 16 chars alphanumeric, vd `cli_a1b2c3d4e5f6g7h8`.
**Fix**: Quay lại Console → Credentials → click icon copy bên cạnh App ID.

### "LARK_APP_SECRET too short"

**Cause**: Copy thiếu, hoặc copy nhầm.
**Format đúng**: 40+ chars random alphanumeric.
**Fix**: Console → Credentials → "App Secret" → click eye icon để show → copy.

---

## Step 4 errors (.mcp.json)

### "JSON parse error"

**Cause**: File `.mcp.json` đã tồn tại với syntax sai.
**Fix**: Validate file bằng `python -c "import json; json.load(open('.mcp.json'))"`. Nếu error, fix syntax (thiếu comma, dư bracket).

### "mcpServers entry 'lark-mcp' đã tồn tại"

**Cause**: Skill đã chạy trước đó.
**Fix**: `install.py` sẽ overwrite entry — confirm với user. Nếu user muốn giữ entry cũ, manual edit `.mcp.json`.

### Claude Code không load `.mcp.json` mới

**Cause**: Cần restart Claude Code hoàn toàn (close hết tabs, mở lại).
**Fix**: Quit process Claude Code (Ctrl+Q hoặc Cmd+Q), launch lại.

---

## Step 5 errors (OAuth login)

### "Invalid app credentials"

**Cause 1**: App chưa Release ở Step 2 sub-step 6.
**Fix**: Vào Console → Version Management → Submit for Release → Self-approve.

**Cause 2**: App Secret copy sai.
**Fix**: Console → Credentials → copy lại Secret (click eye icon).

**Cause 3**: Domain mismatch — app tạo trên Feishu nhưng skill default Lark Suite.
**Fix**: Set `LARK_DOMAIN=https://open.feishu.cn` trong `.env` (hoặc ngược lại).

### "redirect_uri mismatch"

**Cause**: Lark-mcp dùng `http://localhost:8080/callback`. App chưa whitelist URL này.
**Fix**: Console → Security Settings → Redirect URLs → add `http://localhost:8080/callback` → Save.

### Browser không tự mở

**Cause**: WSL / remote shell.
**Fix**: Copy URL từ stderr → paste browser host machine.

### "Insufficient scope"

**Cause**: Step 2 sub-step 4 chưa enable đủ scope.
**Fix**: Console → Permissions → enable thiếu scope → Save → re-run Step 5.

### "Port 8080 already in use"

**Cause**: Process khác chiếm port.
**Fix Windows**:
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8080).OwningProcess
Stop-Process -Id <PID>
```
**Fix macOS/Linux**:
```bash
lsof -i :8080
kill <PID>
```

---

## Step 6 errors (smoke test)

### `tools/list` returns empty

**Cause 1**: lark-mcp chưa login.
**Fix**: Re-run Step 5.

**Cause 2**: Scopes enable nhưng chưa approve trong Console.
**Fix**: Console → Permissions → check status mỗi scope = "Approved" (không phải "Pending").

### "Cannot find module '@larksuiteoapi/lark-mcp'"

**Cause**: npm cache hỏng.
**Fix**:
```bash
npm cache clean --force
npx -y @larksuiteoapi/lark-mcp --version
```

### Claude Code không thấy tool Lark sau restart

**Cause 1**: `.mcp.json` syntax error → CC silent skip.
**Fix**: Validate JSON (`python -c "import json; json.load(open('.mcp.json'))"`), fix error.

**Cause 2**: CC chưa restart hoàn toàn — chỉ reload window.
**Fix**: Quit CC process hoàn toàn, launch lại.

**Cause 3**: Path trong `.mcp.json` sai (vd Windows backslash thay vì forward slash).
**Fix**: Use forward slash trong tất cả path, kể cả Windows.

---

## Runtime errors (sau setup)

### Claude báo "tool not found: im.v1.message.create"

**Cause**: Tool name typo, hoặc preset chưa cover.
**Fix**: Hỏi Claude list tools available: "list all Lark tools you have". Verify tool name chính xác.

### Tool call fail 401

**Cause**: Token expired hoặc revoked.
**Fix**: Re-run Step 5 (OAuth login). lark-mcp tự refresh token nội bộ, nhưng nếu user revoke app trong Lark account settings → cần re-auth.

### Tool call fail 403

**Cause**: Scope thiếu cho tool đó.
**Fix**: Identify scope cần (đọc lark-mcp docs hoặc thử-sai). Vào Console → Permissions → enable → re-login.

### "Rate limit exceeded"

**Cause**: Quá nhiều API call.
**Fix**: Đợi 1-2 phút. Lark rate limit ~100 req/min default.

---

## Diagnosis nhanh

Khi không biết lỗi gì, chạy:
```bash
python .claude/skills/lark-connect/scripts/smoke_test.py --verbose
```

Output sẽ cho biết:
- `.env` có đủ 3 biến không
- `npx lark-mcp` spawn được không
- Tool list count + sample tool names

Copy output → paste vào Claude Code → Claude map ra fix.
