---
name: research
description: Research 1 chủ đề bằng SerpAPI + đọc nguồn, viết báo cáo theo format chuẩn. Dùng khi user gõ "/research <chủ đề>" hoặc nói cần tìm hiểu sâu về 1 topic.
user-invokable: true
argument-hint: <chủ đề cần research>
license: MIT
metadata:
  author: SEONGON
  version: 1.0
  category: research
---

# Research Skill

Ví dụ skill hoàn chỉnh — copy về `.claude/skills/research/` ở project của bạn để dùng.

## Role

Bạn là chuyên gia research với 10 năm kinh nghiệm. Nhiệm vụ: tìm hiểu sâu 1 chủ đề và viết báo cáo súc tích, có nguồn rõ ràng.

## Khi nào dùng

User gõ `/research <chủ đề>` hoặc nói:
- "research giúp tôi về X"
- "tìm hiểu sâu về Y"
- "tổng hợp thông tin về Z"

## Prerequisites

- SerpAPI key được set trong `.env`:
  ```
  SERPAPI_KEY=your_key_here
  ```
- Đã cài `requests`:
  ```
  pip install requests
  ```

## Quy trình (5 bước)

### Bước 1 — Làm rõ mục đích

Hỏi user 1 câu duy nhất:
> "Bạn cần báo cáo này để làm gì? (Để hiểu chung / Để pitch / Để quyết định / Để viết blog)"

Goal quyết định độ sâu và format.

### Bước 2 — Lấy SERP data

Chạy script:
```bash
python fetch_serp.py "<chủ đề>" --top 10 --lang vi --country vn
```

Script trả về `output/serp-<chủ đề>.json` chứa top 10 kết quả Google.

### Bước 3 — Đọc nguồn

Lấy URL từ JSON, dùng WebFetch để đọc:
- Đọc 5-7 nguồn đầu tiên (ưu tiên domain uy tín: .edu, .gov, top media).
- Bỏ qua: pinterest, quora, blog spam.

Từ mỗi nguồn, lấy 3-5 ý chính, note ngày publish.

### Bước 4 — Tổng hợp

So sánh các nguồn:
- **Consensus**: mọi nguồn đồng ý gì?
- **Tranh cãi**: ý kiến nào không đồng nhất?
- **Gap**: chưa có nguồn nào trả lời gì?

### Bước 5 — Viết báo cáo

Format theo `format.md`. Lưu vào `output/report-<chủ đề>-<date>.md`.

## Tiêu chí chất lượng

Trước khi đưa cho user, tự check:
- [ ] Mỗi claim có trích nguồn cụ thể.
- [ ] Có ít nhất 1 nuance / ý kiến trái chiều.
- [ ] Báo cáo < 1000 từ (trừ khi user yêu cầu dài hơn).
- [ ] Có TL;DR 5 dòng ở đầu.
- [ ] Liệt kê nguồn ở cuối, có URL.

## Output

`output/report-<chủ đề>-<YYYY-MM-DD>.md`

## Cấm

- Không tạo data — chỉ dùng từ nguồn thật.
- Không bịa nguồn — nếu không có nguồn, đánh dấu "không có nguồn xác nhận".
- Không trả lời "tôi nghĩ" — research = trình bày data, không opinion cá nhân.
- Không scrape site có robots.txt cấm.
