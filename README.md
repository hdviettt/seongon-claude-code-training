# Claude Code Training — SEONGON

Bể kiến thức về Claude Code cho marketer / quản lý non-tech.

Repo này được thiết kế để **clone về máy và dùng Claude Code của bạn để học**. Không cần phụ thuộc vào giảng viên — Claude Code đọc được hết, sẽ trả lời câu hỏi và hướng dẫn từng bước.

## Đối tượng

- Marketer, quản lý, người làm SEO/Ads — không lập trình.
- Đã có hoặc sắp có tài khoản Claude (Anthropic).
- Muốn dùng Claude Code để tăng năng suất công việc thật, không chỉ học lý thuyết.

## Cách dùng repo này

### Cách 1 — Tự học, hỏi đáp với Claude Code

1. Clone repo về máy:
   ```
   git clone https://github.com/hdviettt/seongon-claude-code-training
   cd seongon-claude-code-training
   ```
2. Mở Claude Code trong thư mục này:
   ```
   claude
   ```
3. Hỏi bất cứ gì:
   - "Setup Claude Code trên Windows như nào?"
   - "Frontend là gì? Tôi nên dùng framework nào cho web app bán hàng?"
   - "Hooks trong Claude Code dùng để làm gì? Cho ví dụ."

Claude Code sẽ tự đọc folder `knowledge/` để trả lời. Không phải đoán — nó đọc tài liệu của khoá này.

### Cách 2 — Ôn theo buổi học đã tham gia

Vào folder `sessions/` — mỗi file là outline 1 buổi, link sang các topic kiến thức tương ứng:

- `buoi-1-setup.md` — Setup Claude Code
- `buoi-2-tech-stack.md` — Tech stack web app
- `buoi-3-mo-rong.md` — Commands, SKILLs, kết nối ngoài
- `buoi-4-agents-memory-hooks.md` — Sub-agents, memory, hooks
- `buoi-5-tu-dong-hoa.md` — Remote control, alternatives

### Cách 3 — Đọc trực tiếp như tài liệu

Vào folder `knowledge/`, mở thẳng các file `.md`. Mỗi folder là 1 mảnh kiến thức tự đủ.

## Cấu trúc

```
seongon-claude-code-training/
├── README.md           — file này
├── CLAUDE.md           — hướng dẫn cho Claude Code
├── INDEX.md            — bản đồ topic → folder
├── knowledge/          — bể kiến thức, topic-based
│   ├── 01-setup-claude-code/
│   ├── 02-tech-stack-web-app/
│   ├── 03-mo-rong-claude-code/
│   ├── 04-agents-memory-hooks/
│   └── 05-tu-dong-hoa/
├── sessions/           — outline từng buổi học
├── exercises/          — bài tập về nhà
└── slides/             — slide PDF của các buổi học
```

## Bài tập

Folder `exercises/` chứa bài tập về nhà tương ứng các buổi. Mỗi bài tập có tiêu chí cụ thể — Claude Code có thể giúp bạn làm từ đầu đến cuối.

## License

- Code và exercise: MIT
- Content (slide, handout, knowledge): CC BY 4.0 — attribution SEONGON + Hoàng Đình Việt

## Đóng góp

Repo này là tài liệu sống. Nếu bạn học được gì hay trong quá trình dùng Claude Code và muốn đóng góp — mở PR hoặc liên hệ SEONGON.
