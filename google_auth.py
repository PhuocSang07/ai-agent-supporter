import os
import pickle
from datetime import datetime, timedelta
import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    """
    Xử lý xác thực Google OAuth 2.0 và trả về service object để tương tác với Google Calendar API.
    
    Returns:
        service: Google Calendar API service object
    """
    creds = None
    token_file = os.getenv('GOOGLE_TOKEN_FILE', 'token.pickle')
    credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
    
    # Kiểm tra xem có token đã lưu từ lần chạy trước không
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            try:
                creds = pickle.load(token)
            except Exception:
                # Nếu token bị lỗi, xóa nó và tạo mới
                os.remove(token_file)
                creds = None
    
    # Nếu không có credentials hợp lệ, yêu cầu người dùng đăng nhập
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                # Nếu refresh thất bại, xóa token và yêu cầu đăng nhập lại
                if os.path.exists(token_file):
                    os.remove(token_file)
                creds = None
        
        if not creds:
            if not os.path.exists(credentials_file):
                raise FileNotFoundError(
                    f"Không tìm thấy file {credentials_file}. "
                    "Vui lòng tải xuống credentials.json từ Google Cloud Console "
                    "và đặt nó trong thư mục dự án."
                )
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, SCOPES)
                
                # Thử nhiều port khác nhau để tránh xung đột
                for port in [8080, 8090, 8888, 9090]:
                    try:
                        creds = flow.run_local_server(port=port, open_browser=True)
                        break
                    except OSError:
                        continue
                else:
                    # Nếu tất cả port đều bị chiếm, sử dụng port ngẫu nhiên
                    creds = flow.run_local_server(port=0, open_browser=True)
                    
            except Exception as e:
                error_msg = str(e).lower()
                
                if any(keyword in error_msg for keyword in ["invalid_request", "access blocked", "access_denied"]):
                    raise Exception(
                        "❌ Google OAuth Error: Truy cập bị chặn\n\n"
                        "🔧 CÁCH KHẮC PHỤC CHI TIẾT:\n\n"
                        "1️⃣ KIỂM TRA OAUTH CONSENT SCREEN:\n"
                        "   • Truy cập: https://console.cloud.google.com/apis/credentials/consent\n"
                        "   • Đảm bảo User Type = 'External'\n"
                        "   • Publishing status = 'In production' HOẶC thêm email của bạn vào 'Test users'\n\n"
                        
                        "2️⃣ KIỂM TRA CREDENTIALS:\n"
                        "   • Truy cập: https://console.cloud.google.com/apis/credentials\n"
                        "   • Chọn OAuth 2.0 Client ID của bạn\n"
                        "   • Trong 'Authorized redirect URIs', thêm:\n"
                        "     - http://localhost:8080/\n"
                        "     - http://localhost:8090/\n"
                        "     - http://localhost:8888/\n"
                        "     - http://127.0.0.1:8080/\n\n"
                        
                        "3️⃣ LÀM MỚI SETUP:\n"
                        "   • Xóa file token.pickle (nếu có)\n"
                        "   • Tải lại credentials.json mới từ Google Cloud Console\n"
                        "   • Restart Streamlit app\n\n"
                        
                        "4️⃣ NẾU VẪN LỖI:\n"
                        "   • Tạo project mới trong Google Cloud Console\n"
                        "   • Bật Calendar API\n"
                        "   • Tạo OAuth credentials mới\n\n"
                        
                        f"📝 Chi tiết lỗi: {str(e)}"
                    )
                    
                elif "port" in error_msg or "address already in use" in error_msg:
                    raise Exception(
                        "❌ Port Error: Không thể khởi động server OAuth\n\n"
                        "🔧 Giải pháp:\n"
                        "1. Đóng tất cả browser tabs có localhost:8080\n"
                        "2. Restart Streamlit app\n"
                        "3. Hoặc chạy lệnh: netstat -ano | findstr :8080 để kiểm tra port\n\n"
                        f"Chi tiết: {str(e)}"
                    )
                    
                else:
                    raise Exception(f"❌ Google Auth Error: {str(e)}")
        
        # Lưu credentials cho lần chạy tiếp theo
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    # Tạo service object
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_calendar_service():
    """
    Helper function để lấy calendar service.
    Sử dụng global variable để tránh phải xác thực lại nhiều lần.
    """
    global _calendar_service
    if '_calendar_service' not in globals() or _calendar_service is None:
        try:
            _calendar_service = authenticate_google()
        except Exception as e:
            # Reset global variable if authentication fails
            _calendar_service = None
            raise e
    return _calendar_service

def reset_google_auth():
    """
    Reset Google authentication by removing stored tokens.
    Useful when OAuth flow encounters errors.
    """
    token_file = os.getenv('GOOGLE_TOKEN_FILE', 'token.pickle')
    if os.path.exists(token_file):
        try:
            os.remove(token_file)
            return f"✅ Đã xóa {token_file}. Vui lòng thử đăng nhập lại."
        except Exception as e:
            return f"❌ Không thể xóa {token_file}: {str(e)}"
    else:
        return f"ℹ️ File {token_file} không tồn tại."

def validate_credentials_file():
    """
    Validate that the credentials.json file exists and is properly formatted.
    """
    credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
    
    if not os.path.exists(credentials_file):
        return False, f"❌ Không tìm thấy file {credentials_file}"
    
    try:
        import json
        with open(credentials_file, 'r') as f:
            creds_data = json.load(f)
            
        # Check if it has the required structure
        if 'installed' not in creds_data:
            return False, "❌ File credentials.json không đúng định dạng (thiếu 'installed' key)"
            
        required_fields = ['client_id', 'client_secret', 'redirect_uris']
        for field in required_fields:
            if field not in creds_data['installed']:
                return False, f"❌ File credentials.json thiếu field '{field}'"
        
        return True, "✅ File credentials.json hợp lệ"
        
    except json.JSONDecodeError:
        return False, "❌ File credentials.json không phải JSON hợp lệ"
    except Exception as e:
        return False, f"❌ Lỗi đọc credentials.json: {str(e)}"
