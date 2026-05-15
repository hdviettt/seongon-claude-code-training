# Troubleshooting — Lark MCP setup (Tenant Mode)

10+ common errors per step. Đọc khi step trong pipeline fail.

## Contents
- [Step 1 errors (pre-check)](#step-1-errors-pre-check)
- [Step 2 errors (Lark Platform)](#step-2-errors-lark-platform)
- [Step 3 errors (.env + app identity)](#step-3-errors-env--app-identity)
- [Step 4 errors (.mcp.json)](#step-4-errors-mcpjson)
- [Step 5 errors (restart + smoke test)](#step-5-errors-restart--smoke-test)
- [Runtime errors (sau setup)](#runtime-errors-sau-setup)
- [Diagnosis nhanh](#diagnosis-nhanh)

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
Hoặc cài global 1 lần:
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
- Nếu vẫn fail → email account đang dùng có thể là Lark workspace company, switch sang email cá nhân.

### "App ID không hiện" sau khi tạo

**Cause**: Đang ở wrong tab.
**Fix**: Click app vừa tạo → menu trái → "Credentials & Basic Info".

---

## Step 3 errors (.env + app identity)

### "LARK_APP_ID format invalid"

**Cause**: Paste nhầm hoặc copy thiếu prefix.
**Format đúng**: `cli_` + 16 chars alphanumeric, vd `cli_a7e3876125b95010`.
**Fix**: Console → Credentials → click icon copy bên cạnh App ID.

### "LARK_APP_SECRET too short"

**Cause**: Copy thiếu hoặc nhầm.
**Format đúng**: 32+ chars random alphanumeric.
**Fix**: Console → Credentials → "App Secret" → click eye icon để show → copy.

### "App identity verify fail" (app name không match expectation)

**Cause**: Anh paste credentials của app khác trong account.
**Fix**:
1. Console → list apps → click đúng app
2. Re-copy App ID + Secret
3. Update `.env`

**Lưu ý về i18n**: API trả `app_name` theo primary language (English). UI Console hiển thị theo language setting (vd Vietnamese). Cùng app, khác name hiển thị — verify bằng App ID match là chính xác.

---

## Step 4 errors (.mcp.json)

### "JSON parse error"

**Cause**: `.mcp.json` tồn tại với syntax sai.
**Fix**:
```bash
python -c "import json; json.load(open('.mcp.json'))"
```
Nếu error → fix syntax (thiếu comma, dư bracket, smart quotes).

### "mcpServers entry 'lark-mcp' đã tồn tại"

**Cause**: Skill chạy trước đó hoặc user manual add.
**Fix**: `install.py` MERGE — nếu entry khác value, overwrite. Nếu user muốn giữ entry cũ, manual edit `.mcp.json`.

### Claude Code không load `.mcp.json`

**Cause**: Path sai (relative vs absolute) hoặc syntax error silent skip.
**Fix**:
- Validate JSON parse OK
- Verify `.mcp.json` ở project root (cùng cấp `.claude/`)
- Use forward slash trong path (kể cả Windows)

---

## Step 5 errors (restart + smoke test)

### Smoke test stuck / timeout 90s

**Cause**: npx tải lark-mcp lần đầu (~50MB).
**Fix**: Đợi thêm. Lần sau dùng npm cache, nhanh hơn nhiều.

### `tools/list` returns empty

**Cause 1**: App chưa Released.
**Fix**: Console → Version Management → Submit for Release → Self-approve.

**Cause 2**: Scopes enable nhưng chưa approve trong Console.
**Fix**: Console → Permissions → check status mỗi scope = "Approved" (không phải "Pending"). Save Changes nếu cần.

### "Cannot find module '@larksuiteoapi/lark-mcp'"

**Cause**: npm cache hỏng.
**Fix**:
```bash
npm cache clean --force
npx -y @larksuiteoapi/lark-mcp --version
```

### Claude Code không thấy tool Lark sau restart

**Cause 1**: Chưa QUIT process hoàn toàn — chỉ close window hoặc reload.
**Fix**: 
- Mac: Cmd+Q hoàn toàn → mở lại
- Windows: Ctrl+Q hoặc Task Manager kill Claude Code → mở lại
- KHÔNG `/restart` hoặc reload window

**Cause 2**: `.mcp.json` syntax error → CC silent skip.
**Fix**: Validate JSON (`python -c "import json; json.load(open('.mcp.json'))"`).

**Cause 3**: Path trong `.mcp.json` sai (Windows backslash).
**Fix**: Use forward slash mọi path.

### Smoke test PASS nhưng Claude không gọi được tool

**Cause**: Claude session chưa load MCP (CC chưa restart đúng).
**Fix**: Quit Claude Code hoàn toàn → mở lại session mới.

---

## Runtime errors (sau setup)

### Claude báo "tool not found: im_v1_chat_list"

**Cause**: Tool name typo (lark-mcp dùng underscore `_` không phải dot `.`).
**Fix**: Hỏi Claude list tools: "list all Lark tools available". Verify tên đúng.

### Tool call fail 401 "invalid_token"

**Cause**: App credentials sai hoặc App chưa Released.
**Fix**:
- Verify `.env` LARK_APP_ID + SECRET đúng
- Console → Version Management status = "Released"

### Tool call fail 403 "FORBIDDEN_SCOPE"

**Cause**: Scope thiếu cho tool đó.
**Fix**:
1. Đọc error message — Lark thường nói rõ scope nào cần
2. Console → Permissions → Add Permission → enable scope
3. Save Changes
4. Restart Claude Code (tools metadata cache)

### "Bot không có quyền truy cập chat này"

**Cause**: Bot không là member của chat.
**Fix**: Trong chat đó → Settings → Add Members → search bot name → Add.

### "Rate limit exceeded"

**Cause**: Quá nhiều API call.
**Fix**: Đợi 1-2 phút. Lark rate limit ~100 req/min default.

---

## Diagnosis nhanh

Khi không biết lỗi gì, chạy:
```bash
python .claude/skills/lark-connect/scripts/smoke_test.py --verbose
```

Output cho biết:
- `.env` có đủ 3 biến không
- `npx lark-mcp` spawn được không
- Tool list count + sample tool names
- Stderr last 500 chars (catch error message)

Copy output → paste vào Claude Code → Claude map ra fix.

Verify app identity manual:
```bash
TOKEN=$(curl -s -X POST 'https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d '{"app_id":"<APP_ID>","app_secret":"<SECRET>"}' | python -c "import json,sys; print(json.load(sys.stdin).get('tenant_access_token',''))")

curl -s "https://open.larksuite.com/open-apis/application/v6/applications/<APP_ID>?lang=en_us" \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
```

Output gồm `app_name`, `description` — verify đúng app.
