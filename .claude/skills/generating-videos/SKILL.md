---
name: generating-videos
description: This skill should be used when the user asks to "generate video", "tạo video", "create video with VEO", "create video with Sora", "tạo video AI", "/generate-video [prompt]", "AI video", "VEO 3 video", "Sora 2 video", "Kling video", "video clip ngắn", "video TikTok AI", "video Instagram AI", or wants Claude Code to generate a short video clip from a text prompt via Together AI's video API. Supports 30+ video models: Google VEO 3.0 / VEO 3.0 audio / VEO 2.0, OpenAI Sora 2 / Sora 2 Pro, Kling 2.1, Hailuo, Vidu, Seedance, Wan, Pixverse. Handles async job polling (30s-4min), downloads MP4, saves locally. End deliverable — video file at output/videos/<slug>.mp4 + metadata JSON với model + cost + size + duration + job_id.
---

# generating-videos

Skill tạo video clip từ text prompt qua Together AI's video API. Output = MP4 saved local + metadata JSON. 30+ video models support: VEO 3, Sora 2, Kling, Hailuo, Vidu, Seedance.

Phù hợp: short clip social (TikTok/Reels/Shorts), product demo, ad teaser, concept visualization.

## Khi nào dùng skill này

User nói một trong các pattern:
- `/generate-video [prompt]` hoặc `/generate-video` (skill sẽ ask prompt)
- "tạo video [mô tả]", "generate video [prompt]"
- "VEO 3 video", "Sora video", "Kling video"
- "tạo TikTok video AI", "tạo Reels concept"

KHÔNG dùng skill này khi:
- User cần video dài >8s (most models max 6-8s, Kling 2.1 max ~15s)
- User cần edit video có sẵn (skill chỉ tạo từ text)
- User cần real footage (không AI gen) — search Pexels/Pixabay
- User CHƯA có `TOGETHER_AI_API_KEY` — apply trước

## Default settings

| Setting | Default | Override khi |
|---|---|---|
| Model | `google/veo-3.0` (premium quality, native audio) | Faster + cheaper → `google/veo-3.0-fast`; alternative → `openai/sora-2-pro`, `kwaivgI/kling-2.1-master` |
| Aspect ratio | `16:9` (landscape, 1920×1080) | Mobile vertical → `9:16` (1080×1920) |
| Output dir | `output/videos/` | User chỉ định khác |
| Polling interval | 15s | Don't override (rate limit) |
| Max wait | 600s (10 phút) | Don't override (API limit) |
| Language | Tiếng Việt báo cáo | User chỉ nói tiếng Anh |

## Pre-conditions

