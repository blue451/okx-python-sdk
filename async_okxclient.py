# okx/async_okxclient.py
import json
import httpx
from loguru import logger
from typing import Optional, Dict, Any

from okx import consts as c
from okx import utils
from okx import exceptions
from okx.limiter import AsyncRateLimiterManager  # 导入中央管理器


class AsyncOkxClient:
    """
    一个底层的、专用的异步HTTP请求处理器。
    它现在内部集成了速率限制管理器，可以自动处理API限速。
    """

    def __init__(
        self,
        api_key: str,
        api_secret_key: str,
        passphrase: str,
        flag: str,
        base_api: str,
        debug: bool,
        proxy: Optional[str] = None,
    ):
        """
        初始化底层异步客户端。

        Args:
            api_key (str): 您的API Key。
            api_secret_key (str): 您的Secret Key。
            passphrase (str): 您的API Passphrase。
            flag (str): 交易模式标识 ('0' for real, '1' for demo)。
            base_api (str): API的基础URL。
            debug (bool): 是否开启调试模式，打印详细日志。
            proxy (Optional[str]): 代理服务器地址，例如 'http://127.0.0.1:8888'。
        """
        self.API_KEY = api_key
        self.API_SECRET_KEY = api_secret_key
        self.PASSPHRASE = passphrase
        self.flag = flag
        self.domain = base_api
        self.debug = debug

        # 使用 httpx.AsyncClient 创建异步客户端
        self.client = httpx.AsyncClient(
            base_url=base_api, http2=True, proxy=proxy, timeout=30
        )
        # 实例化一个全局的速率限制管理器
        self.limiter_manager = AsyncRateLimiterManager()

    def _get_header(self, sign: str, timestamp: str) -> Dict[str, str]:
        """为需要签名的请求构建请求头。"""
        header: Dict[str, str] = {}
        header[c.CONTENT_TYPE] = c.APPLICATION_JSON
        header[c.OK_ACCESS_KEY] = self.API_KEY
        header[c.OK_ACCESS_SIGN] = sign
        header[c.OK_ACCESS_TIMESTAMP] = timestamp
        header[c.OK_ACCESS_PASSPHRASE] = self.PASSPHRASE
        header["x-simulated-trading"] = self.flag
        if self.debug:
            logger.debug(f"Request Header: {header}")
        return header

    def _get_header_no_sign(self) -> Dict[str, str]:
        """为公共的、无需签名的请求构建请求头。"""
        header: Dict[str, str] = {}
        header[c.CONTENT_TYPE] = c.APPLICATION_JSON
        header["x-simulated-trading"] = self.flag
        if self.debug:
            logger.debug(f"Request Header (No Sign): {header}")
        return header

    async def _request(
        self, method: str, request_path: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        核心异步请求方法，集成了自动速率限制。

        Args:
            method (str): HTTP方法 (e.g., 'GET', 'POST').
            request_path (str): API的请求路径 (e.g., '/api/v5/account/balance').
            params (dict): 请求参数。

        Returns:
            dict: API响应的'data'部分或整个响应体。

        Raises:
            OkxRequestException: 如果HTTP请求层面出错。
            OkxAPIException: 如果API返回错误码。
        """
        # 步骤 1: 自动应用限速器
        await self.limiter_manager.acquire(request_path, params, self.API_KEY)

        # 步骤 2: 根据HTTP方法准备URL和请求体
        if method == c.GET:
            # GET请求：参数附加到URL的查询字符串中，请求体为空
            request_path_with_params = request_path + utils.parse_params_to_str(params)
            body = ""
        elif method == c.POST:
            # POST请求：URL路径保持干净，参数序列化后放入请求体
            request_path_with_params = request_path
            # 使用 separators 生成紧凑的JSON字符串，这是API签名的最佳实践
            body = json.dumps(params, separators=(",", ":")) if params else ""
        else:
            # 如果未来支持其他方法，可以在此扩展
            raise ValueError(f"Unsupported HTTP method: {method}")

        # 步骤 3: 准备签名和请求头
        timestamp = await utils.get_timestamp_async()  # 使用异步版本
        if self.API_KEY != "-1":  # 检查是否需要签名
            # 签名使用的是不带查询参数的原始路径(request_path)和请求体(body)
            # 注意：如果utils.pre_hash是异步的，这里需要await
            sign = utils.sign(
                utils.pre_hash(timestamp, method, request_path, body),
                self.API_SECRET_KEY,
            )
            header = self._get_header(sign.decode("utf-8"), timestamp)
        else:
            # 公共接口不需要签名
            header = self._get_header_no_sign()

        if self.debug:
            logger.debug(f"Domain: {self.domain}")
            logger.debug(f"URL to request: {request_path_with_params}")
            logger.debug(f"Body for request: {body}")

        # 步骤 4: 发送HTTP请求
        try:
            if method == c.GET:
                # FIX: 统一使用 request_path_with_params
                response = await self.client.get(
                    request_path_with_params, headers=header
                )
            elif method == c.POST:
                # 使用 content 参数发送原始字符串，解决类型错误
                response = await self.client.post(
                    request_path_with_params, content=body, headers=header
                )

        except httpx.RequestError as e:
            # 捕获所有 httpx 网络层面的错误 (如超时、DNS问题等)
            raise exceptions.OkxRequestException(f"HTTP request failed: {e}") from e

        # 步骤 5: 处理HTTP响应
        if response.status_code != 200:
            # 如果HTTP状态码不是200 OK，抛出异常
            raise exceptions.OkxAPIException(response)

        # 解析JSON响应
        json_res = response.json()

        # 检查OKX业务错误码
        if "code" in json_res and json_res["code"] != "0":
            raise exceptions.OkxAPIException(response)

        # 成功时，返回 'data' 字段内容，如果 'data' 不存在，则返回整个JSON响应
        return json_res.get("data", json_res)

    async def _request_without_params(
        self, method: str, request_path: str
    ) -> Dict[str, Any]:
        """一个便捷方法，用于发送没有参数的异步请求。"""
        # 内部调用_request，并传递一个空字典作为参数
        return await self._request(method, request_path, {})

    async def _request_with_params(
        self, method: str, request_path: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """一个便捷方法，用于发送带有参数的异步请求。"""
        return await self._request(method, request_path, params)

    async def aclose(self):
        """
        优雅地关闭底层的 httpx.AsyncClient 连接池。
        在程序退出时调用此方法是个好习惯。
        """
        if hasattr(self, 'client') and self.client:
            await self.client.aclose()
    
    async def __aenter__(self):
        """异步上下文管理器支持"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步资源清理"""
        await self.aclose()
