# Cài Claude Code trên Windows

5 bước, theo thứ tự. Đừng skip bước nào.

## 1. Tạo tài khoản Claude / Anthropic

Truy cập https://claude.ai và đăng ký bằng email (Google sign-in nhanh nhất).

Để dùng Claude Code dài hạn, bạn cần subscription **Claude Pro** ($20/tháng) hoặc **Claude Max** ($100-200/tháng). Free plan dùng được nhưng giới hạn rất nhanh.

## 2. Cài Git

Git là công cụ quản lý phiên bản — dù bạn không code, Claude Code sẽ dùng Git để track thay đổi.

1. Tải Git từ: https://git-scm.com/download/win
2. Chạy installer, **next next next** với option mặc định.
3. Mở **PowerShell** (Start → gõ "powershell" → Enter), kiểm tra:
   ```powershell
   git --version
   ```
   Nếu hiện `git version 2.xx.xx` là OK.

## 3. Quen với Terminal (PowerShell)

Trên Windows, terminal phổ biến nhất là **PowerShell**. Cách mở:
- Start → gõ "powershell" → Enter.
- Hoặc click chuột phải vào 1 folder → "Open in Terminal".

3 lệnh cần biết:
- `cd <tên folder>` — đi vào folder.
- `cd ..` — quay ra folder cha.
- `ls` — xem nội dung folder hiện tại.

## 4. Cài Claude Code

Mở PowerShell, chạy lệnh cài đặt chính thức:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Sau khi cài xong, đóng PowerShell và mở lại. Gõ:

```powershell
claude
```

Lần đầu chạy sẽ yêu cầu đăng nhập — làm theo hướng dẫn trên màn hình (mở trình duyệt → đăng nhập → copy mã quay lại terminal).

Khi thấy ô chat của Claude Code hiện ra với biểu tượng pixel art con vật → **xong**.

## 5. Cài Bun và Python (cho các tác vụ phát triển)

### Bun
Bun là runtime cho JavaScript (thay thế Node.js). Khi bạn build web app, Claude Code sẽ dùng Bun để chạy code:

```powershell
powershell -c "irm bun.sh/install.ps1 | iex"
```

Kiểm tra: `bun --version`.

### Python
Python dùng cho các script tự động hoá. Tải từ: https://www.python.org/downloads/windows/

**QUAN TRỌNG:** Khi cài, **tick vào ô "Add Python to PATH"** ở màn hình đầu tiên. Bỏ qua bước này là phải cài lại.

Kiểm tra:
```powershell
python --version
```

## Kiểm tra cuối cùng

Trong PowerShell, lần lượt:

```powershell
git --version
claude --version
bun --version
python --version
```

Cả 4 đều ra version number → sẵn sàng học.

## Tips

- Pin PowerShell ra Taskbar — bạn sẽ mở nó nhiều lần mỗi ngày.
- Cài thêm **Windows Terminal** từ Microsoft Store — đẹp và mượt hơn PowerShell mặc định.
- Cài **VS Code** (https://code.visualstudio.com/) — không bắt buộc nhưng giúp bạn nhìn file/folder dễ hơn khi làm việc với Claude Code.

## Khi không cài được

Xem [`troubleshooting.md`](troubleshooting.md).
