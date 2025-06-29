# AI Agent Supporter - Modern AI Assistant with Streamlit UI

Ứng dụng AI Assistant hiện đại tích hợp Weather Bot và Personal Calendar Assistant với giao diện Streamlit, hỗ trợ cả GPT-4o và Gemini 1.5 Flash.

## 🏗️ Cấu trúc Dự án

```
ai-agent-supporter/
├── app.py                    # 🎨 Main Streamlit application
├── agent_factory.py          # 🏭 Agent creation and configuration
├── weather_tools.py          # 🌤️ Weather API integration
├── calendar_tools.py         # 📅 Google Calendar tools
├── google_auth.py           # 🔐 OAuth 2.0 authentication
├── requirements.txt         # 📦 Python dependencies
├── example.env             # ⚙️ Environment variables template
├── .gitignore              # 🚫 Git ignore rules
├── LICENSE                 # 📄 MIT License
└── README.md              # 📖 This file
```

## ✨ Tính năng

### 🌤️ Weather Bot
- Kiểm tra thời tiết hiện tại của bất kỳ thành phố nào trên thế giới
- Hiển thị nhiệt độ, độ ẩm, tốc độ gió và mô tả thời tiết
- Sử dụng Open-Meteo API miễn phí

### 📅 DateTime Assistant (Luôn có sẵn)
- Xác định ngày giờ hiện tại chính xác theo múi giờ Việt Nam
- Tính toán ngày mai, hôm qua và các ngày tương đối
- Cung cấp thông tin chi tiết về thời gian để hỗ trợ các tác vụ khác
- Hỗ trợ LLM hiểu và xử lý câu hỏi về thời gian một cách chính xác

### 📅 Personal Calendar Assistant (Tùy chọn)
- Xem danh sách sự kiện sắp tới
- Tạo sự kiện mới với thông tin chi tiết
- Xóa sự kiện theo tiêu đề
- Tìm kiếm sự kiện trong lịch
- Hỗ trợ xác thực OAuth 2.0

### 🧠 AI Models
- **GPT-4o** (OpenAI) - Mặc định
- **Gemini 2.0 Flash** (Google) - Lựa chọn thay thế

### 🎨 Streamlit UI
- Giao diện web hiện đại và thân thiện
- Cấu hình real-time
- Chat interface trực quan

## 🚀 Cài đặt và Chạy

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Thiết lập environment variables
```bash
cp example.env .env
```

Chỉnh sửa file `.env`:
```env
# Bắt buộc: Ít nhất một trong hai
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Tùy chọn: Cho tính năng Calendar
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.pickle
```

### 3. (Tùy chọn) Thiết lập Google Calendar

**📋 Hướng dẫn chi tiết:** Xem [GOOGLE_SETUP.md](GOOGLE_SETUP.md)

