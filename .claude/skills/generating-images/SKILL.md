---
name: generating-images
description: This skill should be used when the user asks to "generate image", "tạo ảnh", "create image with FLUX", "tạo hình ảnh AI", "/generate-image [prompt]", "make AI art", "tạo banner", "tạo thumbnail", "FLUX image", "Together AI image", or wants Claude Code to generate an image from a text prompt using Together AI's FLUX models (FLUX.1-schnell free, FLUX.1-dev, FLUX.1.1-pro, FLUX.2-pro/max). Produces image file saved locally with model + prompt + dimensions chosen per user spec. End deliverable — image file at output/images/<slug>.jpg (or .png) + metadata JSON với prompt, model, dimensions, seed.
---

# generating-images

Skill tạo ảnh từ text prompt qua Together AI FLUX models. Output = file image saved local + metadata JSON. Phù hợp: thumbnail, banner, social post, mockup, concept art.

## Khi nào dùng skill này

User nói một trong các pattern:
- `/generate-image [prompt]` hoặc `/generate-image` (skill sẽ ask prompt)
- "tạo ảnh [mô tả]", "generate image [prompt]"
- "tạo banner cho [event]", "tạo thumbnail cho [video]"
- "FLUX [prompt]", "AI image [prompt]"

KHÔNG dùng skill này khi:
- User cần edit ảnh có sẵn (skill chỉ tạo từ text, KHÔNG image-to-image — dùng FLUX.1-kontext skill khác)
- User cần upscale ảnh (dùng skill upscaling riêng)
- User cần > 4 ảnh cùng prompt (đổi `n` trong call, max API limit)
- User cần ảnh không qua AI (vd stock photo) — search Unsplash

## Default settings

| Setting | Default | Override khi |
|---|---|---|
| Model | `black-forest-labs/FLUX.1-kontext-max` (premium quality, supports text-to-image + image-to-image) | Quick test free → `FLUX.1-schnell`; quality cao hơn → `FLUX.2-max` |
| Dimensions | 1024×1024 | User chỉ định (vd 1920×1080, 1080×1920, etc.) |
| Steps | 4 (schnell) hoặc 28 (dev/pro) | Cao hơn = chất lượng tăng nhưng chậm + tốn credit |
| Number of images | 1 | User muốn nhiều variation → 2-4 |
| Output dir | `output/images/` | User chỉ định path khác |
| Output format | JPG | User cần PNG cho transparency |
| Language | Tiếng Việt báo cáo | User chỉ nói tiếng Anh |

## Pre-conditions

