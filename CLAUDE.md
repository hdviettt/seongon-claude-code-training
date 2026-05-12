# claude-code-training

Repo materials cho các buổi đào tạo Claude Code do Việt dẫn. Đối tượng chính: **non-tech** (marketer, quản lý).

## Bối cảnh

Việt là người dùng Claude Code thật, không phải lập trình viên dạy code. Buổi học không dạy syntax — dạy mental model để non-tech dùng được Claude Code mà không phá production.

Đọc workspace-level `/personal/viet/voice.md` và `/personal/viet/identity.md` trước khi viết bất cứ content nào.

## Cấu trúc

```
claude-code-training/
├── README.md           — overview toàn repo + danh sách session
├── CLAUDE.md           — file này
├── .gitignore
└── sessions/
    └── 0X-<slug>/
        ├── README.md   — outline session
        ├── slides/     — slide source
        ├── handouts/   — cheatsheet
        ├── demos/      — demo content
        └── exercises/  — hands-on
```

## Quy tắc viết content

- **Tiếng Việt** — đối tượng chính ở VN. Code/CLI giữ nguyên tiếng Anh.
- **Không hype**. Không "tuyệt vời", "đột phá", "bí mật". Direct, no fluff.
- **Không emoji** trong material formal. Slide có thể có icon nhưng không emoji.
- **Mọi khái niệm tech hook vào diagram 3 tầng** (Request flow / Security / Deployment) — đó là xương sống.
- **Mọi bài tập có acceptance rõ ràng**. "Build form thu lead → submit → lưu Google Sheet → email confirm" — không "tự khám phá".

## Anti-patterns

- Đừng viết "khóa học AI đột phá thay đổi cuộc đời".
- Đừng dạy JavaScript syntax cho marketer.
- Đừng làm slide >40 slide cho 1 buổi 3h — học viên không đọc.
- Đừng dùng từ Anh khi tiếng Việt có sẵn ("triển khai" thay "deploy" trong slide nói, nhưng vẫn dùng "deploy" trong demo CLI).

## Khi thêm session mới

1. Tạo folder `sessions/0X-<slug>/`.
2. Copy structure từ session 01 làm baseline.
3. Update bảng session trong `README.md` ngoài cùng.
4. Mỗi session có 1 entry trong `CHANGELOG.md` khi ship lần đầu.

## License & quyền

- Repo này **public** — là 1 content asset của SEONGON, đồng thời là portfolio cá nhân của Việt về Claude Code training.
- **Không commit** vào repo này:
  - Tên khách hàng cụ thể chưa được phép công khai.
  - Số liệu nội bộ SEONGON (doanh thu, headcount cụ thể, P&L).
  - Credentials, API key, screenshot có thông tin định danh học viên.
- Khi cần ví dụ "case study", dùng pseudonym hoặc xin phép trước.
- License code/exercise: MIT (mặc định). License content text (slide, handout): CC BY 4.0 — attribution Việt + SEONGON.
