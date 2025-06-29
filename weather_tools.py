import requests
from langchain.tools import tool

@tool
def get_current_weather(location: str) -> str:
    """
    Get current weather information for a specific location.
    
    Args:
        location (str): The name of the city or location to get weather for
        
    Returns:
        str: Current weather information including temperature and description
    """
    try:
        # Using Open-Meteo API (free weather API)
        # First, get coordinates for the location using their geocoding API
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        geocoding_params = {
            "name": location,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        geocoding_response = requests.get(geocoding_url, params=geocoding_params)
        geocoding_data = geocoding_response.json()
        
        if not geocoding_data.get("results"):
            return f"Không thể tìm thấy thông tin về địa điểm: {location}"
        
        # Get latitude and longitude
        lat = geocoding_data["results"][0]["latitude"]
        lon = geocoding_data["results"][0]["longitude"]
        city_name = geocoding_data["results"][0]["name"]
        country = geocoding_data["results"][0].get("country", "")
        
        # Get weather data
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "auto"
        }
        
        weather_response = requests.get(weather_url, params=weather_params)
        weather_data = weather_response.json()
        
        current = weather_data["current"]
        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind_speed = current["wind_speed_10m"]
        weather_code = current["weather_code"]
        
        # Weather code to description mapping (simplified)
        weather_descriptions = {
            0: "Trời quang đãng",
            1: "Phần lớn quang đãng", 
            2: "Có mây một phần",
            3: "U ám",
            45: "Sương mù",
            48: "Sương mù đóng băng",
            51: "Mưa phùn nhẹ",
            53: "Mưa phùn vừa",
            55: "Mưa phùn nặng",
            61: "Mưa nhẹ",
            63: "Mưa vừa",
            65: "Mưa to",
            80: "Mưa rào nhẹ",
            81: "Mưa rào vừa",
            82: "Mưa rào to"
        }
        
        weather_desc = weather_descriptions.get(weather_code, "Không xác định")
        
        result = f"""
🌍 Thời tiết hiện tại tại {city_name}, {country}:
🌡️ Nhiệt độ: {temperature}°C
💧 Độ ẩm: {humidity}%
💨 Tốc độ gió: {wind_speed} km/h
☁️ Tình trạng: {weather_desc}
        """.strip()
        
        return result
        
    except Exception as e:
        return f"Lỗi khi lấy thông tin thời tiết: {str(e)}"
