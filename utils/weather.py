"""获取多城市实时天气（Open-Meteo 免费接口，无需 API Key）

新增城市只需在 CITIES 里加一行 "城市名": (纬度, 经度)。
"""
import requests

CITIES = {
    "北京": (39.9042, 116.4074),
    "滑县": (35.57, 114.52),
}

# WMO 天气代码 -> 中文描述
WEATHER_TEXT = {
    0: "晴", 1: "基本晴", 2: "多云", 3: "阴",
    45: "雾", 48: "雾凇",
    51: "毛毛雨", 53: "毛毛雨", 55: "毛毛雨",
    61: "小雨", 63: "中雨", 65: "大雨", 66: "冻雨", 67: "冻雨",
    71: "小雪", 73: "中雪", 75: "大雪",
    80: "阵雨", 81: "阵雨", 82: "强阵雨", 85: "阵雪", 86: "阵雪",
    95: "雷阵雨", 96: "雷阵雨伴冰雹", 99: "雷阵雨伴冰雹",
}


def _fetch_one(name: str, lat: float, lon: float) -> str:
    """返回单个城市的"城市名：XX XX°C"，失败时给占位文案"""
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,weather_code&timezone=Asia%2FShanghai"
        )
        current = requests.get(url, timeout=10).json().get("current", {})
        temp = round(current.get("temperature_2m"))
        desc = WEATHER_TEXT.get(current.get("weather_code"), "未知")
        return f"{name}天气：{desc} {temp}°C"
    except Exception:
        return f"{name}天气：获取失败"


def request_weather() -> str:
    """返回所有城市拼接的天气串，如"北京天气：晴 10°C，滑县天气：多云 11°C\""""
    return "，".join(_fetch_one(name, lat, lon) for name, (lat, lon) in CITIES.items())
