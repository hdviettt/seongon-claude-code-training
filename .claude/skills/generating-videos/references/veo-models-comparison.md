# VEO Models Comparison

## Contents
- [3 VEO 3 variants](#3-veo-3-variants)
- [Choosing guide](#choosing-guide)
- [Pricing as of 2026](#pricing-as-of-2026)
- [Capabilities & limitations](#capabilities--limitations)

## 3 VEO 3 variants

Google ship 3 VEO 3 models qua Gemini API:

| Model | Speed | Quality | Cost | Best for |
|---|---|---|---|---|
| `veo-3.1-lite-generate-preview` | 30-90s | Good | **~$0.20/8s 720p** | Quick draft, iterate, concepts |
| `veo-3.1-fast-generate-preview` | 11-60s | Very Good | ~$0.30/8s 720p | Default — balance quality/speed/cost |
| `veo-3.1-generate-preview` | 60-180s | Best | ~$0.40/8s 720p | Final cut, quality cao nhất |

**Default skill: `veo-3.1-fast-generate-preview`** — balance tốt cho most use cases.

## Choosing guide

| Use case | Model recommend |
|---|---|
| Draft, test prompt | `veo-3.1-lite` |
| Social media short clip (TikTok/Reels) | `veo-3.1-fast` |
| Product teaser cho client | `veo-3.1-fast` hoặc `veo-3.1-standard` |
| Hero video landing page | `veo-3.1-generate-preview` (full) |
| Premium ad concept | `veo-3.1-generate-preview` (full) |
| Animation concept | `veo-3.1-fast` |
| Slow scenic shot | `veo-3.1-fast` (handle motion tốt) |

## Pricing as of 2026

| Config | Lite | Fast | Standard |
|---|---|---|---|
| 720p / 4s | ~$0.10 | ~$0.15 | ~$0.20 |
| 720p / 6s | ~$0.15 | ~$0.22 | ~$0.30 |
| 720p / 8s | ~$0.20 | ~$0.30 | ~$0.40 |
| 1080p / 8s | ~$0.40 | ~$0.60 | ~$0.80 |
| 4k / 8s | ~$0.80 | ~$1.20 | ~$1.60 |

**Cost factors**:
- Resolution (1080p ~2x 720p, 4k ~4x 720p)
- Duration linear ($/second)
- Model tier (lite < fast < standard)

**Free tier**: Gemini API có free tier nhưng VEO 3 thường KHÔNG include — phải enable billing.

**Quota**: Gemini API có quota daily (vary by tier). Hit quota → 429.

## Capabilities & limitations

### Capabilities

- **Native audio**: synced sound effects, ambient, dialogue
- **Resolution**: 720p, 1080p, 4k
- **Duration**: 4s, 6s, 8s (1080p/4k chỉ 8s)
- **Aspect ratio**: 16:9 (landscape), 9:16 (vertical/mobile)
- **Input types**: text-only (default), text + image (first frame), text + 2 images (first + last frame), text + reference images (subject guidance)
- **Watermarking**: SynthID embedded (invisible)

### Limitations

- **Max 8s per generation** — longer video cần multi-clip + edit tool
- **No 1:1 aspect** — chỉ 16:9 hoặc 9:16
- **No portrait/landscape pivot mid-clip** — fixed aspect entire video
- **Audio không disable được** — always generate
- **Server retention 2 ngày** — phải download local nếu giữ lâu
- **Polling required** — async, không sync response
- **No real public figures** — Google policy reject celebrity, politician
- **No copyrighted characters** — Disney, Marvel, anime characters → reject
- **Text in video render kém** — như FLUX, dùng edit tool overlay sau
- **First gen lâu hơn** — model warm-up, sau đó fast hơn

### So sánh với VEO predecessor

- **VEO 1**: legacy, không support audio
- **VEO 2**: support audio, but limited motion quality
- **VEO 3**: current, best motion + audio + quality

Skill chỉ support VEO 3.1 variants (latest as of 2026).

## Comparison với competitors

| Model | Pros | Cons |
|---|---|---|
| **VEO 3** (Google) | Native audio, 4k support, motion quality | Paid, server retention 2 ngày |
| Sora (OpenAI) | Long duration support | Limited access, expensive |
| Runway Gen-3 | Image-to-video strong | Web UI focused, API limited |
| Luma Dream Machine | Fast generation | Lower quality vs VEO 3 |
| Pika | Cheap | Quality variance |
| Stable Video Diffusion | Open source, free | Self-host, lower quality |

VEO 3 = best choice for production work với native audio + high quality.

## Multi-clip strategy (cho video dài >8s)

VEO 3 max 8s per gen. Để tạo video 30s:
1. Generate 4-5 clips (mỗi 6-8s) với consistent style trong prompts
2. Use last-frame reference: clip 2 dùng last frame của clip 1 làm first frame → continuity
3. Edit join trong CapCut/Premiere/DaVinci

Skill `generating-videos` chỉ handle 1-clip gen. Multi-clip pipeline = separate skill `generating-long-videos` (future).
