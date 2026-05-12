# Remote Control — Dùng Claude Code trên điện thoại

## Tại sao cần?

Claude Code là CLI — chạy trong terminal trên máy tính. Nhưng nhiều khi bạn:
- Đang đi đường, có ý tưởng → muốn giao Claude làm ngay.
- Đang trong meeting, không tiện mở laptop.
- Muốn check tiến độ task Claude đang chạy nền.

→ Cần cách điều khiển Claude Code từ điện thoại.

## 2 cách kết nối

### Cách 1 — `/remote-control` (cần máy tính bật)

**Cách hoạt động:**
1. Trên máy tính, mở Claude Code, gõ `/remote-control`.
2. Claude tạo session "remote-control" và link với app Claude trên điện thoại.
3. Bạn nhắn task qua app Claude → task chạy trên máy tính bạn.

**Yêu cầu:**
- App **Claude** trên điện thoại (iOS / Android).
- Đã đăng nhập cùng account.
- Máy tính bật, terminal Claude Code đang mở.

**Lưu ý:**
- Nếu đóng terminal trên máy → mất session, phải bắt đầu lại.
- Bạn vẫn có thể can thiệp từ máy tính nếu cần.

### Cách 2 — Kết nối GitHub repo (không cần máy tính)

**Cách hoạt động:**
1. Push code lên GitHub repo.
2. Trong app Claude trên điện thoại → "Code" → bắt đầu session với repo.
3. Claude chạy task trên cloud, không cần máy tính bật.

**Yêu cầu:**
- Code đã trên GitHub.
- Account Claude có quyền truy cập repo.

**Lưu ý:**
- Claude làm việc trên cloud → không truy cập file local trên máy bạn.
- Output (file mới, sửa file) commit thẳng lên branch hoặc PR.

## Khi nào dùng cách nào?

| Tình huống | Dùng |
|---|---|
| Đang làm trên máy, muốn rời đi 30 phút và check tiến độ qua điện thoại | `/remote-control` |
| Đang đi công tác cả tuần, muốn giao task cho Claude | GitHub repo |
| Có ý tưởng đột xuất, muốn build prototype luôn | GitHub repo |
| Cần xem log real-time của task đang chạy | `/remote-control` |

## Cách dùng `/remote-control` từng bước

### Trên máy tính

1. Mở Claude Code trong folder cần làm việc.
2. Gõ:
   ```
   /remote-control
   ```
3. Claude hiển thị: "Remote Control active". Để terminal mở.

### Trên điện thoại

1. Mở app Claude.
2. Vào tab **Code**.
3. Bạn sẽ thấy session đang active (có chấm xanh "Connected").
4. Click vào session → giao task như chat bình thường.

### Khi xong

Trên máy tính, gõ `Esc Esc` để thoát remote control mode, quay lại làm việc bình thường.

## Cách dùng GitHub repo từng bước

### Push code lên GitHub trước

Nếu chưa có, đẩy code lên GitHub:
```bash
git remote add origin https://github.com/<user>/<repo>.git
git push -u origin main
```

(Hoặc nhờ Claude làm hộ.)

### Trên điện thoại

1. Mở app Claude → tab **Code**.
2. Click **+** → **New conversation with repo**.
3. Chọn repo từ list (cần authorize GitHub access lần đầu).
4. Chat task → Claude làm việc trên cloud.

### Output

- Claude commit code lên branch mới hoặc tạo PR.
- Bạn review trên GitHub.
- Merge khi OK.

## Tip thực chiến

- **Remote control cho task ngắn (< 30 phút).** Lâu hơn → máy có thể sleep hoặc Wi-Fi rớt.
- **GitHub repo cho task dài / agentic.** Cloud chạy ổn định hơn máy bạn.
- **Setup notifications.** Trong `/config`, bật "Push when actions required" và "Push when Claude decides" — bạn nhận thông báo khi Claude cần input hoặc xong việc.
- **Đừng giao task quá lớn từ điện thoại.** Mô tả ngắn → output có thể không như ý. Tốt nhất là plan rõ trên máy, rồi tiếp tục từ điện thoại.

## Limitations

- **Không tạo agents / SKILLs từ điện thoại** — flow này tốt hơn trên máy tính.
- **MCP server local không hoạt động qua GitHub repo flow** (chạy cloud → không thấy MCP local).
- **Tốc độ phụ thuộc kết nối điện thoại** — 4G/5G ổn, Wi-Fi yếu thì chậm.

## Quay lại làm việc trên máy

Trên điện thoại bạn giao task xong, Claude làm nửa chừng. Muốn tiếp tục trên máy:

1. Trên máy tính, vào folder repo.
2. `git pull` để lấy code Claude đã commit.
3. Mở Claude Code → `/resume` → tiếp tục cuộc trò chuyện.

Hoặc, nếu dùng GitHub repo flow: review PR Claude tạo, comment góp ý, Claude tự update PR.

## Use case thực tế

**Use case 1 — Bug fix lúc đang đi đường:**
- Khách báo bug.
- Bạn mở app Claude trên điện thoại → repo → "Fix bug X, deploy lên staging".
- Claude làm xong, tạo PR.
- Bạn review, merge, deploy.

**Use case 2 — Research lúc nghỉ trưa:**
- Mở app → "research về AI Overviews trên thị trường Việt Nam, lưu kết quả vào `research/aio-vn.md`".
- 30 phút sau, Claude commit kết quả.
- Tối về xem.

**Use case 3 — Update blog post lúc đang ngủ:**
- Mở app → repo blog → "viết bài về X theo voice trong CLAUDE.md, đẩy lên branch `draft/x`".
- Sáng dậy, review → merge → deploy.

## Tiếp theo

[`best-practice.md`](best-practice.md) — Mindset dùng Claude Code hiệu quả.
