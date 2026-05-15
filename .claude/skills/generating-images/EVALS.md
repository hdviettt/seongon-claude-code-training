# EVALS — generating-images

3 scenarios để test skill có hoạt động đúng không. Chạy ở phiên Claude Code mới.

## Eval 1: Golden path — Generate single image

**Tên scenario**: User cung cấp prompt rõ ràng, dùng default model

**Precondition**:
- `.env` (hoặc `.env.local`) có `TOGETHER_AI_API_KEY` valid (format `tgp_v1_*`)
- Python 3.10+ available
- Internet
- Disk space available

**User input**:
```
/generate-image A minimalist banner design for AI training course, navy blue background, modern typography
```

**Expected behavior**:
1. Skill triggered, prompt parsed
2. Step 1: pre-check TOGETHER_AI_API_KEY OK
3. Step 2: Skip ask (prompt provided in argument), apply defaults (schnell, 1024×1024, n=1)
4. Step 3: Call Together API, ~1-2s response
5. Step 4: Download image to `output/images/<slug>-<timestamp>.jpg`, save metadata JSON
6. Step 5: Report with absolute path

**Pass criteria**:
- [ ] Image file exists tại path reported
- [ ] File size 10KB-200KB (typical FLUX schnell 1024×1024)
- [ ] Metadata JSON cạnh image, có đủ field (prompt, model, dimensions, generated_at)
- [ ] Total time ≤ 10s
- [ ] Report path absolute (clickable trong CC IDE)
- [ ] No emoji, no hype trong report

---

## Eval 2: Edge case — User không có TOGETHER_AI_API_KEY

**Tên scenario**: Fresh repo, key chưa setup

**Precondition**:
- `.env` không tồn tại HOẶC không có TOGETHER_AI_API_KEY

**User input**:
```
/generate-image test image
```

**Expected behavior**:
1. Skill Step 1 detect missing key
2. Báo user CỤ THỂ:
   - Apply free key tại https://api.together.ai/settings/api-keys
   - Add vào `.env` với format `TOGETHER_AI_API_KEY=tgp_v1_xxx`
3. Skill dừng — KHÔNG call API với placeholder key
4. KHÔNG tạo file rác

**Pass criteria**:
- [ ] Skill detect missing key (không silent fail)
- [ ] Error message có URL apply key
- [ ] Hướng dẫn format `.env` rõ
- [ ] No file created in `output/` directory
- [ ] Exit code != 0 (signal error)

---

## Eval 3: Anti-pattern — Prompt vi phạm content policy

**Tên scenario**: User prompt chứa nội dung Together AI sẽ reject (NSFW, copyrighted character, etc.)

**Precondition**:
- API key valid
- Setup OK

**User input**:
```
/generate-image Generate image of Mickey Mouse character
```

**Expected behavior**:
1. Skill call API
2. API trả HTTP 422 hoặc 400 với policy violation message
3. Skill detect error, KHÔNG retry
4. Báo user CỤ THỂ: prompt bị reject vì copyrighted character, suggest rephrase
5. Hint cách viết prompt safe (vd: "cartoon mouse character" thay vì "Mickey Mouse")
6. KHÔNG generate junk file

**Pass criteria**:
- [ ] Skill detect API rejection (không treat as success)
- [ ] Error message specific về reason (copyright/NSFW/etc.)
- [ ] Suggestion rephrase concrete
- [ ] No file created

---

## Cách chạy evals

### Manual test

1. Tạo repo trống test (vd `~/test-flux-image/`)
2. Copy `.claude/skills/generating-images/` vào
3. Setup `.env` với `TOGETHER_AI_API_KEY`
4. Mở phiên Claude Code mới
5. Chạy 3 scenarios theo precondition
6. Tick Pass criteria

### Cleanup giữa evals

- Xoá `output/images/` (test artifacts)
- Reset `.env` cho Eval 2

---

## Eval results log

| Date | Skill version | Eval 1 | Eval 2 | Eval 3 | Notes |
|---|---|---|---|---|---|
| 2026-05-15 | v0.1 | PASS (manual via direct call) | NOT TESTED | NOT TESTED | Initial release; direct Together API call confirmed work (1.1s, 13KB image returned) |
