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

4 cách, sắp xếp theo độ dễ:

### 1. `/create-skill` — KHUYẾN NGHỊ cho người mới

Repo này đã cài sẵn skill `create-skill` (xem `.claude/skills/create-skill/`). Skill này tự generate skill mới cho bạn theo chuẩn Anthropic — bạn chỉ cần trả lời 2-4 câu hỏi.

Cách gọi:
```
/create-skill

Tôi muốn skill tên "nghien-cuu-thi-truong" để research 1 thị trường ngách.
2 ví dụ: "/nghien-cuu-thi-truong thị trường mỹ phẩm hữu cơ VN" hoặc "research thị trường ngách giáo dục online cho người 30+".
```

Skill sẽ tự:
- Hỏi 2-4 câu chuyên biệt theo dạng skill bạn muốn (research / workflow / generator / analyzer / voice / discovery / reference)
- Generate `SKILL.md` đầy đủ frontmatter + body imperative form
- Tạo `EVALS.md` với 3 scenarios để bạn test
- Self-validate theo Anthropic hard gates (description third-person ≥5 triggers, body ≤500 dòng, etc.)

Output: 1 folder skill production-grade sẵn sàng dùng + cách invoke + cách test.

Đây là cách phổ biến nhất cho non-tech.

### 2. Để Claude tự build (không qua /create-skill)

Bảo Claude trực tiếp:

```
"Build cho tôi 1 SKILL tên là 'research' với chỉ dẫn:
- Bước 1: tìm 5 nguồn uy tín nhất
- Bước 2: tóm tắt từng nguồn
- Bước 3: tổng hợp thành báo cáo 1 trang
Kỳ vọng đầu ra: file .md trong folder /output
Khi tôi gõ /research <chủ đề>, skill sẽ chạy.
Lưu skill ở cấp project."
```

Claude sẽ tự tạo folder `.claude/skills/research/` với `SKILL.md`. KHÁC `/create-skill` ở chỗ: không có hard gates, không tự generate EVALS, không enforce best practices. Output có thể OK nhưng không đảm bảo production-grade.

→ Dùng cách 2 nếu skill đơn giản hoặc bạn đã thạo quy trình.

### 3. Copy SKILL người khác đã build

Repos SKILLs công khai:
- `ui-ux-pro-max` — design UI: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- `claude-ads` — chạy Google/Meta Ads: https://github.com/AgriciDaniel/claude-ads
- `claude-seo` — SEO workflows: https://github.com/AgriciDaniel/claude-seo
- `marketing-skills` — marketing chung: https://github.com/coreyhaines31/marketingskills
- `awesome-claude-skills` — danh sách 50+ skills curated: https://github.com/karanb192/awesome-claude-skills

Cách dùng:
```
"Cài SKILL từ repo này về project tôi: <URL Github>
Lưu ở .claude/skills/"
```

Claude sẽ clone về và setup giúp.

### 4. Tự viết tay file `SKILL.md`

Cho người có kinh nghiệm. Xem cấu trúc ở [`cau-truc.md`](cau-truc.md).

## Cách đánh giá 1 SKILL tốt

