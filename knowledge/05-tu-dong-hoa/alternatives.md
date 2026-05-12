# Alternatives — Khi Claude Code quá đắt

## Tại sao xem xét alternatives?

Claude Code rất mạnh, nhưng:
- **Cost**: Claude Pro $20/tháng, Claude Max $100-200/tháng. Với heavy user, dễ đụng quota.
- **Model lock-in**: chỉ dùng được Claude. Một số task model khác (GPT, Gemini) làm tốt hơn.
- **Vendor lock-in**: nếu Anthropic đổi pricing hoặc giới hạn → bạn bị động.

→ Biết alternatives để có backup plan.

## 4 alternatives chính

### 1. Codex

**Của:** OpenAI.

**Model:** GPT-5 / o1 series.

**Strength:**
- Tích hợp sẵn với ChatGPT subscription ($20/tháng Plus, $200/tháng Pro).
- GPT mạnh ở 1 số task: viết creative, debug Python phức tạp.

**Weakness:**
- Workflow agentic chưa bằng Claude Code.
- Ít plugin / extension.

**Khi nào dùng:** đã có ChatGPT Pro, ít cost thêm.

### 2. Antigravity

**Của:** Google.

**Model:** Gemini 2.5 / 3.

**Strength:**
- Tích hợp sâu với Google ecosystem (Workspace, Cloud).
- Free tier rộng.
- Gemini mạnh ở long context (1M+ tokens).

**Weakness:**
- Mới ra, ecosystem chưa mature.
- UX còn vụng.

**Khi nào dùng:** dự án có context cực dài (đọc cả codebase lớn).

### 3. Cursor

**Của:** Anysphere (startup).

**Model:** Đa dạng — bạn chọn Claude, GPT, Gemini, hoặc model local.

**Strength:**
- Là IDE, không phải CLI → trực quan hơn cho người mới.
- Switch model linh hoạt.
- Cộng đồng lớn, nhiều tutorial.

**Weakness:**
- Pricing $20/tháng cho Pro, nhưng vẫn dùng API riêng → có thể tốn hơn.
- Workflow agentic chưa bằng Claude Code thuần.

**Khi nào dùng:** quen IDE (VS Code), muốn experience similar.

### 4. OpenCode

**Của:** Anomaly (open source).

**Model:** Đa dạng (Claude, GPT, Gemini, local) — tự bạn chọn.

**Strength:**
- **Open source.** Không lock-in vendor.
- **Pricing flexible:**
  - **OpenCode Go**: $5/tháng đầu, $10/tháng sau → model open source giá rẻ.
  - **OpenCode Zen**: $20 deposit, pay-as-you-go → model có brand (Claude, GPT).
- Workflow tương tự Claude Code (CLI, agentic).

**Weakness:**
- Cần config nhiều hơn.
- Chất lượng model open source < Claude/GPT.

**Khi nào dùng:** muốn tiết kiệm cost cho task vừa và nhỏ, sẵn sàng config.

## Bảng so sánh

| Tên | Vendor | Model | Pricing entry | Strength | Khi nào dùng |
|---|---|---|---|---|---|
| **Claude Code** | Anthropic | Claude | $20 (Pro) | Workflow agentic mạnh nhất | Task hằng ngày, build sản phẩm |
| **Codex** | OpenAI | GPT-5/o1 | $20 (Plus) | Đã có ChatGPT sub | Đã trả ChatGPT, ít cost thêm |
| **Antigravity** | Google | Gemini | Free / cheap | Long context | Đọc cả codebase, dự án dài |
| **Cursor** | Anysphere | Đa dạng | $20/tháng | IDE GUI | Người quen VS Code |
| **OpenCode** | Anomaly (OSS) | Đa dạng | $5-10/tháng | Open source, flexible | Tiết kiệm cost, không lock-in |

## Pattern khuyến nghị

### Cho 1 người / freelancer

- **Default:** Claude Code (Pro $20/tháng).
- **Cost optimize:** OpenCode Go cho task nặng repetition.
- **Backup:** đăng ký Cursor free tier để có sẵn khi cần.

### Cho team / agency

- **Default:** Claude Code Max ($100-200/tháng) cho 1-2 user heavy.
- **Junior / occasional users:** Cursor hoặc OpenCode.
- **Standardize trên 1 tool** để dễ chia sẻ SKILLs, CLAUDE.md, conventions.

### Cho dự án có ngân sách hẹp

- **OpenCode Go** với model open source.
- Trade-off chất lượng — chấp nhận output kém hơn 10-20% so với Claude.

## Migration giữa các tool

Nếu bạn move từ Claude Code sang tool khác:

### `CLAUDE.md` → `AGENTS.md` / `.cursor/rules`

- Cursor đọc `.cursor/rules/*.mdc`.
- Codex đọc `AGENTS.md`.
- OpenCode đọc `AGENTS.md` hoặc `CLAUDE.md`.

→ Convert format: nội dung gần như giống, chỉ đổi file name.

### SKILLs

- Mỗi tool có format riêng. Cursor có "Rules", Codex có "Custom GPT", OpenCode có format tương tự Claude Code.
- Logic chung: chỉ dẫn quy trình + tiêu chí chất lượng. Convert format không khó.

### MCP

- MCP là standard mở → các tool đang dần support (Cursor đã support, OpenCode support).
- Codex chưa hỗ trợ MCP đầy đủ tại thời điểm hiện tại.

## Tip thực chiến

- **Bắt đầu với Claude Code.** Đầu tư học 1 tool tốt > nhảy nhiều tool.
- **Sau 3-6 tháng**, đánh giá lại cost vs value. Lúc đó mới cân nhắc switch.
- **Đừng switch chỉ vì hype.** Tool mới ra → đợi 3-6 tháng cho ecosystem ổn.
- **Học **workflow** (mindset, SKILLs, hooks, agents) — workflow chuyển được giữa tool.**

## Khi Claude Code đột ngột không dùng được

- Anthropic outage → check status.anthropic.com.
- Hết quota → đợi reset hoặc upgrade plan.
- Bug update mới → rollback version: `claude --version` → install version cũ.

Trong khi chờ:
- Dùng Claude.ai (web) làm task nhẹ.
- Dùng tool fallback (Cursor / OpenCode).

## Tóm tắt

Claude Code là default best choice cho marketer/manager non-tech hiện tại (2026). Nhưng đừng lock-in mindset — biết alternatives để có backup khi cần.

## Kết thúc khoá học

Bạn đã đi qua 5 folder kiến thức:

1. Setup Claude Code.
2. Tech stack web app.
3. Mở rộng (Commands, SKILLs, kết nối ngoài).
4. Agents, Memory, Hooks.
5. Tự động hoá, alternatives.

Bước tiếp theo:
- Làm **bài tập** trong `exercises/` để biến lý thuyết thành cái bạn dùng được.
- **Audit workspace** của bạn — apply 10 quy tắc trong `best-practice.md`.
- **Build SKILL cho việc bạn làm nhiều nhất** trong công việc hằng ngày.

Học Claude Code không phải đích đến — là **thay đổi cách làm việc**. Bạn không còn dùng "tool" — bạn **kiến trúc workflow** với 1 trợ lý có khả năng vô hạn.
