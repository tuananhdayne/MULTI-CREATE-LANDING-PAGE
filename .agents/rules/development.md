# Development Rules

## Quy tắc tuân thủ kế hoạch và quy trình phát triển

1. **Tuân thủ Implementation Plan**:
   - Mọi công việc phát triển phải bám sát tuyệt đối theo kế hoạch đã được phê duyệt trong `docs/superpowers/plans/2026-10-27-multi-agent-landing-page-builder.md`.
   - Không tự ý thay đổi kiến trúc hệ thống (FastAPI + LangGraph + React/Vite + Single HTML5 + Dual DevTools) hoặc scope dự án khi chưa có sự thảo luận và đồng ý của người dùng.

2. **Triển khai tuần tự theo từng Task (Bite-sized Execution)**:
   - Thực hiện từng task một cách tuần tự (Task 1 -> Task 2 -> ... -> Task 9).
   - Mỗi task phải hoàn thành trọn vẹn cả mã nguồn, kiểm thử tương ứng và tự kiểm tra trước khi chuyển sang task kế tiếp.
   - Không nhảy cóc hoặc viết code dàn trải nhiều tính năng cùng một lúc.

3. **Cập nhật tiến độ**:
   - Đánh dấu checkbox (`[x]`) trong tệp plan tương ứng khi mỗi step/task hoàn thành.
   - Báo cáo rõ ràng kết quả kiểm thử sau mỗi task hoàn thành.
