# FLUX Models Comparison

## Contents
- [5 main variants](#5-main-variants)
- [Choosing guide](#choosing-guide)
- [Steps parameter](#steps-parameter)
- [Pricing as of 2026](#pricing-as-of-2026)

## 5 main variants

Together AI host 12 FLUX models. 5 cốt lõi cho most use cases:

| Model | Speed | Quality | Cost | Best for |
|---|---|---|---|---|
| `FLUX.1-schnell` | 1-2s | Good | **FREE** | Quick mockup, draft, learning |
| `FLUX.1-krea-dev` | 3-5s | Better | ~$0.02/img | General quality boost |
| `FLUX.1.1-pro` | 5-10s | Excellent | ~$0.04/img | Production, social posts, banners |
| `FLUX.2-pro` | 8-15s | Excellent+ | ~$0.06/img | Higher fidelity, complex scenes |
| `FLUX.2-max` | 15-25s | Best | ~$0.10/img | Premium output, large format print |

**Default skill: `FLUX.1-schnell`** — free, fast enough cho 90% use case. Override khi user explicit cần quality cao hơn.

## Choosing guide

| Use case | Model recommend |
|---|---|
| Test prompt, iterate ideas | `FLUX.1-schnell` |
| Social media post (FB, Instagram) | `FLUX.1.1-pro` |
| Blog thumbnail, hero banner | `FLUX.1.1-pro` |
| Print materials (poster, brochure) | `FLUX.2-pro` |
| Detailed character/scene | `FLUX.2-max` |
| Photorealistic portrait | `FLUX.2-pro` hoặc `FLUX.2-max` |
| Abstract art, concept | Any (schnell đủ) |
| Logo design | `FLUX.1.1-pro` (multiple iterations) |

## Steps parameter

`steps` = số lần model refine ảnh. Trade-off speed vs quality:

| Model | Default steps | Range valid |
|---|---|---|
| FLUX.1-schnell | **4** (fixed) | 4 only — train cho 4 steps |
| FLUX.1-dev | 28 | 20-50 |
| FLUX.1.1-pro | 28 | 20-50 |
| FLUX.2-pro/max | 28 | 20-50 |

Schnell hard-coded 4 steps — đổi không giúp gì. Pro/max: 28 default optimal, 50 marginal improvement với 2x latency.

## Pricing as of 2026

Đơn giá Together AI (1024×1024 image):
- `FLUX.1-schnell`: $0.00 (free tier, 60 RPM)
- `FLUX.1-krea-dev`: ~$0.025/img
- `FLUX.1.1-pro`: ~$0.04/img
- `FLUX.2-pro`: ~$0.06/img
- `FLUX.2-max`: ~$0.10/img

Pricing tăng theo dimension — 2048×2048 cost ~4x.

Free tier limits:
- 60 requests/minute
- Schnell models only
- Image URL expire 24h sau gen

Paid tier:
- Unlimited RPM (rate limit theo plan)
- Tất cả model variants
- Image URL không expire (vẫn nên download save local)

## Aspect ratios common

| Use case | Dimensions | Aspect |
|---|---|---|
| Square (Instagram, FB post) | 1024×1024 | 1:1 |
| Landscape (banner, hero) | 1920×1080 | 16:9 |
| Portrait (story, reel) | 1080×1920 | 9:16 |
| YouTube thumbnail | 1280×720 | 16:9 |
| LinkedIn post | 1200×627 | ~1.91:1 |
| Twitter header | 1500×500 | 3:1 |

FLUX API hard limit: width/height range 64-1792. Vượt → API reject với `"width must be between 64 and 1792"`.
