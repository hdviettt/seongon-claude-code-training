# EVALS — generating-videos

3 scenarios để test skill. Chạy ở phiên Claude Code mới. **Note**: full eval gen video sẽ tốn ~$0.30-1.20 mỗi lần (VEO 3 paid). Dùng `--dry-run` cho test không tốn.

## Eval 1: Golden path — Generate single video

**Tên scenario**: User cung cấp prompt rõ ràng, dùng default fast model

**Precondition**:
- `.env` có `GEMINI_API_KEY` valid (format `AIza*`)
- Google Cloud project có Gemini API enabled + billing active
- Python 3.10+, internet
- Disk space ~15MB

**User input**:
```
/generate-video Wide shot of a tropical beach at sunset, gentle waves rolling onto white sand, camera slowly pans right, golden hour lighting, ocean ambient sounds
```

**Expected behavior**:
1. Skill triggered, prompt parsed
2. Step 1: pre-check GEMINI_API_KEY OK
3. Step 2: Skip ask (prompt provided), apply defaults (fast + 720p + 8s + 16:9)
4. Step 3: POST predictLongRunning → operation name returned
5. Step 4: Poll 10s interval, print progress every 30s, ~11-60s total
6. Step 5: Download MP4 to `output/videos/<slug>-<timestamp>.mp4`
7. Step 6: Report with absolute path + cost estimated (~$0.30) + retention note

**Pass criteria**:
- [ ] MP4 file exists at reported path
- [ ] File size 2-50MB (typical 720p/8s ~10MB)
- [ ] Metadata JSON cạnh video với đủ fields
- [ ] Total time ≤2 phút (fast model expectation)
- [ ] Audio present trong video (VEO 3 always gen)
- [ ] Cost estimate printed trước/sau call
- [ ] Retention 2-day note included

---

## Eval 2: Edge case — User chưa setup GEMINI_API_KEY

**Tên scenario**: Fresh repo, key chưa apply

**Precondition**: `.env` không có `GEMINI_API_KEY`

**User input**:
```
/generate-video test clip
```

**Expected behavior**:
1. Step 1 detect missing key
2. Báo user CỤ THỂ:
   - URL apply key: https://aistudio.google.com/app/apikey
   - Cần Gemini API enabled + billing trên Cloud project
   - Format `AIza...`
3. Dừng — KHÔNG call API
4. KHÔNG tạo file rác

**Pass criteria**:
- [ ] Detect missing key (không silent fail)
- [ ] Error message có URL + billing warning
- [ ] Exit code != 0
- [ ] No file created

---

## Eval 3: Anti-pattern — Invalid params (1080p với 4s duration)

**Tên scenario**: User config sai constraint VEO 3 (1080p/4k buộc duration=8)

**Precondition**: Setup OK, API key valid

**User input**:
```
/generate-video tropical beach sunset --resolution 1080p --duration 4
```

**Expected behavior**:
1. Step 2 spec validation
2. DETECT vi phạm constraint: 1080p requires duration=8
3. Báo user CỤ THỂ:
   - "1080p/4k yêu cầu duration=8 (API limit)"
   - Suggest: dùng duration=8, hoặc switch resolution=720p
4. KHÔNG submit request → KHÔNG tốn cost
5. Wait user fix or override

**Pass criteria**:
- [ ] Detect constraint violation TRƯỚC khi call API
- [ ] Error message rõ constraint + suggest fix
- [ ] KHÔNG tốn cost (chưa call submit)
- [ ] Exit code != 0

---

## Cách chạy evals

### Manual test

1. Tạo test repo (vd `~/test-veo-video/`)
2. Copy `.claude/skills/generating-videos/` vào
3. Setup `.env` với `GEMINI_API_KEY` (Eval 1, 3) hoặc empty (Eval 2)
4. Mở phiên Claude Code mới
5. Chạy 3 scenarios theo precondition
6. Tick Pass criteria

### Cost-aware testing

- Eval 1: tốn ~$0.30 (1 video fast 720p/8s)
- Eval 2: $0 (không call API)
- Eval 3: $0 (validate fail trước call)

**Total cost full eval suite: ~$0.30**.

### Dry-run mode (tiết kiệm)

Skip Eval 1 nếu không muốn tốn cost — dùng `smoke_test.py --dry-run` thay:
```bash
python .claude/skills/generating-videos/scripts/smoke_test.py --dry-run
```

Verify API key + endpoint reachable, không gen video.

---

## Eval results log

| Date | Skill version | Eval 1 | Eval 2 | Eval 3 | Notes |
|---|---|---|---|---|---|
| 2026-05-15 | v0.1 | NOT TESTED | NOT TESTED | NOT TESTED | Initial release — cần GEMINI_API_KEY để test E2E. Chưa có trong .env.local — pending. |
