---
name: generating-videos
description: This skill should be used when the user asks to "generate video", "tạo video", "create video with VEO", "tạo video AI", "/generate-video [prompt]", "AI video", "VEO 3 video", "video clip ngắn", "video TikTok AI", "video Instagram AI", or wants Claude Code to generate a short video clip (4-8s) from a text prompt using Google's VEO 3 model via Gemini API. Handles async operation polling (11s-6min latency), downloads MP4 file, saves locally. Includes native audio generation (synced sound effects, ambient, dialogue). End deliverable — video file at output/videos/<slug>.mp4 + metadata JSON với prompt, model, duration, resolution, aspect ratio.
---

# generating-videos

Skill tạo video clip ngắn từ text prompt qua Google VEO 3 (Gemini API). Output = file MP4 saved local + audio embedded + metadata JSON. Phù hợp: short clip cho social (TikTok/Reels/Shorts), product demo, ad teaser, concept visualization.

## Khi nào dùng skill này

User nói một trong các pattern:
- `/generate-video [prompt]` hoặc `/generate-video` (skill sẽ ask prompt)
- "tạo video [mô tả]", "generate video [prompt]"
- "AI video [prompt]", "VEO clip [scene]"
- "tạo TikTok video AI", "tạo Reels concept"

KHÔNG dùng skill này khi:
- User cần video dài >8s (VEO 3 max 8s per generation — cần multi-clip + edit tool)
- User cần edit video có sẵn (skill chỉ tạo từ text, image-to-video xem section khác)
- User cần real footage (không phải AI gen) — search Pexels/Pixabay
- User cần video không kèm audio (VEO 3 always gen audio — disable không support)
- User CHƯA có `GEMINI_API_KEY` — skill sẽ guide setup nhưng cần user apply trước

## Default settings

| Setting | Default | Override khi |
|---|---|---|
| Model | `veo-3.1-fast-generate-preview` (faster, cheaper) | Quality cao hơn → `veo-3.1-generate-preview` |
| Resolution | `720p` | Quality cao hơn → `1080p` hoặc `4k` (require 8s duration) |
| Duration | `8` giây | Shorter clip → `4` hoặc `6` (chỉ với 720p) |
| Aspect ratio | `16:9` (landscape) | Mobile vertical → `9:16` |
| Person generation | `allow_all` (text-to-video) | Có image input → `allow_adult` |
| Output dir | `output/videos/` | User chỉ định path khác |
| Polling interval | 10s | Don't override |
| Max wait | 360s (6 phút) | Don't override (API limit) |

## Pre-conditions

