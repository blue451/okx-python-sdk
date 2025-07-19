import hmac
import base64
import datetime
import logging
import json
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


async def get_server_timestamp() -> Optional[float]:
    """使用httpx异步获取OKX服务器时间戳(秒)."""
    url = "https://www.okx.com/api/v5/public/time"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("code") == "0":
                # 将毫秒时间戳字符串转换为秒的浮点数
                return float(data['data'][0]['ts']) / 1000.0
            else:
                logger.error(f"Failed to get server time, API response: {data}")
                return None
    except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError) as e:
        logger.exception(f"Error fetching server time: {e}")
        return None


def get_timestamp() -> str:
    """同步版本：获取符合OKX API要求的UTC时区ISO 8601格式的时间戳"""
    now = datetime.datetime.utcnow()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"


async def get_timestamp_async() -> str:
    """异步版本：获取符合OKX API要求的UTC时区ISO 8601格式的时间戳（从服务器获取）。"""
    server_time_sec = await get_server_timestamp()
    if server_time_sec:
        dt_object = datetime.datetime.fromtimestamp(
            server_time_sec, tz=datetime.timezone.utc
        )
        return dt_object.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    else:
        # 如果无法获取服务器时间，则回退到本地UTC时间
        logger.warning("无法获取服务器时间，回退到本地UTC时间生成时间戳。")
        return get_timestamp()


def sign(message: str, secretKey: str) -> str:
    """
    使用HMAC-SHA256算法生成签名。

    :param message: 待签名的字符串
    :param secretKey: API Secret
    :return: Base64编码后的签名字符串
    """
    mac = hmac.new(
        bytes(secretKey, encoding="utf8"),
        bytes(message, encoding="utf-8"),
        digestmod="sha256",
    )
    d = mac.digest()
    return base64.b64encode(d)


def pre_hash(timestamp: str, method: str, request_path: str, body: str) -> str:
    """
    拼接生成待签名的源字符串。
    格式: timestamp + method + requestPath + body

    :param timestamp: ISO 8601格式的时间戳
    :param method: HTTP请求方法 (大写)
    :param request_path: 请求路径
    :param body: 请求体字符串
    :return: 拼接后的待签名字符串
    """
    pre_hash_string = str(timestamp) + str.upper(method) + request_path + body
    logger.debug(f"Pre-hash string: {pre_hash_string}")
    return pre_hash_string


def parse_params_to_str(params: dict) -> str:
    """
    将GET请求的参数字典转换为URL查询字符串。

    :param params: 参数字典
    :return: '?key1=value1&key2=value2' 格式的字符串
    """
    if not params:
        return ""
    url = "?"
    for key, value in params.items():
        if value is not None and value != "":
            url = url + str(key) + "=" + str(value) + "&"

    # 移除末尾的 '&'
    if url.endswith("&"):
        url = url[:-1]

    return "" if url == "?" else url
