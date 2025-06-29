# 🤖 AI Assistant Project

This is a versatile AI assistant built with Streamlit, designed to be an interactive and intelligent tool for everyday tasks. It leverages powerful AI models like GPT-4 and Gemini to provide a wide range of functionalities, from answering questions to managing your schedule.

## ✨ Features

- **Interactive Chat Interface**: A clean and user-friendly web interface for seamless interaction.
- **Multi-Model Support**: Easily switch between different large language models:
  - **GPT-4**: For advanced reasoning and text generation.
  - **Gemini 2.0 Flash**: For fast and efficient responses.
- **Real-time Weather Information**: Get current weather updates for any location worldwide.
- **Google Calendar Integration**: 
  - View your upcoming events.
  - Create new events and schedule meetings.
- **Configurable Agent**: Use the sidebar to initialize the agent with your desired model and features.
- **Asynchronous Processing**: Ensures a smooth user experience without blocking.

## 📁 Project Structure

Here is an overview of the key files in this project:

```
/
├── app.py                  # Main Streamlit application file
├── agent_factory.py        # Creates the AI agent with selected tools
├── weather_tools.py        # Provides weather checking functionality
├── calendar_tools.py       # Tools for Google Calendar integration
├── google_auth.py          # Handles Google OAuth2 authentication
├── requirements.txt        # Python dependencies
├── example.env             # Template for environment variables
└── GOOGLE_SETUP.md         # Guide for setting up Google Calendar API
```

## 🛠️ Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Prerequisites

- Python 3.8 or higher
- `pip` for package management

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-directory>
```

### 3. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables

Create a `.env` file in the root directory by copying the `example.env` file.

```bash
cp example.env .env
```

Now, open the `.env` file and add your API keys:

```
# .env
OPENAI_API_KEY="your_openai_api_key"
GOOGLE_API_KEY="your_google_api_key"
```

- `OPENAI_API_KEY`: Required if you want to use the GPT-4 model.
- `GOOGLE_API_KEY`: Required for the Gemini model and Google services.

### 6. Set Up Google Calendar API

To enable the Google Calendar feature, you need to set up OAuth 2.0 credentials.

1.  Follow the instructions in the `GOOGLE_SETUP.md` file to enable the Google Calendar API and get your `credentials.json` file.
2.  Place the downloaded `credentials.json` file in the root directory of the project.

## 🚀 How to Run

Once you have completed the setup, you can run the application using Streamlit.

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501` in your web browser.

### Usage Guide

1.  **Open the application** in your browser.
2.  Use the **sidebar** on the left to configure the agent.
3.  **Select an AI model** (GPT-4 or Gemini 2.0 Flash).
4.  **Enable Google Calendar** if you have set up the credentials.
5.  Click the **"Initialize"** button to start the agent.
6.  Once the agent is ready, you can start **chatting** in the main window!

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
