# Workspace Rules: Multi-Agent Landing Page Builder

Dự án này tuân thủ các quy tắc làm việc cục bộ (Workspace Rules) được định nghĩa trong `.agents/rules/`:

## 1. Bảo mật (Security)
- Tuyệt đối không đọc, in ra màn hình hoặc tiết lộ nội dung của bất kỳ tệp chứa secrets nào như `.env`, `.env.local`, credentials hay tokens.
- Luôn sử dụng tệp mẫu `.env.example` để hướng dẫn cấu hình.
- Không hardcode API key (Gemini API Key) trong mã nguồn và không trả key ra client/API responses.
- Tệp `.env` bắt buộc phải nằm trong `.gitignore`.

## 2. Quy trình phát triển (Development)
- Bám sát chặt chẽ kế hoạch triển khai tại `docs/superpowers/plans/2026-10-27-multi-agent-landing-page-builder.md`.
- Triển khai tuần tự từng task (Task 1 -> Task 9), hoàn thiện trọn vẹn kèm test trước khi chuyển task.
- Không tự ý thay đổi kiến trúc hoặc scope của hệ thống khi chưa có sự thảo luận và đồng thuận từ người dùng.

## 3. Tiêu chuẩn mã nguồn (Coding Standards)
- Viết code rõ ràng, mang tính module cao, cấu trúc theo Single Responsibility.
- Bắt buộc dùng Type Hints đầy đủ cho Python (kèm Pydantic schemas) và TypeScript interfaces/types cho Frontend (hạn chế tối đa `any`).
- Xử lý ngoại lệ toàn diện (graceful error handling) cho tất cả các tác vụ I/O, LLM API calls, và Playwright CDP operations.

## 4. Kiểm thử và xác minh (Testing & Verification)
- Luôn chạy lệnh kiểm thử thực tế (`pytest`, `npm run build`, linting) và xác nhận pass trước khi kết luận task hoàn thành ("Evidence before assertion").
- Kiểm tra trực quan giao diện trên đầy đủ các khung nhìn Responsive (Desktop, Tablet, Mobile) và kiểm tra console logs không còn lỗi runtime.