- [ ] `GEMINI_API_KEY` trong `.env` (apply tại https://aistudio.google.com/app/apikey)
- [ ] Python 3.10+ với stdlib `urllib`
- [ ] Internet (Gemini API endpoint)
- [ ] Disk space ~5-50MB per video (tuỳ resolution + duration)
- [ ] Billing enabled trên Google Cloud (VEO 3 paid model, ~$0.40/8s 720p)

Skill check pre-conditions ở Step 1. Fail → báo user fix + dừng.

## Pipeline — 6 bước

Theo thứ tự, không skip.

### Step 1 — Pre-check + read API key

Verify `.env` có `GEMINI_API_KEY`:
```bash
grep "GEMINI_API_KEY=" .env || grep "GEMINI_API_KEY=" .env.local
```

Format: key bắt đầu `AIza...` (Google API key format, ~39 chars). Invalid → ask user re-apply tại https://aistudio.google.com/app/apikey.

**KHÁC OAuth Google**: GEMINI_API_KEY là API key đơn giản, KHÔNG cần OAuth flow. Apply 1 click trong AI Studio.

### Step 2 — Gather spec

Nếu user gọi `/generate-video` không có prompt, hỏi 1 message duy nhất:

```
Mô tả video anh muốn tạo:
1. Prompt (mô tả scene chi tiết, có audio cues nếu cần)
2. Model: fast (cheaper) | standard (quality) | lite (cheapest)
3. Resolution: 720p (default) | 1080p (8s only) | 4k (8s only)
4. Duration: 4s | 6s | 8s
5. Aspect: 16:9 (landscape) | 9:16 (vertical/mobile)
```

Nếu user provide prompt qua argument, skip — dùng default (fast + 720p + 8s + 16:9).

Validate:
- Prompt ≥15 chars
- 1080p/4k → duration buộc 8s
- Aspect chỉ 16:9 hoặc 9:16

### Step 3 — Submit generation request

Run `scripts/generate.py`:
```bash
python .claude/skills/generating-videos/scripts/generate.py \
  --prompt "<prompt>" \
  --model "<model>" \
  --resolution 720p --duration 8 --aspect 16:9
```

Script POST tới:
```
https://generativelanguage.googleapis.com/v1beta/models/{model}:predictLongRunning?key=<API_KEY>
```

Body:
```json
{
  "instances": [{"prompt": "..."}],
  "parameters": {
    "aspectRatio": "16:9",
    "resolution": "720p",
    "durationSeconds": "8",
    "personGeneration": "allow_all"
  }
}
```

Response: `{"name": "operations/abc123..."}` (operation ID).

### Step 4 — Poll operation status

Loop poll mỗi 10s đến khi `done: true` hoặc timeout 6 phút:
```
GET https://generativelanguage.googleapis.com/v1beta/{operation_name}?key=<API_KEY>
```

Print progress tiếng Việt mỗi 30s:
```
[generate] Đang generate video... 30s elapsed (~$0.40 estimated cost)
```

Latency thực tế:
- veo-3.1-fast: 11-60s
- veo-3.1-standard: 60-180s
- veo-3.1-lite: 30-90s

Timeout 6 phút → fail.

### Step 5 — Download MP4 + save local

Khi `done: true`, response có:
```json
{"response": {"generatedVideos": [{"video": {"uri": "gs://...", "mimeType": "video/mp4"}}]}}
```

URI `gs://` là Google Cloud Storage. Cần dùng Gemini Files API để download:
```
GET https://generativelanguage.googleapis.com/v1beta/files/{file_id}?alt=media&key=<API_KEY>
```

Save to `output/videos/<slug>-<timestamp>.mp4`. Metadata JSON cạnh file.

### Step 6 — Report

```
Video generated successfully:

output/videos/<slug>-20260515.mp4 (8s, 720p, 16:9, ~12MB)

Audio: included (native VEO 3 audio)
Cost estimated: ~$0.40

Metadata: output/videos/<slug>-20260515.json

Lưu ý: Server side video retention 2 ngày. Backup local nếu cần lâu hơn.
```

## Decision points

| Step | Hỏi user khi | Auto-proceed khi |
|---|---|---|
| 1 (pre-check) | Key thiếu/sai format | Format OK |
| 2 (spec) | User chưa cung cấp prompt | Argument provided, apply defaults |
| 3 (submit) | HTTP 400 invalid params | 200 OK với operation name |
| 4 (poll) | Timeout 6 phút | done=true |
| 5 (download) | gs URI fetch fail | Save local OK |
| 6 (report) | N/A | — |

## Recovery

| Failure | Fix |
|---|---|
| `GEMINI_API_KEY` thiếu | Apply tại https://aistudio.google.com/app/apikey, add vào `.env` |
| HTTP 400 invalid params | 1080p/4k require duration=8 (skill validate trước call) |
| HTTP 401 invalid key | Re-copy key từ AI Studio, check chưa expire |
| HTTP 403 billing not enabled | Google Cloud project chưa enable billing — VEO paid model |
| HTTP 429 quota exceeded | Đợi quota reset (hourly/daily), hoặc apply increase tại Cloud Console |
| HTTP 500 generation failed | Re-submit (model occasionally fail, latency variance) |
| Polling timeout 6 phút | VEO occasionally slow — retry sau 5 phút |
| gs:// URI download fail | Use Files API endpoint `?alt=media` (skill handle) |
| Prompt content policy | Skip violence, NSFW, real public figures |

## Anti-patterns

- KHÔNG poll faster than 10s (Google rate limit ops queries)
- KHÔNG cache gs:// URI — expire 2 ngày, download ngay
- KHÔNG generate >1 video concurrent với cùng API key (queue, hit rate limit)
- KHÔNG dùng veo-3.1-standard cho draft — dùng -fast hoặc -lite trước, standard chỉ final
- KHÔNG over-prompt audio details — VEO 3 generate audio tự động, prompt audio cues nhẹ enough

## Common pitfalls

1. **1080p/4k buộc duration=8s** — try duration=4 với 1080p → API reject. Skill validate trước.
2. **Audio không thể disable** — VEO 3 always generate. Nếu cần silent, mute post-process bằng ffmpeg.
3. **First gen lâu** — VEO model warm up, first call có thể chậm hơn average 30s.
4. **2-day retention** — server xoá video sau 2 ngày. Backup local hoặc upload Drive ngay.
5. **Cost surprise** — VEO 3 paid. 720p/8s ~$0.40, 1080p ~$0.80, 4k ~$1.60. Báo user trước.
6. **Polling burns quota** — mỗi GET operation count vào quota. Poll 10s interval, max 6 phút = 36 polls per gen.
7. **Audio sync issue rare** — đôi khi audio không match lip nếu prompt người nói. Re-gen thường fix.

## Skill files

| File | Purpose | Khi nào load |
|---|---|---|
| `references/veo-models-comparison.md` | 3 VEO variants + pricing + use case | User hỏi "dùng model nào" |
| `references/prompt-engineering.md` | Tips viết prompt cho VEO (motion + audio cues) | User prompt quality kém |
| `references/troubleshooting.md` | Errors detail per HTTP code + recovery | Step fail |
| `scripts/generate.py` | Submit + poll + download + save | Step 3-5 |
| `scripts/smoke_test.py` | Verify API key + test gen 4s clip | Manual test |
| `assets/env.template` | Skeleton `.env` với GEMINI_API_KEY | Step 1 (nếu .env không tồn tại) |

## Tiêu chí chất lượng (self-check)

Trước khi report Step 6:
- [ ] MP4 file tồn tại tại `output/videos/<slug>.mp4`
- [ ] File size 2-50MB (typical 720p/8s ~10MB, 1080p ~25MB, 4k ~50MB)
- [ ] Metadata JSON cạnh video, đủ field
- [ ] Total elapsed time logged (cho user biết cost)
- [ ] Path absolute trong report

## Voice rules

- Tiếng Việt direct, imperative
- KHÔNG emoji
- BÁO COST estimated trước khi call (~$0.40 cho 720p/8s)
- Note retention 2 ngày (user cần backup nếu giữ lâu)

## Sample timing

- Step 1 pre-check: <1s
- Step 2 gather spec: 30s (user input)
- Step 3 submit: <2s
- Step 4 poll + wait: **11s - 6 phút** (tuỳ model)
- Step 5 download: 5-30s tuỳ size
- Step 6 report: <1s

**Total: 30 giây - 6 phút** từ prompt đến MP4 ready. Cost ~$0.40-1.60 per video.
