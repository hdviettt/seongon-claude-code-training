# Prompt Engineering cho FLUX

## Contents
- [Anatomy prompt tốt](#anatomy-prompt-tốt)
- [Tiếng Anh vs Tiếng Việt](#tiếng-anh-vs-tiếng-việt)
- [Negative prompt (KHÔNG support)](#negative-prompt-không-support)
- [Style modifiers](#style-modifiers)
- [Examples Vietnamese use case](#examples-vietnamese-use-case)

## Anatomy prompt tốt

FLUX hiểu prompt theo thứ tự: subject → action → setting → style → quality.

**Template**:
```
[Subject] [doing action] in [setting], [style], [quality/medium]
```

Vd:
- ❌ Vague: "a cat"
- ✅ Specific: "A black cat sleeping on a marble countertop next to a window, soft morning light, photorealistic, depth of field"

**6 elements quan trọng**:
1. **Subject**: rõ ràng (people, object, scene)
2. **Composition**: close-up, wide shot, top-down, etc.
3. **Lighting**: golden hour, neon, studio, natural, dramatic
4. **Color palette**: warm tones, monochrome, pastel, vibrant
5. **Style**: photorealistic, oil painting, watercolor, anime, 3D render
6. **Quality cues**: 4K, detailed, sharp, professional photography

## Tiếng Anh vs Tiếng Việt

FLUX train chủ yếu English. Recommend:

- **Prompt EN**: quality cao nhất, model hiểu nuance
- **Prompt VN**: vẫn work (FLUX 2 cải thiện multilingual), chất lượng thấp hơn ~20%

Compromise: viết prompt bằng tiếng Anh, sau đó note bằng Vietnamese trong metadata.

Vd:
- VN: "Banner cho khoá học AI SEONGON, tone xanh navy"
- EN equivalent: "Marketing banner for AI training course, navy blue color scheme, professional corporate design, bold typography mentioning 'AI Training', clean modern layout"

EN version produce ảnh chất lượng cao hơn rõ rệt.

## Negative prompt (KHÔNG support)

FLUX KHÔNG có `negative_prompt` parameter như Stable Diffusion. Để exclude element:
- ❌ Không write "no people, no text" trong prompt
- ✅ Skip mention element không muốn

Hoặc dùng positive framing:
- "empty street" thay vì "street with no people"
- "clean background" thay vì "background without clutter"

## Style modifiers

Common style triggers FLUX hiểu tốt:

**Photography**:
- `photorealistic`, `4K`, `DSLR photo`, `35mm`, `bokeh`
- `golden hour`, `studio lighting`, `natural light`
- `Canon EOS R5`, `Sony A7IV` (mention camera model = increase realism cue)

**Illustration**:
- `digital illustration`, `flat design`, `vector art`
- `watercolor`, `oil painting`, `ink drawing`
- `Studio Ghibli style`, `Pixar style`, `anime style`

**3D/Render**:
- `3D render`, `Octane render`, `Blender`
- `cinematic`, `Unreal Engine 5`
- `isometric`, `low poly`

**Mood**:
- `moody`, `dramatic`, `serene`, `vibrant`, `melancholy`
- `cyberpunk`, `vaporwave`, `minimalist`, `maximalist`

## Examples Vietnamese use case

### Use case 1: Blog thumbnail SEO

Bad:
> "thumbnail blog về SEO"

Good (EN):
> "Marketing blog thumbnail design about SEO ranking, featuring a stylized magnifying glass over Google search results, navy blue and gold color scheme, clean modern flat design, 16:9 aspect ratio, professional editorial style"

### Use case 2: Social post SEONGON

Bad:
> "post Facebook SEONGON về AI"

Good (EN):
> "Square social media post for AI training company, featuring abstract neural network visualization in deep blue tones with bright accent dots, minimalist composition, large readable headline space at top, corporate professional aesthetic"

### Use case 3: Avatar/Logo concept

Bad:
> "logo công ty SEO"

Good (EN):
> "Modern minimalist logo concept for SEO consulting agency, abstract mark combining magnifying glass and upward arrow, monochromatic deep navy, clean geometric forms, white background, professional brand identity"

### Use case 4: Hero banner course

Bad:
> "banner khoá học AI"

Good (EN):
> "Landing page hero banner for AI training course, split composition: left side abstract glowing neural network in cyan, right side dark background with bold 'AI MASTERY' text space, ultra-wide 21:9 cinematic aspect, futuristic professional design"

## Common mistakes

1. **Prompt quá ngắn** (< 10 words) → output generic
2. **Conflict styles** ("oil painting + photorealistic") → model confused
3. **Quá nhiều subject** (>3) → model split attention, không subject nào sharp
4. **Quá nhiều adjective** → model ignore, output không match
5. **Yêu cầu text trong ảnh** — FLUX render text kém, dùng design tool sau (Canva/Figma) overlay text

## Iteration approach

1. Generate 4 variations với schnell (free)
2. Pick best concept
3. Refine prompt dựa trên kết quả
4. Re-generate với schnell lần 2-3
5. Final pass với pro/max nếu cần quality

Total cost cho 1 image production-ready: ~$0.04-0.10 (1 pro/max call sau iteration với schnell).