3 tier theo Anthropic best practices chính thức (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

### Tier 1 — Non-negotiable

1. **Description "pushy" có trigger phrases cụ thể** — Anthropic cảnh báo Claude tendency UNDERTRIGGER skills. Description phải:
   - Third-person: "This skill should be used when..." (KHÔNG "Use this when..." / "I can help...")
   - ≥5 trigger phrases cụ thể (cả VN + EN nếu bạn dùng cả 2)
   - ≤1024 ký tự
2. **Quy trình từng bước cụ thể** — imperative form ("Tạo X", "Hỏi user Y"), KHÔNG "Bạn nên" / "You should".
3. **Tiêu chí chất lượng** — checklist binary self-check trước khi output.

### Tier 2 — Production-grade

4. **Progressive disclosure 3 tầng** — Anthropic design principle quan trọng nhất:
   - Tier 1: metadata (name + description) — luôn load
   - Tier 2: SKILL.md body — load khi triggers, **≤500 dòng / 1500-2000 từ**
   - Tier 3: bundled resources — load on-demand
5. **Tách `scripts/` / `references/` / `assets/` đúng mục đích**:
   - `scripts/` — code execute, không vào context
   - `references/` — docs Claude đọc khi cần (load on-demand)
   - `assets/` — file dùng TRONG output (templates)
6. **EVALS.md với 3 scenarios** — Golden / Edge / Anti pattern.

### Tier 3 — Đỉnh cao

7. **Reference depth ≤ 1 level** từ SKILL.md (không nested reference)
8. **TOC cho reference file >100 dòng**
9. **Naming gerund form** (`processing-pdfs`, không `pdf-tool`) — exception: Reference skills naming domain entity dùng noun-phrase (`brand-guidelines`)
10. **Anti-patterns explicit** — list các pattern KHÔNG được làm với good/bad examples

### SKILL tệ vs SKILL tốt

SKILL tệ:
```
---
name: research
description: Helps with research.
---

# research
Hãy research giúp tôi.
```

3 vấn đề:
- Description vague + first person + 0 trigger phrases → Claude undertrigger
- Body không có quy trình cụ thể
- Không có tiêu chí chất lượng

SKILL tốt:
```
---
name: research
description: This skill should be used when the user asks to "research about [topic]", "tìm hiểu về [X]", "/research [Y]", "compile findings on Z", "tổng hợp thông tin về W". Produces a structured research report with 5-10 cited sources, comparison of consensus vs disagreement, and TL;DR — output as markdown file in /output folder.
---

# research

## Khi nào dùng
User gõ "/research <chủ đề>" hoặc nói cần research 1 topic.

## Pipeline 5 bước

### Step 1 — Clarify scope
Hỏi user 1 câu: "Mục đích research là gì? (Hiểu chung / pitch / quyết định / blog)"

### Step 2 — Tìm 5-10 nguồn uy tín
Ưu tiên: báo cáo nghiên cứu (Pew, McKinsey, Gartner), .gov, .edu, top 3-5 media uy tín trong ngành.
Tránh: blog cá nhân không chứng cứ, forum (trừ khi cần insight nhanh, đánh dấu rõ).

### Step 3 — Đọc + lấy ý
Mỗi nguồn: 3-5 ý chính, ngày publish, bias note.

### Step 4 — So sánh các nguồn
Consensus / tranh cãi / gap data.

### Step 5 — Viết báo cáo
Format trong `format.md`.

## Tiêu chí chất lượng (self-check)
- [ ] Mỗi claim có trích nguồn cụ thể
- [ ] Có ≥1 ý kiến trái chiều
- [ ] Báo cáo ≤1000 từ
- [ ] Có TL;DR (5 dòng) ở đầu
- [ ] Sources đầy đủ ở cuối với URL

## Anti-patterns
- KHÔNG tạo data — chỉ dùng từ nguồn thật
- KHÔNG bịa nguồn — nếu không tìm được, đánh dấu "không có nguồn xác nhận"
- KHÔNG "tôi nghĩ" — research = data, không opinion cá nhân
```

## Tip thực chiến

- **Bắt đầu với 1-2 SKILL cho việc bạn làm thường xuyên nhất.** Không cần build 20 cái.
- **Không build SKILL cho việc bạn chỉ làm 1 lần.** Prompt thẳng là nhanh hơn.
- **Sau 1 task hay, xem có nên đóng gói thành SKILL không.** Nếu bạn nghĩ "tôi sẽ làm việc này 5 lần nữa" → build SKILL.

## Tiếp theo

Đọc [`cau-truc.md`](cau-truc.md) để xem cấu trúc 1 SKILL chi tiết — bao gồm phân loại Reference vs Task, 6 dạng skill, và progressive disclosure pattern.

Hoặc gõ `/create-skill` luôn để skill tự generate skill mới cho bạn.
