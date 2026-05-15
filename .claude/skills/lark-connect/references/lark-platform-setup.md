# Lark Developer Console Setup — Walkthrough chi tiết

Đây là phần học viên struggle nhiều nhất. Đọc kỹ, làm theo từng step. Tổng thời gian: ~5-7 phút.

## Contents
- [Bước 1: Login Lark Developer Console](#bước-1-login-lark-developer-console)
- [Bước 2: Create Custom App](#bước-2-create-custom-app)
- [Bước 3: Copy App ID + App Secret](#bước-3-copy-app-id--app-secret)
- [Bước 4: Enable Permissions & Scopes](#bước-4-enable-permissions--scopes)
- [Bước 5: Bot Capability (optional, khuyến nghị)](#bước-5-bot-capability-optional-khuyến-nghị)
- [Bước 6: Release app (Self-approve)](#bước-6-release-app-self-approve)
- [Bước 7: Verify ready](#bước-7-verify-ready)
- [Checklist hoàn thành](#checklist-hoàn-thành)
- [Lark Suite vs Feishu — chọn đúng domain](#lark-suite-vs-feishu--chọn-đúng-domain)

---

## Bước 1: Login Lark Developer Console

1. Mở: https://open.larksuite.com
2. Click **Sign In** (góc trên phải) → login Lark account
3. Sau khi login, click **Developer Console** trên menu

Nếu là tài khoản Feishu (China region): https://open.feishu.cn

**Tại sao bước này**: Developer Console là nơi quản lý mọi Custom App của bạn. Không có app = không có credentials.

---

## Bước 2: Create Custom App

1. Trong Developer Console, click **Create Custom App** (hoặc "Create App")
2. Điền form:
   - **App Name**: `claude-seongon` (hoặc tên gì cũng được, dễ nhớ)
   - **App Description**: "Claude Code integration" (optional)
   - **App Icon**: upload icon hoặc dùng default
3. Click **Create**

Chờ ~5 giây. Bạn sẽ được chuyển vào dashboard của app vừa tạo.

**Tại sao bước này**: Mỗi credential thuộc 1 app. App = container Lark của bạn.

**Lưu ý**: Chọn **Custom App** (cho internal use), KHÔNG phải **Marketplace App** (cho public distribution — phức tạp hơn, cần Lark review).

---

## Bước 3: Copy App ID + App Secret

1. Trong dashboard app, vào tab **Credentials & Basic Info** (menu trái)
2. Bạn sẽ thấy 2 field:
   - **App ID** — dạng `cli_a1b2c3d4e5f6g7h8`
   - **App Secret** — dạng dài 40+ ký tự
3. Copy cả 2 (hoặc click icon "copy" bên cạnh)

Lưu tạm 2 giá trị này — sẽ paste cho skill ở Step 3 pipeline.

**Tại sao bước này**: Skill cần 2 credential này để identify app với Lark API. Không có 2 cái này = lark-mcp không gọi được API.

---

## Bước 4: Enable Permissions & Scopes

Mặc định Custom App có 0 permission. Phải enable scope cho từng nhóm tính năng muốn dùng.

1. Trong dashboard app, vào tab **Permissions & Scopes** (menu trái)
2. Click **Add Permission**
3. Search và enable 7 scope sau (cho use case AI assistant phổ biến):

**Instant Messaging (IM)**:
- `im:message` — gửi/đọc message
- `im:chat` — quản lý chat groups

**Documents**:
- `docx:document` — đọc/ghi Lark Docs
- `sheets:spreadsheet` — đọc/ghi Lark Sheets
- `bitable:app` — đọc/ghi Bitable (Airtable-like)

**Calendar & Task**:
- `calendar:calendar` — quản lý calendar
- `task:task` — quản lý tasks

**Contact** (cần để identify user):
- `contact:user.base:readonly` — đọc basic user info

**OAuth**:
- `offline_access` — refresh token tự động (BẮT BUỘC nếu enable OAuth user mode)

4. Sau khi add đủ, click **Save Changes**

**Tại sao bước này**: Scope = quyền. Thiếu scope = tool call fail 403. Skill default enable 9 scope cho most use cases. Nếu cần thêm (gmail, custom Bitable field), đọc `scopes-and-tools.md`.

**Lưu ý**: Một số scope là "user_access_token only" — nghĩa là chỉ work với OAuth user mode (skill default mode), KHÔNG work với bot-only mode.

---

## Bước 5: Bot Capability (optional, khuyến nghị)

Bật Bot cho phép app gửi message như 1 bot user trong workspace.

1. Trong dashboard app, vào **Features** → **Bot**
2. Click **Enable Bot**
3. Configure:
   - **Bot Name**: tên hiển thị trong message (vd: "Claude Assistant")
   - **Bot Description**: optional
4. **Add to Groups** — chọn group muốn bot tham gia (cần thiết để gửi message vào group đó)
5. Save

**Tại sao bước này**: Nếu skip, vẫn dùng được lark-mcp với user_access_token (Claude act như user). Nhưng có Bot capability cho phép gửi message với danh nghĩa bot — chuyên nghiệp hơn cho automation.

---

## Bước 6: Release app (Self-approve)

QUAN TRỌNG — bỏ bước này sẽ bị lỗi "App pending review" khi OAuth.

1. Trong dashboard app, vào tab **Version Management** (menu trái)
2. Click **Create Version** → fill basic info → Save
3. Click **Submit for Release**
4. Vì là Custom App → bạn (creator) tự duyệt được. Click **Approve** trên dialog hiện ra.

Status app chuyển từ "In Development" → "Released". Lark API mới chấp nhận credentials.

**Tại sao bước này**: Custom App ở Development mode chỉ test được bởi creator. Phải Release để API endpoints chấp nhận App ID/Secret.

---

## Bước 7: Verify ready

Quick check trước khi quay lại skill:

1. Tab **Credentials**: App ID + Secret hiện rõ
2. Tab **Permissions & Scopes**: ≥7 scope enabled, status "Approved"
3. Tab **Version Management**: status "Released"
4. (Optional) Tab **Bot**: enabled

Có đủ 3 check đầu → paste credentials cho skill ở pipeline Step 3.

---

## Checklist hoàn thành

- [ ] App đã tạo trong Developer Console
- [ ] App ID copy được (dạng `cli_xxxx`)
- [ ] App Secret copy được (40+ chars)
- [ ] 7+ scope enabled
- [ ] Version Released (self-approved)
- [ ] (Optional) Bot capability enabled + added to test group

---

## Lark Suite vs Feishu — chọn đúng domain

Đây là 2 phiên bản khác nhau cùng platform:

| | Lark Suite | Feishu |
|---|---|---|
| Domain | `open.larksuite.com` | `open.feishu.cn` |
| Region | Global (gồm Vietnam) | China only |
| Data residency | Singapore | Mainland China |
| UI language | English/multi | Chinese-first |

**User Vietnam dùng Lark Suite** (domain `open.larksuite.com`). Default trong skill.

Nếu user đã có Feishu account (vd làm việc với team China), set `LARK_DOMAIN=https://open.feishu.cn` trong `.env`. App tạo bên nào, dùng domain bên đó — KHÔNG cross-platform.

---

## Câu hỏi thường gặp

**Q: Tạo Custom App có tốn phí không?**
A: Không. Custom App miễn phí, không giới hạn số app per account.

**Q: 1 Lark account tạo được bao nhiêu app?**
A: Không giới hạn cứng. Practical 5-10 app per account là bình thường.

**Q: Phải có Lark Enterprise/Workspace không?**
A: Không. Lark cá nhân (free tier) tạo Custom App được.

**Q: Đào tạo 30 học viên thì sao?**
A: Mỗi học viên tự tạo Custom App riêng (~7 phút mỗi người). KHÔNG share App ID/Secret — mỗi credential gắn 1 tenant.

**Q: Có thể submit app lên Lark Marketplace không?**
A: Có nhưng phức tạp — cần Lark review, app phải có business logic rõ ràng. Cho use case nội bộ SEONGON, Custom App + self-approve là đủ.
