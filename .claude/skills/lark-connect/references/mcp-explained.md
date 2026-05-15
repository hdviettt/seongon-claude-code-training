# MCP với Lark — Vì sao skill này dùng MCP, không phải raw API

## Contents
- [MCP là gì](#mcp-là-gì)
- [Vì sao dùng MCP với Lark thay vì raw API](#vì-sao-dùng-mcp-với-lark-thay-vì-raw-api)
- [Architecture: Claude → MCP → Lark](#architecture-claude--mcp--lark)
- [Khác biệt với google-connect](#khác-biệt-với-google-connect)
- [Khi nào KHÔNG dùng MCP](#khi-nào-không-dùng-mcp)

---

## MCP là gì

**MCP** (Model Context Protocol) là protocol chuẩn Anthropic để AI agent (Claude) gọi external tools.

Workflow:
1. User nói "gửi Lark cho group X" → Claude
2. Claude detect cần tool Lark → list available MCP tools
3. Claude pick `im.v1.message.create` → call MCP server với params
4. MCP server (lark-mcp) translate → HTTP call tới Lark API
5. Lark API return → MCP → Claude → user

Claude KHÔNG cần biết Lark HTTP endpoint format. MCP server xử lý hết.

---

## Vì sao dùng MCP với Lark thay vì raw API

| | Raw API approach | MCP approach (skill này) |
|---|---|---|
| Setup | Write custom Python scripts cho mỗi tính năng | Install 1 package: `@larksuiteoapi/lark-mcp` |
| Tools available | Chỉ tools mình code | 50+ tools official ship sẵn |
| Maintenance | User maintain code, update API breaking changes | Lark team maintain MCP server |
| Token refresh | User code logic refresh + hook | lark-mcp tự refresh internal |
| Type safety | User parse JSON manual | MCP schema validate input/output |
| New API | User wait → code | Auto-available khi Lark add tool |

Lark có sẵn official MCP — phí phạm nếu reinvent.

---

## Architecture: Claude → MCP → Lark

```
┌─────────────────────────────────────────────┐
│  Claude Code session                         │
│  ┌──────────────────────────────────────┐    │
│  │ User: "Gửi Lark cho group Atlas:     │    │
│  │       Team report sẵn sàng"          │    │
│  └────────────────┬─────────────────────┘    │
│                   │                          │
│                   ▼                          │
│  ┌──────────────────────────────────────┐    │
│  │ Claude: detect cần tool messaging    │    │
│  │ → call im.v1.message.create          │    │
│  │   {receive_id: "group_atlas",        │    │
│  │    content: "Team report sẵn sàng"}  │    │
│  └────────────────┬─────────────────────┘    │
└───────────────────┼──────────────────────────┘
                    │ stdio JSON-RPC
                    ▼
┌─────────────────────────────────────────────┐
│  lark-mcp server (process spawn by CC)       │
│  ┌──────────────────────────────────────┐    │
│  │ Load token từ ~/.lark-mcp/           │    │
│  │ Translate JSON → HTTP POST           │    │
│  │ POST https://open.larksuite.com/     │    │
│  │      open-apis/im/v1/messages        │    │
│  │      Authorization: Bearer <token>   │    │
│  └────────────────┬─────────────────────┘    │
└───────────────────┼──────────────────────────┘
                    │ HTTPS
                    ▼
┌─────────────────────────────────────────────┐
│  Lark Open Platform API                      │
│  → Lark Suite database                       │
│  → Message delivered to group Atlas          │
└─────────────────────────────────────────────┘
```

---

## Khác biệt với google-connect

`google-connect` skill viết custom Python scripts (`oauth_refresh.py`, hook PostToolUse) vì Google KHÔNG có official MCP server cho non-enterprise users.

`lark-connect` skill wrap official lark-mcp + dùng **tenant mode** — không cần OAuth flow, đơn giản hơn nhiều.

| Aspect | google-connect | lark-connect (tenant mode) |
|---|---|---|
| Authentication | OAuth user flow (custom Python ~100 lines) | tenant_access_token (lark-mcp tự handle) |
| Token refresh | Custom hook PostToolUse | lark-mcp internal |
| API calls | Claude generate Python code → run | Claude call MCP tool directly |
| Config file | `.env` only | `.env` + `.mcp.json` |
| Browser OAuth | YES (mỗi lần token expire) | NO (tenant mode bypass) |
| Restart needed | No | YES (sau khi `.mcp.json` thay đổi) |
| Tools count | Whatever user code | 17 default (200+ available custom) |
| Setup time | 10-15 phút | 5-7 phút |

google-connect = OAuth user mode (read personal data).
lark-connect = tenant bot mode (act as bot — phù hợp 80% use case SEONGON).

**Note về user_access_token mode cho Lark**: lark-mcp support OAuth user mode nhưng hiện có bug với Larksuite (error 20029 dù setup chuẩn). Skill `lark-connect` chỉ support tenant mode để tránh bug này. Khi user cần user mode, đợi lark-mcp upstream fix.

**Khi build skill mới cho 1 platform**: check first xem có official MCP không. Có → wrap MCP. Không → write custom scripts như google-connect.

---

## Khi nào KHÔNG dùng MCP

Edge case không nên dùng MCP path:

### 1. One-off webhook trigger

Nếu chỉ cần gửi 1 message khi event X happen (không có Claude trong loop), webhook URL Lark đủ:
```bash
curl -X POST https://open.larksuite.com/open-apis/bot/v2/hook/<WEBHOOK_ID> \
  -H "Content-Type: application/json" \
  -d '{"msg_type":"text","content":{"text":"hello"}}'
```

Đơn giản hơn full MCP setup.

### 2. Background job 24/7

MCP server spawn khi CC session active. Nếu cần job chạy 24/7 không có CC session, dùng Lark SDK trực tiếp (`@larksuiteoapi/node-sdk`).

### 3. Custom business logic

MCP expose generic tools. Nếu cần logic "if A then B then C" với multi-step orchestration → write app riêng, không dùng MCP.

Cho hầu hết use case của marketing/operations Vietnam → MCP path phù hợp. Skill `lark-connect` cover đúng case này.

---

## References

- MCP protocol spec: https://modelcontextprotocol.io
- lark-mcp repository: https://github.com/larksuite/lark-openapi-mcp
- lark-mcp npm: https://www.npmjs.com/package/@larksuiteoapi/lark-mcp
- Claude Code MCP docs: https://code.claude.com/docs/en/mcp
