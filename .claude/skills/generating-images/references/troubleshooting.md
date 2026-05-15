# Troubleshooting — generating-images

## Contents
- [Auth errors](#auth-errors)
- [API errors](#api-errors)
- [Generation errors](#generation-errors)
- [Output errors](#output-errors)

## Auth errors

### `TOGETHER_AI_API_KEY khong tim thay`

**Cause**: `.env` (hoặc `.env.local`) thiếu biến.
**Fix**:
1. Apply free key tại https://api.together.ai/settings/api-keys
2. Copy key (format `tgp_v1_...`)
3. Add vào `.env`:
   ```
   TOGETHER_AI_API_KEY=tgp_v1_xxxx
   ```

### HTTP 401 `invalid_api_key`

**Cause**: Key sai/typo/revoked.
**Fix**:
- Check format `tgp_v1_` prefix
- Re-copy từ dashboard
- Verify key chưa expire (revoke ở dashboard)

## API errors

### HTTP 403 error code 1010 (Cloudflare)

**Cause**: User-Agent header sai → Cloudflare block.
**Fix**: Script `generate.py` đã set UA `Mozilla/5.0 (compatible; ClaudeCode-generating-images/1.0)`. Nếu vẫn fail:
- Check IP có bị Cloudflare flag không (try từ network khác)
- Update UA trong script gần với browser thật hơn

### HTTP 400 "Unable to access non-serverless model"

**Cause**: Model name typo. Common mistake:
- ❌ `FLUX.1-schnell-Free` 
- ✅ `FLUX.1-schnell`
- ❌ `flux-pro`
- ✅ `black-forest-labs/FLUX.1.1-pro`

**Fix**: Verify model name từ `references/models-comparison.md`. Always prefix `black-forest-labs/`.

### HTTP 429 rate limit

**Cause**: Free tier 60 RPM exceeded.
**Fix**:
- Đợi 60s retry
- Upgrade paid plan (unlimited RPM)
- Batch sequential thay vì parallel

### HTTP 500 server error

**Cause**: Together AI internal issue, hoặc model overloaded.
**Fix**:
- Retry sau 30s
- Switch model (schnell → dev → pro)
- Check status https://status.together.ai/

### HTTP 422 prompt rejected

**Cause**: Prompt vi phạm content policy:
- NSFW (sexual, nudity)
- Violence, gore
- Public figures (celebrity, politician)
- Copyrighted characters (Disney, Marvel)
- Hate speech

**Fix**: Rephrase prompt, remove triggering keywords.

## Generation errors

### Image quality thấp / blurry

**Cause 1**: Steps quá thấp.
**Fix**: Schnell fix 4 steps. Cho dev/pro: dùng `--steps 28` (default).

**Cause 2**: Prompt quá vague.
**Fix**: Đọc `references/prompt-engineering.md` — thêm subject + lighting + style.

**Cause 3**: Model không phù hợp use case.
**Fix**: Schnell cho quick draft, pro/max cho final.

### Image không match prompt

**Cause**: FLUX không support `negative_prompt`. Mention element trong prompt → model thường sinh element đó.
**Fix**: 
- Skip mention element không muốn
- Dùng positive framing ("empty street" thay "no people")

### Multiple subject blurry

**Cause**: Prompt có >3 main subjects → model split attention.
**Fix**: Limit 1-2 main subjects, rest là context.

### Text trong ảnh sai/lộn xộn

**Cause**: FLUX render text kém (limitation hiện tại).
**Fix**:
- Generate ảnh KHÔNG text
- Overlay text bằng Canva/Figma/Photoshop sau

## Output errors

### File size <5KB

**Cause**: API trả empty/corrupt image.
**Fix**: Re-generate. Nếu lặp lại → check prompt content (có thể bị policy flag, API trả placeholder).

### Output dir not writable

**Cause**: Permission hoặc disk full.
**Fix**:
- `chmod u+w output/` (Unix)
- Đổi `--output-dir /tmp/images`

### URL expire trước khi download

**Cause**: Together URL expire 24h. Nếu skill chạy trong session lâu, URL hết hạn.
**Fix**: Script download NGAY sau API call (đã handle), không cache URL persistent.

### Filename collision

**Cause**: 2 prompts ra slug giống.
**Fix**: Script auto append timestamp `<slug>-<YYYYMMDD-HHMMSS>.jpg`. Hoặc append `-002`, `-003` nếu vẫn collide.

## Diagnosis nhanh

Run smoke test:
```bash
python .claude/skills/generating-images/scripts/smoke_test.py
```

Generate 1 test image với prompt simple. Output cho biết:
- API key valid
- Endpoint reachable
- Image save successful

Nếu smoke test PASS nhưng real use case FAIL → vấn đề ở prompt content hoặc model selection.
