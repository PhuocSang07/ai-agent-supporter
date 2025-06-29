# 🚀 Quick Start Guide

## Chạy nhanh chỉ với 3 bước:

### 1. Cài đặt
```bash
pip install -r requirements.txt
```

### 2. Cấu hình
```bash
cp example.env .env
# Chỉnh sửa .env với API key của bạn
```

### 3. Chạy
```bash
streamlit run app.py
```

## 🔧 Diagnostic Tool

Nếu gặp lỗi, chạy tool chẩn đoán để kiểm tra setup:
```bash
python diagnostic.py
```

## 🔑 API Keys cần thiết:

- **OPENAI_API_KEY** - Lấy từ [OpenAI Platform](https://platform.openai.com/api-keys)
- **GOOGLE_API_KEY** - Lấy từ [Google AI Studio](https://makersuite.google.com/app/apikey)

## 📅 Google Calendar (Tùy chọn):

Nếu muốn sử dụng tính năng Calendar:
1. **Xem hướng dẫn chi tiết:** [GOOGLE_SETUP.md](GOOGLE_SETUP.md)
2. Hoặc setup nhanh:
   - Truy cập [Google Cloud Console](https://console.cloud.google.com/)
   - Tạo project và bật Calendar API
   - Cấu hình OAuth consent screen
   - Tạo OAuth credentials (Desktop application)
   - Tải file `credentials.json` vào thư mục này

## 💡 Tip:
Bạn có thể chỉ sử dụng Weather Bot mà không cần Google Calendar!

## 🔧 Troubleshooting:

### ❌ "models/gemini-pro is not found" 
- **Giải pháp:** Restart app, model đã được cập nhật thành `gemini-2.0-flash`

### ❌ "Access blocked: This app's request is invalid"
- **Giải pháp:** Xem hướng dẫn chi tiết trong [GOOGLE_SETUP.md](GOOGLE_SETUP.md)
- Thường do OAuth consent screen chưa cấu hình đúng
- Cần thêm email vào "Test users" hoặc publish app

### ❌ Multiple OAuth requests
- **Giải pháp:** Chỉ click "Khởi tạo Agent" một lần, restart app nếu cần

### ❌ "API Key not found"
- **Giải pháp:** Kiểm tra file `.env` có đúng API key không

### ❌ "redirect_uri_mismatch"
- **Giải pháp:** Thêm redirect URIs vào Google Cloud Console credentials
- Cần thêm: http://localhost:8080/, http://localhost:8090/, etc.
