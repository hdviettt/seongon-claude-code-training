# Lập trình cơ bản

Đây là **nền** — đọc trước khi học tech stack. Bạn không cần biết code, nhưng cần hiểu các khái niệm sau để đọc được code Claude viết và giao việc đúng.

## Lập trình là gì

Lập trình là **con người dùng ngôn ngữ lập trình để hướng dẫn máy tính làm việc**.

Ngôn ngữ lập trình là cầu nối giữa cách con người nghĩ và cách máy tính hiểu. Máy tính chỉ hiểu `01010101...`, nhưng bạn không cần viết bằng 0 và 1 — bạn viết bằng Python, JavaScript, Go... và máy sẽ tự dịch.

Ví dụ — bài toán: cho 2 số x và y, cộng chúng lại.

**Cách con người hiểu:**
> Cộng x với y, in ra kết quả. Nếu x hoặc y không phải số, báo lỗi.

**Cách viết bằng ngôn ngữ lập trình (giả lập tiếng Việt):**
```
định nghĩa hàm cộng(x, y):
    nếu (x hoặc y không phải số):
        ghi("vui lòng nhập số")
    còn không thì:
        tổng = x + y
        ghi(tổng)

cộng(2, 1)
```

**Cách máy tính hiểu:**
```
01010101010...
```

Máy nhận lệnh `cộng(2, 1)` → trả về `3` (chính là `11` trong nhị phân).

## 4 khái niệm quan trọng nhất

### 1. Biến (Variable) — chiếc hộp chứa dữ liệu

Biến là chỗ chứa giá trị. Cứ tưởng tượng nó là chiếc hộp, có thể lấy đồ ra cất đồ vào.

```
tên = "Việt"
tuổi = 21
```

Có nhiều **loại hộp** (loại dữ liệu):

- **String (chữ)**: `"Việt"`, `"SEONGON"` — luôn nằm trong dấu ngoặc kép.
- **Số (int, float)**: `21`, `8.5` — không cần ngoặc.
- **Boolean (đúng/sai)**: `True`, `False` — chỉ có 2 giá trị.
- **List (danh sách)**: `[8, 10, 7]`, `["đánh cầu", "xem phim"]` — nhiều giá trị trong `[]`.
- **Object (đối tượng)**: 
  ```
  học viên = {
      "tên": "Việt",
      "tuổi": 21,
      "sở thích": ["đánh cầu", "xem phim"]
  }
  ```
  Tập hợp nhiều cặp key-value trong `{}`.

### 2. Hàm (Function) — cái máy xử lý

Hàm là 1 cái máy. **Đưa nguyên liệu vào → máy xử lý → trả về kết quả**.

```
cộng(2, 1)
```

- `cộng` là tên hàm.
- `(2, 1)` là **tham số** (parameters) — nguyên liệu đưa vào.
- Kết quả: `3`.

Trong web app, mọi nút bấm, mọi action đều gọi 1 hàm.

Ví dụ trên trang bán hàng Printify:
```
product(tên, giá, ảnh, tag, ...)
```
- `product` là hàm vẽ ra 1 thẻ sản phẩm.
- `tên, giá, ảnh, tag` là tham số.
- Mỗi sản phẩm trên trang là kết quả của hàm này được gọi 1 lần với bộ tham số khác nhau.

### 3. Toán tử (Operators) — phép toán & so sánh

- `+`, `-`, `*`, `/` — cộng trừ nhân chia.
- `==` — bằng (lưu ý: `=` là gán, `==` là so sánh).
- `!=` — khác.
- `<`, `>`, `<=`, `>=` — so sánh lớn nhỏ.
- `and`, `or`, `not` — logic.

### 4. Cấu trúc điều khiển (Control Flow) — người chỉ đường

Quyết định khi nào chạy đoạn nào:

```
nếu (điều kiện):
    làm A
còn không thì:
    làm B
```

Trong tiếng Anh: `if ... else`.

Ví dụ:
```
nếu (số tiền >= 100000):
    áp dụng giảm giá
còn không thì:
    không giảm
```

## Thư viện (Library)

**Thư viện là code người khác viết, mình chỉ việc đem về dùng lại.**

Ví dụ: bạn muốn vẽ biểu đồ — không cần tự viết code vẽ từ đầu, dùng thư viện `chart.js` hoặc `recharts`. Bạn muốn xử lý ngày tháng — dùng thư viện `date-fns`.

Khi Claude Code build app, nó dùng rất nhiều thư viện. Đừng sợ — đó là chuyện bình thường.

## Tóm tắt 1 trang

| Khái niệm | Vai trò | Ví dụ |
|---|---|---|
| Biến | Hộp chứa data | `x = 5`, `tên = "Việt"` |
| Hàm | Máy xử lý | `cộng(2, 1)` → `3` |
| Toán tử | Phép toán / so sánh | `+`, `==`, `>` |
| Control flow | Quyết định nhánh | `if ... else` |
| Thư viện | Code người khác viết, dùng lại | `import chart.js` |

Hiểu 5 thứ này là đủ để đọc 90% code Claude Code viết ra.

## Tiếp theo

Đọc [`frontend.md`](frontend.md) để bắt đầu tech stack của 1 web app.
