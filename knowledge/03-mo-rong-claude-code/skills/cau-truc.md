# Cấu trúc 1 SKILL

## Layout folder

Mỗi SKILL là 1 folder. Cấu trúc:

```
.claude/skills/
└── <ten-skill>/
    ├── SKILL.md        ← bắt buộc, mô tả skill
    ├── script.py       ← optional, code đi kèm
    ├── checklist.md    ← optional, danh sách check
    ├── format.md       ← optional, template output
    └── references/     ← optional, tài liệu tham khảo
        └── ...
```

- `SKILL.md` là **bắt buộc**. Tất cả file khác là optional, tuỳ skill.
- Tên folder = tên gọi của skill khi dùng `/`.

## File `SKILL.md` chuẩn

Format khuyến nghị (frontmatter YAML + nội dung):

```markdown
---
name: research
description: Research 1 chủ đề và viết báo cáo theo format chuẩn. Dùng khi user gõ "/research <chủ đề>" hoặc nói cần tìm hiểu sâu về 1 topic.
user-invokable: true
argument-hint: <chủ đề cần research>
license: MIT
metadata:
    author: Việt
    version: 1.0
    category: research
---

# Research Skill

## Role

Bạn là chuyên gia research với 10 năm kinh nghiệm. Nhiệm vụ: tìm hiểu sâu 1 chủ đề và viết báo cáo súc tích, có nguồn rõ ràng.

## Khi nào dùng

User gõ `/research <chủ đề>` hoặc nói:
- "research giúp tôi về X"
- "tìm hiểu sâu về Y"
- "tổng hợp thông tin về Z"

## Quy trình (5 bước)

### Bước 1 — Làm rõ mục đích

Hỏi user 1 câu (chỉ 1):
- "Bạn cần báo cáo này để làm gì? (Để hiểu chung / Để pitch / Để quyết định / Để viết blog)"

Goal quyết định độ sâu và format báo cáo.

### Bước 2 — Tìm nguồn

Tìm 5-10 nguồn uy tín. Ưu tiên:
1. Báo cáo từ tổ chức nghiên cứu (Pew, McKinsey, Gartner).
2. Tài liệu chính phủ (.gov).
3. Tài liệu học thuật (.edu, Google Scholar).
4. Top 3-5 media uy tín trong ngành.

Tránh:
- Blog cá nhân không có chứng cứ.
- Forum / Reddit (trừ khi cần insight nhanh, đánh dấu rõ).

### Bước 3 — Đọc và lấy ý

Mỗi nguồn:
- Lấy 3-5 ý chính.
- Note rõ ngày publish (nguồn cũ <2020 cẩn thận với data thay đổi nhanh).
- Note quan điểm bias nếu có.

### Bước 4 — Tổng hợp

So sánh các nguồn:
- Đâu là consensus (mọi nguồn đồng ý)?
- Đâu là tranh cãi (nguồn không đồng ý)?
- Đâu là gap (chưa có nguồn nào trả lời)?

### Bước 5 — Viết báo cáo

Theo template trong `format.md`.

## Format đầu ra

Đọc `format.md` để biết structure chi tiết.

## Tiêu chí chất lượng

Trước khi đưa cho user, tự check:
- [ ] Mỗi claim có trích nguồn cụ thể.
- [ ] Có ít nhất 1 ý kiến trái chiều / nuance.
- [ ] Báo cáo dưới 1000 từ (trừ khi user yêu cầu dài hơn).
- [ ] Có TL;DR (5 dòng) ở đầu.
- [ ] Nguồn liệt kê đầy đủ ở cuối, có URL.

## Output

Lưu báo cáo vào `output/<tên-chủ-đề>-<date>.md`.

## Cấm

- Không tạo data — chỉ dùng từ nguồn thật.
- Không bịa nguồn — nếu không tìm được nguồn cho claim, đánh dấu rõ "không có nguồn xác nhận".
- Không trả lời "tôi nghĩ" — research = trình bày data, không opinion cá nhân.
```

