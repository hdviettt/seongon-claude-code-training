# Frontend — Cái user thấy và chạm vào

## Định nghĩa 1 dòng

**Frontend = phần của web app mà user thấy được trên màn hình và tương tác (click, gõ, scroll).**

Đẹp hay xấu không quan trọng — quan trọng là "user thấy và chạm vào". Trang Google chỉ có 1 ô search và 2 nút — đó cũng là frontend. Trang Shopee đầy nội dung — cũng là frontend.

## 3 ngôn ngữ nền của frontend

Mọi trang web đều build từ 3 ngôn ngữ này:

### HTML — Cấu trúc, "có gì trên trang"

HTML mô tả **các thành phần** có trên trang. Tiêu đề, đoạn văn, ảnh, nút bấm, form... đều là HTML.

```html
<h1>Tiêu đề chính</h1>
<p>Đoạn văn mô tả.</p>
<button>Đăng ký</button>
```

### CSS — Hình thức, "trông như nào"

CSS quyết định **trông thế nào**: màu, font, kích thước, vị trí, animation.

```css
button {
    background: blue;
    color: white;
    padding: 12px 24px;
    border-radius: 8px;
}
```

### JavaScript — Hành động, "khi user làm X thì sao"

JavaScript là **logic** trên trang: khi click thì làm gì, khi gõ thì validate, khi scroll thì load thêm...

```javascript
button.onclick = () => {
    alert("Đã đăng ký!")
}
```

## Framework — code có sẵn để không phải viết từ đầu

3 ngôn ngữ trên thuần (vanilla) thì viết khá dài. Framework là **bộ code sẵn** giúp bạn build trang nhanh hơn.

Framework phổ biến nhất cho web app hiện nay:

### React
- Thư viện do Facebook tạo, dùng rộng nhất thế giới.
- Cho phép chia trang thành **components** (linh kiện) — viết 1 lần, dùng nhiều nơi.
- Hơi khó để bắt đầu thuần, thường dùng kèm framework lớn hơn.

### Next.js
- Framework build trên React, do Vercel tạo.
- Có sẵn nhiều tính năng: routing, SSR (SEO tốt), API routes, image optimization.
- **Default khuyến nghị** cho hầu hết web app cần SEO (blog, landing, e-commerce).

### Vue / Nuxt
- Tương tự React/Next nhưng cú pháp khác. Phổ biến ở châu Á.
- Nhẹ hơn, dễ học hơn React.

### Svelte / SvelteKit
- Modern, hiệu năng cao. Cộng đồng nhỏ hơn nhưng tăng nhanh.

## Khi giao việc cho Claude Code, chọn framework nào?

| Use case | Framework |
|---|---|
| Blog cá nhân / công ty | **Next.js** (SEO tốt) |
| Landing page khoá học | **Next.js** hoặc HTML thuần (nếu chỉ 1 trang) |
| Dashboard nội bộ (sau khi login) | **Vite + React** (không cần SEO, dev loop nhanh) |
| Site bán hàng | **Next.js** |
| App realtime (chat, collab) | **Vite + React + WebSocket** |
| Trang tĩnh 1 page | **HTML + Tailwind CSS** |

**Default an toàn:** Next.js + Tailwind CSS + shadcn/ui (thư viện UI component đẹp sẵn).

Nếu không có lý do cụ thể, nói với Claude Code: "build cho tôi 1 trang với stack Next.js + Tailwind". Claude sẽ tự setup phần còn lại.

## Tailwind CSS

Tailwind là **CSS framework** — thay vì viết CSS từ đầu, bạn dùng class có sẵn:

```html
<button class="bg-blue-500 text-white px-6 py-3 rounded-lg">
    Đăng ký
</button>
```

Tất cả button đẹp đẹp bạn thấy trên web hiện đại đều dùng Tailwind hoặc tương đương.

## UI Components Library

Component library = bộ component có sẵn, đẹp sẵn, copy về dùng.

- **shadcn/ui** — phổ biến nhất hiện nay. Copy code component về repo, customize được.
- **Radix UI** — base của shadcn/ui.
- **Material UI** — phong cách Google.
- **Chakra UI** — clean, đơn giản.

Khi giao Claude: "build trang dùng shadcn/ui cho button, card, dialog". Claude sẽ tự cài và dùng.

## Frontend khi audit dự án có sẵn

Claude Code đọc file `package.json` để biết frontend stack hiện tại:
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "tailwindcss": "^3.0.0"
  }
}
```
- `next` → đây là Next.js app.
- `vite` → đây là Vite app.
- `vue` → đây là Vue app.

Khi không chắc, nói với Claude: "đọc `package.json` và cho tôi biết frontend đang dùng gì".

## Tip thực chiến

Khi build mới, mô tả cho Claude:
- **Loại trang** (landing / blog / dashboard / e-commerce).
- **Cần SEO không** (có nếu public-facing).
- **Brand color / phong cách** (nếu có).
- **Stack ưu tiên** (Next.js + Tailwind thường an toàn).

Đừng mô tả từng component — Claude sẽ tự đề xuất layout.

## Tiếp theo

Đọc [`backend.md`](backend.md) — cái xử lý sau khi user click.
