# Troubleshooting cài Claude Code

Các lỗi thường gặp và cách xử lý.

## "Command not found: claude"

Sau khi cài Claude Code, gõ `claude` không nhận lệnh.

**Nguyên nhân:** PATH chưa được update sau khi cài.

**Cách xử lý:**
1. Đóng terminal hoàn toàn (không chỉ tab — đóng cả app).
2. Mở terminal lại.
3. Gõ lại `claude`.

Nếu vẫn không được:
- **Windows:** Chạy installer Claude Code lại với quyền Admin (chuột phải PowerShell → Run as Administrator).
- **Mac:** Chạy `source ~/.zshrc` hoặc `source ~/.bash_profile`.

## "Permission denied" khi cài trên Mac

Lỗi quyền truy cập khi chạy `curl ... | bash`.

**Cách xử lý:**
- Đừng dùng `sudo` với installer của Claude Code. Nếu lỡ dùng, quyền user sẽ sai → cài lại bằng user account thường.
- Nếu vẫn lỗi, cài trong folder home: `cd ~ && curl -fsSL https://claude.ai/install.sh | bash`.

## "Git is not recognized" trên Windows

Đã cài Git nhưng PowerShell không nhận.

**Cách xử lý:**
1. Mở Start → gõ "Environment Variables" → Edit the system environment variables.
2. Click "Environment Variables..." ở dưới.
3. Trong **System variables**, tìm `Path` → Edit.
4. Kiểm tra có dòng `C:\Program Files\Git\cmd` chưa. Nếu chưa, Add.
5. OK → đóng PowerShell → mở lại.

## "Python is not recognized" trên Windows

**Nguyên nhân:** Khi cài Python, không tick "Add Python to PATH".

**Cách xử lý:**
- Cách dễ: gỡ Python ra (Settings → Apps), cài lại, **tick "Add Python to PATH"**.
- Cách thủ công: thêm vào PATH như hướng dẫn cho Git ở trên (đường dẫn thường là `C:\Users\<user>\AppData\Local\Programs\Python\Python3xx\`).

## Login bị treo / hết hạn

Claude Code yêu cầu login lại liên tục, hoặc trang đăng nhập không quay về terminal.

**Cách xử lý:**
1. Trong Claude Code, gõ `/login` để bắt đầu lại flow.
2. Nếu vẫn lỗi, xoá session cũ:
   - Windows: `Remove-Item -Recurse $env:USERPROFILE\.claude\credentials.json` (cẩn thận)
   - Mac: `rm ~/.claude/credentials.json`
3. Gõ `claude` lại — yêu cầu login mới từ đầu.

## Claude Code chạy chậm / "thinking" rất lâu

**Nguyên nhân thường gặp:**
1. Đang dùng Opus với effort xhigh trên task đơn giản.
2. Context quá dài (hơn 100k tokens).

**Cách xử lý:**
- Gõ `/model` → đổi sang Sonnet hoặc Haiku với effort medium/high.
- Gõ `/compact` để nén context.
- Gõ `/clear` để bắt đầu cuộc trò chuyện mới (mất context cũ).

## "Rate limit" / "You've reached your usage limit"

Đã dùng hết quota cho khoảng thời gian.

**Cách xử lý:**
- Đợi reset (thường vài giờ).
- Nâng cấp plan (Pro → Max).
- Đổi tạm sang model rẻ hơn (`/model` → Haiku).
- Gõ `/usage` để xem chi tiết quota còn lại.

## Tag file bằng `@` không hoạt động

**Nguyên nhân:** File không nằm trong folder hiện tại của Claude Code.

**Cách xử lý:**
- Kiểm tra Claude Code đang ở folder nào (xem dòng đầu của Welcome screen).
- Hoặc gõ `! pwd` (Mac) / `! cd` (Windows) để xem thư mục hiện tại.
- Nếu sai, thoát Claude Code (`Ctrl+D` hoặc `exit`), `cd` vào folder đúng, mở lại `claude`.

## VS Code không thấy Claude Code

Bạn dùng VS Code mà không thấy CC trong terminal panel.

**Cách xử lý:**
- Trong VS Code, mở terminal: View → Terminal (`` Ctrl+` ``).
- Trong terminal đó, gõ `claude`.
- Nếu không nhận lệnh, terminal trong VS Code có thể đang dùng shell khác (Cmd thay vì PowerShell). Đổi bằng cách: click dropdown bên cạnh nút **+** trong terminal → chọn PowerShell.

## Khi tất cả không hoạt động

Hỏi Claude Code chính nó (nếu chạy được dù 1 chút):
```
Tôi bị lỗi <mô tả lỗi>. Hãy đoán nguyên nhân và hướng dẫn fix.
```

Hoặc liên hệ trợ giảng SEONGON.
