# Troubleshooting — generating-videos

## Contents
- [Auth errors](#auth-errors)
- [Submission errors](#submission-errors)
- [Polling errors](#polling-errors)
- [Download errors](#download-errors)
- [Quality issues](#quality-issues)
- [Cost surprise](#cost-surprise)

## Auth errors

### `GEMINI_API_KEY không tìm thấy`

**Cause**: `.env` thiếu biến.
**Fix**:
1. Apply tại https://aistudio.google.com/app/apikey
2. Click "Create API Key" → chọn project
3. Copy key (format `AIza...`, ~39 chars)
4. Add `.env`:
   ```
   GEMINI_API_KEY=AIzaSyXXXX
   ```

### HTTP 401 invalid key

**Cause**: Key sai/expired/revoked.
**Fix**:
- Verify format `AIza...`
- Re-copy từ AI Studio
- Check key chưa restrict (Cloud Console → APIs & Services → Credentials)

### HTTP 403 billing not enabled

**Cause**: Project Cloud chưa enable billing. VEO 3 = paid model.
**Fix**:
1. Vào https://console.cloud.google.com/billing
2. Link billing account vào project có Gemini API enabled
3. Verify card valid + có credit

## Submission errors

### HTTP 400 "invalid argument: duration must be 8 for {resolution}"

**Cause**: 1080p/4k require duration=8.
**Fix**: Truyền `--duration 8` khi dùng 1080p/4k. Skill validate trước call.

### HTTP 400 "prompt too short"

**Cause**: Prompt < 15 chars.
**Fix**: Viết prompt mô tả ≥15 chars. Đọc `references/prompt-engineering.md`.

### HTTP 400 invalid model name

**Cause**: Typo model name. Common:
- ❌ `veo-3` (thiếu version)
- ❌ `veo-3.1` (thiếu suffix)
- ✅ `veo-3.1-fast-generate-preview`

**Fix**: Verify từ `references/veo-models-comparison.md`.

### HTTP 422 content policy

**Cause**: Prompt vi phạm:
- Public figures (celebrity, politician)
- Copyrighted characters (Disney, Marvel, anime)
- NSFW, violence, gore
- Hate speech

**Fix**: Rephrase prompt safe. Avoid real names + copyrighted IP.

## Polling errors

### Timeout 6 phút

**Cause**: VEO model occasionally slow, hoặc queue saturated.
**Fix**:
- Retry sau 5 phút
- Switch model: `veo-3.1-fast-generate-preview` (rồi lên standard nếu cần)
- Check Google Cloud status page

### HTTP 404 operation not found

**Cause**: Operation ID expire (24h+ stale) hoặc typo.
**Fix**: Re-submit generation request.

### HTTP 429 quota exceeded

**Cause**: 
- Free tier daily quota hit
- Paid tier hourly burst limit
**Fix**:
- Đợi quota reset (display rõ trong dashboard)
- Apply quota increase tại Cloud Console → Quotas

## Download errors

### Video URI 404

**Cause**: 
- URI format khác expected (skill expect `files/{id}`)
- Server retention 2 ngày đã pass
**Fix**:
- Re-submit gen request — old URI gone
- Check response format có thay đổi (Gemini API beta — schema có thể update)

### Download timeout

**Cause**: Network slow, file lớn (4k video ~50MB).
**Fix**: Tăng timeout trong `generate.py` từ 120s → 300s.

### Saved file 0 bytes

**Cause**: Download fail mid-stream, hoặc API trả empty.
**Fix**: Re-run generate.py. Nếu lặp lại check API response trực tiếp.

## Quality issues

### Video không có motion

**Cause**: Prompt static (vd "a beach scene"), VEO không biết motion gì.
**Fix**: Add motion verbs ("waves rolling", "camera pans right"). Đọc `references/prompt-engineering.md` mục Motion cues.

### Audio không match

**Cause**: Audio cues quá specific hoặc conflict (vd nói "silent" nhưng prompt có "music").
**Fix**: 
- Audio cues nhẹ thôi (general ambient)
- Skip music spec → VEO tự generate phù hợp

### Lip-sync issue khi có dialogue

**Cause**: VEO 3 generate dialogue được nhưng lip-sync varies.
**Fix**:
- Avoid dialogue trong prompt
- Hoặc accept imperfect sync (re-gen 2-3 lần lấy best)

### Color tone lệch

**Cause**: VEO sometimes drift color từ prompt intent.
**Fix**:
- Specify color explicit ("warm golden tones", "cool blue palette")
- Re-gen với prompt clearer

### Aspect ratio sai

**Cause**: User truyền nhầm `--aspect`.
**Fix**: Skill validate accept chỉ `16:9` hoặc `9:16`. Custom aspect không support — crop post-process.

## Cost surprise

### Hóa đơn Google Cloud bất ngờ

**Cause**: Generate nhiều video không track.
**Fix**:
- Set budget alert tại Cloud Console → Billing → Budgets
- Use `veo-3.1-lite-generate-preview` cho draft (~$0.20 vs $0.40)
- Avoid 1080p/4k cho test

**Cost estimation per video** (skill auto-print trước call):
- Lite + 720p/4s: ~$0.10
- Fast + 720p/8s: ~$0.30 (default skill)
- Standard + 1080p/8s: ~$0.80
- Standard + 4k/8s: ~$1.60

### Polling burn quota

**Cause**: Mỗi GET operation count vào API quota.
**Fix**: Skill poll 10s interval (max 36 polls per gen) — đã optimal. Không tăng interval thấp hơn.

## Diagnosis nhanh

```bash
# Test API key only (no cost)
python .claude/skills/generating-videos/scripts/smoke_test.py --dry-run

# Full test (cost ~$0.10)
python .claude/skills/generating-videos/scripts/smoke_test.py
```

Dry-run cho biết:
- API key valid
- Endpoint reachable
- VEO models accessible cho account

Full test extra verify gen flow end-to-end.
