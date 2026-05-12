# Memory — Claude Code nhớ thông tin giữa session

## Định nghĩa 1 dòng

**Memory = thông tin được Claude Code lưu lâu dài và tự load mỗi khi bắt đầu session mới.**

Khác **context của 1 cuộc trò chuyện** — context mất khi đóng terminal. Memory không mất.

## 2 cơ chế memory

### 1. `CLAUDE.md` (manual)

File `CLAUDE.md` được Claude Code **đọc đầu tiên** khi mở session mới trong folder có file này.

Bạn quyết định nội dung. Dùng để mô tả:
- Project này là gì.
- Quy tắc viết code / writing convention.
- Các file quan trọng cần biết.
- Lệnh thường dùng.
- Cấm.

**Ví dụ `CLAUDE.md` cho project blog cá nhân:**

```markdown
# Blog cá nhân Việt

Next.js 14 + Tailwind + Drizzle + Postgres on Railway.

## Stack
- Frontend: Next.js App Router
- Backend: Next.js Route Handlers
- DB: Postgres trên Railway
- Auth: NextAuth + Google OAuth

## Conventions
- Tiếng Việt cho UI, tiếng Anh cho code/comment.
- Component: PascalCase. File: kebab-case.
- Mỗi PR có description, không commit thẳng vào main.

## Lệnh thường dùng
- `npm run dev` — chạy local
- `npm run build` — build prod
- `bun run deploy` — deploy lên Railway

## Cấm
- Không commit `.env`.
- Không push thẳng main.
- Không xoá file trong `/legacy/`.
```

→ Mỗi lần bạn mở Claude Code trong folder này, nó tự đọc CLAUDE.md → biết toàn bộ context.

### 2. `MEMORY.md` (auto)

File `MEMORY.md` do **Claude Code tự viết** trong quá trình làm việc. Khi nó học được gì quan trọng về preferences của bạn, nó note vào đây.

Cũng được auto-load khi mở session mới.

## CLAUDE.md được tổ chức theo tầng phân cấp

Claude Code load nhiều `CLAUDE.md` cùng lúc:

```
~/                              ← home folder
├── CLAUDE.md                   ← user-level CLAUDE.md (toàn cục)
└── Work/
    └── projects/
        └── blog/
            ├── CLAUDE.md       ← project CLAUDE.md
            └── posts/
                └── CLAUDE.md   ← folder con CLAUDE.md
```

Khi bạn mở Claude Code trong `~/Work/projects/blog/posts/`, Claude tự load **cả 3 file**:
- `~/CLAUDE.md` — preferences của bạn (voice, conventions chung).
- `~/Work/projects/blog/CLAUDE.md` — về project blog.
- `~/Work/projects/blog/posts/CLAUDE.md` — về folder posts cụ thể.

3 file tổng hợp lại = context Claude có ngay khi bắt đầu.

## Tạo CLAUDE.md tự động

Chạy `/init` trong Claude Code:

```
> /init
```

Claude sẽ:
1. Đọc cấu trúc folder.
2. Đọc `package.json`, `README.md`, config files.
3. Tạo `CLAUDE.md` đầy đủ với stack, structure, conventions detect được.

Sau đó bạn xem lại, chỉnh sửa nếu cần.

## Pattern viết CLAUDE.md tốt

### Cấu trúc khuyến nghị

```markdown
# Tên Project

1-2 câu tagline.

## Stack
<bullet list>

## Structure
<cấu trúc folder>

## Conventions
<quy ước viết code, naming>

## Lệnh thường dùng
<command list>

## Common operations
<workflow phổ biến>

## Don't
<các điều cấm>
```

### Mẹo viết CLAUDE.md hiệu quả

1. **Súc tích.** CLAUDE.md được load mỗi session → càng dài càng tốn token. Mục tiêu < 200 dòng.

2. **Tập trung vào "Claude cần biết gì để không phải hỏi bạn".**
   - Tốt: "Project này dùng Drizzle, file schema ở `db/schema.ts`."
   - Tệ: "Tôi rất quan tâm tới chất lượng code."

3. **Cấp project và cấp user có vai trò khác nhau:**
   - User CLAUDE.md: voice, preferences chung của bạn.
   - Project CLAUDE.md: chi tiết project cụ thể.

4. **Audit định kỳ.** Tháng 1 lần, hỏi Claude:
   > "Audit CLAUDE.md của project này — bỏ phần không còn relevant, gộp phần lặp lại."

## MEMORY.md — nên tắt auto-memory

`MEMORY.md` auto-write có vẻ tiện, nhưng có 2 vấn đề:
1. **Khó kiểm soát** — Claude tự note, bạn không biết note gì.
2. **Dễ đầy noise** — note linh tinh, làm context dài lên.

**Khuyến nghị:** Tắt auto-memory.

Cách tắt:
```
> /memory
```
Trong giao diện hiện ra, đổi `Auto-memory` từ `on` thành `off`.

Sau khi tắt, bạn **chủ động** đưa thông tin vào `CLAUDE.md` thay vì để Claude tự note.

## Khi nào CLAUDE.md vs SKILL?

| | CLAUDE.md | SKILL |
|---|---|---|
| **Auto-load** | Có | Không (phải gọi bằng `/`) |
| **Mục đích** | Context project | Quy trình tái sử dụng |
| **Mô hình mental** | "Mọi session đều cần biết" | "Khi cần làm việc X" |
| **Kích thước** | Ngắn | Có thể dài + nhiều file |

Pattern phổ biến:
- `CLAUDE.md` — tổng quan project + danh sách SKILLs có trong project.
- `SKILLs` — chi tiết quy trình.

## Tip thực chiến

- **Mỗi project có 1 `CLAUDE.md`.** Project to thì có nhiều file con.
- **`.gitignore` không cần ignore `CLAUDE.md`** — commit vào Git để cả team chia sẻ.
- **Khi onboard người mới**, bảo họ "đọc `CLAUDE.md`" thay vì giải thích miệng.
- **Khi đổi structure project**, update `CLAUDE.md` ngay — đừng để outdated.

## Tiếp theo

[`hooks.md`](hooks.md) — Tự động hoá Claude Code bằng hooks.
