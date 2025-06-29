from datetime import datetime, timedelta
import pytz
from langchain.tools import tool
from googleapiclient.errors import HttpError
from google_auth import get_calendar_service

@tool
def list_upcoming_events(n: int = 10) -> str:
    """
    Liệt kê n sự kiện sắp tới từ Google Calendar.
    
    Args:
        n (int): Số lượng sự kiện muốn lấy (mặc định 10, tối đa 50)
        
    Returns:
        str: Danh sách các sự kiện sắp tới
    """
    try:
        service = get_calendar_service()
        
        # Giới hạn số lượng sự kiện
        n = min(max(n, 1), 50)
        
        # Lấy thời gian hiện tại
        now = datetime.utcnow().isoformat() + 'Z'
        
        # Gọi Calendar API
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=n,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return f"Không có sự kiện nào sắp tới trong lịch của bạn."
        
        result = f"📅 {len(events)} sự kiện sắp tới:\n\n"
        
        for i, event in enumerate(events, 1):
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'Không có tiêu đề')
            
            # Xử lý thời gian
            if 'T' in start:  # Event có thời gian cụ thể
                dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                # Chuyển đổi sang múi giờ địa phương
                local_tz = pytz.timezone('Asia/Ho_Chi_Minh')
                dt_local = dt.astimezone(local_tz)
                time_str = dt_local.strftime('%d/%m/%Y %H:%M')
            else:  # Event cả ngày
                dt = datetime.fromisoformat(start)
                time_str = dt.strftime('%d/%m/%Y (Cả ngày)')
            
            # Thêm mô tả nếu có
            description = event.get('description', '')
            location = event.get('location', '')
            
            result += f"{i}. 📝 {summary}\n"
            result += f"   ⏰ {time_str}\n"
            if location:
                result += f"   📍 {location}\n"
            if description:
                result += f"   📄 {description[:100]}{'...' if len(description) > 100 else ''}\n"
            result += "\n"
        
        return result.strip()
        
    except HttpError as error:
        return f"Lỗi khi truy cập Google Calendar: {error}"
    except Exception as error:
        return f"Đã xảy ra lỗi: {error}"

@tool
def create_calendar_event(summary: str, start_time: str, end_time: str, description: str = "", location: str = "") -> str:
    """
    Tạo một sự kiện mới trong Google Calendar.
    
    Args:
        summary (str): Tiêu đề của sự kiện
        start_time (str): Thời gian bắt đầu (định dạng: 'YYYY-MM-DD HH:MM' hoặc 'YYYY-MM-DD')
        end_time (str): Thời gian kết thúc (định dạng: 'YYYY-MM-DD HH:MM' hoặc 'YYYY-MM-DD')
        description (str, optional): Mô tả chi tiết của sự kiện
        location (str, optional): Địa điểm tổ chức sự kiện
        
    Returns:
        str: Kết quả tạo sự kiện
    """
    try:
        service = get_calendar_service()
        
        # Xử lý thời gian
        def parse_datetime(time_str):
            """Parse datetime string and return appropriate format for Google Calendar"""
            try:
                # Thử parse với giờ:phút
                if len(time_str.split()) == 2:
                    dt = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
                    # Chuyển sang UTC
                    local_tz = pytz.timezone('Asia/Ho_Chi_Minh')
                    dt_local = local_tz.localize(dt)
                    dt_utc = dt_local.astimezone(pytz.UTC)
                    return {
                        'dateTime': dt_utc.isoformat(),
                        'timeZone': 'UTC'
                    }
                else:
                    # Event cả ngày
                    dt = datetime.strptime(time_str, '%Y-%m-%d')
                    return {
                        'date': dt.strftime('%Y-%m-%d')
                    }
            except ValueError:
                raise ValueError(f"Định dạng thời gian không hợp lệ: {time_str}. Sử dụng 'YYYY-MM-DD HH:MM' hoặc 'YYYY-MM-DD'")
        
        start_parsed = parse_datetime(start_time)
        end_parsed = parse_datetime(end_time)
        
        # Tạo event object
        event = {
            'summary': summary,
            'start': start_parsed,
            'end': end_parsed,
        }
        
        if description:
            event['description'] = description
        if location:
            event['location'] = location
        
        # Tạo sự kiện
        created_event = service.events().insert(
            calendarId='primary',
            body=event
        ).execute()
        
        # Format response
        result = f"✅ Đã tạo sự kiện thành công!\n\n"
        result += f"📝 Tiêu đề: {summary}\n"
        result += f"⏰ Bắt đầu: {start_time}\n"
        result += f"⏰ Kết thúc: {end_time}\n"
        
        if location:
            result += f"📍 Địa điểm: {location}\n"
        if description:
            result += f"📄 Mô tả: {description}\n"
        
        result += f"\n🔗 Link: {created_event.get('htmlLink', 'Không có')}"
        
        return result
        
    except HttpError as error:
        return f"Lỗi khi tạo sự kiện: {error}"
    except ValueError as error:
        return f"Lỗi dữ liệu đầu vào: {error}"
    except Exception as error:
        return f"Đã xảy ra lỗi: {error}"

