# BTVN buổi 2 — Web app full-stack

## Đề bài

Dùng Claude Code để **xây 1 web app full-stack**.

Chủ đề: bạn tự chọn. Gợi ý:
- Blog cá nhân / doanh nghiệp.
- Site bán hàng.
- Mini-tool (calculator, converter, generator...).
- Dashboard kéo dữ liệu từ nền tảng thứ 3.
- Chatbot AI.

Nếu bạn không có idea, **làm Blog cá nhân/doanh nghiệp**:
- **Phía người dùng**: nhìn và đọc được bài viết. Có cả chữ, hình ảnh trong nội dung, tiêu đề mẹ và con.
- **Phía admin**: thêm, chỉnh sửa, xoá được bài viết. Có lớp bảo mật cho admin.

## Tiêu chí

- **Full-stack**: có frontend + backend + database (không chỉ trang tĩnh).
- **Code nằm trên GitHub** (public repo).
- **Có URL public** ai cũng truy cập được (deploy lên Vercel / Railway / Netlify).
- **Có các file:**
  - `README.md` — mô tả project.
  - `CLAUDE.md` — context cho Claude Code (chạy `/init` để tạo).
  - `PLAN.md` — bảo Claude Code tạo trong khi build.
  - File export chat history với Claude.

## Cách nộp

Upload link GitHub (public) + URL site live vào form SEONGON gửi trên nhóm.

## Rules

- Làm mọi cách để đạt được kết quả cuối cùng.
- Không đặt câu hỏi cho trợ giảng (mà chưa) đặt câu hỏi cho Claude Code.

## Deadline

23h59 Thứ 5 của tuần học buổi 2.

## Gợi ý quy trình

### Bước 1 — Mô tả idea cho Claude (thật chi tiết)

```
Tôi muốn xây 1 web app blog cá nhân full-stack.

Tính năng:
- Phía người dùng (public): xem trang chủ với list bài viết, click vào 
  đọc chi tiết. Bài có chữ + ảnh + tiêu đề cấp 1, 2.
- Phía admin (sau login): thêm/sửa/xoá bài, upload ảnh.

Stack ưu tiên:
- Frontend: Next.js 14 + Tailwind + shadcn/ui
- Backend: Next.js API routes
- Database: Postgres trên Railway (hoặc Supabase)
- Auth: NextAuth + Google OAuth (admin login bằng email cụ thể)
- Deploy: Vercel

Bạn hãy lên PLAN.md chi tiết cho dự án này trước. Plan xong tôi sẽ duyệt 
rồi mới bắt đầu code.
```

### Bước 2 — Plan Mode

Sau khi Claude lên PLAN.md, dùng Plan Mode (Shift + Tab 2 lần hoặc `/plan`) để Claude planning chi tiết hơn cho từng step.

### Bước 3 — Build từng phần

Đừng yêu cầu build hết 1 lần. Tách:
1. Setup project (Next.js + Tailwind + shadcn).
2. Setup database (schema).
3. Trang chủ (list bài).
4. Trang chi tiết bài.
5. Auth.
6. Admin CRUD.
7. Upload ảnh.
8. Deploy.

Mỗi bước: yêu cầu Claude làm → test → commit → tiếp.

### Bước 4 — Push lên GitHub + Deploy

- Tạo repo public trên GitHub (qua `gh repo create` hoặc dashboard).
- Push code.
- Connect Vercel với repo → auto-deploy.
- Test URL live.

### Bước 5 — Audit trước khi nộp

Hỏi Claude:
```
Hãy audit toàn diện web app này trước khi tôi nộp:
- Kiểm tra frontend, backend, database, auth.
- Kiểm tra env vars, secrets không bị leak.
- Kiểm tra UI/UX responsive.
- Kiểm tra security (OWASP basic).
Xuất báo cáo Critical / High / Medium / Low.
```

Fix các vấn đề Critical / High trước khi nộp.

## Tips từ học viên khoá trước

- **Mô tả đầu vào cực kỹ.** Càng nhiều context Claude có ngay từ đầu, càng ít phải sửa.
- **Dùng plan mode** cho task lớn.
- **Feedback và debug nhiều lượt.** Output đầu tiên hiếm khi hoàn hảo.
- **Cấu trúc folder rõ ràng:** tách `frontend/` và `backend/` nếu có thể, hoặc dùng convention Next.js (`app/`, `components/`, `lib/`).
- **Luôn nhớ folder hiện tại** — Claude làm việc trong folder bạn mở terminal. Cẩn thận `cd` nhầm.

## Kiến thức liên quan

Toàn bộ folder [`knowledge/02-tech-stack-web-app/`](../knowledge/02-tech-stack-web-app/):
- [`frontend.md`](../knowledge/02-tech-stack-web-app/frontend/)
- [`backend.md`](../knowledge/02-tech-stack-web-app/backend/)
- [`database.md`](../knowledge/02-tech-stack-web-app/database/)
- [`security.md`](../knowledge/02-tech-stack-web-app/security/)
- [`deployment.md`](../knowledge/02-tech-stack-web-app/deployment/)
- [`source-control.md`](../knowledge/02-tech-stack-web-app/source-control/)
