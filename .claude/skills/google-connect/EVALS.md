# EVALS — google-connect

3 scenarios để test skill có hoạt động đúng không. Chạy ở phiên Claude Code mới (fresh context).

## Eval 1: Golden path — Học viên mới setup lần đầu

**Tên scenario**: Repo trắng, học viên chưa có Google Cloud project

**Precondition**:
- Repo mới (không có `.env`, không có `.claude/hooks/`)
- Python 3.10+ installed
- Học viên có Gmail account

**User input**:
```
/google-connect
```

**Expected behavior**:
1. Skill `google-connect` triggered
2. Step 1: Pre-check Python + packages, install nếu thiếu
3. Step 2: Hỏi "Đã có Google Cloud project chưa?" → CHƯA → walkthrough 6 sub-steps từ `references/google-cloud-setup.md`
4. Step 3: User paste CLIENT_ID + SECRET → skill validate format + ghi `.env`
5. Step 4: Run `oauth_refresh.py` → browser mở → user authorize → token written
6. Step 5: Run `install.py` → deploy hook + lib + patch settings.local.json
7. Step 6: Run `smoke_test.py` → PASS
8. Step 7: Report 3 files created, hook active, smoke PASS

**Pass criteria**:
- [ ] `.env` ở project root có GOOGLE_CLIENT_ID + GOOGLE_CLIENT_SECRET + GOOGLE_REFRESH_TOKEN
- [ ] `.claude/hooks/google_token_refresh.py` tồn tại
- [ ] `.claude/skills/lib/oauth_refresh.py` tồn tại
- [ ] `.claude/settings.local.json` có entry PostToolUse matcher "Bash" với hook command
- [ ] `.gitignore` có `.env`
- [ ] Smoke test exit code 0
- [ ] Tổng thời gian end-to-end ≤15 phút (lần đầu, bao gồm Cloud Console setup)
- [ ] User không cần Google nội dung kỹ thuật ngoài Cloud Console click-through

---

## Eval 2: Edge case — Học viên đã có Google Cloud nhưng .env trắng

**Tên scenario**: Returning user — Cloud project đã có sẵn, chỉ cần re-setup OAuth

**Precondition**:
- Repo mới (không có `.env`)
- Học viên đã có Google Cloud project + OAuth Client ID từ lần đào tạo trước
- User có CLIENT_ID + SECRET trong note/clipboard

**User input**:
```
/google-connect

Tôi đã có Google Cloud project + OAuth Client ID rồi, chỉ cần setup .env và refresh token thôi.
```

**Expected behavior**:
1. Skill triggered
2. Step 1: Pre-check OK
3. Step 2: User confirm "đã có credentials" → SKIP walkthrough Cloud Console
4. Step 3: Ask user paste CLIENT_ID + CLIENT_SECRET → validate format
5. Skip Step 2 sub-steps (đỡ thời gian)
6. Step 4-7: như Eval 1

**Pass criteria**:
- [ ] Skill DETECT user đã có credentials, KHÔNG force walk through 6 sub-steps Cloud Console
- [ ] Format validation vẫn enforce (reject paste sai format)
- [ ] Tổng thời gian end-to-end ≤5 phút
- [ ] All deliverables như Eval 1

---

## Eval 3: Anti-pattern — User input bị reject

**Tên scenario**: User paste sai format CLIENT_ID

**Precondition**: Repo mới

**User input** (sau khi skill hỏi paste CLIENT_ID):
```
abcd1234
```

**Expected behavior**:
1. Skill ở Step 3 validate format
2. DETECT format không match regex `^\d+-[\w]+\.apps\.googleusercontent\.com$`
3. Report cụ thể: "CLIENT_ID format invalid. Expected: 123456-abc...apps.googleusercontent.com"
4. Hỏi user paste lại → nếu lần 2 vẫn sai, hỏi user check Cloud Console
5. KHÔNG ghi `.env` với value invalid
6. KHÔNG tiếp tục Step 4 OAuth flow

**Pass criteria**:
- [ ] Skill DETECT format invalid (không silent accept)
- [ ] Error message CỤ THỂ — expected vs got
- [ ] `.env` KHÔNG bị ghi với value invalid
- [ ] Step 4 KHÔNG chạy (không waste browser session)
- [ ] User được hướng dẫn cụ thể cách lấy lại CLIENT_ID đúng

---

## Cách chạy evals

### Manual test (recommended)

1. Tạo 1 repo trống (vd: `~/test-google-connect/`)
2. Copy `.claude/skills/google-connect/` từ workspace vào repo test
3. Mở phiên Claude Code mới ở repo test
4. Chạy Eval 1/2/3 theo precondition
5. Tick Pass criteria sau khi skill xong

### Cleanup giữa các evals

Để re-run scenario, xoá:
- `.env`
- `.claude/hooks/google_token_refresh.py`
- `.claude/skills/lib/oauth_refresh.py`
- Entry trong `.claude/settings.local.json` (manual edit)
- `.gitignore` line `.env` (nếu test fresh `.gitignore`)

Hoặc dùng git: `git stash` để revert mọi thay đổi.

---

## Eval results log

| Date | Skill version | Eval 1 | Eval 2 | Eval 3 | Notes |
|---|---|---|---|---|---|
| 2026-05-15 | v0.1 | NOT TESTED | NOT TESTED | NOT TESTED | Initial release — pending manual test ở phiên CC fresh |
