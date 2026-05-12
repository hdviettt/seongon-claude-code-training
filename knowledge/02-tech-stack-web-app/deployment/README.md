# Deployment — Đưa code lên Internet

> **Sub-file trong folder này:**
> - [`platforms.md`](platforms.md) — Recipe deploy chi tiết: Vercel+Neon, Railway, Cloudflare Pages, domain DNS, monitoring.

## Định nghĩa 1 dòng

**Deployment = đưa code từ máy bạn lên server để người khác truy cập được qua Internet.**

App chạy trên máy bạn (`localhost:3000`) chỉ bạn thấy. Muốn user thật vào được, phải deploy.

## Pipeline 4 bước

```
Source code → Git → CI/CD → Hosting
   (máy bạn)  (cloud) (build/test) (live)
```

1. **Source code**: bạn viết code trên máy bạn.
2. **Git**: push code lên GitHub (hoặc nơi khác).
3. **CI/CD**: hệ thống tự động build và test code.
4. **Hosting**: code chạy trên server cloud, có URL public.

## Hosting platforms

### Cho web app Next.js / React

**Vercel** — của team Next.js. Deploy 1 click từ GitHub. Free tier rất rộng.
- Strength: edge network global, preview deploy cho mỗi PR, auto HTTPS.
- Weakness: DB không cùng nhà (phải dùng provider khác).

**Railway** — deploy app + DB cùng 1 nơi.
- Strength: Postgres + app cùng repo, $5-10/tháng cho 1 app nhỏ.
- Weakness: không có edge network như Vercel.

**Netlify** — tương tự Vercel, tốt cho static site.

**Cloudflare Pages** — static + edge functions, miễn phí rộng.

### Cho app cần GPU (AI)

**Modal**, **RunPod**, **Replicate** — chạy AI inference với GPU.

### Cho enterprise / có infra AWS

**AWS** (EC2, ECS, Fargate, Lambda) — flexible nhất, nhưng setup phức tạp.
**Google Cloud** (GCE, Cloud Run).
**Azure**.

### Khuyến nghị cho người mới

| Use case | Pick |
|---|---|
| Web app Next.js, không DB phức tạp | **Vercel** |
| Web app + Postgres + cần region cố định | **Railway** |
| Static site / blog | **Cloudflare Pages** hoặc **Vercel** |
| App có cron / worker / queue | **Railway** với multiple services |

**Default an toàn:** Railway (cho app full-stack) hoặc Vercel (cho Next.js không DB).

## CI/CD — Tự động build, test, deploy

**CI** (Continuous Integration) = mỗi lần push code, hệ thống tự build và test.

**CD** (Continuous Deployment) = nếu build và test pass, tự deploy lên production.

### GitHub Actions

Tool CI/CD phổ biến nhất, tích hợp sẵn với GitHub. Workflow định nghĩa trong `.github/workflows/*.yml`:

```yaml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
      - run: npm test
```

### Auto-deploy từ Git push

Vercel / Railway có sẵn tính năng:
- Bạn connect GitHub repo.
- Mỗi lần push lên `main` → auto deploy.
- Mỗi lần mở PR → auto tạo preview URL.

→ Không cần config CI/CD thủ công cho task deploy.

## Domain & DNS

Sau khi deploy, app có URL dạng `your-app.vercel.app`. Muốn URL đẹp như `seongon.com`?

1. Mua domain ở **Namecheap**, **GoDaddy**, hoặc **Cloudflare**.
2. Trên dashboard hosting (Vercel/Railway), add custom domain.
3. Update DNS records ở provider domain → trỏ về hosting.
4. Đợi DNS propagate (5 phút - 24 giờ).

**Khuyến nghị:** dùng **Cloudflare** cho DNS — miễn phí, có WAF, có proxy.

## Pipeline chuẩn

```
1. Code trên máy → git push origin feature/x
2. Mở PR
3. CI tự chạy: lint + typecheck + test
4. Vercel/Railway tạo preview deploy
5. Review code → merge to main
6. Auto-deploy lên production
```

Quy tắc:
- **Không deploy thẳng từ local lên production.** Luôn qua Git.
- **Branch protection trên main.** Bắt buộc CI pass + review trước khi merge.
- **Migration DB chạy thủ công** hoặc qua release step riêng — không tự động trong build.

## Environment

Có 3 environment phổ biến:
- **Development**: máy local của bạn.
- **Staging / Preview**: server giống production nhưng riêng — test trước khi đưa lên production.
- **Production**: server thật, user thật.

Mỗi env có **secret riêng** (DB URL, API key khác nhau).

## Monitoring sau khi deploy

Sau khi app live, theo dõi:

- **Logs**: dashboard Vercel/Railway có sẵn. Stream log để debug.
- **Error tracking**: **Sentry** (free tier 5k errors/tháng) — bắt mọi crash, alert email.
- **Uptime**: **BetterStack**, **Cronitor** — alert khi site down.
- **Analytics**: **Plausible** (privacy-first), **Vercel Analytics**, hoặc Google Analytics.

**Default cho người mới:** chỉ cần Sentry + uptime monitor cơ bản. Datadog, New Relic là overkill cho team nhỏ.

## ⚠️ Danger zone

3 việc **không bao giờ** để Claude tự quyết khi deploy:

1. **Deploy lên production** mà chưa test trên staging.
2. **Chạy migration DB production** mà chưa backup.
3. **Force push lên `main`** — có thể overwrite lịch sử commit, mất code.

Khi Claude muốn làm 1 trong 3 việc, dừng lại, xác nhận trước.

## Tip thực chiến

Khi build mới, hỏi Claude:
> "Setup deployment cho repo này lên Railway, có CI/CD qua GitHub Actions chạy lint + test trước khi deploy."

Claude sẽ:
1. Tạo file `.github/workflows/ci.yml`.
2. Tạo `railway.json` config.
3. Tạo `.env.example` để bạn biết secret nào cần set.
4. Hướng dẫn bạn connect GitHub với Railway.

## Khi audit dự án có sẵn

Đọc:
- `.github/workflows/*.yml` — CI/CD setup.
- `railway.json`, `vercel.json`, `fly.toml`, `netlify.toml` — hosting config.
- `Dockerfile` — nếu container hoá.
- `package.json` scripts → `build`, `start`, `deploy`.

Hỏi Claude:
> "Repo này deploy ở đâu, có CI/CD chưa, monitoring có chưa?"

## Tiếp theo

Đọc [`source-control.md`](source-control.md) — Git và GitHub cơ bản.