@tool
def delete_calendar_event(event_summary: str) -> str:
    """
    Xóa sự kiện khỏi Google Calendar dựa trên tiêu đề.
    
    Args:
        event_summary (str): Tiêu đề của sự kiện cần xóa
        
    Returns:
        str: Kết quả xóa sự kiện
    """
    try:
        service = get_calendar_service()
        
        # Tìm sự kiện
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=50,
            singleEvents=True,
            orderBy='startTime',
            q=event_summary
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return f"❌ Không tìm thấy sự kiện nào với tiêu đề '{event_summary}'"
        
        # Nếu có nhiều sự kiện, xóa sự kiện đầu tiên tìm thấy
        event_to_delete = events[0]
        
        # Xóa sự kiện
        service.events().delete(
            calendarId='primary',
            eventId=event_to_delete['id']
        ).execute()
        
        start = event_to_delete['start'].get('dateTime', event_to_delete['start'].get('date'))
        
        result = f"✅ Đã xóa sự kiện thành công!\n\n"
        result += f"📝 Tiêu đề: {event_to_delete.get('summary', 'Không có tiêu đề')}\n"
        result += f"⏰ Thời gian: {start}\n"
        
        if len(events) > 1:
            result += f"\n⚠️ Lưu ý: Tìm thấy {len(events)} sự kiện tương tự, đã xóa sự kiện đầu tiên."
        
        return result
        
    except HttpError as error:
        return f"Lỗi khi xóa sự kiện: {error}"
    except Exception as error:
        return f"Đã xảy ra lỗi: {error}"

@tool  
def search_calendar_events(query: str, max_results: int = 10) -> str:
    """
    Tìm kiếm sự kiện trong Google Calendar.
    
    Args:
        query (str): Từ khóa tìm kiếm
        max_results (int): Số lượng kết quả tối đa (mặc định 10)
        
    Returns:
        str: Danh sách sự kiện tìm thấy
    """
    try:
        service = get_calendar_service()
        
        # Giới hạn số lượng kết quả
        max_results = min(max(max_results, 1), 50)
        
        # Tìm kiếm sự kiện
        events_result = service.events().list(
            calendarId='primary',
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime',
            q=query
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return f"🔍 Không tìm thấy sự kiện nào với từ khóa '{query}'"
        
        result = f"🔍 Tìm thấy {len(events)} sự kiện với từ khóa '{query}':\n\n"
        
        for i, event in enumerate(events, 1):
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'Không có tiêu đề')
            
            # Xử lý thời gian
            if 'T' in start:  # Event có thời gian cụ thể
                dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                local_tz = pytz.timezone('Asia/Ho_Chi_Minh')
                dt_local = dt.astimezone(local_tz)
                time_str = dt_local.strftime('%d/%m/%Y %H:%M')
            else:  # Event cả ngày
                dt = datetime.fromisoformat(start)
                time_str = dt.strftime('%d/%m/%Y (Cả ngày)')
            
            result += f"{i}. 📝 {summary}\n"
            result += f"   ⏰ {time_str}\n"
            
            location = event.get('location', '')
            if location:
                result += f"   📍 {location}\n"
            
            result += "\n"
        
        return result.strip()
        
    except HttpError as error:
        return f"Lỗi khi tìm kiếm: {error}"
    except Exception as error:
        return f"Đã xảy ra lỗi: {error}"