- [ ] `TOGETHER_AI_API_KEY` trong `.env` (apply tại https://api.together.ai/settings/api-keys)
- [ ] Python 3.10+ với `urllib` (stdlib, không cần pip install)
- [ ] Internet (Together AI endpoint)
- [ ] Disk space (~50KB-2MB per image tuỳ dimension + model)

Skill check pre-conditions ở Step 1. Fail → báo user fix + dừng.

## Pipeline — 5 bước

Theo thứ tự, không skip.

### Step 1 — Pre-check + read API key

Verify `.env` (hoặc `.env.local`) có `TOGETHER_AI_API_KEY`:
```bash
grep "TOGETHER_AI_API_KEY=" .env || grep "TOGETHER_AI_API_KEY=" .env.local
```

Format check: key bắt đầu `tgp_v1_` + 40+ chars. Invalid → ask user re-paste từ https://api.together.ai/settings/api-keys.

### Step 2 — Gather spec

Nếu user gọi `/generate-image` không có prompt, hỏi 1 message duy nhất:

```
Mô tả ảnh anh muốn tạo:
1. Prompt (mô tả ảnh chi tiết, tiếng Anh cho chất lượng cao nhất)
2. Model: schnell (free, fast) | pro (quality, ~$0.04) | max (best, ~$0.10)
3. Dimensions: 1024x1024 (square) | 1920x1080 (landscape) | 1080x1920 (portrait) | custom
4. Số lượng: 1 | 2 | 4
```

Nếu user provide prompt qua argument, skip — dùng default cho 3 params còn lại (schnell + 1024 + 1 image).

Validate:
- Prompt ≥10 chars
- Dimensions ≤1792×1792 (FLUX API hard limit — width/height range 64-1792)
- N ≤ 4

### Step 3 — Call Together AI API

Run `scripts/generate.py`:
```bash
python .claude/skills/generating-images/scripts/generate.py \
  --prompt "<prompt>" \
  --model "<model>" \
  --width <W> --height <H> --n <N>
```

Script sẽ:
1. POST `https://api.together.xyz/v1/images/generations`
2. Body: `{model, prompt, width, height, steps, n}`
3. Headers: `Authorization: Bearer <KEY>`, `User-Agent` (BẮT BUỘC — tránh Cloudflare 1010)
4. Response: array of image URLs

Latency: schnell ~1-2s, pro ~5-10s, max ~10-20s.

### Step 4 — Download + save local

Script download URL + save to `output/images/<slug>.jpg`:
- Slug = first 50 chars của prompt, kebab-case, ASCII
- Vd: "Banner cho khoá AI" → `banner-cho-khoa-ai-20260515.jpg`

Skill KHÔNG tạo metadata JSON sidecar — info trả về qua stdout JSON cho parent process xử lý nếu cần.

### Step 5 — Report

```
Generated N image(s):

1. output/images/<slug>-001.jpg
   Model: <model>, 1024x1024, 13KB
   Prompt: "<first 80 chars>..."

Mở file để xem.
```

Output path absolute để user click mở được trực tiếp (CC IDE integration).

## Decision points

| Step | Hỏi user khi | Auto-proceed khi |
|---|---|---|
| 1 (pre-check) | Key fail format | Format OK |
| 2 (gather spec) | User chưa cung cấp prompt | Argument có sẵn — apply default cho params khác |
| 3 (API call) | HTTP 429 (rate limit) → ask user retry | 200 OK |
| 4 (save) | File exist same slug → append `-002`, `-003` | Slug unique |
| 5 (report) | N/A | — |

## Recovery

| Failure | Fix |
|---|---|
| `TOGETHER_AI_API_KEY` thiếu | Apply free key tại https://api.together.ai/settings/api-keys, add vào `.env` |
| HTTP 401 invalid_api_key | Check key format `tgp_v1_*`, re-copy từ dashboard |
| HTTP 403 error 1010 | Cloudflare block UA — script tự set User-Agent đúng, nếu vẫn fail check IP block |
| HTTP 400 "Unable to access non-serverless model" | Model name typo (vd `FLUX.1-schnell-Free` sai, đúng là `FLUX.1-schnell`) |
| HTTP 429 rate limit | Free tier 60 RPM, đợi 1 phút retry |
| HTTP 500 generation failed | Prompt vi phạm content policy (NSFW, violence, copyrighted), rephrase |
| Image URL 404 sau gen | URL expire sau 24h — script download + save local ngay tránh issue này |
| Output dir not writable | Check permission, hoặc đổi `--output-dir` |

## Anti-patterns

- KHÔNG hardcode API key trong script — luôn đọc `.env` runtime
- KHÔNG commit `.env` lên git (skill check `.gitignore` có `.env` chưa)
- KHÔNG cache image URL (expire 24h) — luôn download + save local
- KHÔNG dùng prompt tiếng Việt cho model pro/max nếu cần highest quality — FLUX train chủ yếu English, prompt EN tốt hơn
- KHÔNG generate >4 image cùng request — API limit, dùng loop nếu cần nhiều

## Common pitfalls

1. **Cloudflare error 1010** — script BẮT BUỘC set `User-Agent` header (urllib default UA bị Cloudflare block). Đã handle trong `generate.py`.
2. **Model name confusion** — Together dùng `black-forest-labs/FLUX.1-schnell` (KHÔNG `FLUX.1-schnell-Free`). Skill validate trước khi call.
3. **Free tier 60 RPM** — generate nhanh quá hit rate limit. Script có retry với backoff.
4. **URL expire 24h** — Together store image temporary. Skill download ngay, save local persistent.
5. **Prompt language ảnh hưởng quality** — FLUX train English. Tiếng Việt vẫn work nhưng quality thấp hơn. Skill suggest EN prompt cho user.
6. **Dimensions limit 2048** — FLUX hard limit width/height ≤2048. Larger → API reject.
7. **Steps trade-off** — schnell phải dùng steps=4 (fixed). Dev/pro: 28-50. Cao hơn không cải thiện gì.

## Skill files

| File | Purpose | Khi nào load |
|---|---|---|
| `references/models-comparison.md` | 5 FLUX variants + pricing + use case | User hỏi "dùng model nào" |
| `references/prompt-engineering.md` | Tips viết prompt tốt cho FLUX | User prompt quality kém |
| `references/troubleshooting.md` | Errors detail per HTTP code | Step fail |
| `scripts/generate.py` | API call + download + save | Step 3-4 |
| `scripts/smoke_test.py` | Verify API key + generate 1 test image | Manual test |
| `assets/env.template` | Skeleton `.env` với TOGETHER_AI_API_KEY | Step 1 (nếu .env không tồn tại) |

## Tiêu chí chất lượng (self-check)

Trước khi report Step 5:
- [ ] Image file tồn tại tại `output/images/<slug>.jpg`
- [ ] File size > 5KB (tránh case API trả empty image)
- [ ] Path absolute trong report (user click mở được)
- [ ] N images = N tương ứng với request

## Voice rules

- Tiếng Việt direct, imperative
- KHÔNG emoji
- KHÔNG hype về quality ("đẹp tuyệt vời") — user tự đánh giá
- Báo cáo cost nếu dùng paid model (`pro` ~$0.04, `max` ~$0.10)

## Sample timing

- Step 1 pre-check: <1s
- Step 2 gather spec: 30s (user input)
- Step 3 API call: 1-20s tuỳ model
- Step 4 download + save: <1s per image
- Step 5 report: <1s

**Total: 5-30 giây** từ prompt đến file ready.
