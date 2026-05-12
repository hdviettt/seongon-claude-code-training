# BTVN buổi 3 — Workspace cá nhân với SKILLs

## Đề bài

Dùng Claude Code để **xây 1 không gian làm việc cá nhân (workspace) với các SKILLs**.

Workspace = 1 folder bạn quay lại làm việc thường xuyên (không phải project ngắn hạn). Ví dụ:
- Folder "SEO research" để làm research SEO hằng ngày.
- Folder "Content production" để viết bài.
- Folder "Ads campaigns" để quản lý Ads.
- Folder "Personal knowledge" để lưu kiến thức cá nhân.

## Tiêu chí bắt buộc

Workspace phải có **ít nhất**:

- 1 SKILL kết nối với nền tảng ngoài (API, MCP, hoặc CLI).
- 1 SKILL chứa các file & folder bên cạnh `SKILL.md` (không chỉ là 1 file đơn).

## Output

| STT | Output | Format |
|---|---|---|
| 1 | Files và folder workspace nằm trên 1 GitHub repo | Github repo |
| 2 | File ghi chép lịch sử trò chuyện với Claude (`/export`) | `.txt` |
| 3 | Các file output từ việc chạy SKILL | Tự do |

## Cách nộp

Setup GitHub repo public, push code, gán link GitHub vào form SEONGON.

## Rules

- Làm mọi cách để đạt được kết quả cuối cùng.
- Không đặt câu hỏi cho trợ giảng (mà chưa) đặt câu hỏi cho Claude Code.

## Deadline

23h59 Chủ Nhật của tuần học buổi 3.

## Gợi ý — Một workspace SEO mẫu

```
my-seo-workspace/
├── .claude/
│   ├── skills/
│   │   ├── keyword-research/         ← SKILL kết nối API (SerpAPI)
│   │   │   ├── SKILL.md
│   │   │   ├── fetch_keywords.py
│   │   │   └── format.md
│   │   ├── content-brief/             ← SKILL có nhiều file
│   │   │   ├── SKILL.md
│   │   │   ├── template.md
│   │   │   └── voice-guide.md
│   │   └── seo-audit/
│   │       └── SKILL.md
│   └── CLAUDE.md
├── output/
│   ├── keyword-research/
│   └── content-briefs/
├── .env.example
├── .gitignore
└── README.md
```

### SKILL 1 — `keyword-research` (kết nối API)

Setup:
- API: SerpAPI hoặc DataForSEO.
- Lưu key trong `.env` (không commit).
- Script Python gọi API → lấy data → lưu JSON vào `output/`.

`SKILL.md`:
- Mô tả khi nào dùng (user gõ `/keyword-research <keyword>`).
- Quy trình: chạy script Python → đọc kết quả → phân nhóm intent → ưu tiên.
- Format output: bảng từ khoá với intent, cluster, ưu tiên P1/P2/P3.

### SKILL 2 — `content-brief` (nhiều file)

Setup:
- Folder `.claude/skills/content-brief/`:
  - `SKILL.md` — quy trình tạo brief.
  - `template.md` — template brief mẫu.
  - `voice-guide.md` — voice của brand bạn.

`SKILL.md`:
- Khi nào dùng (user gõ `/content-brief <topic>`).
- Quy trình: research → chọn angle → fill template với voice trong `voice-guide.md`.
- Output: file `.md` trong `output/content-briefs/`.

## Gợi ý — Một workspace Ads mẫu

```
my-ads-workspace/
├── .claude/
│   ├── skills/
│   │   ├── google-ads-report/        ← SKILL kết nối Google Ads MCP
│   │   │   └── SKILL.md
│   │   ├── ad-copy-generator/         ← SKILL có nhiều file
│   │   │   ├── SKILL.md
│   │   │   ├── voice-guide.md
│   │   │   └── examples.md
│   │   └── ...
│   └── CLAUDE.md
└── ...
```

## Cách bắt đầu

```
Tôi muốn build 1 workspace cá nhân cho công việc SEO của tôi. Tôi cần:

1. Folder structure: .claude/skills/, output/, README.md, CLAUDE.md.
2. SKILL #1: keyword-research, dùng SerpAPI để lấy data Google. 
   Tôi đã có SERPAPI_KEY. Hãy tạo skill này với script Python đi kèm.
3. SKILL #2: content-brief, có template và voice guide riêng. 
   Tôi sẽ provide voice guide sau.
4. CLAUDE.md mô tả workspace này, conventions, lệnh thường dùng.

Hãy lên PLAN.md trước, rồi tôi duyệt.
```

## Sai lầm phổ biến cần tránh

Theo kinh nghiệm khoá trước, **sai lầm hay gặp nhất:**

> **Tạo skill nhưng đặt sai folder** — không nằm trong `.claude/skills/<tên>/`.

Skill **phải** nằm chính xác trong path đó. Đặt ở chỗ khác → Claude Code không nhận skill.

Kiểm tra:
```bash
ls .claude/skills/
```

Phải thấy tên skill là folder, trong folder có `SKILL.md`.

## Kiến thức liên quan

- [`knowledge/03-mo-rong-claude-code/skills-co-ban.md`](../knowledge/03-mo-rong-claude-code/skills-co-ban.md)
- [`knowledge/03-mo-rong-claude-code/cau-truc-skill.md`](../knowledge/03-mo-rong-claude-code/cau-truc-skill.md)
- [`knowledge/03-mo-rong-claude-code/ket-noi-ben-ngoai.md`](../knowledge/03-mo-rong-claude-code/ket-noi-ben-ngoai.md)
- Ví dụ skill hoàn chỉnh: [`knowledge/03-mo-rong-claude-code/examples/research-skill/`](../knowledge/03-mo-rong-claude-code/examples/research-skill/)

## SKILL repos tham khảo

4 repo skills SEONGON đã check chất lượng — có thể tham khảo cấu trúc:
- `ui-ux-pro-max` — design UI
- `claude-ads` — Google/Meta Ads workflows
- `claude-seo` — SEO workflows
- `marketing-skills` — marketing chung

Link đầy đủ trong `knowledge/03-mo-rong-claude-code/skills-co-ban.md`.
