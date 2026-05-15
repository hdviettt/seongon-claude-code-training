# Cấu trúc 1 SKILL

## Cách nhanh nhất: gõ `/create-skill`

Repo này đã cài skill `create-skill` — tự generate SKILL.md đầy đủ chuẩn Anthropic cho bạn. Đọc tiếp file này chỉ khi:
- Bạn muốn HIỂU cấu trúc (không phải tự viết)
- Bạn cần chỉnh skill có sẵn
- Bạn build skill phức tạp cần fine-tune

Còn lại, gõ `/create-skill` luôn.

## 2 loại skill — Reference vs Task

Trước khi học cấu trúc, biết skill bạn build thuộc loại nào — vì cấu trúc khác:

### Reference skill — Claude áp dụng kiến thức song song
- Output user nhận = deliverable của task khác (skill chỉ inject knowledge)
- Vd: `brand-guidelines` (Claude áp dụng voice khi viết content), `bigquery-schema` (Claude consult schema khi viết SQL)
- KHÔNG có Pipeline numbered — thay bằng "Core principles" + "Reference files"

### Task skill — Claude chạy pipeline tạo deliverable riêng
- Output user nhận = artifact MỚI ĐỘC LẬP từ skill
- Vd: `macro-research` (output 1 PDF), `audit-webapp` (output 1 audit report)
- CÓ Pipeline numbered, có decision points

Phân biệt bằng 1 câu hỏi: **"Sau khi skill chạy xong, user có nhận được artifact MỚI ĐỘC LẬP không?"**

Nếu CÓ → Task. Nếu KHÔNG → Reference.

6 dạng Task skill: Research, Workflow, Generator, Analyzer, Voice/Style, Discovery — xem `.claude/skills/create-skill/references/skill-taxonomy.md` cho chi tiết.

## Progressive disclosure — design principle quan trọng nhất

Anthropic chia skill thành 3 tầng load:

```
Tier 1: Metadata (name + description)        ← Luôn load, ~100 từ
Tier 2: SKILL.md body                        ← Load khi skill triggers, ≤500 dòng
Tier 3: Bundled resources (references/...)   ← Load on-demand, không giới hạn
```

→ Đừng nhồi mọi thứ vào SKILL.md. Body ≤500 dòng / 1500-2000 từ. Detail dài tách `references/`.

## Layout folder

Mỗi SKILL là 1 folder. Cấu trúc chuẩn Anthropic — tách bạch 3 loại bundled resources:

```
.claude/skills/
└── <ten-skill>/
    ├── SKILL.md              ← BẮT BUỘC, mô tả skill (≤500 dòng)
    ├── EVALS.md              ← KHUYẾN NGHỊ, 3 scenarios test
    ├── references/           ← optional — docs Claude đọc khi cần
    │   ├── schemas.md
    │   ├── advanced.md
    │   └── ...
    ├── scripts/              ← optional — code chạy được (Python/Bash)
    │   └── helper.py
    └── assets/               ← optional — file dùng TRONG output (templates, fonts)
        └── template.html
```

**3 thư mục KHÔNG gộp lại** — mỗi mục đích khác:
| Folder | Mục đích | Khi nào load |
|---|---|---|
| `references/` | Docs Claude đọc khi cần | Khi pipeline reference tới file đó |
| `scripts/` | Code execute (deterministic) | Khi pipeline run command đó |
| `assets/` | File dùng trong output | Skill copy/modify ra cho user |

- `SKILL.md` là **bắt buộc**. Tất cả file/folder khác là optional.
- Tên folder = tên gọi của skill khi dùng `/`.

## File `SKILL.md` chuẩn

Format chuẩn Anthropic (frontmatter YAML + nội dung). Frontmatter chỉ cần `name` + `description`:

```markdown
---
name: research
description: This skill should be used when the user asks to "research about [topic]", "tìm hiểu về [X]", "/research [Y]", "compile findings on Z", "tổng hợp thông tin về W". Produces structured research report with 5-10 cited sources, comparison of consensus vs disagreement, and TL;DR.
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

Phần `---...---` ở đầu là **frontmatter** — metadata mô tả skill. Anthropic chỉ require 2 field:

| Field | Bắt buộc | Constraints |
|---|---|---|
| `name` | YES | Lowercase + hyphens + numbers. ≤64 ký tự. KHÔNG chứa "anthropic" / "claude" (reserved). Match tên folder. |
| `description` | YES | ≤1024 ký tự. Third-person ("This skill should be used when..."). ≥5 trigger phrases cụ thể. |

**Description quan trọng nhất** — Anthropic cảnh báo Claude tendency UNDERTRIGGER skills nếu description vague. Phải:
- Third-person — KHÔNG "Use this when..." / "I can help..."
- Pushy — dùng "should be used"
- Có cả *what* skill làm + *when* nên trigger
- Cụ thể, không generic

**Naming convention**: Anthropic preferred = gerund form (`processing-pdfs`, `analyzing-spreadsheets`). Exception: Reference skill naming domain entity dùng noun-phrase (`brand-guidelines`, `bigquery-schema-reference`).

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

2 chỗ tham khảo:

1. **`.claude/skills/create-skill/`** trong repo này — skill production-grade với đầy đủ:
   - SKILL.md pipeline 8 bước
   - EVALS.md với 3 scenarios
   - 4 file references/ (taxonomy, type-guides, validation, anti-patterns)
   - 2 file assets/ (skill-template, eval-template)
   - Đây là skill TỰ GENERATE skill mới — đọc để hiểu best practices applied thực tế

2. **[`examples/research-skill/`](examples/research-skill/)** — skill đơn giản 1 file để bắt đầu

## Tiếp theo

Đọc [`ket-noi-ben-ngoai.md`](ket-noi-ben-ngoai.md) để học cách cho SKILL truy cập dữ liệu ngoài (API, MCP, CLI).
