# Google OAuth Scopes — Giải thích

Scope = quyền truy cập. Skill mặc định request 3 scope. Đọc khi muốn hiểu mỗi cái cho phép gì hoặc thêm scope mới.

## 3 Scope Default

### `https://www.googleapis.com/auth/spreadsheets`

**Cho phép**: Đọc + ghi Google Sheets thuộc account user.

**Use cases**:
- Đọc data từ Sheet (vd: list từ khoá, danh sách bài chưa publish)
- Ghi data vào Sheet (vd: update status "Published", paste URL kết quả)
- Tạo Sheet mới

**KHÔNG cho phép**: Đọc Sheet người khác chia sẻ (cần scope `drive.readonly`).

### `https://www.googleapis.com/auth/drive`

**Cho phép**: Toàn quyền Google Drive — list, đọc, ghi, xoá, share file.

**Use cases**:
- List file trong Drive
- Download file Drive về local
- Upload file lên Drive
- Share file (set permissions)

**Lưu ý**: Đây là scope rộng. Cân nhắc dùng scope hẹp hơn nếu chỉ cần đọc:
- `https://www.googleapis.com/auth/drive.readonly` — chỉ đọc
- `https://www.googleapis.com/auth/drive.file` — chỉ file app tạo ra
- `https://www.googleapis.com/auth/drive.metadata.readonly` — chỉ metadata

### `https://www.googleapis.com/auth/documents`

**Cho phép**: Đọc + ghi Google Docs.

**Use cases**:
- Đọc nội dung Doc (vd: lấy body để paste vào WordPress)
- Tạo Doc mới
- Update Doc (replace text, insert image)

**KHÔNG cho phép**: List Docs trong Drive (cần `drive` scope).

---

## Cách thêm scope

Nếu muốn thêm Gmail, Calendar, hoặc scope khác:

### Step 1: Sửa `scripts/oauth_refresh.py`

```python
SCOPES = " ".join([
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/gmail.readonly",  # MỚI
    "https://www.googleapis.com/auth/calendar",        # MỚI
])
```

### Step 2: Enable API tương ứng ở Cloud Console

- Gmail: enable Gmail API
- Calendar: enable Google Calendar API

### Step 3: Re-run OAuth flow

```bash
python .claude/skills/google-connect/scripts/oauth_refresh.py
```

Google sẽ prompt user re-grant với scopes mới. Sau đó refresh_token mới sẽ có quyền mới.

---

## Common Google API Scopes Reference

| Scope | Purpose |
|---|---|
| `gmail.readonly` | Đọc Gmail |
| `gmail.send` | Gửi email từ Gmail |
| `calendar` | Quản lý Google Calendar |
| `youtube.readonly` | Đọc YouTube data |
| `analytics.readonly` | Đọc Google Analytics |
| `webmasters.readonly` | Đọc Google Search Console |
| `adwords` | Google Ads |
| `cloud-platform` | Toàn bộ Cloud Platform (powerful, dùng cẩn thận) |

Full list: https://developers.google.com/identity/protocols/oauth2/scopes

---

## Security note

Scope càng rộng → token càng quyền lực → rủi ro nếu leak.

**Best practice**:
- Chỉ request scope thực sự dùng
- KHÔNG dùng `cloud-platform` trừ khi build admin tool
- Rotate token định kỳ (delete + re-auth) cho production
- KHÔNG commit `.env` lên git
- Add `.env` vào `.gitignore`

Skill `google-connect` enforce `.env` trong `.gitignore` ở Step 5 — nếu chưa có sẽ tự thêm.

---

## Khi nào dùng OAuth user flow vs Service Account

Skill này dùng **OAuth user flow** — user trực tiếp authorize bằng Google account của họ.

**Đặc điểm**:
- Token gắn với 1 Google account
- User phải mở browser authorize lần đầu
- Refresh token expire ~6 tháng nếu inactive
- Phù hợp: cá nhân, dev local, đào tạo

**Alternative: Service Account**:
- Token gắn với 1 service account (không phải user)
- Không cần browser flow — token JSON sẵn
- Token không expire (rotate manual)
- Phù hợp: production server, automation chạy 24/7

Nếu user cần service account, tạo skill riêng (`google-service-account-setup`). Skill `google-connect` này KHÔNG handle service account.
