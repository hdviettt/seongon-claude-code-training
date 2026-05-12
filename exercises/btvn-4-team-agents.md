# BTVN buổi 4 — Team Sub-Agents

## Đề bài

Từ workspace BTVN buổi 3, **nâng cấp thành team sub-agents**:

- Tạo **≥ 2 sub-agents**.
- Mỗi sub-agent có **≥ 2 SKILLs** để dùng.
- Giao **1 nhiệm vụ lớn** cho Claude Code → để nó tự phân bổ task cho các sub-agents phù hợp.

## Output

| STT | Output | Format |
|---|---|---|
| 1 | Files và folder workspace trên GitHub repo | Github repo (có folder `.claude/`, trong đó có `/skills/` và `/agents/`) |
| 2 | File ghi chép lịch sử trò chuyện với Claude (`/export`) | `.txt` |
| 3 | Các file output từ việc giao việc cho Agent và sử dụng SKILLs | Tự do |

## Cách nộp

Setup GitHub repo public, push code, gán link vào form SEONGON.

## Rules

- Làm mọi cách để đạt được kết quả cuối cùng.
- Không đặt câu hỏi cho trợ giảng (mà chưa) đặt câu hỏi cho Claude Code.

## Deadline

23h59 Thứ 5 của tuần học buổi 4.

## Gợi ý — 2 setup mẫu

### Setup 1 — Team làm Web App

```
Sub-agents:
- frontend-specialist (chuyên thiết kế UI/UX)
- backend-specialist (chuyên API, DB)
- security-specialist (chuyên audit bảo mật)

SKILLs cho frontend-specialist:
- /design-component (xây component theo design system)
- /responsive-check (audit responsive)

SKILLs cho backend-specialist:
- /design-api (thiết kế REST API endpoint)
- /db-schema (thiết kế DB schema)

SKILLs cho security-specialist:
- /security-audit (audit OWASP basic)
- /env-check (check secret leakage)

Nhiệm vụ lớn: "Build cho tôi 1 web app SaaS quản lý task team nhỏ"
→ Claude dispatch:
  1. frontend-specialist → design UI (gọi /design-component)
  2. backend-specialist → design API + DB (gọi /design-api, /db-schema)
  3. Build code thực thi
  4. security-specialist audit (gọi /security-audit, /env-check)
```

### Setup 2 — Team làm SEO

```
Sub-agents:
- content-seo-specialist
- technical-seo-specialist
- geo-specialist (GEO = Generative Engine Optimization)

SKILLs cho content-seo-specialist:
- /keyword-research (kết nối SerpAPI)
- /content-brief (template + voice guide)

SKILLs cho technical-seo-specialist:
- /technical-audit (audit code SEO)
- /schema-markup (tạo schema markup)

SKILLs cho geo-specialist:
- /aio-analysis (phân tích AI Overviews)
- /citation-check (check brand được cite trong AIO)

Nhiệm vụ lớn: "Lên chiến lược SEO toàn diện cho seongon.com cho Q3"
→ Claude dispatch:
  1. content-seo-specialist → research từ khoá → content plan
  2. technical-seo-specialist → audit kỹ thuật site
  3. geo-specialist → phân tích AIO competitor
  4. Tổng hợp thành 1 PLAN.md đầy đủ
```

## Cách bắt đầu

```
Nâng cấp workspace BTVN buổi 3 của tôi:

1. Tạo 3 sub-agents trong .claude/agents/:
   - seo-content-specialist
   - seo-technical-specialist
   - geo-specialist

   Mỗi agent có description rõ, role rõ, tools phù hợp.

2. Cho mỗi agent có ≥ 2 SKILLs để dùng. SKILLs đã có sẵn từ 
   BTVN trước, agent chỉ cần biết khi nào gọi skill nào.

3. Update CLAUDE.md để mô tả team này.

Sau đó tôi sẽ giao nhiệm vụ lớn để test.
```

Sau khi setup xong, test bằng nhiệm vụ lớn:
```
Lên chiến lược SEO toàn diện cho 1 brand hosting (ví dụ: 
seongon.com) cho Q3-2026.

Bao gồm:
- Phân tích từ khoá top 50.
- Audit kỹ thuật current state.
- Phân tích AI Overviews các từ khoá quan trọng.
- Tổng hợp thành PLAN.md.

Hãy tự dispatch task cho sub-agents phù hợp. Tôi sẽ theo dõi.
```

Quan sát Claude có dispatch đúng agent không. Nếu chưa đúng, edit `description` của agent cho rõ hơn.

## Tips từ khoá trước

- **`description` của sub-agent rất quan trọng.** Đó là cách agent chính quyết khi nào dispatch. Viết description chi tiết, có trigger word rõ ràng.
- **Limit `tools` của sub-agent.** Đừng cho mọi agent full quyền. Ví dụ: agent research chỉ cần `Read, Glob, Grep, WebFetch, WebSearch` — không cần `Write`, `Edit`.
- **Mỗi sub-agent 1 model phù hợp.** Agent strategy (làm plan) → opus. Agent thực thi → sonnet. Agent đơn giản (rename file, format JSON) → haiku.
- **Test trước khi nộp.** Giao 1-2 nhiệm vụ lớn, xem Claude dispatch có hợp lý không.

## Kiến thức liên quan

- [`knowledge/04-agents-memory-hooks/sub-agents.md`](../knowledge/04-agents-memory-hooks/sub-agents.md)
- [`knowledge/04-agents-memory-hooks/memory.md`](../knowledge/04-agents-memory-hooks/memory.md) — Update CLAUDE.md để biết team.
- [`knowledge/03-mo-rong-claude-code/skills-co-ban.md`](../knowledge/03-mo-rong-claude-code/skills-co-ban.md) — SKILLs cho agents dùng.
