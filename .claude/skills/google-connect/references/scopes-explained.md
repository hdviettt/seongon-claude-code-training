# Google OAuth Scopes — Giải thích

Scope = quyền truy cập. Skill mặc định request 3 scope. Đọc khi muốn hiểu mỗi cái cho phép gì hoặc thêm scope mới.

## Contents
- [3 Scope Default](#3-scope-default)
- [Cách thêm scope](#cách-thêm-scope)
- [Common Google API Scopes Reference](#common-google-api-scopes-reference)
- [Lưu ý: 1 số Google API cần credentials BỔ SUNG ngoài OAuth scope](#lưu-ý-1-số-google-api-cần-credentials-bổ-sung-ngoài-oauth-scope)
- [Security note](#security-note)
- [Khi nào dùng OAuth user flow vs Service Account](#khi-nào-dùng-oauth-user-flow-vs-service-account)

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

## Lưu ý: 1 số Google API cần credentials BỔ SUNG ngoài OAuth scope

Mỗi Google API có yêu cầu khác nhau. OAuth scope ĐỦ cho phần lớn API (Sheets/Drive/Docs/GSC/Calendar/Gmail/Analytics). Nhưng vài API marketing-focused cần thêm credentials/setup:

| API | OAuth scope | Extra requirement | Tại sao |
|---|---|---|---|
| Google Sheets | `spreadsheets` | — | Đủ |
| Google Drive | `drive` | — | Đủ |
| Google Docs | `documents` | — | Đủ |
| Search Console | `webmasters.readonly` | User phải là verified owner/user của site | GSC enforce ownership |
| Google Analytics | `analytics.readonly` | — | Đủ (cần GA4 property access) |
| Gmail | `gmail.readonly` | — | Đủ |
| Calendar | `calendar` | — | Đủ |
| **Google Ads** | `adwords` | **`developer-token` từ MCC** + login-customer-id header | Anti-abuse, Google review token |
| **DV360 (Display & Video)** | `display-video` | Allowlist by Google cho production | Limited GA |
| **YouTube Data v3** | `youtube.readonly` | — | Đủ (rate-limited free tier) |
| **YouTube Content ID** | `youtubepartner` | Content ID partnership | Music labels only |
| **Campaign Manager 360** | `dfatrafficking` | CM360 user account active | Enterprise |
| **Search Ads 360** | `doubleclicksearch` | SA360 Manager access | Enterprise |
| **Google My Business** | `business.manage` | API allowlist (deprecated → Business Profile API) | Replaced |

**Pattern chung**: API càng "enterprise/abuse-sensitive" càng cần extra credentials beyond OAuth. Marketing APIs (Ads/DV360/SA360/CM360) Google review tay từng app.

### Google Ads — cách lấy developer-token

1. Phải có **Manager account (MCC)** — không phải individual Ads account. Tạo free tại https://ads.google.com/home/tools/manager-accounts/
2. Login MCC → **Admin** (top-right wrench icon) → **SETUP** → **API Center**
3. Apply form → Google review 1-3 ngày → status "Test" (free tier, 15k ops/day) hoặc "Standard" (production)
4. Copy token → `.env`:
   ```env
   GOOGLE_ADS_DEVELOPER_TOKEN=xxx
   GOOGLE_ADS_LOGIN_CUSTOMER_ID=1234567890  # MCC customer ID, no dashes
   ```
5. Khi call API, send header `developer-token` + (optional) `login-customer-id`

### GSC — site ownership requirement

OAuth scope `webmasters.readonly` cho phép gọi API, nhưng user CHỈ list được sites đã được add làm owner/user.

Để add user vào property:
1. https://search.google.com/search-console
2. Chọn property → Settings (gear icon) → Users and permissions
3. Add user → email cần grant → role (Restricted / Full)
4. User mới có thể OAuth + list property này

Nếu OAuth account chưa được add vào property nào → `sites.list()` return empty (KHÔNG fail).

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