@tool
def get_events_by_date(date: str) -> str:
    """
    Lấy tất cả sự kiện trong một ngày cụ thể.
    
    Args:
        date (str): Ngày cần tìm kiếm (định dạng: 'YYYY-MM-DD' hoặc 'DD/MM/YYYY')
        
    Returns:
        str: Danh sách các sự kiện trong ngày đó
    """
    try:
        service = get_calendar_service()
        
        # Parse và chuẩn hóa ngày
        def parse_date(date_str):
            """Parse various date formats"""
            try:
                # Thử format DD/MM/YYYY
                if '/' in date_str:
                    day, month, year = date_str.split('/')
                    return datetime(int(year), int(month), int(day))
                # Thử format YYYY-MM-DD
                elif '-' in date_str:
                    year, month, day = date_str.split('-')
                    return datetime(int(year), int(month), int(day))
                else:
                    raise ValueError("Invalid date format")
            except:
                raise ValueError(f"Không thể parse ngày '{date_str}'. Vui lòng sử dụng format 'YYYY-MM-DD' hoặc 'DD/MM/YYYY'")
        
        target_date = parse_date(date)
        
        # Tạo thời gian bắt đầu và kết thúc cho ngày đó
        start_of_day = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = target_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Chuyển đổi sang UTC để gọi API
        local_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        
        # Nếu ngày không có timezone info, coi như múi giờ địa phương
        if start_of_day.tzinfo is None:
            start_of_day = local_tz.localize(start_of_day)
            end_of_day = local_tz.localize(end_of_day)
        
        start_utc = start_of_day.astimezone(pytz.UTC)
        end_utc = end_of_day.astimezone(pytz.UTC)
        
        # Gọi Calendar API
        events_result = service.events().list(
            calendarId='primary',
            timeMin=start_utc.isoformat(),
            timeMax=end_utc.isoformat(),
            maxResults=50,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return f"📅 Không có sự kiện nào vào ngày {target_date.strftime('%d/%m/%Y')}"
        
        result = f"📅 **Lịch trình ngày {target_date.strftime('%d/%m/%Y')}** ({len(events)} sự kiện):\n\n"
        
        for i, event in enumerate(events, 1):
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'Không có tiêu đề')
            
            # Xử lý thời gian
            if 'T' in start:  # Event có thời gian cụ thể
                dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                dt_local = dt.astimezone(local_tz)
                time_str = dt_local.strftime('%H:%M')
            else:  # Event cả ngày
                time_str = "Cả ngày"
            
            # Thêm thông tin chi tiết
            description = event.get('description', '')
            location = event.get('location', '')
            
            result += f"{i}. 📝 **{summary}**\n"
            result += f"   ⏰ {time_str}\n"
            if location:
                result += f"   📍 {location}\n"
            if description:
                # Hiển thị mô tả ngắn gọn
                desc_short = description.replace('\n', ' ').strip()
                if len(desc_short) > 150:
                    desc_short = desc_short[:150] + "..."
                result += f"   📄 {desc_short}\n"
            result += "\n"
        
        return result.strip()
        
    except ValueError as ve:
        return f"❌ Lỗi định dạng ngày: {str(ve)}"
    except HttpError as error:
        return f"❌ Lỗi khi truy cập Google Calendar: {error}"
    except Exception as error:
        return f"❌ Đã xảy ra lỗi: {error}"

@tool
def get_tomorrow_events() -> str:
    """
    Lấy tất cả sự kiện của ngày mai.
    Tool này tự động tính toán ngày mai dựa trên múi giờ Việt Nam.
    
    Returns:
        str: Danh sách các sự kiện ngày mai
    """
    try:
        # Tính toán ngày mai
        local_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(local_tz)
        tomorrow = now + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')
        
        # Gọi tool get_events_by_date với ngày mai
        return get_events_by_date(tomorrow_str)
        
    except Exception as error:
        return f"❌ Lỗi khi lấy lịch ngày mai: {error}"

