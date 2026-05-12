# SKILLs cơ bản

## Định nghĩa 1 dòng

**SKILL = kỹ năng nghiệp vụ bạn tự xây cho Claude Code, đóng gói 1 chỉ dẫn để dùng lại nhiều lần.**

Gọi SKILL bằng `/`, giống commands. Khác commands: SKILLs do **bạn** tự build, commands có sẵn.

## Tại sao cần SKILL?

Tình huống không có SKILL:

> Bạn muốn thiết kế giao diện cho website thứ 100. Mỗi lần bạn phải copy-paste 1 đoạn prompt:
> ```
> "Giúp tôi thiết kế giao diện:
> - Phong cách tối giản, hiện đại
> - Màu chủ đạo tím
> - Dùng Tailwind + shadcn/ui
> - Mobile-first
> - ..."
> ```
> Lặp 100 lần = lãng phí thời gian + dễ thiếu sót.

Tình huống có SKILL:

> Bạn tạo SKILL `/thiet-ke-website` với toàn bộ chỉ dẫn ở trên. Mỗi lần dùng chỉ gõ:
> ```
> /thiet-ke-website Hãy build giao diện cho khoá học X
> ```
> Claude tự load chỉ dẫn, áp dụng đúng phong cách bạn muốn.

## Bản chất của SKILL

**SKILL là chỉ dẫn được đóng gói để dùng lại.**

Bạn có thể tự build skill cho:
- Research chủ đề theo format chuẩn của bạn.
- Viết content theo voice của bạn / công ty.
- Phân tích từ khoá SEO theo quy trình riêng.
- Tạo ads creative theo template.
- Bất cứ workflow nào bạn lặp đi lặp lại.

## SKILL được lưu ở đâu

```
project/
├── .claude/
│   └── skills/
│       ├── thiet-ke-website/
│       │   └── SKILL.md
│       ├── research/
│       │   ├── SKILL.md
│       │   └── format.md
│       └── ...
```

- `.claude/skills/` là folder chứa skills.
- Mỗi skill = 1 folder (không phải 1 file).
- Trong folder bắt buộc có `SKILL.md` — file mô tả skill.
- Có thể có thêm file khác đi kèm (xem `cau-truc-skill.md`).

## 2 cấp SKILL: project vs user

### Project SKILL — chỉ dùng trong 1 project

Lưu ở `.claude/skills/` của project. Chỉ Claude Code khi mở trong project đó mới thấy.

→ Dùng khi SKILL liên quan riêng project (ví dụ: SKILL để check style của trang web cụ thể này).

### User SKILL — dùng cho mọi project

Lưu ở `~/.claude/skills/` (folder home, ngoài mọi project). Claude Code thấy ở mọi nơi.

→ Dùng cho SKILL chung (research, viết email, format file).

**Khi giao Claude build skill, nói rõ:**
- "Build skill ở cấp project" → `.claude/skills/`
- "Build skill ở cấp user" → `~/.claude/skills/`

## So sánh SKILLs vs Commands

| Đặc điểm | SKILLs | Commands |
|---|---|---|
| Cú pháp | `/<tên>` | `/<tên>` |
| Ai xây | Bạn | Claude Code |
| Phạm vi | Project hoặc user | Toàn cục |
| Có argument không | Có | Có (1 số) |

## Cách build 1 SKILL

3 cách:

### 1. Để Claude tự build cho bạn

Đây là cách phổ biến nhất:

```
"Build cho tôi 1 SKILL tên là 'research' với chỉ dẫn:
- Bước 1: tìm 5 nguồn uy tín nhất
- Bước 2: tóm tắt từng nguồn
- Bước 3: tổng hợp thành báo cáo 1 trang
Kỳ vọng đầu ra: file .md trong folder /output
Khi tôi gõ /research <chủ đề>, skill sẽ chạy.
Lưu skill ở cấp project."
```

Claude sẽ tự tạo folder `.claude/skills/research/` với `SKILL.md` đầy đủ.

### 2. Copy SKILL người khác đã build

Repos SKILLs công khai:
- `ui-ux-pro-max` — design UI: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- `claude-ads` — chạy Google/Meta Ads: https://github.com/AgriciDaniel/claude-ads
- `claude-seo` — SEO workflows: https://github.com/AgriciDaniel/claude-seo
- `marketing-skills` — marketing chung: https://github.com/coreyhaines31/marketingskills

Cách dùng:
```
"Cài SKILL từ repo này về project tôi: <URL Github>
Lưu ở .claude/skills/"
```

Claude sẽ clone về và setup giúp.

### 3. Tự viết tay file `SKILL.md`

Cho người có kinh nghiệm. Xem cấu trúc ở [`cau-truc-skill.md`](cau-truc-skill.md).

## Cách đánh giá 1 SKILL tốt

SKILL tốt có 3 đặc điểm:

1. **Mô tả rõ skill làm gì** — Claude biết khi nào gọi skill này.
2. **Chỉ dẫn các bước cụ thể** — không chỉ "make it good", mà "bước 1, bước 2..." kèm ví dụ.
3. **Tiêu chí chất lượng đầu ra** — checklist cho Claude tự đánh giá output trước khi đưa cho bạn.

SKILL tệ:
```
# research
Hãy research giúp tôi.
```

SKILL tốt:
```
# research

## Khi nào dùng
User gõ "/research <chủ đề>" hoặc nói cần research về 1 topic.

## Quy trình
1. Hỏi user mục đích research để hiểu rõ goal (1 câu).
2. Tìm 5-10 nguồn uy tín (ưu tiên .edu, .gov, top media).
3. Đọc từng nguồn, lấy 3-5 ý chính.
4. So sánh các nguồn — đâu là consensus, đâu là tranh cãi.
5. Viết báo cáo theo format ở `format.md`.

## Tiêu chí chất lượng
- [ ] Mỗi claim có trích nguồn.
- [ ] Có ít nhất 1 ý kiến trái chiều.
- [ ] Báo cáo dưới 1000 từ.
- [ ] Có TL;DR ở đầu.
```

## Tip thực chiến

- **Bắt đầu với 1-2 SKILL cho việc bạn làm thường xuyên nhất.** Không cần build 20 cái.
- **Không build SKILL cho việc bạn chỉ làm 1 lần.** Prompt thẳng là nhanh hơn.
- **Sau 1 task hay, xem có nên đóng gói thành SKILL không.** Nếu bạn nghĩ "tôi sẽ làm việc này 5 lần nữa" → build SKILL.

## Tiếp theo

Đọc [`cau-truc-skill.md`](cau-truc-skill.md) để xem cấu trúc 1 SKILL chi tiết.
