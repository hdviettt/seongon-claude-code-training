# Giao diện cơ bản Claude Code

Sau khi cài xong, mở Terminal trong folder bạn muốn làm việc, gõ `claude`. Bạn thấy giao diện text với ô chat ở dưới.

## Các phím / ký tự đặc biệt

### `@` — Tag file vào prompt

Gõ `@` rồi tên file để cho Claude Code đọc file đó:
```
@doanh_thu_2025.csv Hãy đọc và phân tích
```

Claude Code sẽ tự complete tên file nếu file nằm trong folder hiện tại.

### `/` — Lệnh hệ thống (commands) hoặc SKILLs

- `/commands` là các lệnh xây sẵn trong Claude Code: `/clear`, `/model`, `/compact`, `/init`...
- `/SKILLs` là các kỹ năng bạn (hoặc người khác) tự xây cho Claude Code.

Cả hai gõ cùng kiểu — Claude Code phân biệt tự động.

Lệnh thường dùng:
- `/login` — đăng nhập lại nếu hết session.
- `/model` — đổi model (Opus / Sonnet / Haiku).
- `/effort` — điều chỉnh nỗ lực suy luận (low → max).
- `/clear` — xoá cuộc trò chuyện hiện tại, bắt đầu mới.
- `/compact` — nén context khi cuộc trò chuyện quá dài.
- `/usage` — xem đang dùng bao nhiêu token / chi phí.
- `/plan` — bật plan mode (xem dưới).
- `/agents` — quản lý sub-agents.
- `/resume` — quay lại cuộc trò chuyện trước.
- `/init` — Claude Code tự đọc folder và tạo file CLAUDE.md tóm tắt.

### `!` — Chạy lệnh terminal trực tiếp

Đặt `!` ở đầu prompt để bypass Claude và chạy lệnh thẳng cho terminal:
```
! ls -la
! npm install
```

Hữu ích khi bạn cần chạy nhanh 1 lệnh mà không muốn Claude xử lý.

### `Alt + V` (Windows) hoặc `Cmd + V` (Mac) — Dán ảnh

Khi bạn copy ảnh vào clipboard (chụp màn hình, copy từ web), dán vào Claude Code bằng phím tắt trên. Claude sẽ đọc nội dung ảnh.

### `Esc + Esc` (2 lần) — Xoá nhanh prompt dài

Nếu bạn gõ 1 đoạn dài và muốn xoá hết, bấm `Esc` 2 lần.

Hoặc:
- Windows: `Ctrl + Backspace`
- Mac: `Cmd + Delete`

### `Shift + Tab` — Đổi mode (auto/plan/etc)

Bấm `Shift + Tab` để chuyển giữa các mode của Claude Code. Mode quan trọng nhất: **Plan Mode**.

## Plan Mode

Khi bạn cần Claude Code **suy nghĩ kỹ trước khi làm** — đặc biệt với task lớn (xây web app, refactor code, research dài) — dùng Plan Mode.

**Cách bật:**
- Bấm `Shift + Tab` 2 lần, hoặc
- Gõ `/plan` (hoặc `/ultraplan` cho task siêu lớn).

Trong Plan Mode, Claude sẽ:
1. Đọc file, hỏi câu hỏi, thu thập thông tin.
2. Soạn ra 1 bản kế hoạch chi tiết.
3. Hiện kế hoạch cho bạn duyệt.

Bạn duyệt → Claude bắt đầu thực thi.

**Khi nào dùng:**
- Task có nhiều bước phức tạp.
- Bạn không chắc nên approach thế nào.
- Bạn muốn review trước khi Claude bắt đầu sửa file.

## Approval

Khi Claude Code muốn làm thứ có rủi ro (xoá file, cài package, chạy lệnh truy cập internet), nó **hỏi bạn duyệt trước**:

```
Bash(curl -s https://api.github.com/zen)
This command requires approval
1. Yes
2. Yes, and don't ask again for: curl *
3. No
```

- **Yes** — đồng ý 1 lần.
- **Yes, and don't ask again** — đồng ý vĩnh viễn cho lệnh dạng này (cẩn thận, đừng đồng ý vĩnh viễn cho lệnh nguy hiểm).
- **No** — không đồng ý, Claude sẽ tìm cách khác.

## Lựa chọn (single / multi)

Claude có thể hiển thị danh sách lựa chọn cho bạn pick:

```
Kênh marketing nào đang hiệu quả nhất?
> 1. SEO / Content
  2. Social Media
  3. Email Marketing
  4. Paid Ads
```

Dùng **mũi tên lên / xuống** để di chuyển, **Enter** để chọn, **Esc** để huỷ.

Khi có lựa chọn nhiều (checkbox), tick từng option bằng phím cách, rồi chuyển sang nút Submit bằng mũi tên.

## Chia terminal — chạy nhiều Claude Code

Bạn có thể mở **nhiều terminal cùng lúc** và chạy nhiều phiên Claude Code song song. Hữu ích khi:
- 1 phiên đang chạy task dài, bạn muốn làm việc khác.
- Bạn muốn so sánh kết quả của 2 cách approach.

Trên VS Code, nhấn nút **+** ở Terminal panel để mở terminal mới.

## Tips

- Khi bắt đầu cuộc trò chuyện mới, **đặt mình ở đúng folder làm việc** (`cd ...`). Claude Code chỉ thấy file trong folder hiện tại và folder con.
- Khi cuộc trò chuyện dài >100 tin nhắn, dùng `/compact` để nén lại — đỡ tốn token và chất lượng trả lời tốt hơn.
- Luôn biết Claude đang dùng model gì (xem góc trên màn hình hoặc gõ `/model`). Với task khó, dùng **Opus** với effort **xhigh**. Với task đơn giản lặp đi lặp lại, dùng **Sonnet** với effort **high**.
