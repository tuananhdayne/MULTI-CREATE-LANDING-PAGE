# Coding Standards Rules

## Quy tắc tiêu chuẩn mã nguồn và chất lượng code

1. **Rõ ràng và Tính Module (Clean Code & Modularity)**:
   - Mã nguồn phải được phân tách thành các module/component có trách nhiệm duy nhất (Single Responsibility Principle).
   - Tên biến, hàm, lớp phải mang tính gợi tả, rõ nghĩa bằng tiếng Anh chuẩn.
   - Tránh các hàm quá dài hoặc các file "god object". Giữ các file tinh gọn, dễ đọc, dễ bảo trì.

2. **Type Safety & Type Annotations**:
   - **Python (Backend)**: Bắt buộc sử dụng Type Hints đầy đủ cho tham số đầu vào và kiểu dữ liệu trả về của tất cả các hàm/phương thức. Sử dụng Pydantic models cho schema dữ liệu.
   - **TypeScript (Frontend)**: Khai báo interface/type rõ ràng cho tất cả props, state và API payload; tuyệt đối hạn chế dùng `any`.

3. **Xử lý ngoại lệ và lỗi (Graceful Error Handling)**:
   - Mọi thao tác kết nối mạng, gọi API ngoài (Gemini API, Playwright CDP), đọc ghi dữ liệu đều phải được bọc trong khối `try...except` hoặc `try...catch`.
   - Có cơ chế retry hoặc fallback khi LLM gặp timeout hoặc rate limit.
   - Phản hồi lỗi thân thiện, chi tiết cho người dùng trên giao diện thay vì để ứng dụng crash hoặc màn hình trắng.
