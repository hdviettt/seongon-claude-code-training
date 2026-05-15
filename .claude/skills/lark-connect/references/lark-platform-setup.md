# Lark Developer Console Setup — Walkthrough chi tiết (Tenant Mode)

Đây là phần học viên struggle nhiều nhất. Đọc kỹ, làm theo từng step. Tổng thời gian: ~5-7 phút.

Skill `lark-connect` chỉ support **tenant mode (bot)** — đơn giản hơn user OAuth mode. KHÔNG cần OAuth consent screen, redirect URLs, hay Bot capability (Bot tuỳ chọn — đọc Bước 5).

## Contents
- [Bước 1: Login Lark Developer Console](#bước-1-login-lark-developer-console)
- [Bước 2: Create Custom App](#bước-2-create-custom-app)
- [Bước 3: Copy App ID + App Secret](#bước-3-copy-app-id--app-secret)
- [Bước 4: Enable Permissions & Scopes](#bước-4-enable-permissions--scopes)
- [Bước 5: Bot Capability (optional nhưng khuyến nghị)](#bước-5-bot-capability-optional-nhưng-khuyến-nghị)
- [Bước 6: Release app (Self-approve)](#bước-6-release-app-self-approve)
- [Checklist hoàn thành](#checklist-hoàn-thành)
- [Lark Suite vs Feishu — chọn đúng domain](#lark-suite-vs-feishu--chọn-đúng-domain)

---

## Bước 1: Login Lark Developer Console

1. Mở: https://open.larksuite.com
2. Click **Sign In** (góc trên phải) → login Lark account
3. Sau khi login, click **Developer Console** trên menu

Nếu tài khoản Feishu (China region): https://open.feishu.cn

**Tại sao bước này**: Developer Console là nơi quản lý mọi Custom App. Không có app = không có credentials.

---

## Bước 2: Create Custom App

1. Developer Console → click **Create Custom App**
2. Form:
   - **App Name**: tên dễ nhớ (vd `claude-seongon`, `tro-ly-seongon`)
   - **App Description**: optional
   - **App Icon**: optional
3. Click **Create**

Chờ ~5 giây. App dashboard mở.

**Tại sao bước này**: Mỗi credential thuộc 1 app. App = container Lark của bạn.

**Lưu ý**: Chọn **Custom App** (internal use), KHÔNG phải **Marketplace App** (public distribution — cần Lark review).

---

## Bước 3: Copy App ID + App Secret

1. App dashboard → tab **Credentials & Basic Info** (menu trái)
2. Copy:
   - **App ID** — format `cli_a1b2c3d4e5f6g7h8` (16 chars sau `cli_`)
   - **App Secret** — 32+ chars random

Lưu tạm 2 giá trị này → paste cho skill ở Step 3 pipeline.

**Tại sao bước này**: Tenant mode chỉ cần App ID + Secret. KHÔNG cần OAuth client config, redirect URLs, hay user consent screen.

---

## Bước 4: Enable Permissions & Scopes

Mặc định Custom App có 0 permission. Phải enable scope.

1. Tab **Permissions & Scopes** (menu trái)
2. Click **Add Permission**
3. Enable 8 scope default (cover most use case):

**Instant Messaging**:
- `im:message` — gửi/đọc message (BẮT BUỘC)
- `im:chat` — quản lý chat groups (BẮT BUỘC để list groups bot là member)

**Documents**:
- `docx:document` — đọc/ghi Lark Docs
- `sheets:spreadsheet` — đọc/ghi Lark Sheets
- `bitable:app` — đọc/ghi Bitable (Airtable-like)

**Calendar & Task**:
- `calendar:calendar` — quản lý calendar
- `task:task` — quản lý tasks

**Contact**:
- `contact:user.base:readonly` — đọc basic user info (cần để identify users trong API responses)

4. Save Changes

**Lưu ý**: Tenant mode bypass `offline_access` scope (chỉ cần cho OAuth user mode).

**Tại sao bước này**: Scope = quyền. Thiếu scope = tool call fail 403. Default 8 scope cover most use cases SEONGON: messaging, Bitable, Docs, Calendar.

---

## Bước 5: Bot Capability (optional nhưng khuyến nghị)

Bot capability cho phép app gửi message như 1 bot user trong workspace.

1. **Features** → **Bot** (menu trái)
2. Click **Enable Bot**
3. Configure:
   - **Bot Name**: tên hiển thị trong chat (vd "Trợ lý SEONGON")
   - **Bot Description**: optional
4. **Add to Groups** — chọn group muốn bot join (cần cho bot gửi/đọc message trong group đó)
5. Save

**Tại sao bước này**: Tenant mode work với hoặc không Bot capability, nhưng có Bot:
- Bot hiển thị trong group members
- User có thể @mention bot
- Skill `im_v1_chat_list` returns groups bot là member

KHÔNG có Bot:
- Vẫn có thể gọi API như Bitable, Docs
- KHÔNG list được chats/groups (vì bot không là member)
- KHÔNG gửi được message trực tiếp vào group

→ Cho use case SEONGON (gửi notification vào group SEO, Bitable automation), bật Bot.

---

## Bước 6: Release app (Self-approve)

QUAN TRỌNG — bỏ bước này sẽ bị lỗi "App pending review" khi authenticate.

1. Tab **Version Management** (menu trái)
2. Click **Create Version** → fill info → Save
3. Click **Submit for Release**
4. Vì Custom App → bạn (creator) tự duyệt được. Click **Approve**.

Status: "In Development" → "Released". Lark API mới chấp nhận credentials.

**Tại sao bước này**: Custom App ở Development mode chỉ test được bởi creator. Phải Release để tenant API endpoints chấp nhận App ID/Secret.

---

## Checklist hoàn thành

- [ ] App đã tạo trong Developer Console
- [ ] App ID copy được (`cli_xxxx`)
- [ ] App Secret copy được (32+ chars)
- [ ] 8 scope enabled, status "Approved"
- [ ] (Khuyến nghị) Bot capability enabled + added to test group
- [ ] Version Released (self-approved)

---

## Lark Suite vs Feishu — chọn đúng domain

| | Lark Suite | Feishu |
|---|---|---|
| Domain | `open.larksuite.com` | `open.feishu.cn` |
| Region | Global (gồm Vietnam) | China only |
| Data residency | Singapore | Mainland China |
| UI language | English/multi | Chinese-first |

**User Vietnam → Lark Suite** (`open.larksuite.com`). Default trong skill.

Nếu user đã có Feishu account (làm việc với team China), set `LARK_DOMAIN=https://open.feishu.cn` trong `.env`. App tạo bên nào, dùng domain bên đó — KHÔNG cross-platform.

---

## Câu hỏi thường gặp

**Q: Tenant mode khác gì user_access_token mode?**
A: Tenant mode = bot acts as ITSELF (app identity). User_access_token mode = bot acts AS user (cần OAuth flow). Skill chỉ support tenant mode vì user mode hiện có bug với Larksuite (error 20029 dù setup chuẩn).

**Q: Bot có thể đọc message của user khác không?**
A: Trong group bot là member — có thể đọc message group (nếu enable `im:message`). KHÔNG đọc được 1-1 chat của user khác.

**Q: Tại sao bot không thấy chat nào sau khi setup?**
A: Bot chỉ list được chat nó là MEMBER. Webhook subscription ≠ membership. Add bot vào group qua Settings → Add Members hoặc Bước 5 sub-step 4 (Add to Groups).

**Q: Tạo Custom App có tốn phí không?**
A: Không. Custom App miễn phí, không giới hạn số app per account.

**Q: 1 Lark account tạo được bao nhiêu app?**
A: Không giới hạn cứng. Practical 5-10 app per account là bình thường.

**Q: Đào tạo 30 học viên thì sao?**
A: Mỗi học viên tự tạo Custom App riêng (~5-7 phút mỗi người). KHÔNG share App ID/Secret — mỗi credential gắn 1 tenant.

**Q: Có cần verify domain không?**
A: KHÔNG cho Custom App. Tenant mode bypass verify domain.

**Q: Có thể publish app lên Marketplace không?**
A: Có nhưng phức tạp — cần Lark review. Cho use case nội bộ SEONGON, Custom App + self-approve là đủ.
