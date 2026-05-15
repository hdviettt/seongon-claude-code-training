# Google Cloud Console Setup — Walkthrough chi tiết

Đây là phần KHÓ NHẤT cho non-tech. Đọc kỹ, làm theo từng step. Tổng thời gian: ~5-7 phút.

## Contents
- [Step 1: Tạo Google Cloud project](#step-1-tạo-google-cloud-project)
- [Step 2: Enable 3 APIs cần thiết](#step-2-enable-3-apis-cần-thiết)
- [Step 3: Tạo OAuth consent screen](#step-3-tạo-oauth-consent-screen)
- [Step 4: Add Test User](#step-4-add-test-user)
- [Step 5: Tạo OAuth Client ID](#step-5-tạo-oauth-client-id)
- [Step 6: Lấy CLIENT_ID + CLIENT_SECRET](#step-6-lấy-client_id--client_secret)
- [Checklist hoàn thành](#checklist-hoàn-thành)

---

## Step 1: Tạo Google Cloud project

1. Mở: https://console.cloud.google.com/projectcreate
2. **Project name**: gõ `claude-seongon` (hoặc tên gì cũng được, ngắn)
3. **Location**: để mặc định "No organization"
4. Click **CREATE**

Chờ ~10 giây project tạo xong. Phía trên cùng sẽ có dropdown chọn project — đảm bảo đang chọn project vừa tạo.

**Tại sao bước này**: Mỗi OAuth credential phải thuộc 1 project. Project = container Google Cloud của bạn.

---

## Step 2: Enable 3 APIs cần thiết

Mặc định project chưa "biết" về Sheets/Drive/Docs. Phải enable từng API.

1. Mở: https://console.cloud.google.com/apis/library
2. Đảm bảo trên cùng đang chọn đúng project `claude-seongon`
3. Search **"Google Sheets API"** → click → **ENABLE**
4. Lặp lại với:
   - **Google Drive API**
   - **Google Docs API**

Mỗi API mất ~5 giây enable. Tổng 3 APIs ~30 giây.

**Tại sao bước này**: Skill cần quyền đọc/ghi cả 3 dịch vụ. Thiếu API nào → lỗi 403 khi gọi.

---

## Step 3: Tạo OAuth consent screen

Đây là màn hình Google hiện cho user khi authorize.

1. Mở: https://console.cloud.google.com/apis/credentials/consent
2. **User Type**: chọn **External** → CREATE
3. App information:
   - **App name**: `claude-seongon-local` (hoặc gì cũng được)
   - **User support email**: chọn email Gmail của bạn
   - **Developer contact**: gõ email Gmail của bạn (cùng email)
4. Click **SAVE AND CONTINUE**
5. **Scopes**: bỏ qua, click **SAVE AND CONTINUE**
6. **Test users**: sẽ làm ở Step 4 — tạm click **SAVE AND CONTINUE**
7. **Summary**: click **BACK TO DASHBOARD**

App giờ ở "Testing" mode. Đây là OK — bạn dùng cho bản thân, không cần publish.

**Tại sao bước này**: Google require mọi OAuth app phải có consent screen. App ở "Testing" mode chỉ cho phép test users (bạn) authorize — không public.

---

## Step 4: Add Test User

CRITICAL — bỏ bước này sẽ bị lỗi "Access blocked: This app's request is invalid".

1. Vẫn ở trang OAuth consent screen
2. Scroll xuống section **Test users**
3. Click **ADD USERS**
4. Gõ email Gmail của bạn (cùng email sẽ login OAuth)
5. Click **SAVE**

Có thể add tối đa 100 test users (vd: nếu đào tạo, add email học viên vào).

**Tại sao bước này**: App ở Testing mode chỉ cho phép emails trong Test users list authorize. Email không có trong list → bị block.

---

## Step 5: Tạo OAuth Client ID

Đây là credential thực sự để dùng.

1. Mở: https://console.cloud.google.com/apis/credentials
2. Click **+ CREATE CREDENTIALS** (góc trên) → **OAuth client ID**
3. **Application type**: chọn **Desktop app**
4. **Name**: gõ `claude-code-cli` (hoặc gì cũng được)
5. Click **CREATE**

Popup hiện ra với:
- **Client ID** — copy dòng dạng `123456-abc...apps.googleusercontent.com`
- **Client secret** — copy dòng dạng `GOCSPX-...`

Hoặc click **DOWNLOAD JSON** → mở file → lấy 2 field `client_id` và `client_secret`.

**Tại sao bước này**: Skill cần 2 credential này để identify app khi gọi OAuth flow. Không có 2 cái này = Google không biết app bạn là ai.

---

## Step 6: Lấy CLIENT_ID + CLIENT_SECRET

Sau khi click **CREATE** ở Step 5, có 2 cách lấy:

**Cách 1 — Popup hiện ra ngay**:
- Copy "Client ID" → đây là `GOOGLE_CLIENT_ID`
- Copy "Client secret" → đây là `GOOGLE_CLIENT_SECRET`
- Click **OK**

**Cách 2 — Nếu lỡ đóng popup**:
1. Vẫn ở trang Credentials: https://console.cloud.google.com/apis/credentials
2. Section "OAuth 2.0 Client IDs" → click vào name client vừa tạo (vd "claude-code-cli")
3. Phía trên: "Client ID" hiện rõ — copy
4. Phía dưới: "Client secret" — click eye icon để show, copy

Hoặc click **DOWNLOAD JSON** ở góc phải → file `client_secret_XXX.json` chứa cả 2.

---

## Checklist hoàn thành

Trước khi quay lại skill, verify:

- [ ] Project đã tạo + đang được select ở Cloud Console
- [ ] 3 APIs enabled: Sheets, Drive, Docs
- [ ] OAuth consent screen đã configure (Testing mode OK)
- [ ] Email của bạn đã add vào Test users
- [ ] OAuth Client ID tạo type **Desktop app**
- [ ] Đã copy CLIENT_ID và CLIENT_SECRET vào clipboard hoặc note

Có đủ 6 check → paste credentials cho skill ở Step 3.

---

## Câu hỏi thường gặp

**Q: Project tạo có tốn phí không?**
A: Không. Google Cloud free tier rất rộng. OAuth flow + Sheets/Drive/Docs API đều free (chỉ tốn phí nếu gọi >100k requests/day, không thực tế cho user cá nhân).

**Q: Có cần verify domain không?**
A: Không. App ở "Testing" mode skip toàn bộ verification.

**Q: Có thể publish app để mọi người dùng được không?**
A: Có, nhưng phức tạp — cần verify domain, đôi khi cần Google review. Cho use case nội bộ SEONGON, giữ Testing mode + add emails học viên vào Test users là đủ.

**Q: Mỗi học viên cần tự tạo Project riêng?**
A: Có. Mỗi credential thuộc 1 Google account. Học viên A không thể dùng credential của học viên B. Đây là design Google để bảo mật.

**Q: Đào tạo cho 30 học viên thì sao?**
A: Mỗi học viên tự làm 6 step trên (mất ~5-7 phút). Hoặc setup chung 1 SEONGON Google Cloud project + add 30 email vào Test users + share CLIENT_ID/SECRET. Cách 2 nhanh hơn nhưng kém isolated.
