# Video Models Comparison — Together AI

## Contents
- [6 model families](#6-model-families)
- [Pricing as of 2026](#pricing-as-of-2026)
- [Choosing guide](#choosing-guide)
- [VEO 3 variants chi tiết](#veo-3-variants-chi-tiết)
- [Capabilities matrix](#capabilities-matrix)

## 6 model families

Together AI ship 30+ video models from 6 providers:

### 1. Google VEO (Best audio quality)
- `google/veo-3.0` — premium, native audio sync, high quality
- `google/veo-3.0-fast` — DEFAULT skill, balance quality/speed
- `google/veo-3.0-audio` — variant emphasizing audio fidelity
- `google/veo-3.0-fast-audio` — fast + audio
- `google/veo-2.0` — older, no audio
- `google/veo-3.1-test-debug` — experimental, KHÔNG dùng

### 2. OpenAI Sora (Best motion realism)
- `openai/sora-2` — base, $1.00 area
- `openai/sora-2-pro` — premium, $1.50 area

### 3. Kuaishou Kling (Best for stylized motion)
- `kwaivgI/kling-2.1-standard` — cheaper option, ~$0.40
- `kwaivgI/kling-2.1-pro` — quality boost
- `kwaivgI/kling-2.1-master` — best quality
- `kwaivgI/kling-2.0-master`, `kwaivgI/kling-1.6-pro` — older generations

### 4. MiniMax Hailuo
- `minimax/hailuo-02` — competitive pricing, good for character animation

### 5. Shengshu Vidu
- `vidu/vidu-q1`, `vidu/vidu-2.0` — fast generation, asian context strong

### 6. ByteDance Seedance + Pixverse + Wan
- `ByteDance/Seedance-1.0-lite`, `Seedance-1.0-pro` — Bytedance video gen
- `pixverse/pixverse-v5` — Pixverse latest
- `Wan-AI/Wan2.2-T2V-A14B`, `Wan-AI/Wan2.2-I2V-A14B` — open Wan models

## Pricing as of 2026

Approximate per-clip (8s, default size):

| Model | Cost/clip | Has Audio | Speed |
|---|---|---|---|
| `google/veo-3.0-fast` | $0.80 | YES | 30s-4min |
| `google/veo-3.0` | $1.20 | YES | 2-6min |
| `google/veo-3.0-audio` | $1.20 | YES (emphasis) | 2-5min |
| `openai/sora-2` | $1.00 | YES | 1-3min |
| `openai/sora-2-pro` | $1.50 | YES | 2-5min |
| `kwaivgI/kling-2.1-standard` | $0.40 | NO | 30s-2min |
| `kwaivgI/kling-2.1-pro` | $0.70 | NO | 1-3min |
| `kwaivgI/kling-2.1-master` | $1.00 | NO | 2-5min |
| `minimax/hailuo-02` | $0.50 | NO | 30s-2min |
| `vidu/vidu-q1` | $0.30 | NO | 20s-1min |
| `ByteDance/Seedance-1.0-lite` | $0.30 | NO | 30s-1min |

Pricing chính thức: https://www.together.ai/pricing

## Choosing guide

| Use case | Model recommend |
|---|---|
| Draft, test prompt concept | `kwaivgI/kling-2.1-standard` ($0.40) hoặc `vidu/vidu-q1` ($0.30) |
| Social media short clip với audio | `google/veo-3.0-fast` ($0.80) |
| Realistic motion (character, action) | `openai/sora-2` ($1.00) |
| Stylized animation | `kwaivgI/kling-2.1-pro` ($0.70) |
| Premium ad concept với audio | `google/veo-3.0` ($1.20) hoặc `openai/sora-2-pro` ($1.50) |
| Asian context, vlog style | `vidu/vidu-q1` |
| Character animation cảm xúc | `minimax/hailuo-02` |
| Quick iteration | `vidu/vidu-q1` (cheapest, fastest) |

**Default skill: `google/veo-3.0-fast`** — balance audio + quality + speed cho most SEONGON use cases.

## VEO 3 variants chi tiết

VEO 3.0 family đặc biệt vì native audio generation:

| Variant | Audio | Speed | Quality | Cost |
|---|---|---|---|---|
| `veo-3.0` | Yes (synced) | Medium | Highest | $1.20 |
| `veo-3.0-fast` | Yes | Fast | High | $0.80 |
| `veo-3.0-audio` | Yes (emphasis) | Medium | High + audio focused | $1.20 |
| `veo-3.0-fast-audio` | Yes | Fast | Audio focused | $0.80 |

Audio variants prioritize sound effects + ambient quality. Non-audio variants vẫn có audio (VEO 3 always), nhưng tối ưu visual hơn.

## Capabilities matrix

| Feature | VEO 3 | Sora 2 | Kling 2.1 | Hailuo | Vidu Q1 |
|---|---|---|---|---|---|
| Native audio | YES | YES | NO | NO | NO |
| Max duration | 8s | 8s | ~15s | 6s | 5s |
| Resolution max | 1920×1080 | 1920×1080 | 1080p | 720p | 720p |
| Aspect ratios | 16:9, 9:16 | 16:9, 9:16, 1:1 | 16:9, 9:16, 1:1 | 16:9, 9:16 | 16:9 |
| Image-to-video | Limited | YES | YES (strong) | YES | YES |
| Camera control | Basic | Strong | Strong (motion brush) | Basic | Basic |
| Watermark | SynthID invisible | Visible logo | Optional | Optional | None |

## Cost optimization

Cho production workflow:
1. Iterate concept với `vidu/vidu-q1` ($0.30) hoặc `kwaivgI/kling-2.1-standard` ($0.40) — quick + cheap
2. Test prompt cuối với `veo-3.0-fast` ($0.80) — verify audio
3. Final render với `veo-3.0` hoặc `sora-2-pro` ($1.20-1.50) chỉ khi cần highest quality

Total cost per production video: $1.50-3 (3-5 iterations).

## Limitations chung

- **Max 8-15s per gen** — cần multi-clip + edit cho video dài
- **No real public figures** — celebrity, politician → reject
- **No copyrighted characters** — Disney, anime → reject
- **Text in video render kém** — overlay sau bằng edit tool
- **Audio không disable được** với VEO/Sora (nếu cần silent, mute post-process)
- **URL expire 24h** — Together store temporary, download ngay
