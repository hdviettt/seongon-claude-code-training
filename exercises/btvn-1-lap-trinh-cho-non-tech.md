# BTVN buổi 1 — Bài học lập trình cho non-tech

## Đề bài

Dùng Claude Code chuẩn bị **bài học lập trình cơ bản cho người non-tech** cho chính mình.

Mục đích: bạn sẽ là người đầu tiên hiểu kiến thức lập trình theo cách dễ nhất → bài học của bạn sẽ là tài liệu để bạn ôn về sau.

## Output bắt buộc

| STT | Output | Format |
|---|---|---|
| 1 | Một (hoặc nhiều) file tài liệu giảng dạy cho chính mình | `.ipynb` (Colab/Jupyter notebook) |
| 2 | File ghi chép lịch sử trò chuyện với Claude Code | `.txt` |
| - | Bất kỳ sản phẩm, dự án, workflow nào khác bạn muốn | Tự do |

### File 1 — `.ipynb` (Jupyter notebook)

Notebook chứa lý thuyết + code chạy được. Bài học bao gồm:
- Biến và kiểu dữ liệu.
- Hàm.
- Toán tử.
- Control flow.
- Vài ví dụ đơn giản, có code chạy được trong Jupyter.

Bài học **cho chính bạn** — bạn quyết style. Có thể tiếng Việt, có thể tiếng Anh.

### File 2 — Lịch sử chat (`.txt`)

Export cuộc trò chuyện với Claude trong khi làm BTVN này. Để bạn ôn lại quá trình bạn đã prompt Claude thế nào.

Cách export: trong Claude Code, gõ `/export` → lưu thành file `.txt`.

## Tiêu chí

- Notebook chạy được (không lỗi syntax).
- Mỗi khái niệm có ít nhất 1 ví dụ code.
- Lịch sử chat đầy đủ — không xoá phần nào.

## Rules

- **Làm mọi cách để đạt được kết quả cuối cùng.**
- **Không đặt câu hỏi cho trợ giảng (mà chưa) đặt câu hỏi cho Claude Code.**

## Deadline

23h59 Chủ Nhật của tuần học buổi 1.

## Cách nộp

Upload file lên 1 thư mục Google Drive, mở quyền truy cập (anyone with link), gán link vào form SEONGON gửi trên nhóm.

## Gợi ý — Cách bắt đầu

Khi bạn lúng túng không biết bắt đầu thế nào, dùng prompt sau với Claude Code:

```
Tôi cần bạn giúp tôi tạo 1 file notebook (.ipynb) dạy lập trình cơ bản 
cho người non-tech. Tôi là 1 marketer, chưa biết code, vừa học xong 
buổi 1 Claude Code.

Nội dung cần có:
- Biến và 5 kiểu dữ liệu cơ bản (string, int, float, boolean, list, dict)
- Hàm (definition, parameter, return)
- Toán tử (arithmetic, comparison, logical)
- Control flow (if/else, for, while)

Format:
- Notebook Python (.ipynb) chạy được trên Jupyter hoặc Google Colab.
- Mỗi khái niệm: giải thích bằng tiếng Việt, dùng metaphor đời thật, 
  rồi có 1-2 code cell chạy được.
- Cuối mỗi phần có 1 bài tập nhỏ.

Hãy tạo file này, đặt trong folder ./notebooks/.
```

Sau khi Claude làm xong:
- Mở file `.ipynb` trên Jupyter/Colab.
- Chạy thử từng cell.
- Edit / bổ sung phần bạn thấy chưa rõ.

## Kiến thức liên quan

- [`knowledge/01-setup-claude-code/`](../knowledge/01-setup-claude-code/) — Setup, giao diện cơ bản.
- [`knowledge/02-tech-stack-web-app/lap-trinh-co-ban.md`](../knowledge/02-tech-stack-web-app/lap-trinh-co-ban.md) — Khái niệm lập trình cơ bản (đọc trước để có ý tưởng).
