# Security Rules

## Quy tắc bảo mật và quản lý thông tin nhạy cảm

1. **Tuyệt đối không đọc hoặc tiết lộ bí mật**:
   - Không được đọc nội dung, hiển thị, sao chép hoặc in ra màn hình bất kỳ tệp chứa thông tin nhạy cảm nào như `.env`, `.env.local`, các tệp credentials, private keys, SSH keys, hoặc tokens.
   - Khi cần thiết lập môi trường, chỉ tham chiếu và làm việc với tệp mẫu `.env.example`.

2. **Bảo vệ API Keys**:
   - Tuyệt đối không hardcode API keys (bao gồm `GEMINI_API_KEY`) trong mã nguồn (backend lẫn frontend).
   - Không trả về API key qua bất kỳ REST API endpoint, GraphQL, hoặc SSE/WebSocket payload nào ra client.
   - Không in (print/log) API keys ra terminal, console log hoặc tệp log hệ thống.

3. **Kiểm soát phiên bản và Git**:
   - Tệp `.env` và các tệp môi trường thực tế phải luôn được khai báo trong `.gitignore` ngay từ đầu và không bao giờ được commit lên git repository.
   - Trước khi commit mã nguồn, phải kiểm tra kỹ diff để đảm bảo không có bất kỳ secret/token nào bị đưa vào staging.
