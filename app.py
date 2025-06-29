import streamlit as st
import os
from dotenv import load_dotenv
from agent_factory import create_agent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🤖 AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal custom CSS for essential styling only
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Clean background */
    .stApp {
        background: #f8fafc;
    }
    
    /* Better chat messages */
    .stChatMessage {
        background: white;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent_ready" not in st.session_state:
        st.session_state.agent_ready = False
    if "calendar_enabled" not in st.session_state:
        st.session_state.calendar_enabled = False
    if "current_model" not in st.session_state:
        st.session_state.current_model = None

def check_environment():
    """Check if required environment variables are set"""
    missing_vars = []
    
    if not os.getenv('OPENAI_API_KEY'):
        missing_vars.append('OPENAI_API_KEY')
    if not os.getenv('GOOGLE_API_KEY'):
        missing_vars.append('GOOGLE_API_KEY')
    
    return missing_vars

def create_sidebar():
    """Create the sidebar with configuration options"""
    with st.sidebar:
        st.title("⚙️ Cấu hình")
        
        # Model selection
        st.subheader("🤖 Model AI")
        model_choice = st.selectbox(
            "Chọn model:",
            ["gpt", "gemini"],
            format_func=lambda x: "GPT-4" if x == "gpt" else "Gemini 2.0 Flash",
            index=1
        )
        
        # Features
        st.subheader("🔧 Tính năng")
        calendar_enabled = st.checkbox("Google Calendar", value=st.session_state.get('calendar_enabled', False))
        
        # API status
        st.subheader("🔑 API Keys")
        missing_vars = check_environment()
        
        if model_choice == "gpt":
            if 'OPENAI_API_KEY' not in missing_vars:
                st.success("✅ OpenAI API OK")
            else:
                st.error("❌ Thiếu OpenAI API Key")
        
        if os.path.exists('credentials.json'):
            st.success("✅ credentials.json OK")
        if os.environ.get('GOOGLE_API_KEY'):
            st.success("✅ Google API OK")
        else:
            st.error("❌ Thiếu Google API Key")
        
        # Control buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Khởi tạo", use_container_width=True):
                with st.spinner("Đang khởi tạo..."):
                    try:
                        st.session_state.agent = create_agent(model_choice, calendar_enabled)
                        st.session_state.agent_ready = True
                        st.session_state.calendar_enabled = calendar_enabled
                        st.session_state.current_model = model_choice
                        st.success("✅ Đã khởi tạo thành công!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Lỗi: {str(e)}")
        
        with col2:
            if st.button("🗑️ Xóa Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

def render_welcome_message():
    """Render welcome message when no messages exist"""
    st.markdown("### 👋 Chào mừng bạn!")
    
    # Feature cards using columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🌤️ **Thời tiết**\n\nXem thông tin thời tiết theo thời gian thực")
        st.info("⚡ **Phản hồi nhanh**\n\nTrả lời nhanh chóng và chính xác")
    
    with col2:
        st.info("📅 **Quản lý lịch**\n\nXem và quản lý Google Calendar")
        st.info("🎯 **Hỗ trợ công việc**\n\nGiúp lập kế hoạch và tổ chức")

def render_chat_interface():
    """Render the chat interface using Streamlit components"""
    
    # Show welcome message if no messages exist
    if not st.session_state.messages:
        render_welcome_message()
    
    # Chat messages using Streamlit's chat_message
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if "agent" in st.session_state and st.session_state.agent:
        prompt = st.chat_input("Hỏi gì đó...")
        
        if prompt:
            # Add user message
            st.chat_message("user").write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            try:
                # Get AI response
                with st.chat_message("assistant"):
                    with st.spinner("Đang xử lý..."):
                        response = st.session_state.agent.invoke({"input": prompt})
                        response_text = response.get('output', 'Không có phản hồi')
                        st.write(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"Lỗi: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": f"Xin lỗi, tôi gặp lỗi: {str(e)}"})
    else:
        st.warning("⚠️ Vui lòng khởi tạo agent trước khi chat")

def render_status_panel():
    """Render the status panel"""
    with st.sidebar:
        st.subheader("📊 Trạng thái")
        
        # Agent status
        if "agent" in st.session_state and st.session_state.agent:
            model_name = "GPT-4" if st.session_state.current_model == "gpt" else "Gemini 2.0 Flash"
            st.success(f"🟢 Agent đang hoạt động ({model_name})")
        else:
            st.warning("🟡 Agent chưa khởi tạo")
        
        # Calendar status
        if st.session_state.calendar_enabled:
            st.info("📅 Calendar: Đã kích hoạt")
        else:
            st.info("📅 Calendar: Chưa kích hoạt")
        
        # Message count
        if st.session_state.messages:
            st.text(f"💬 Tin nhắn: {len(st.session_state.messages)}")
        
        # Quick examples
        if "agent" in st.session_state and st.session_state.agent:
            st.subheader("💡 Thử ngay:")
            examples = [
                "🌤️ Thời tiết Tokyo",
                "📅 Hôm nay thứ mấy?",
                "⏰ Bây giờ mấy giờ?",
                "📆 Lịch tuần này"
            ]
            for example in examples:
                if st.button(example, use_container_width=True):
                    # Remove emoji and add to chat
                    clean_text = example.split(" ", 1)[1]
                    st.session_state.messages.append({"role": "user", "content": clean_text})
                    st.rerun()

def main():
    """Main application"""
    initialize_session_state()
    create_sidebar()
    
    # Main content area
    st.title("🤖 AI Assistant")
    render_chat_interface()
    render_status_panel()

if __name__ == "__main__":
    main()