- [ ] `TOGETHER_AI_API_KEY` trong `.env` (apply tại https://api.together.ai/settings/api-keys)
- [ ] Together AI account có credit (video gen $0.20-1.60+ per clip)
- [ ] Python 3.10+, internet
- [ ] Disk space ~5-50MB per video

Skill check pre-conditions ở Step 1.

## Pipeline — 6 bước

### Step 1 — Pre-check + read API key

Verify `.env` có `TOGETHER_AI_API_KEY`. Same key cho cả image + video gen (Together unified API).

### Step 2 — Gather spec

Nếu user gọi `/generate-video` không có prompt, hỏi 1 message:

```
Mô tả video anh muốn tạo:
1. Prompt (mô tả scene chi tiết, có audio cues nếu cần)
2. Model: veo-3.0-fast (default, $0.80/clip) | veo-3.0 (premium) | sora-2 | kling-2.1-standard (cheaper)
3. Aspect: 16:9 (landscape, default) | 9:16 (vertical/mobile)
```

Nếu user provide prompt qua argument, skip — dùng defaults.

Validate prompt ≥15 chars.

### Step 3 — Submit job

Run `scripts/generate.py`:
```bash
python .claude/skills/generating-videos/scripts/generate.py \
  --prompt "<prompt>" --model "<model>" --aspect "<aspect>"
```

Script POST tới:
```
POST https://api.together.xyz/v2/videos
```

Body:
```json
{
  "model": "google/veo-3.0-fast",
  "prompt": "...",
  "size": "1920x1080"
}
```

Response: `{id, status: "in_progress", seconds, size, created_at}`.

### Step 4 — Poll job status

Loop GET `/v2/videos/{id}` mỗi 15s đến status `completed`. Max wait 10 phút.

Latency thực tế:
- veo-3.0-fast: 30s-4 phút
- veo-3.0: 2-6 phút
- sora-2: 1-3 phút
- kling models: varied

Skill print progress mỗi 30s.

### Step 5 — Download MP4 + save local

Khi `status: completed`, response có:
```json
{
  "outputs": {
    "cost": 0.8,
    "video_url": "https://api.together.ai/shrt/..."
  }
}
```

Script download URL + save to `output/videos/<slug>-<timestamp>.mp4`. KHÔNG tạo metadata JSON sidecar — info trả về qua stdout JSON cho parent process.

### Step 6 — Report

```
Video generated successfully:

output/videos/<slug>-20260515.mp4 (8s, 1920×1080, ~14MB)

Model: google/veo-3.0
Cost: $1.20
Total time: 4 phút

Lưu ý: URL Together expire 24h. File đã save local persistent.
```

## Decision points

| Step | Hỏi user khi | Auto-proceed khi |
|---|---|---|
| 1 (pre-check) | Key thiếu/sai | Format OK |
| 2 (spec) | User chưa cung cấp prompt | Argument provided |
| 3 (submit) | HTTP 400 invalid model | 200 với job id |
| 4 (poll) | Timeout 10 phút | status=completed |
| 5 (download) | URL fetch fail | Save OK |
| 6 (report) | N/A | — |

## Recovery

| Failure | Fix |
|---|---|
| `TOGETHER_AI_API_KEY` thiếu | Apply tại https://api.together.ai/settings/api-keys |
| HTTP 401 invalid key | Re-copy key từ dashboard |
| HTTP 402 insufficient credit | Nạp tiền tại https://api.together.ai/settings/billing |
| HTTP 400 invalid model | Verify model name từ `references/video-models-comparison.md` |
| HTTP 429 rate limit | Đợi 60s retry |
| HTTP 500 internal | Retry sau 30s |
| Job status `failed` | Re-submit với prompt khác (content policy fail) |
| Polling timeout 10 phút | Job stuck — re-submit |
| Download URL 404 | URL expire 24h — script download ngay sau done (handled) |

## Anti-patterns

- KHÔNG poll faster than 15s (rate limit)
- KHÔNG cache video URL (expire 24h)
- KHÔNG dùng veo-3.0 (premium) cho draft — dùng veo-3.0-fast hoặc kling cheaper trước
- KHÔNG share API key (mỗi user/team key riêng)
- KHÔNG generate >2 video concurrent (queue, hit rate limit)

## Common pitfalls

1. **Cost varies model** — veo-3.0-fast $0.80, veo-3.0 ~$1.20, sora-2-pro ~$1.50. Báo user trước khi gen.
2. **`size` param thay vì `aspect_ratio`** — Together API dùng `size` (vd "1920x1080"), không phải `aspectRatio`. Wrapper handle conversion.
3. **All VEO models include audio** — VEO 3.0 series có audio (synced sound). Sora 2 cũng có. Kling không.
4. **URL expire 24h** — Together store temporary. Skill download ngay.
5. **First gen lâu hơn average** — model warm up, sub gen nhanh hơn.
6. **Same TOGETHER_AI_API_KEY cho image + video** — unified credit pool.

## Skill files

| File | Purpose | Khi nào load |
|---|---|---|
| `references/video-models-comparison.md` | 6 model families: VEO/Sora/Kling/Hailuo/Vidu/Seedance — pricing + use case | User hỏi "dùng model nào" |
| `references/prompt-engineering.md` | Tips viết prompt cho video models | User prompt quality kém |
| `references/troubleshooting.md` | Errors detail per HTTP code | Step fail |
| `scripts/generate.py` | Submit + poll + download + save | Step 3-5 |
| `scripts/smoke_test.py` | Verify API key + endpoint reachable | Manual test |
| `assets/env.template` | Skeleton `.env` với TOGETHER_AI_API_KEY | Step 1 |

## Tiêu chí chất lượng (self-check)

Trước khi report Step 6:
- [ ] MP4 file exists ở `output/videos/<slug>.mp4`
- [ ] File size 2-50MB
- [ ] Total time logged
- [ ] Cost reported
- [ ] Path absolute trong report

## Voice rules

- Tiếng Việt direct, imperative
- KHÔNG emoji
- BÁO COST estimated trước call (~$0.80 cho veo-3.0-fast)
- Note URL expire 24h

## Sample timing

- Step 1-2: 30s
- Step 3 submit: <2s
- Step 4 poll: 30s-4 phút (model varies)
- Step 5 download: 10-30s
- Step 6 report: <1s

**Total: 1-5 phút** từ prompt đến MP4 ready. Cost $0.20-1.60 per video.
