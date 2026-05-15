# Prompt Engineering cho VEO 3

## Contents
- [Anatomy prompt video tốt](#anatomy-prompt-video-tốt)
- [Motion cues](#motion-cues)
- [Audio cues](#audio-cues)
- [Camera movements](#camera-movements)
- [Tiếng Anh vs Tiếng Việt](#tiếng-anh-vs-tiếng-việt)
- [Examples Vietnamese use case](#examples-vietnamese-use-case)

## Anatomy prompt video tốt

VEO 3 khác FLUX image — cần thêm **temporal** elements (motion, sound, camera).

**Template**:
```
[Scene] với [subject doing action]. [Camera movement]. [Lighting/mood]. [Audio cue].
```

Vd:
- ❌ Vague: "a beach scene"
- ✅ Specific: "Wide shot of an empty tropical beach at sunset. Gentle waves rolling onto white sand. Camera slowly pans right. Golden hour lighting, lens flare. Soft ocean sounds with seagulls in distance."

**7 elements quan trọng** (vs FLUX 6):
1. **Scene/Setting**: where + when
2. **Subject + Action**: what's moving + how
3. **Camera**: pan/zoom/static/dolly
4. **Lighting**: warm/cold/dramatic/natural
5. **Style**: cinematic/documentary/animation
6. **Mood**: serene/tense/joyful
7. **Audio**: ambient sounds, music style, dialogue (rare)

## Motion cues

VEO 3 expects motion description. Static prompt → output có thể đứng yên hoặc motion ngẫu nhiên.

**Motion verbs strong**:
- `walking`, `running`, `jumping`, `dancing`
- `flowing`, `swirling`, `rolling`, `floating`
- `panning`, `zooming`, `tracking`, `tilting` (camera)
- `glowing`, `pulsing`, `flickering` (lighting)

**Speed modifiers**:
- `slowly` / `gently` → smooth, peaceful
- `quickly` / `rapidly` → energetic
- `in slow motion` → cinematic emphasis
- `time-lapse` → fast forward

Vd: `"A traveler walking slowly through a bustling Tokyo street, neon lights pulsing"`

## Audio cues

VEO 3 generate audio synced với scene. Prompt audio nhẹ enough, model tự fill gaps.

**Ambient sounds**:
- `ocean waves`, `wind through trees`, `birds chirping`
- `city traffic`, `crowd murmur`, `cafe ambience`
- `rain on roof`, `fireplace crackling`

**Music style** (optional):
- `with cinematic orchestral music`
- `with upbeat electronic background music`
- `with subtle ambient music`
- `no music, just ambient sounds` (silent music)

**Dialogue** (advanced):
- VEO 3 generate dialogue được nhưng quality varies. Recommend skip cho dependable output.

**Audio anti-pattern**:
- ❌ Over-specify ("a violin plays a B-flat note") → model confused
- ❌ Dialogue dài (>1 sentence) → lip-sync issue

## Camera movements

Cinematography terms VEO 3 hiểu tốt:

| Term | Effect |
|---|---|
| `static shot` | Camera đứng yên |
| `pan left/right` | Quay ngang |
| `tilt up/down` | Quay dọc |
| `dolly in/out` | Camera tiến gần / lùi xa subject |
| `zoom in/out` | Focal length thay đổi |
| `tracking shot` | Camera đi theo subject |
| `crane shot` | Camera lên/xuống cao |
| `aerial shot` / `drone shot` | Top-down view |
| `pov shot` / `first-person` | Mắt nhân vật |
| `over-the-shoulder` | Sau lưng nhìn ra |
| `close-up` | Tight on subject |
| `wide shot` | Full scene |

## Tiếng Anh vs Tiếng Việt

VEO 3 cải thiện multilingual nhưng English vẫn tốt nhất.

**Best practice**:
- Prompt EN cho final production
- Tiếng Việt OK cho draft/iterate (~70-80% quality vs EN)
- KHÔNG mix EN + VN trong cùng prompt (model confused)

## Examples Vietnamese use case

### Use case 1: TikTok short cho SEONGON

Bad:
> "video về AI"

Good (EN):
> "Cinematic close-up shot: a person's hands typing on a laptop, glowing AI interface visualization floating above the keyboard with abstract neural network patterns. Camera slowly tilts up to reveal the user's focused face in soft blue light. Ambient electronic music with subtle keyboard sounds. 9:16 vertical for mobile."

### Use case 2: Reels concept cho client

Bad:
> "video sản phẩm máy lọc nước"

Good (EN):
> "Product showcase: a modern white water filter on a kitchen counter, sunlight streaming through window. Camera slowly dollies in. Water flows from filter into glass with elegant slow-motion droplets. Clean ambient sound of pouring water, gentle background music. Bright clean lifestyle aesthetic, 9:16 portrait."

### Use case 3: Landing page hero video

Bad:
> "video team họp"

Good (EN):
> "Wide shot of a modern open-plan office: team members collaborating around a wooden conference table with laptops, soft natural light through floor-to-ceiling windows. Camera slowly pans right showing whiteboard with brand strategy. Warm professional mood. Soft ambient office chatter, subtle uplifting background music. 16:9 cinematic."

### Use case 4: Hook video cho ads

Bad:
> "hook video AI"

Good (EN):
> "Quick energetic montage: glowing AI brain visualization pulsing rapidly, transitioning to user's surprised face reacting to laptop screen, then quick close-up of revenue chart climbing upward. Fast cuts, vibrant colors, dramatic electronic music building tension. 9:16 vertical, hook style for social ads."

### Use case 5: Atmospheric scenic

Bad:
> "video phong cảnh sapa"

Good (EN):
> "Aerial drone shot slowly descending over Vietnamese rice terraces in Sapa at golden hour. Mountain mist rolling between green terraced fields, small village visible in distance. Camera continues forward in cinematic slow motion. Warm sunset lighting, peaceful birds chirping, gentle wind, traditional Vietnamese flute music. 16:9 widescreen."

## Common mistakes

1. **Prompt quá static** ("a beautiful sunset") → video không có motion
2. **Quá nhiều scenes trong 8s** ("man walks then jumps then dances") → choppy
3. **Conflict motion** ("static shot with fast pan") → confused
4. **Real public figures** ("video of Donald Trump") → reject
5. **Copyrighted character** ("video of Pikachu") → reject
6. **Dialogue dài** — pick visual storytelling > dialogue
7. **Audio over-specified** — let VEO generate naturally

## Iteration approach

1. Generate 1 clip với `lite` (cheapest) — verify concept
2. Refine prompt dựa trên kết quả
3. Re-gen với `fast` — quality check
4. Final với `standard` nếu cần highest quality

Total cost cho 1 video production-ready: ~$0.50-1.50 (1 lite + 1 fast + 1 standard).

## Reference image (advanced)

Skill này hiện chỉ support text-to-video. Image-to-video (animate static image) là feature riêng — tạo skill `animating-images` future.

VEO 3 support image input via `image` parameter (Veo 3 sẽ animate, không VEO 3 fast/lite). Pricing cao hơn ~2x.