**🚀 Setup nhanh:**
1. **Tạo Google Cloud Project:**
   - Truy cập [Google Cloud Console](https://console.cloud.google.com/)
   - Tạo project mới hoặc chọn project hiện có

2. **Bật Google Calendar API:**
   - Đi đến APIs & Services > Library
   - Tìm và bật "Google Calendar API"

3. **Cấu hình OAuth consent screen:**
   - Đi đến APIs & Services > OAuth consent screen
   - Chọn "External" và điền thông tin cơ bản
   - Thêm email của bạn vào "Test users"

4. **Tạo OAuth 2.0 Credentials:**
   - Đi đến APIs & Services > Credentials
   - Tạo OAuth client ID (Desktop application)
   - Thêm redirect URIs: `http://localhost:8080/`, `http://localhost:8090/`, etc.
   - Tải xuống file JSON và đổi tên thành `credentials.json`
   - Đặt file này vào thư mục dự án

### 4. Chạy ứng dụng
```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại `http://localhost:8501`

## 🎯 Cách sử dụng

### Bước 1: Cấu hình
1. Mở sidebar (nếu chưa mở)
2. Chọn AI model (GPT hoặc Gemini)
3. Bật/tắt tính năng Calendar nếu cần
4. Nhấn "🚀 Khởi tạo Agent"

### Bước 2: Chat
1. Nhập câu hỏi vào ô chat
2. Agent sẽ tự động chọn tool phù hợp
3. Xem kết quả và tiếp tục hội thoại

### 📝 Ví dụ câu hỏi

#### Weather Bot:
```
"Thời tiết ở Tokyo như thế nào?"
"Cho tôi biết thời tiết hiện tại ở Hà Nội"
"What's the weather in New York?"
```

#### DateTime Assistant:
```
"Hôm nay là thứ mấy?"
"Ngày hôm nay là ngày bao nhiêu?"
"Bây giờ là mấy giờ?"
"Ngày mai là ngày gì?"
"Cho tôi biết thông tin thời gian hiện tại"
```

#### Calendar Assistant:
```
"Liệt kê 5 sự kiện sắp tới"
"Lịch trình ngày mai"
"Tất cả sự kiện ngày 30/6/2025"
"Tạo cuộc họp 'Báo cáo dự án' vào 2025-07-01 từ 14:00 đến 15:30"
"Tìm kiếm sự kiện có từ 'họp'"
"Xóa sự kiện 'Cuộc họp team'"
```

## 🔧 Troubleshooting

### Lỗi "API Key not found"
- Kiểm tra file `.env` có đúng tên biến không
- Đảm bảo đã restart ứng dụng sau khi thay đổi `.env`

### Lỗi Google Calendar
- Đảm bảo đã đặt đúng file `credentials.json`
- Kiểm tra OAuth consent screen đã được cấu hình
- Xóa file `token.pickle` nếu gặp lỗi authentication

### Lỗi import
- Kiểm tra đã cài đặt đủ dependencies: `pip install -r requirements.txt`
- Đảm bảo đang sử dụng đúng Python environment

### Lỗi "models/gemini-pro is not found"
- Model `gemini-pro` đã bị deprecated
- Ứng dụng hiện sử dụng `gemini-2.0-flash` (đã được cập nhật)
- Restart ứng dụng nếu vẫn gặp lỗi này

### Lỗi Multiple OAuth requests
- Chỉ click "Khởi tạo Agent" một lần
- Nếu gặp nhiều yêu cầu OAuth, restart ứng dụng và thử lại

## 🔒 Bảo mật

- File `.env` chứa API keys, không commit vào Git
- File `credentials.json` chứa OAuth secrets, cần bảo mật
- File `token.pickle` chứa access token, không chia sẻ

## 🎨 Tùy chỉnh

### Thêm AI Model mới
Chỉnh sửa `agent_factory.py` để thêm model:
```python
elif model_choice.lower() == "claude":
    llm = ChatAnthropic(model="claude-3-sonnet-20240229")
```

### Thêm Tool mới
1. Tạo function với decorator `@tool`
2. Thêm vào list tools trong `agent_factory.py`
3. Cập nhật system prompt

### Thay đổi giao diện
Chỉnh sửa CSS trong `app.py` hoặc thêm file CSS riêng.

## 🎯 Mục tiêu học tập

Qua dự án này, bạn sẽ học được:

1. **Tool Calling** - Cách AI agent quyết định và sử dụng tools
2. **LangChain Framework** - Xây dựng agent với LangChain
3. **API Integration** - Tích hợp với API bên ngoài (Weather, Calendar)
4. **OAuth Authentication** - Xử lý xác thực người dùng
5. **Streamlit Development** - Xây dựng web app với Streamlit
6. **Multi-model Support** - Hỗ trợ nhiều AI model
7. **Error Handling** - Xử lý lỗi và exception
8. **Best Practices** - Thực hành tốt trong phát triển AI agent

## 🤝 Đóng góp

Nếu bạn có ý tưởng cải thiện hoặc muốn thêm tính năng mới, hãy tạo issue hoặc pull request!

## 📄 License

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết.
