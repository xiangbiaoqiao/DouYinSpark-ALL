"""消息模板解析，构建发送内容

可用占位符：
  [API]  -> 一言随机句子
  [天气] -> 所有配置城市的实时天气（如"北京天气：晴 10°C，滑县天气：多云 11°C"）
  [时间] -> 发送时刻（如"10月23日 14:00"）
"""
from datetime import datetime

from utils.config import get_config
from utils.hitokoto import request_hitokoto
from utils.weather import request_weather


def build_message() -> str:
    message = get_config().get("messageTemplate", "续火花")
    if "[API]" in message:
        api_content = request_hitokoto()
        message = message.replace("[API]", api_content)
    if "[天气]" in message:
        message = message.replace("[天气]", request_weather())
    if "[时间]" in message:
        message = message.replace("[时间]", datetime.now().strftime("%m月%d日 %H:%M"))

    return message.strip()