## Frontmatter (YAML đầu file)

Phần `---...---` ở đầu là **frontmatter** — metadata mô tả skill.

| Field | Bắt buộc? | Mô tả |
|---|---|---|
| `name` | Bắt buộc | Tên skill (matching tên folder) |
| `description` | Bắt buộc | Mô tả ngắn, Claude dùng để quyết định khi nào gọi skill |
| `user-invokable` | Optional | `true` nếu user gõ `/` để dùng được |
| `argument-hint` | Optional | Gợi ý argument để hiện khi user gõ |
| `license` | Optional | License (MIT, CC BY...) |
| `metadata` | Optional | Tác giả, version, category... |

## Cấu trúc nội dung skill (sau frontmatter)

Không có format bắt buộc tuyệt đối — nhưng pattern tốt:

1. **Role** — Claude đóng vai gì khi chạy skill này.
2. **Khi nào dùng** — trigger chi tiết.
3. **Quy trình từng bước** — đánh số rõ.
4. **Input/output format** — Claude biết nhận gì, trả gì.
5. **Tiêu chí chất lượng** — checklist tự đánh giá trước khi đưa cho user.
6. **Cấm** — các pattern KHÔNG được làm.

## File đi kèm

### `format.md` — Template output

Chứa structure chuẩn cho output:

```markdown
# Báo cáo: <chủ đề>

## TL;DR
<5 dòng tóm tắt>

## Bối cảnh
<2-3 đoạn về sao chủ đề này quan trọng>

## Các tìm thấy chính
1. ...
2. ...
3. ...

## Ý kiến trái chiều / Nuance
<các tranh cãi, gap data>

## Nguồn
1. [Tên nguồn 1](URL) — 2024
2. ...
```

### `script.py` — Code đi kèm

Khi skill cần chạy code (gọi API, xử lý data...), code nằm cạnh `SKILL.md`. Trong `SKILL.md`, mention file:

```markdown
## Bước 1 — Lấy data

Chạy script:
\`\`\`bash
python script.py "<chủ đề>" --save
\`\`\`

Script trả về file JSON ở `output/data.json`.
```

### `checklist.md` — Danh sách check chi tiết

Khi tiêu chí chất lượng dài, tách ra file riêng.

### `references/` — Tài liệu tham khảo

Ví dụ guideline branding của công ty bạn, để skill viết content luôn theo voice đó.

## Ví dụ SKILL có nhiều file

```
.claude/skills/seo-content/
├── SKILL.md
├── voice-guide.md          ← voice của brand
├── seo-checklist.md        ← checklist SEO on-page
├── format.md               ← template content
└── scripts/
    ├── check_keyword.py    ← script check density từ khoá
    └── word_count.py       ← script đếm từ
```

## Cấp project vs cấp user

```
# Project skill
project/.claude/skills/research/SKILL.md

# User skill (toàn cục)
~/.claude/skills/research/SKILL.md
```

## Tip thực chiến

- **SKILL.md càng cụ thể càng tốt.** Đừng viết "research kỹ" — viết "tìm 5 nguồn uy tín nhất, lấy 3 ý từ mỗi nguồn".
- **Luôn có "Khi nào dùng".** Không thì Claude không biết khi nào gọi skill.
- **Luôn có "Tiêu chí chất lượng".** Đây là cách skill self-check, tránh output kém.
- **Khi build skill, test 3 lần với 3 input khác nhau** trước khi tin nó hoạt động ổn định.

## Ví dụ skill hoàn chỉnh

Xem [`examples/research-skill/`](examples/research-skill/) trong folder này.

## Tiếp theo

Đọc [`ket-noi-ben-ngoai.md`](ket-noi-ben-ngoai.md) để học cách cho SKILL truy cập dữ liệu ngoài (API, MCP, CLI).
