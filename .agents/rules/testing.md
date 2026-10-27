# Testing & Verification Rules

## Quy tắc kiểm thử và xác minh chất lượng

1. **Kiểm thử tự động trước khi hoàn thành (Test-First & Evidence)**:
   - Trước khi tuyên bố một task hoàn thành hoặc sửa xong bug, bắt buộc phải chạy lệnh kiểm thử thực tế và xác nhận output thành công.
   - Chạy test suite backend bằng `pytest` và đảm bảo 100% test cases pass.
   - Chạy kiểm tra build frontend bằng `npm run build` và linting trước khi bàn giao.

2. **Kiểm thử hiển thị giao diện (Visual & UX Verification)**:
   - Khi chỉnh sửa hoặc thêm mới giao diện (Frontend / Live Preview / Inspector), phải kiểm tra thực tế trên cả 3 kích thước màn hình: Desktop (100%), Tablet (768px), và Mobile (375px).
   - Kiểm tra console logs trong trình duyệt để đảm bảo không có cảnh báo nghiêm trọng hoặc lỗi runtime JavaScript chưa được xử lý.

3. **Nguyên tắc "Chứng cứ trước khẳng định" (Evidence Before Assertion)**:
   - Không đưa ra kết luận "code đã chạy tốt" nếu chưa thực sự chạy lệnh kiểm tra và nhìn thấy log thành công.
