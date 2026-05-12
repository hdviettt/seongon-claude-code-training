# Source Control — Git và GitHub

## Định nghĩa 1 dòng

**Source control = hệ thống theo dõi mọi thay đổi của code, cho phép quay lại version cũ bất cứ lúc nào.**

Git là source control phổ biến nhất. GitHub là dịch vụ host code Git online (Microsoft sở hữu).

## Tại sao cần Git khi bạn không code?

Dù bạn không tự viết code, Claude Code viết code cho bạn → bạn vẫn cần Git để:

1. **Backup**: code có lịch sử, không lo mất.
2. **Quay lại version cũ**: Claude làm hỏng → revert 1 lệnh là xong.
3. **Collaborate**: nhiều người (hoặc nhiều phiên Claude) làm việc cùng repo.
4. **Deploy**: hosting hiện đại (Vercel, Railway) deploy thẳng từ Git.

## Các khái niệm quan trọng

### Repository (repo)

= 1 dự án trên Git. 1 repo = 1 folder có lịch sử Git.

### Commit

= 1 "snapshot" của code tại 1 thời điểm. Mỗi commit có ID duy nhất, message mô tả thay đổi.

```bash
git commit -m "thêm trang đăng ký"
```

### Branch (nhánh)

= 1 dòng phát triển độc lập của code. `main` (hoặc `master`) là branch chính.

Khi làm 1 tính năng mới, bạn tạo branch riêng (vd: `feature/dang-ky`), làm xong thì merge vào `main`.

### Push / Pull

- **Push**: đẩy code từ máy bạn lên server (GitHub).
- **Pull**: lấy code mới nhất từ server về máy.

### Pull Request (PR)

= yêu cầu merge branch của bạn vào `main`. Có review, có CI tự chạy, có thể comment góp ý.

## 5 lệnh Git cần biết

Đa số bạn không cần gõ — Claude Code sẽ làm hết. Nhưng cần hiểu:

```bash
git status              # xem thay đổi hiện tại
git add <file>          # đánh dấu file để commit
git commit -m "..."     # tạo commit với message
git push                # đẩy lên GitHub
git pull                # kéo từ GitHub về
```

## Quy trình làm việc với Claude Code và Git

### Khi bắt đầu dự án mới

```
1. Tạo folder dự án trên máy.
2. Mở Claude Code trong folder đó.
3. Nói: "init Git, tạo .gitignore phù hợp, commit lần đầu."
4. Claude làm hết.
5. Bạn tạo repo trên GitHub (qua dashboard hoặc lệnh `gh repo create`).
6. Nói Claude: "push lên repo này: <URL>"
7. Xong.
```

### Khi làm 1 tính năng mới

```
1. Nói Claude: "tạo branch mới cho tính năng X."
2. Làm việc, Claude commit từng bước.
3. Khi xong: "push branch lên, mở PR."
4. Review trên GitHub.
5. Merge vào main.
```

### Khi muốn quay lại version cũ

```
1. Nói Claude: "xem history 10 commit gần nhất."
2. Tìm commit cần quay lại.
3. Nói: "revert về commit ABC123" hoặc "rollback file X về trước commit ABC123."
```

## `.gitignore` — File không commit

`.gitignore` liệt kê các file/folder **không được commit** lên Git:

```
node_modules/        # thư viện cài về, dung lượng lớn
.env                 # secret
.env.local           # secret local
*.log                # log file
.DS_Store            # rác Mac
dist/, build/        # output build
.next/               # output Next.js
```

**Quan trọng:** `.env` luôn phải có trong `.gitignore`. Nếu lỡ commit `.env` chứa secret, **đổi secret ngay lập tức** vì nó đã có trên Git history (kể cả khi bạn delete).

## Commit message — viết cho người, không cho máy

Commit message tốt:
```
feat(auth): thêm login bằng Google
fix(form): validate email không hợp lệ
docs: cập nhật README
```

Format phổ biến (Conventional Commits):
- `feat` — tính năng mới
- `fix` — sửa bug
- `refactor` — sắp xếp lại code, không đổi behavior
- `docs` — tài liệu
- `chore` — task vặt (cập nhật dependency, etc)
- `test` — thêm/sửa test

Khi Claude Code commit cho bạn, nó sẽ tự viết message theo style này.

## GitHub vs các option khác

- **GitHub** — phổ biến nhất, Microsoft sở hữu. Free cho repo private vô hạn (với 3 collaborator).
- **GitLab** — open source, self-host được.
- **Bitbucket** — của Atlassian, ít phổ biến hơn.

Default: **GitHub**. Cài CLI `gh` để dùng từ terminal:
```bash
# Windows
winget install GitHub.cli

# Mac
brew install gh
```

Sau khi cài: `gh auth login` → đăng nhập.

## Repo public vs private

- **Public**: ai cũng xem được. Dùng cho project open source, portfolio.
- **Private**: chỉ bạn và người được mời. Dùng cho code công ty, project nhạy cảm.

**Quy tắc:** nếu repo có secret (kể cả từng có và đã xoá), giữ private.

## ⚠️ Danger zone

3 lệnh Git nguy hiểm:

1. **`git push --force`** trên branch chia sẻ — overwrite lịch sử của người khác.
2. **`git reset --hard`** trên branch có commit chưa push — mất hết thay đổi.
3. **Commit file `.env`** chứa secret thật — kể cả xoá sau đó, secret vẫn lộ.

Khi Claude muốn force push hoặc reset hard, dừng lại, hỏi kỹ.

## Tip thực chiến

- **Commit nhỏ, thường xuyên.** 5-10 commit/ngày tốt hơn 1 commit khổng lồ.
- **Mỗi branch 1 tính năng.** Không gộp 3 tính năng vào 1 branch.
- **Pull main mỗi sáng** trước khi bắt đầu — tránh conflict.
- **Khi Claude làm hỏng, đừng panic** — `git status` xem thay đổi, `git restore <file>` để bỏ thay đổi 1 file, `git reset --hard HEAD` để bỏ tất cả về commit gần nhất.

## Tóm tắt

Git không khó với người dùng Claude Code — bạn để Claude làm hết phần phức tạp. Chỉ cần nhớ:
- Repo = dự án.
- Commit = snapshot.
- Branch = nhánh phát triển.
- Push = lên cloud. Pull = về máy.
- `.env` không bao giờ commit.

## Quay lại tech stack overview

Đọc [`README.md`](README.md) của folder này để xem flow tổng.
