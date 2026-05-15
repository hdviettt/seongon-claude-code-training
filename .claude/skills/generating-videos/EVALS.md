# EVALS — generating-videos (Together AI)

3 scenarios. Full eval tốn ~$0.40-0.80 mỗi lần (Together AI paid). Dùng `--dry-run` cho test free.

## Eval 1: Golden path — Generate VEO 3 fast video

**Tên scenario**: User cung cấp prompt rõ ràng, default veo-3.0-fast

**Precondition**:
- `.env` có `TOGETHER_AI_API_KEY` valid
- Together account có credit ≥$1
- Python 3.10+, internet
- Disk space ~20MB

**User input**:
```
/generate-video Wide shot of a tropical beach at sunset, gentle waves rolling onto white sand, camera slowly pans right, golden hour lighting
```

**Expected behavior**:
1. Skill triggered
2. Step 1 pre-check key OK
3. Step 2 skip ask (argument provided), apply defaults (veo-3.0-fast + 16:9)
4. Step 3 POST /v2/videos → job id returned
5. Step 4 poll 15s interval, ~30s-4min total
6. Step 5 download MP4 → `output/videos/<slug>.mp4`
7. Step 6 report path + cost (~$0.80) + size

**Pass criteria**:
- [ ] MP4 file exists ở reported path
- [ ] Size 10-30MB (typical 8s/1920×1080)
- [ ] Metadata JSON đủ field (model, cost, size, duration, job_id)
- [ ] Total time ≤5 phút
- [ ] Audio present (VEO 3 always)
- [ ] Cost reported

---

## Eval 2: Edge case — TOGETHER_AI_API_KEY chưa setup

**Tên scenario**: Fresh repo, key thiếu

**Precondition**: `.env` không có `TOGETHER_AI_API_KEY`

**User input**:
```
/generate-video test clip
```

**Expected behavior**:
1. Step 1 detect missing key
2. Báo user CỤ THỂ:
   - URL apply: https://api.together.ai/settings/api-keys
   - Note paid (~$0.30-1.50/clip)
3. Dừng — KHÔNG call API

**Pass criteria**:
- [ ] Detect missing key
- [ ] Error có URL + cost note
- [ ] Exit code != 0
- [ ] No file created

---

## Eval 3: Anti-pattern — Invalid model name

**Tên scenario**: User truyền model name sai (thiếu provider prefix)

**Precondition**: Key valid

**User input**:
```
/generate-video tropical beach --model "veo-3.0-fast"
```

**Expected behavior**:
1. Skill submit job
2. API trả HTTP 400 "invalid model" (đúng phải `google/veo-3.0-fast`)
3. Skill báo user:
   - Model name sai format
   - Correct format `<provider>/<model>` (vd `google/veo-3.0-fast`)
   - Reference `references/video-models-comparison.md` cho full list
4. KHÔNG retry với placeholder

**Pass criteria**:
- [ ] Detect 400 error
- [ ] Suggest correct format
- [ ] Reference docs trỏ rõ
- [ ] No file created (job fail trước download)

---

## Cách chạy evals

### Manual test

1. Tạo test repo
2. Copy skill vào
3. Setup `.env` với key (Eval 1, 3) hoặc empty (Eval 2)
4. Mở phiên Claude Code mới
5. Run scenarios

### Cost-aware

- Eval 1: ~$0.80 (1 veo-3.0-fast)
- Eval 2: $0
- Eval 3: $0 (fail trước submit, hoặc job fail immediately)

**Total: ~$0.80 full suite**.

Cheap variant: replace Eval 1 model với `kwaivgI/kling-2.1-standard` ($0.40) hoặc `vidu/vidu-q1` ($0.30).

---

## Eval results log

| Date | Skill version | Eval 1 | Eval 2 | Eval 3 | Notes |
|---|---|---|---|---|---|
| 2026-05-15 | v0.2 (Together AI) | PASS (real test) | NOT TESTED | NOT TESTED | Real test: VEO 3.0 fast beach video 8s 1920×1080 13.8MB $0.80 — 218s total |
