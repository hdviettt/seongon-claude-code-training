# Sub-agents

## Định nghĩa 1 dòng

**Sub-agent = đồng nghiệp ảo của Claude Code, có context riêng (không thừa hưởng từ agent chính).**

## Tại sao cần sub-agent?

Vấn đề khi dùng 1 Claude Code (agent chính):
- Mọi context (file đọc, lệnh chạy, kết quả) đều nằm trong **1 context window**.
- Context dài → tốn token + chất lượng giảm.
- Không làm song song được — 1 agent xử lý 1 task tại 1 thời điểm.

Giải pháp:
- Tạo **sub-agent** cho task con.
- Sub-agent có context **riêng**, không thừa hưởng.
- Nhiều sub-agent chạy song song.

## Workflow ví dụ

**Không sub-agent:**

```
Bạn: "Build website tổng hợp research về AI trong SEO và Ads"

Claude Code:
- Đọc tất cả file về SEO
- Đọc tất cả file về Ads
- Đọc design guideline
- Lên kế hoạch website
- Code frontend
- Code backend
- Deploy

→ Context khổng lồ, tốn token, chậm
```

**Có sub-agent:**

```
Bạn: "Build website tổng hợp research về AI trong SEO và Ads"

Claude Code (main):
"Tôi sẽ chia việc:
- Agent SEO: research AI trong SEO → trả về output [1]
- Agent Ads: research AI trong Ads → trả về output [2]
- Agent Web: dùng [1] + [2] build website"

Agent SEO ─┐
           ├─→ chạy song song, không thấy nhau
Agent Ads ─┘
           ↓
      Agent Web → website cuối cùng
```

3 hệ quả chính:
1. **Song song** — Agent SEO và Ads chạy cùng lúc, không đợi nhau.
2. **Giảm token** — Mỗi sub-agent chỉ load context cần thiết.
3. **Chất lượng cao hơn** — Ít noise trong context.

## Sub-agent được lưu ở đâu

```
project/
├── .claude/
│   └── agents/
│       ├── seo-research.md
│       ├── ads-research.md
│       └── web-builder.md
```

Mỗi sub-agent = 1 file `.md` trong `.claude/agents/`.

## Cấu trúc 1 sub-agent

```markdown
---
name: seo-research
description: Chuyên gia nghiên cứu SEO. Dùng khi user cần phân tích chiến lược SEO, từ khoá, AI Overviews, GEO, on-page SEO.
tools: Read, Glob, Grep, WebFetch, WebSearch
model: sonnet
---

# SEO Research Agent

Bạn là chuyên gia SEO với 10 năm kinh nghiệm.

## Khi được gọi

Khi user (qua agent chính) yêu cầu task liên quan SEO:
- Phân tích keyword
- Tìm hiểu AI Overviews
- Audit on-page SEO
- Research competitor

## Quy trình

1. Đọc yêu cầu cụ thể từ agent chính.
2. Nếu cần data thêm, dùng WebSearch / WebFetch.
3. Phân tích theo framework SEONGON (xem `references/seongon-seo-framework.md`).
4. Trả về output ngắn gọn, có data backing.

## Output format

```
## Insight chính
<3-5 bullet points>

## Data backing
<table hoặc bullet với nguồn>

## Recommendations
<2-3 action items>
```

## Cấm

- Không cài tool mới.
- Không sửa file ngoài folder `output/`.
- Không trả về > 500 từ.
```

## Frontmatter của sub-agent

| Field | Mô tả |
|---|---|
| `name` | Tên agent (matching tên file) |
| `description` | Khi nào agent chính nên gọi sub-agent này |
| `tools` | Danh sách tool sub-agent được dùng |
| `model` | Model cho sub-agent (`sonnet`/`opus`/`haiku`/`inherit`) |

`description` rất quan trọng — agent chính dùng để quyết định khi nào dispatch sang sub-agent này.

## 2 cấp sub-agent

### Project agent — chỉ trong project
```
project/.claude/agents/seo-research.md
```

### User agent — toàn cục
```
~/.claude/agents/seo-research.md
```

## Cách gọi sub-agent

Có 2 cách:

### 1. Tự động (recommended)

Agent chính tự quyết khi nào dispatch sang sub-agent, dựa vào `description` của agent đó.

Bạn chỉ cần nói task lớn:
> "Build website tổng hợp research AI trong SEO và Ads"

Agent chính tự nghĩ:
> "Mình sẽ gọi `seo-research`, `ads-research`, `web-builder`..."

### 2. Gọi explicit

```
"Dùng agent seo-research để phân tích từ khoá X"
```

Khi muốn control rõ.

## Khi nào dùng sub-agent

**Dùng khi:**
- Task lớn có nhiều phần độc lập nhau (research + build + design).
- Cần xử lý nhiều input độc lập (10 file, mỗi file 1 phân tích riêng).
- Cần "góc nhìn fresh" (sub-agent không có bias từ context trước).

**Không dùng khi:**
- Task tuyến tính (bước 2 phụ thuộc bước 1).
- Task nhỏ, dưới 5 phút.

## Sub-agent vs SKILL

| | Sub-agent | SKILL |
|---|---|---|
| **Context** | Riêng, không thừa hưởng | Chung với agent chính |
| **Mục đích** | Đại diện 1 "vai trò" | Đại diện 1 "quy trình" |
| **Khi nào gọi** | Task lớn cần delegate | Task lặp lại |
| **Output** | Trả lại cho agent chính | Tạo file output trực tiếp |

Pattern phổ biến: **sub-agent gọi SKILL**.
- Bạn có sub-agent `web-builder`.
- `web-builder` dùng SKILL `/frontend-stack` để quyết stack.
- Rồi dùng SKILL `/build-component` để build từng component.

## Tip thực chiến

- **Bắt đầu với 2-3 sub-agent.** Không cần build 10 ngay từ đầu.
- **Cho mỗi sub-agent có "role" rõ ràng** (chuyên gia SEO, chuyên gia thiết kế, etc).
- **Description chi tiết** để agent chính biết khi nào dispatch.
- **Giới hạn tools** của sub-agent — không cho nó full quyền.
- **Test bằng cách giao task lớn**, xem agent chính có dispatch đúng không.

## Khi build mới

```
"Tạo cho tôi 3 sub-agent:
1. seo-research — chuyên SEO
2. content-writer — viết bài chuẩn voice của tôi
3. wordpress-publisher — đăng bài lên WP

Mỗi agent có description rõ, role rõ, tools phù hợp.
Lưu vào .claude/agents/."
```

Claude sẽ tạo 3 file `.md` đầy đủ.

## Tiếp theo

- [`memory.md`](memory.md) — Làm sao Claude nhớ context giữa session.
- [`hooks.md`](hooks.md) — Tự động chạy script ở các event.