@tool  
def get_today_events() -> str:
    """
    Lấy tất cả sự kiện của hôm nay.
    Tool này tự động lấy ngày hiện tại dựa trên múi giờ Việt Nam.
    
    Returns:
        str: Danh sách các sự kiện hôm nay
    """
    try:
        # Tính toán ngày hôm nay
        local_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        today = datetime.now(local_tz)
        today_str = today.strftime('%Y-%m-%d')
        
        # Gọi tool get_events_by_date với ngày hôm nay
        return get_events_by_date(today_str)
        
    except Exception as error:
        return f"❌ Lỗi khi lấy lịch hôm nay: {error}"

@tool
def get_current_datetime() -> str:
    """
    Lấy thông tin ngày giờ hiện tại theo múi giờ Việt Nam.
    Tool này giúp AI agent biết được thời gian cụ thể để xử lý các câu hỏi về thời gian.
    
    Returns:
        str: Thông tin chi tiết về ngày giờ hiện tại
    """
    try:
        # Lấy thời gian theo múi giờ Việt Nam
        local_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(local_tz)
        
        # Lấy thời gian UTC
        utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
        
        # Format thông tin chi tiết
        result = f"""📅 **Thông tin thời gian hiện tại:**

🇻🇳 **Múi giờ Việt Nam (UTC+7):**
- Ngày: {now.strftime('%A, %d/%m/%Y')}
- Thời gian: {now.strftime('%H:%M:%S')}
- Tuần: Tuần {now.isocalendar()[1]} của năm {now.year}
- Tháng: Tháng {now.month}/2025

🌍 **Thời gian UTC:**
- Ngày: {utc_now.strftime('%A, %d/%m/%Y')}
- Thời gian: {utc_now.strftime('%H:%M:%S')} UTC

📊 **Thông tin bổ sung:**
- Múi giờ: {now.tzname()} ({now.strftime('%z')})
- Năm nhuận: {'Có' if now.year % 4 == 0 and (now.year % 100 != 0 or now.year % 400 == 0) else 'Không'}
- Ngày trong năm: {now.timetuple().tm_yday}/365

💡 **Ghi chú:** Thông tin này giúp bạn biết chính xác thời gian để:
- Tính toán "ngày mai" = {(now + timedelta(days=1)).strftime('%d/%m/%Y')}
- Tính toán "hôm qua" = {(now - timedelta(days=1)).strftime('%d/%m/%Y')}
- Xác định thời gian cho việc tạo sự kiện calendar
"""
        
        return result.strip()
        
    except Exception as error:
        return f"❌ Lỗi khi lấy thông tin thời gian: {error}"

@tool
def get_today_info() -> str:
    """
    Lấy thông tin cơ bản về ngày hôm nay dưới dạng structured data.
    Tool này cung cấp thông tin ngắn gọn về ngày hiện tại cho AI agent.
    
    Returns:
        str: Thông tin ngày hôm nay dưới dạng JSON-like
    """
    try:
        local_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        today = datetime.now(local_tz)
        
        # Tên các ngày trong tuần bằng tiếng Việt
        weekdays_vn = {
            'Monday': 'Thứ Hai',
            'Tuesday': 'Thứ Ba', 
            'Wednesday': 'Thứ Tư',
            'Thursday': 'Thứ Năm',
            'Friday': 'Thứ Sáu',
            'Saturday': 'Thứ Bảy',
            'Sunday': 'Chủ Nhật'
        }
        
        weekday_en = today.strftime('%A')
        weekday_vn = weekdays_vn.get(weekday_en, weekday_en)
        
        result = f"""Today's Information:
- Date: {today.strftime('%Y-%m-%d')} ({today.strftime('%d/%m/%Y')})
- Day: {weekday_vn} ({weekday_en})
- Time: {today.strftime('%H:%M:%S')}
- Timezone: Asia/Ho_Chi_Minh (UTC+7)
- Tomorrow: {(today + timedelta(days=1)).strftime('%Y-%m-%d')} ({(today + timedelta(days=1)).strftime('%d/%m/%Y')})
- Yesterday: {(today - timedelta(days=1)).strftime('%Y-%m-%d')} ({(today - timedelta(days=1)).strftime('%d/%m/%Y')})

Note: Use this information to understand relative dates like "today", "tomorrow", "yesterday" in user requests."""
        
        return result.strip()
        
    except Exception as error:
        return f"Error getting today's info: {error}"
