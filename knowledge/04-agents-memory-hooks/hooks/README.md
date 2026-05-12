# Hooks — Tự động hoá Claude Code

## Định nghĩa 1 dòng

**Hook = script tự chạy ở 1 event nhất định trong quá trình Claude Code làm việc.**

Giống automation trong n8n / Zapier: **trigger** xảy ra → **action** chạy.

## Tại sao cần hooks?

Có những việc bạn muốn Claude **luôn làm** ở 1 thời điểm cụ thể, không cần nhắc:

- Trước khi tạo file `.md`: load template format.
- Sau khi gọi Google API: refresh token nếu hết hạn.
- Trước khi `/compact`: backup cuộc trò chuyện.
- Mỗi khi user gõ prompt: append ngày tháng hiện tại vào prompt.

→ Hooks tự động hoá những việc này.

## Các loại event kích hoạt hooks

| Event | Khi nào trigger | Use case điển hình |
|---|---|---|
| `SessionStart` | Mở session mới | Inject context tươi |
| `UserPromptSubmit` | Mỗi lần user gõ Enter | Prepend env vào prompt (date, branch, active client) |
| `PreToolUse` | Trước khi gọi tool | Block lệnh nguy hiểm, validate input |
| `PostToolUse` | Sau khi gọi tool | Filter output dài, summarize, log |
| `Stop` | Agent dừng | Log session summary |
| `PreCompact` / `PostCompact` | Trước/sau khi compact | Backup history, log sau compact |
| `SubagentStart` / `SubagentStop` | Sub-agent start/stop | Track activity sub-agent |
| `SessionEnd` | Đóng session | Cleanup |
| `FileChanged` | File được watch thay đổi | Trigger workflow |

## Ví dụ thực chiến

### Ví dụ 1 — Load template format trước khi tạo file `.md`

**Vấn đề:** Bạn dùng Claude làm research, output file `.md` thường không đúng format bạn muốn.

**Hook:**
- **Trigger:** PreToolUse, khi Claude muốn tạo file `.md`.
- **Action:** Đọc file `format.md` đã định sẵn, append vào prompt.

Cấu hình trong `.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "match": "*.md",
        "command": "cat ./format.md"
      }
    ]
  }
}
```

### Ví dụ 2 — Refresh token Google API khi hết hạn

**Vấn đề:** Bạn dùng các tool liên quan Google. Token thường hết hạn, phải refresh thủ công.

**Hook:**
- **Trigger:** PostToolUse, khi tool trả về output có chứa "token expired".
- **Action:** Chạy script refresh token.

### Ví dụ 3 — Backup cuộc trò chuyện trước khi compact

**Vấn đề:** Sau khi `/compact`, lịch sử chi tiết bị mất.

**Hook:**
- **Trigger:** PreCompact.
- **Action:** Export cuộc trò chuyện sang `chat-history-<timestamp>.txt`.

### Ví dụ 4 — Cắt file Excel trước khi đọc

**Vấn đề:** Bạn xử lý Excel với Claude. Excel 10,000 dòng → Claude tải hết → tốn token kinh khủng.

**Hook:**
- **Trigger:** PreToolUse, khi Claude muốn đọc `.xlsx`.
- **Action:** Chạy script cắt file xuống max 200 dòng.

⚠️ Cẩn thận: cắt file có thể làm mất thông tin quan trọng. Chỉ làm khi bạn chắc 200 dòng đầu đủ.

## Cấu trúc 1 hook

Hooks được khai báo trong `.claude/settings.json`:

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<tool name pattern>",
        "match": "<argument pattern>",
        "command": "<bash command to run>"
      }
    ]
  }
}
```

- **EventName**: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, etc.
- **matcher**: tool name nào match — `Write`, `Bash`, `Read`, etc.
- **match**: pattern match argument (optional).
- **command**: lệnh bash chạy khi trigger.

## Hook scripts

Đa số hooks gọi script Python/Bash đặt trong `.claude/hooks/`:

```
.claude/
├── settings.json
└── hooks/
    ├── inject-date.sh
    ├── refresh-google-token.py
    └── backup-chat.sh
```

`settings.json`:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "command": ".claude/hooks/inject-date.sh"
      }
    ]
  }
}
```

`inject-date.sh`:
```bash
#!/bin/bash
echo "Ngày hôm nay: $(date +%Y-%m-%d)"
```

## ⚠️ Nguyên tắc dùng hooks

Hooks là tính năng mạnh nhưng dễ làm hỏng workflow nếu lạm dụng. **Nguyên tắc:**

1. **Chỉ tạo hook khi workflow 100% dự đoán được mọi case.**
   - Tệ: hook cắt file Excel → có khi cắt mất data quan trọng.
   - Tốt: hook log session summary → không phá gì.

2. **Workflow càng hẹp, càng cụ thể, càng hay gặp → càng nên có hook.**

3. **Nếu vấn đề có thể giải bằng SKILL hoặc CLAUDE.md, ưu tiên 2 cái đó.**
   - SKILL: dễ debug, dễ disable.
   - Hook: chạy tự động → khó debug khi sai.

4. **Đừng dùng hook để "fix" Claude.**
   - Tệ: hook nhắc Claude "không emoji" → Claude vẫn quên, hook không reliable 100%.
   - Tốt: ghi "không emoji" trong `CLAUDE.md`.

## Khi nào dùng hook

| Vấn đề | Dùng | Vì sao |
|---|---|---|
| Inject ngày tháng vào mỗi prompt | Hook | Workflow 100% giống nhau mọi lần |
| Block lệnh `rm -rf` | Hook | An toàn, deterministic |
| Refresh OAuth token | Hook | Trigger rõ ràng, action rõ ràng |
| "Claude nên dùng voice X khi viết" | CLAUDE.md | Quyết định linguistic, không deterministic |
| "Phân tích đối thủ theo framework Y" | SKILL | Quy trình có nhiều bước |
| "Project này dùng stack Z" | CLAUDE.md | Context, không phải hành động |

## Tip thực chiến

- **Bắt đầu không có hook.** Làm việc 1-2 tháng, observe pattern lặp lại → mới build hook.
- **Test hook trước khi commit.** Chạy với dry-run, xem output có đúng không.
- **Document hook trong CLAUDE.md.** Khi đồng đội mở project, biết hook nào đang chạy.

## Khi build hook mới

```
"Tạo cho tôi 1 hook:
- Trigger: trước khi Claude gõ lệnh git push
- Action: chạy lint + typecheck, fail nếu lỗi
Đặt trong .claude/hooks/, config .claude/settings.json."
```

Claude tự setup.

## Hooks hệ thống: SessionStart, UserPromptSubmit

2 hooks bạn có thể muốn setup ngay:

**`SessionStart`** — Inject ngày tháng + active project:
```bash
#!/bin/bash
echo "=== Session start: $(date +'%Y-%m-%d %H:%M') ==="
echo "Working dir: $(pwd)"
echo "Branch: $(git branch --show-current 2>/dev/null || echo 'no git')"
```

**`UserPromptSubmit`** — Reminder voice / convention:
```bash
#!/bin/bash
echo "<reminder>Tiếng Việt, không emoji, súc tích.</reminder>"
```

## Cấm

- Không tạo hook làm side-effect không reversible (xoá file, send email, push code).
- Không tạo hook tốn nhiều token (cat 10,000 dòng từ file → vô nghĩa).
- Không tạo hook chạy lệnh chậm > 5 giây (block UX).

## Tóm tắt

Hooks = automation cho Claude Code, dùng cho workflow deterministic. Không thay thế SKILLs (cho quy trình) hoặc CLAUDE.md (cho context).
