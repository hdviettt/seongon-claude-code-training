# Cài Claude Code trên Mac

5 bước, theo thứ tự.

## 1. Tạo tài khoản Claude / Anthropic

Truy cập https://claude.ai → đăng ký bằng Google sign-in. Đăng ký Pro hoặc Max nếu dùng dài hạn.

## 2. Cài Homebrew (nếu chưa có)

Homebrew là package manager cho Mac — bạn cài mọi thứ qua nó. Mở **Terminal** (Cmd + Space → gõ "terminal") và chạy:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Cài xong, kiểm tra:
```bash
brew --version
```

## 3. Cài Git

Mac thường có Git sẵn. Kiểm tra:

```bash
git --version
```

Nếu chưa có, sẽ tự bật installer của Xcode Command Line Tools — click "Install".

Hoặc cài qua brew:
```bash
brew install git
```

## 4. Cài Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Đóng Terminal, mở lại, gõ:

```bash
claude
```

Đăng nhập theo hướng dẫn trên màn hình (mở browser → đăng nhập → copy code quay lại terminal).

## 5. Cài Bun và Python

### Bun
```bash
curl -fsSL https://bun.sh/install | bash
```

Sau khi cài, đóng terminal và mở lại. Kiểm tra: `bun --version`.

### Python
Mac có Python 3 sẵn (kiểm tra: `python3 --version`).

Nếu version cũ (< 3.10), cài bản mới qua brew:
```bash
brew install python@3.12
```

## Kiểm tra cuối cùng

```bash
git --version
claude --version
bun --version
python3 --version
```

Cả 4 ra version number → xong.

## Tips

- Cài **iTerm2** thay cho Terminal mặc định — nhiều tính năng hơn:
  ```bash
  brew install --cask iterm2
  ```
- Cài **VS Code**:
  ```bash
  brew install --cask visual-studio-code
  ```

## Khi không cài được

Xem [`troubleshooting.md`](troubleshooting.md).
