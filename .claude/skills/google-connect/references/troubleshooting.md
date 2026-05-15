# Troubleshooting — Google OAuth setup

10+ common errors và fix. Đọc khi step nào trong pipeline fail.

## Contents
- [Step 1 errors (pre-check)](#step-1-errors-pre-check)
- [Step 2 errors (Cloud Console)](#step-2-errors-cloud-console)
- [Step 3 errors (.env)](#step-3-errors-env)
- [Step 4 errors (OAuth flow)](#step-4-errors-oauth-flow)
- [Step 5 errors (install hook)](#step-5-errors-install-hook)
- [Step 6 errors (smoke test)](#step-6-errors-smoke-test)
- [Runtime errors (sau khi setup xong)](#runtime-errors-sau-khi-setup-xong)

---

## Step 1 errors (pre-check)

### "python: command not found"

**Cause**: Python chưa cài hoặc không trong PATH.
**Fix**:
- Windows: download Python 3.12+ tại https://python.org → install với option "Add to PATH" tick
- macOS: `brew install python@3.12`
- Linux: `sudo apt install python3 python3-pip`

### "ModuleNotFoundError: No module named 'google'"

**Cause**: Packages chưa cài.
**Fix**:
```bash
python -m pip install google-auth google-auth-oauthlib google-api-python-client
```

Nếu fail vì permission: thêm `--user`:
```bash
python -m pip install --user google-auth google-auth-oauthlib google-api-python-client
```

---

## Step 2 errors (Cloud Console)

### Không thấy nút "ENABLE" cho API

**Cause**: Project chưa select đúng.
**Fix**: Trên top bar Cloud Console, click dropdown project → chọn project mới tạo.

### "You do not have permission" khi tạo OAuth consent screen

**Cause**: Đang dùng Google Workspace account của công ty có policy restriction.
**Fix**: Dùng Gmail cá nhân (`@gmail.com`) thay vì Workspace email.

---

## Step 3 errors (.env)

### "GOOGLE_CLIENT_ID format invalid"

**Cause**: Paste nhầm string, hoặc copy thiếu/dư ký tự.
**Format đúng**:
```
GOOGLE_CLIENT_ID=123456789012-abcdefghijklmnop.apps.googleusercontent.com
```
Phải match pattern `^\d+-[\w]+\.apps\.googleusercontent\.com$`.

**Fix**: Quay lại Cloud Console → Credentials → click OAuth Client → copy lại Client ID.

### "GOOGLE_CLIENT_SECRET format invalid"

**Cause**: Trailing space, hoặc copy nhầm.
**Format đúng**:
```
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghij_klmnopqrstu
```
Phải bắt đầu `GOCSPX-`.

**Fix**: Copy lại từ Cloud Console (click eye icon để show secret).

### ".env file write permission denied"

**Cause**: Folder readonly.
**Fix**: `chmod u+w .` (macOS/Linux) hoặc check folder properties (Windows).

---

## Step 4 errors (OAuth flow)

### "Access blocked: This app's request is invalid"

**Cause**: Email user đang login KHÔNG ở Test users list của OAuth consent screen.
**Fix**:
1. Vào https://console.cloud.google.com/apis/credentials/consent
2. Scroll Test users → ADD USERS → add email user đang dùng
3. SAVE → quay lại run lại Step 4

### "redirect_uri_mismatch"

**Cause**: OAuth Client ID không phải type "Desktop app".
**Fix**:
1. Vào https://console.cloud.google.com/apis/credentials
2. Delete OAuth client cũ
3. Create new → type **Desktop app** (KHÔNG phải Web app)

### "Port 8080 already in use"

**Cause**: Process khác đang chiếm port.
**Fix Windows**:
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8080).OwningProcess
# Identify process → kill nếu safe:
Stop-Process -Id <PID>
```
**Fix macOS/Linux**:
```bash
lsof -i :8080
kill <PID>
```

Hoặc đổi port trong `scripts/oauth_refresh.py`:
```python
PORT = 8090  # đổi 8080 → 8090
```

### Browser không tự mở

**Cause**: Windows Subsystem for Linux (WSL) hoặc remote shell không có browser.
**Fix**: Copy URL skill in ra stderr, paste manual vào browser của host machine.

### "invalid_grant" ngay sau khi authorize

**Cause**: Authorization code đã được dùng (skill chạy 2 lần liên tiếp).
**Fix**: Đợi 30 giây, chạy lại `oauth_refresh.py` từ đầu.

### "Khong nhan duoc refresh_token"

**Cause**: User đã authorize app này trước đó — Google không gửi refresh_token lần 2.
**Fix**:
1. Vào https://myaccount.google.com/permissions
2. Tìm app name (vd "claude-seongon-local") → REMOVE ACCESS
3. Chạy lại Step 4 — Google sẽ prompt lại + cấp refresh_token mới

---

## Step 5 errors (install hook)

### "settings.local.json not found"

**Cause**: Project chưa từng config hook nào.
**Fix**: `install.py` sẽ tự tạo file. Nếu fail, tạo manual:
```bash
mkdir -p .claude
echo '{"hooks":{},"permissions":{"allow":[]}}' > .claude/settings.local.json
```

### "PostToolUse hook đã có entry khác"

**Cause**: Project đã có hook khác (vd validation hook).
**Fix**: `install.py` phải MERGE, không overwrite. Nếu install.py không handle đúng, manual edit `.claude/settings.local.json` thêm:
```json
{
  "matcher": "Bash",
  "hooks": [{"type": "command", "command": "python .claude/hooks/google_token_refresh.py"}]
}
```
Vào array `hooks.PostToolUse`.

---

## Step 6 errors (smoke test)

### "401 UNAUTHENTICATED"

**Cause 1**: GOOGLE_REFRESH_TOKEN sai/expired.
**Fix**: Quay lại Step 4 chạy lại OAuth flow.

**Cause 2**: Scopes không đủ.
**Fix**: Vào Cloud Console → OAuth consent screen → Scopes → thêm 3 scopes:
- `https://www.googleapis.com/auth/spreadsheets`
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/documents`

Sau đó re-run Step 4 (user phải re-grant).

### "403 PERMISSION_DENIED"

**Cause**: API chưa enable.
**Fix**: Vào Cloud Console → APIs Library → enable API tương ứng (Sheets/Drive/Docs).

### "Request had insufficient authentication scopes"

**Cause**: Refresh token được cấp với scope cũ, code đang gọi API cần scope mới.
**Fix**: Như "401 cause 2" — thêm scope + re-run OAuth.

### Google Ads API: `DEVELOPER_TOKEN_NOT_APPROVED`

**Full error**: `"The developer token is only approved for use with test accounts. To access non-test accounts, apply for Basic Access."`

**Cause**: Developer token đang ở **Test Access** level (mặc định mới apply). Test tokens chỉ work với test Ads accounts, KHÔNG access production accounts.

**Gotcha**: `listAccessibleCustomers` WORK với Test token (return IDs OK), nhưng query data của chúng FAIL với error này. Đây là discovery vs data distinction — test enough cho enumeration, không đủ data work.

**Fix**:
1. Vào MCC → Admin → API Center → trang token
2. Click **"Apply for Basic Access"**
3. Fill form (use case, expected traffic)
4. Google review 1-2 business days → email confirm
5. Token tự upgrade → call API lại work

Xem chi tiết: `references/scopes-explained.md` mục "Developer-token — 3 access levels".

---

## Runtime errors (sau khi setup xong)

Lỗi gặp khi đang dùng skill khác (vd `/wp-publish`) gọi Google API.

### "invalid_grant" hoặc "Token has been expired"

**Cause**: Refresh token expire (~6 tháng inactive, hoặc revoked manual).
**Auto-fix**: Hook PostToolUse sẽ detect + tự refresh. User chỉ cần:
1. Đợi browser mở (hook tự mở)
2. Re-authorize Google account
3. Browser hiện "OK — anh quay lai terminal"
4. Quay lại Claude Code, retry lệnh Bash trước đó

Nếu hook không trigger (đã uninstall, settings.local.json bị edit), chạy manual:
```bash
python .claude/skills/lib/oauth_refresh.py
```

### "Quota exceeded" hoặc "Rate limit"

**Cause**: Gọi API quá nhanh.
**Fix**: Đợi 1-2 phút retry. Nếu lặp lại nhiều, check quota tại https://console.cloud.google.com/apis/api/sheets.googleapis.com/quotas.

### Hook chạy nhưng vẫn fail

**Cause**: Hook đã refresh được token mới nhưng Claude chưa retry, hoặc retry vẫn dùng cache cũ.
**Fix**: Đóng phiên CC, mở phiên mới — script sẽ load lại `.env` với token mới.

---

## Diagnosis nhanh

Khi không biết lỗi gì, chạy `smoke_test.py` với verbose:

```bash
python .claude/skills/google-connect/scripts/smoke_test.py --verbose
```

Output sẽ cho biết:
- `.env` có đủ 3 biến không
- Refresh access token success / fail (cause nào)
- API call success / fail (HTTP code)

Copy output đầy đủ → paste vào Claude Code → Claude sẽ map ra fix cụ thể.
