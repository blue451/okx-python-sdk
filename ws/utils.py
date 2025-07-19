# okx/ws/utils.py

import base64
import hmac
import json
import logging
import time
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


async def get_server_timestamp() -> Optional[float]: # <-- 返回类型改为 float
    """使用httpx异步获取OKX服务器时间戳(秒)."""
    url = "https://www.okx.com/api/v5/public/time"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("code") == "0":
                # 将毫秒时间戳字符串转换为秒的浮点数
                return float(data['data'][0]['ts']) / 1000.0 # <-- 转换为秒
            else:
                logger.error(f"Failed to get server time, API response: {data}")
                return None
    except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError) as e:
        logger.error(f"Error fetching server time: {e}")
        return None

def get_local_timestamp() -> str:
    """获取本地UTC时间戳（秒）"""
    return str(int(time.time()))

async def generate_login_payload(api_key, passphrase, secret_key, use_server_time=False) -> str:
    """异步生成登录认证的JSON负载"""
    if use_server_time:
        server_time_sec = await get_server_timestamp()
        if not server_time_sec:
            logger.error("Could not get server time, falling back to local time.")
            timestamp_s = get_local_timestamp()
        else:
            timestamp_s = str(int(server_time_sec))
    else:
        timestamp_s = get_local_timestamp()

    message = timestamp_s + 'GET' + '/users/self/verify'
    
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    sign = base64.b64encode(d).decode('utf-8')
    
    arg = {
        "apiKey": api_key,
        "passphrase": passphrase,
        "timestamp": timestamp_s,
        "sign": sign
    }
    
    payload = {"op": "login", "args": [arg]}
    return json.dumps(payload)