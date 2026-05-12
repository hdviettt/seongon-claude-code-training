# Cài đặt Claude Code

5 bước cài đặt trên máy. Đi theo OS bạn dùng.

## Sub-files trong folder này

- **[`windows.md`](windows.md)** — Cài Windows từng bước.
- **[`mac.md`](mac.md)** — Cài Mac từng bước.
- **[`troubleshooting.md`](troubleshooting.md)** — Lỗi thường gặp khi cài.

## 5 thứ cần có

Dù Windows hay Mac, đều cần:

1. **Tài khoản Claude (Anthropic).**
2. **Git** — quản lý phiên bản.
3. **Terminal** — PowerShell (Win) / Terminal (Mac).
4. **Claude Code** — bản thân CLI.
5. **Bun + Python** — cho task lập trình.

Chi tiết từng bước trong `windows.md` / `mac.md`.

## Kiểm tra cuối cùng

Sau khi cài xong, chạy 4 lệnh:

```bash
git --version
claude --version
bun --version
python --version    # hoặc python3 --version trên Mac
```

Cả 4 ra version number → sẵn sàng. Còn lỗi → đọc `troubleshooting.md`.

## Subscription Claude

- **Free**: dùng được nhưng giới hạn nhanh, không phù hợp khoá học.
- **Claude Pro** ($20/tháng): đủ cho học viên individual.
- **Claude Max** ($100-200/tháng): cho heavy user, dùng nhiều agent/SKILL hằng ngày.

Trong khoá học, **Pro là đủ**.

## Tiếp theo

Sau khi cài xong, đọc [`../giao-dien/`](../giao-dien/) để làm quen giao diện.
