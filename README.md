# 🚀 LandingCraft: Multi-Agent Landing Page Builder

Hệ thống Full-stack phối hợp **5 Agent chuyên sâu** (sử dụng Google Gemini / 9router) để tự động nghiên cứu, viết nội dung, thiết kế giao diện và lập trình trang **Landing Page HTML5 + Tailwind CSS** hoàn chỉnh, hỗ trợ xem trước thời gian thực (**Live Preview**) và chỉnh sửa từng phần tử theo kiểu **Chrome DevTools Click-to-Inspect**.

---

## 🌟 Tính Năng Nổi Bật

1. **Đội ngũ 5 AI Agents chuyên sâu**:
   - 🧭 **Product Strategist**: Phân tích đề bài, xây dựng dàn ý cấu trúc tối ưu tỷ lệ chuyển đổi (CRO Blueprint).
   - ✍️ **Copywriter**: Viết tiêu đề bắt mắt (Headlines), lời kêu gọi hành động (CTAs), lợi ích sản phẩm và FAQs.
   - 🎨 **UI/UX Designer**: Thiết lập bảng màu Tailwind, Typography Google Fonts, hiệu ứng Glassmorphism & Micro-interactions.
   - 💻 **Frontend Coder**: Tổng hợp và sinh ra tệp mã HTML5 độc lập nạp Tailwind CSS CDN & Lucide Icons.
   - 🔍 **Visual QA & DevTools**: Kiểm tra tính toàn vẹn cú pháp HTML và các thẻ đóng (vòng lặp phản biện Critic-fix loop).
2. **Trải nghiệm Chrome DevTools Click-to-Inspect**:
   - Nhấp trực tiếp vào bất kỳ phần tử nào trên giao diện (nút bấm, tiêu đề, thẻ card) để ra lệnh cho AI sửa chính xác phần đó.
3. **Quản lý phiên bản & Xem trước đa màn hình**:
   - Hỗ trợ **Hoàn tác (Undo)** và **Làm lại (Redo)** qua từng lần chỉnh sửa.
   - Chuyển đổi khung nhìn linh hoạt: **Desktop (100%)**, **Tablet (768px)**, **Mobile (375px)**.
   - Xuất bản và tải về tệp `index.html` chạy ngay chỉ với 1 cú click.
4. **Hỗ trợ 9router Local Gateway**:
   - Tích hợp sẵn cổng kết nối `http://localhost:20128/v1` của 9router với các model như `ag/gemini-3.7-flash-high` hoặc Google AI Studio trực tiếp.
   - Tuyệt đối bảo mật API Key, không lưu vết hay để lộ key ra ngoài.

---

## 🛠️ Hướng Dẫn Cài Đặt & Khởi Chạy

### 1. Cấu hình biến môi trường
Sao chép tệp mẫu `.env.example` thành `.env`:
```bash
cp .env.example .env
```
Mở `.env` và điền key của bạn:
```env
# Gemini API Key hoặc 9router Token
GEMINI_API_KEY=your_key_here

# 9router Gateway (để trống nếu dùng thẳng Google API)
LLM_BASE_URL=http://localhost:20128/v1

# Model Gemini mong muốn
GEMINI_MODEL=ag/gemini-3.7-flash-high

HOST=0.0.0.0
PORT=8000
```

---

### 2. Khởi chạy Backend Server (FastAPI)
```bash
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
* API Documentation (Swagger UI): `http://localhost:8000/docs`
* Health Check: `http://localhost:8000/api/health`

---

### 3. Khởi chạy Frontend (React + Vite)
Mở một terminal mới:
```bash
cd frontend
npm run dev
```
Truy cập giao diện Web tại: **`http://localhost:5173`**

---

## 🧪 Chạy Kiểm Thử (Testing)

### Kiểm thử Backend (pytest):
```bash
PYTHONPATH=backend pytest backend/tests/ -v
```
*(Hiện có 22 test cases pass 100% bao gồm cả E2E lifecycle)*

### Kiểm tra build Frontend:
```bash
cd frontend && npm run build
```

---

## 📁 Cấu Trúc Mã Nguồn

```
GEN_LANDING/
├── .env.example                # Tệp mẫu cấu hình môi trường
├── .gitignore                  # Loại trừ .env và các dữ liệu nhạy cảm
├── AGENTS.md                   # Workspace rules cho Antigravity IDE
├── README.md                   # Hướng dẫn dự án
├── backend/
│   ├── app/
│   │   ├── config.py           # Quản lý cấu hình an toàn
│   │   ├── main.py             # FastAPI entrypoint & SSE streaming
│   │   ├── agents/             # 5 Agent chuyên sâu & Element Editor
│   │   ├── graph/              # LangGraph StateGraph & Critic Loop
│   │   ├── models/             # Pydantic schemas & AgentState
│   │   └── services/           # Quản lý phiên bản Undo/Redo
│   └── tests/                  # Bộ 22 test cases tự động
└── frontend/
    ├── index.html
    ├── package.json
    ├── tailwind.config.js
    └── src/
        ├── App.tsx             # Giao diện chính điều khiển Workspace
        ├── components/
        │   ├── Header.tsx      # Viewports, Undo/Redo, Export
        │   ├── PromptInput.tsx # Ô nhập prompt & Templates gợi ý
        │   ├── AgentTimeline.tsx # Hiển thị luồng 5 Agent thời gian thực
        │   ├── LivePreview.tsx # Iframe preview & DevTools Inspector
        │   ├── InspectModal.tsx # Popup sửa phần tử chọn trên giao diện
        │   └── CodeModal.tsx   # Xem & copy mã HTML
        └── services/
            └── api.ts          # Kết nối REST & SSE với Backend
```
