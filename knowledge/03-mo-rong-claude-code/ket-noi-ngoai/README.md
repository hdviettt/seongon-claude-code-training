# Kết nối Claude Code với thế giới ngoài

Claude Code mạnh vì nó truy cập được hệ thống ngoài. 3 cách kết nối:

| Cách | Mô tả | Khi nào dùng |
|---|---|---|
| **API** | Claude gọi 1 endpoint cụ thể qua HTTP | Có 1 tác vụ riêng cần lấy data (vd: lấy top 10 SERP cho từ khoá) |
| **MCP** | Claude có cả 1 bộ tool sẵn, tự quyết khi nào dùng | Cần làm việc nhiều với 1 platform (WordPress, Figma, Google Ads) |
| **CLI** | Claude gọi lệnh terminal | Tương tác với môi trường lập trình (GitHub, Railway, Vercel) |

## 1. API — Application Programming Interface

### Định nghĩa

API là cách 2 hệ thống "nói chuyện" với nhau qua HTTP. Bạn gửi request, nhận response.

### Ví dụ

**SerpAPI** — API để lấy kết quả Google Search:

```python
import requests

response = requests.get(
    "https://serpapi.com/search",
    params={
        "q": "claude code là gì",
        "api_key": "YOUR_KEY",
        "hl": "vi",
        "gl": "vn"
    }
)
results = response.json()
```

Claude Code chạy script này → lấy được top 10 Google cho từ khoá.

### Các API phổ biến cho SEO / Ads

- **SerpAPI** (https://serpapi.com) — kết quả Google, Bing, YouTube. ~$50/tháng cho gói nhỏ.
- **DataForSEO** (https://dataforseo.com) — keyword data, SERP, backlinks.
- **Google Ads API** — quản lý campaign Ads.
- **Google Search Console API** — data SEO của site bạn.
- **Anthropic API** — gọi Claude từ script (tự build app AI).

### Cách dùng API trong SKILL

Setup:
1. Đăng ký service, lấy API key.
2. Lưu key vào file `.env` (KHÔNG commit):
   ```
   SERPAPI_KEY=abc123...
   ```
3. Trong SKILL, có script Python/Node đọc key và gọi API.
4. SKILL.md mention cách chạy script.

Xem ví dụ: [`examples/research-skill/`](examples/research-skill/) trong folder này.

### Trade-off

- **Pro:** simple, control rõ ràng — bạn biết Claude đang gọi cái gì.
- **Con:** mỗi API cần 1 script riêng. Nhiều API = nhiều script.

## 2. MCP — Model Context Protocol

### Định nghĩa

MCP là **standard** Anthropic định nghĩa để Claude làm việc với 1 platform. Khác API ở chỗ:

- API: 1 endpoint = 1 tác vụ.
- MCP: 1 server = nhiều tool. Claude tự quyết khi nào dùng tool nào.

Hình dung:
- API = bạn đưa Claude 1 cái búa, bảo "đóng cái đinh này".
- MCP = bạn đưa Claude 1 hộp dụng cụ (búa + tua-vít + cờ-lê), bảo "sửa cái bàn này đi" — Claude tự chọn dụng cụ phù hợp.

### MCP server phổ biến

- **WordPress MCP** — đăng bài, sửa post, quản lý plugin.
- **Playwright MCP** — tự động hoá browser (scrape, test UI).
- **Netlify MCP** — deploy site lên Netlify.
- **Figma MCP** — đọc design file, lấy spec component.
- **Google Ads MCP** — quản lý campaign.
- **Google Search Console MCP** — kéo data SEO.
- **GitHub MCP** — tương tác với GitHub repo.

### Cách cài MCP

Mỗi MCP server có hướng dẫn riêng. Pattern chung:

1. Cài MCP server (thường là npm package hoặc binary).
2. Thêm config vào `.claude/mcp.json`:
   ```json
   {
     "mcpServers": {
       "wordpress": {
         "command": "node",
         "args": ["path/to/wp-mcp-server.js"],
         "env": {
           "WP_URL": "https://yoursite.com",
           "WP_USER": "admin",
           "WP_PASS": "..."
         }
       }
     }
   }
   ```
3. Restart Claude Code.
4. Gõ `/mcp` để check MCP đã kết nối chưa.

Khi MCP ready, bạn nói tự nhiên với Claude:
> "Đăng bài này lên WordPress"

Claude sẽ tự dùng WordPress MCP để đăng — bạn không phải nói chi tiết tool nào.

### Trade-off

- **Pro:** rất mạnh, Claude tự quyết, ít prompt.
- **Con:** setup ban đầu phức tạp. Khó debug khi sai.

## 3. CLI — Command Line Interface

### Định nghĩa

CLI là **lệnh terminal** của 1 platform. Claude chạy lệnh trực tiếp.

Ví dụ:
- `gh repo create my-app --public` — tạo GitHub repo.
- `railway up` — deploy lên Railway.
- `vercel --prod` — deploy lên Vercel.
- `wp post create --post_title="Hello"` — tạo post WordPress (WP-CLI).

### CLI phổ biến

- **`gh`** — GitHub CLI. Cài: `winget install GitHub.cli` (Win) hoặc `brew install gh` (Mac).
- **`railway`** — Railway CLI.
- **`vercel`** — Vercel CLI.
- **`netlify`** — Netlify CLI.
- **`firebase`** — Firebase CLI.
- **`gcloud`** — Google Cloud CLI.
- **`aws`** — AWS CLI.
- **`docker`** — Docker.

### Cách dùng

1. Cài CLI lên máy.
2. Authenticate: `<cli> login` hoặc tương đương.
3. Trong Claude Code, bạn yêu cầu task — Claude tự chạy CLI:
   ```
   "Deploy app này lên Vercel"
   ```
   Claude sẽ chạy `vercel --prod` → ra URL.

### Trade-off

- **Pro:** rất phổ biến, mọi platform deploy hiện đại đều có CLI.
- **Con:** mỗi platform 1 CLI khác nhau, syntax khác nhau.

## So sánh API vs MCP vs CLI

| Tiêu chí | API | MCP | CLI |
|---|---|---|---|
| **Phạm vi** | 1 tác vụ cụ thể | 1 platform với nhiều tool | 1 platform với nhiều lệnh |
| **Setup** | Đơn giản (key + script) | Phức tạp (server + config) | Trung bình (cài CLI + auth) |
| **Claude tự quyết** | Không (bạn quyết) | Có | Một phần |
| **Debug** | Dễ | Khó | Trung bình |
| **Khi nào dùng** | Tác vụ riêng lẻ, có data | Tương tác phức tạp với 1 platform | Deploy / config / DevOps |

## Tip thực chiến

**Bắt đầu với API** — đơn giản, kiểm soát rõ.

**Khi 1 platform được dùng quá nhiều** (đăng 10 bài WordPress / tuần), upgrade lên MCP để Claude tự quản lý.

**Mọi platform deploy đều dùng CLI** — `gh`, `railway`, `vercel`. Cài 3 cái này là đủ.

**Không pha tạp** — đừng tạo 5 SKILL cho 5 API trong khi MCP đã có sẵn cho cùng platform.

## Ví dụ thực chiến

Xem [`examples/research-skill/`](examples/research-skill/) — SKILL research dùng SerpAPI để lấy data Google.

## Tiếp theo

- Để build SKILL có file đi kèm, đọc [`cau-truc-skill.md`](cau-truc-skill.md).
- Để mở rộng với sub-agents, đọc `knowledge/04-agents-memory-hooks/`.
