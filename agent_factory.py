from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from weather_tools import get_current_weather
from calendar_tools import (
    list_upcoming_events,
    create_calendar_event,
    delete_calendar_event,
    search_calendar_events,
    get_events_by_date,
    get_tomorrow_events,
    get_today_events,
    get_current_datetime,
    get_today_info
)
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_agent(model_choice: str = "gpt", enable_calendar: bool = False):
    """
    Tạo và trả về AI agent với model và tools được chọn
    
    Args:
        model_choice (str): "gpt" hoặc "gemini"
        enable_calendar (bool): Có bật tính năng calendar không
        
    Returns:
        AgentExecutor: Agent executor object
    """
    
    # Initialize the LLM based on choice
    if model_choice.lower() == "gemini":
        if not os.getenv('GOOGLE_API_KEY'):
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
    else:  # Default to GPT
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0
        )
    
    # Define tools based on enabled features
    tools = [get_current_weather, get_current_datetime, get_today_info]
    
    if enable_calendar:
        try:
            # Test calendar connection
            from google_auth import get_calendar_service
            get_calendar_service()
            tools.extend([
                list_upcoming_events,
                create_calendar_event,
                delete_calendar_event,
                search_calendar_events,
                get_events_by_date,
                get_tomorrow_events,
                get_today_events
            ])
        except Exception as e:
            raise Exception(f"Lỗi kết nối Google Calendar: {str(e)}")
    
    # Create system prompt
    calendar_features = """
    
    📅 **Tính năng Calendar (đã kích hoạt):**
    - Xem danh sách sự kiện sắp tới: `list_upcoming_events()`
    - Xem sự kiện theo ngày cụ thể: `get_events_by_date(date)` 
    - Tạo sự kiện mới: `create_calendar_event()`
    - Xóa sự kiện: `delete_calendar_event()`
    - Tìm kiếm sự kiện: `search_calendar_events()`
    
    **Xử lý yêu cầu theo ngày:**
    - "ngày mai", "tomorrow" → tính toán ngày tiếp theo và dùng get_events_by_date()
    - "ngày 30/6/2025", "2025-06-30" → dùng get_events_by_date() với ngày cụ thể
    - "tuần này", "tháng này" → dùng list_upcoming_events() với số lượng phù hợp
    
    **Định dạng ngày hỗ trợ:**
    - 'YYYY-MM-DD' (ví dụ: '2025-06-30')  
    - 'DD/MM/YYYY' (ví dụ: '30/06/2025')
    - Múi giờ mặc định: Asia/Ho_Chi_Minh (UTC+7)
    """ if enable_calendar else ""
    
    system_prompt = f"""
    Bạn là một trợ lý AI thông minh và hiệu quả với các tính năng sau:
    
    🌤️ **Tính năng Weather (luôn có sẵn):**
    - Kiểm tra thời tiết hiện tại của bất kỳ thành phố nào trên thế giới
    - Hiển thị nhiệt độ, độ ẩm, tốc độ gió và mô tả thời tiết
    
    📅 **Tính năng DateTime (luôn có sẵn):**
    - Xác định ngày giờ hiện tại: `get_current_datetime()` và `get_today_info()`
    - Biết chính xác ngày hôm nay để xử lý các câu hỏi về thời gian
    - Tính toán ngày mai, hôm qua, và các ngày tương đối khác
    {calendar_features}
    
    **Model đang sử dụng:** {model_choice.upper()}
    
    **QUAN TRỌNG - Xử lý thời gian:**
    1. LUÔN sử dụng `get_today_info()` đầu tiên khi cần biết ngày hiện tại
    2. Khi user hỏi về "ngày mai", "hôm nay", "hôm qua" → dùng thông tin từ get_today_info()
    3. Khi user hỏi về ngày cụ thể (ví dụ: "30/6/2025"), dùng get_events_by_date() với ngày đó
    4. Múi giờ mặc định: Asia/Ho_Chi_Minh (UTC+7)
    5. Hiểu các format ngày: DD/MM/YYYY, YYYY-MM-DD, "ngày mai", v.v.
    
    **Nguyên tắc trả lời:**
    - Trả lời trực tiếp, không hỏi quá nhiều
    - Sử dụng tools ngay khi có đủ thông tin  
    - Nếu thiếu thông tin quan trọng, hỏi cụ thể và ngắn gọn
    - Luôn cung cấp kết quả hữu ích cho user
    
    Hãy trả lời một cách thân thiện, chi tiết và hữu ích!
    """
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    # Create agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=False,  # Set to False for cleaner Streamlit output
        handle_parsing_errors=True
    )
    
    return agent_executor
