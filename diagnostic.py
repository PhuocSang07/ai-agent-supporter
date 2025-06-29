#!/usr/bin/env python3
"""
🔧 AI Agent Supporter - Diagnostic Tool
Kiểm tra setup và cấu hình của dự án
"""

import os
import sys
from dotenv import load_dotenv

def check_python_version():
    """Kiểm tra phiên bản Python"""
    print("🐍 Python Version Check:")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Python version OK")
        return True
    else:
        print("   ❌ Python 3.8+ required")
        return False

def check_packages():
    """Kiểm tra các package cần thiết"""
    print("\n📦 Package Check:")
    required_packages = [
        'streamlit',
        'openai', 
        'google-generativeai',
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
        'requests',
        'python-dotenv'
    ]
    
    all_good = True
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NOT INSTALLED")
            all_good = False
    
    return all_good

def check_env_file():
    """Kiểm tra file .env"""
    print("\n🔐 Environment Variables Check:")
    
    if not os.path.exists('.env'):
        print("   ❌ .env file not found")
        print("   💡 Run: cp example.env .env")
        return False
    
    print("   ✅ .env file exists")
    
    # Load env vars
    load_dotenv()
    
    # Check API keys
    api_keys = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY')
    }
    
    has_api_key = False
    for key, value in api_keys.items():
        if value and value != 'your_api_key_here':
            print(f"   ✅ {key} is set")
            has_api_key = True
        else:
            print(f"   ⚠️ {key} not set or using placeholder")
    
    if not has_api_key:
        print("   ❌ No valid API keys found")
        return False
    
    return True

def check_google_credentials():
    """Kiểm tra Google credentials"""
    print("\n📅 Google Calendar Setup Check:")
    
    credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
    
    if not os.path.exists(credentials_file):
        print(f"   ⚠️ {credentials_file} not found (OK if not using Calendar)")
        return True
    
    print(f"   ✅ {credentials_file} exists")
    
    try:
        import json
        with open(credentials_file, 'r') as f:
            creds_data = json.load(f)
        
        if 'installed' in creds_data:
            print("   ✅ credentials.json format is valid")
            
            # Check redirect URIs
            redirect_uris = creds_data.get('installed', {}).get('redirect_uris', [])
            required_uris = ['http://localhost:8080/', 'http://127.0.0.1:8080/']
            
            has_localhost = any('localhost' in uri for uri in redirect_uris)
            if has_localhost:
                print("   ✅ Redirect URIs include localhost")
            else:
                print("   ⚠️ Redirect URIs might not include localhost:8080")
                
            return True
        else:
            print("   ❌ credentials.json invalid format")
            return False
            
    except Exception as e:
        print(f"   ❌ Error reading credentials.json: {e}")
        return False

def check_ports():
    """Kiểm tra ports có bị chiếm không"""
    print("\n🔌 Port Check:")
    
    import socket
    ports_to_check = [8501, 8080, 8090]
    
    for port in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print(f"   ⚠️ Port {port} is in use")
        else:
            print(f"   ✅ Port {port} is available")

def main():
    """Chạy tất cả diagnostic checks"""
    print("🔧 AI Agent Supporter - Diagnostic Tool")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_packages(),
        check_env_file(),
        check_google_credentials()
    ]
    
    check_ports()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY:")
    
    if all(checks):
        print("✅ All checks passed! Your setup looks good.")
        print("\n🚀 To start the app: streamlit run app.py")
    else:
        print("❌ Some issues found. Please fix them before running the app.")
        print("\n📚 For help:")
        print("   - QUICKSTART.md - Quick setup guide")
        print("   - GOOGLE_SETUP.md - Google OAuth setup")
        print("   - README.md - Full documentation")

if __name__ == "__main__":
    main()
