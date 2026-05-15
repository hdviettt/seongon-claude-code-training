# Troubleshooting — generating-videos (Together AI)

## Contents
- [Auth errors](#auth-errors)
- [Submission errors](#submission-errors)
- [Polling errors](#polling-errors)
- [Download errors](#download-errors)
- [Quality issues](#quality-issues)
- [Cost surprise](#cost-surprise)

## Auth errors

### `TOGETHER_AI_API_KEY không tìm thấy`

**Cause**: `.env` thiếu biến.
**Fix**:
1. Apply tại https://api.together.ai/settings/api-keys
2. Copy key (format `tgp_v1_...`)
3. Add `.env`:
   ```
   TOGETHER_AI_API_KEY=tgp_v1_xxxx
   ```

### HTTP 401 invalid key

**Cause**: Key sai/expired/revoked.
**Fix**: Re-copy từ dashboard. Check key chưa được revoke.

### HTTP 402 insufficient credit

**Cause**: Together account hết credit. Video gen paid ($0.30-1.50/clip).
**Fix**: Nạp tiền tại https://api.together.ai/settings/billing.

## Submission errors

### HTTP 400 invalid model

**Cause**: Model name typo. Common mistakes:
- ❌ `veo-3.0-fast` (thiếu provider prefix)
- ✅ `google/veo-3.0-fast`
- ❌ `sora-2`
- ✅ `openai/sora-2`
- ❌ `kling-pro`
- ✅ `kwaivgI/kling-2.1-pro`

**Fix**: Verify model name từ `references/video-models-comparison.md`. Luôn có provider prefix.

### HTTP 400 invalid size

**Cause**: `size` param sai format.
**Fix**: Use `"1920x1080"` (16:9) hoặc `"1080x1920"` (9:16). Skill handle conversion từ `--aspect` flag.

### HTTP 400 prompt too short

**Cause**: Prompt < 15 chars.
**Fix**: Viết prompt mô tả ≥15 chars. Đọc `references/prompt-engineering.md`.

### HTTP 400 content policy

**Cause**: Prompt vi phạm:
- Public figures (celebrity, politician)
- Copyrighted characters
- NSFW, violence
- Hate speech

**Fix**: Rephrase prompt safe.

## Polling errors

### Timeout 10 phút

**Cause**: Model occasionally slow, hoặc queue saturated.
**Fix**:
- Retry sau 5 phút (new job)
- Switch model: dùng fast variant (vd `veo-3.0-fast` thay `veo-3.0`)
- Check status https://status.together.ai

### Job status `failed`

**Cause**: Generation internal error, hoặc prompt fail safety filter.
**Fix**: 
- Re-submit với prompt khác nếu content policy issue
- Re-submit nguyên prompt nếu internal (50/50 fix)

### Polling 429

**Cause**: Poll faster than allowed rate.
**Fix**: Skill default 15s interval — đã OK. Nếu override < 10s sẽ hit.

## Download errors

### Video URL 404

**Cause**: URL expire 24h.
**Fix**: 
- Script download NGAY sau job done (đã handle)
- Nếu skill chạy session lâu, URL gone — re-submit job

### Download timeout

**Cause**: Network slow, file lớn (1080p ~15-25MB).
**Fix**: Tăng timeout trong `generate.py` từ 180s → 300s.

### File 0 bytes

**Cause**: Download fail mid-stream.
**Fix**: Re-download URL (vẫn valid 24h).

## Quality issues

### Video không có motion

**Cause**: Prompt static, model không biết motion gì.
**Fix**: Add motion verbs ("waves rolling", "camera pans right"). Đọc `references/prompt-engineering.md`.

### Audio không match (VEO/Sora)

**Cause**: Audio cues quá specific hoặc conflict.
**Fix**: 
- Audio cues nhẹ thôi
- Skip music spec → model tự generate phù hợp

### Sora vs VEO khác biệt motion

**Cause**: Sora strong realistic motion, VEO better audio. Khác model khác trade-off.
**Fix**: Match model với use case:
- Realistic action → Sora
- Audio + ambient → VEO
- Stylized → Kling

### Aspect ratio output sai

**Cause**: `--aspect` flag truyền sai.
**Fix**: Skill accept chỉ `16:9` hoặc `9:16`. Custom aspect → crop post-process.

## Cost surprise

### Bill bất ngờ

**Cause**: Generate nhiều video không track.
**Fix**:
- Check usage tại https://api.together.ai/settings/usage
- Set budget alert
- Use cheap models cho draft (`vidu/vidu-q1` $0.30)

**Cost estimation per video** (skill auto-print):
- Vidu/Seedance: ~$0.30
- Kling standard: ~$0.40
- Kling pro: ~$0.70
- Hailuo: ~$0.50
- VEO 3 fast: ~$0.80 (default)
- VEO 3 / Sora 2: ~$1.00-1.20
- Sora 2 pro: ~$1.50

### Concurrent jobs

**Cause**: Submit 5 jobs cùng lúc → bill 5x.
**Fix**: Submit sequential nếu muốn budget control. Together không có queue priority.

## Diagnosis nhanh

```bash
python .claude/skills/generating-videos/scripts/smoke_test.py --dry-run
```

Dry-run cho biết:
- API key valid
- Endpoint reachable
- Account có credit không

Full test (~$0.30 với kling-standard):
```bash
python .claude/skills/generating-videos/scripts/smoke_test.py
```
