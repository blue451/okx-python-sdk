# okx/async_api/AsyncFDBroker.py
from typing import Optional, Dict, Any
from okx.consts import *

class AsyncFDBrokerAPI:
    """
    FD经纪商相关的API - 异步版本
    """

    def __init__(self, client):
        self._client = client

    async def generate_rebate_details_download_link(self, begin: Optional[str] = None, end: Optional[str] = None) -> Dict[str, Any]:
        """生成返佣明细下载链接。"""
        params = {}
        if begin is not None:
            params["begin"] = begin
        if end is not None:
            params["end"] = end
        return await self._client._request_with_params(POST, FD_REBATE_PER_ORDERS, params)

    async def get_rebate_details_download_link(self, type: Optional[str] = None, begin: Optional[str] = None, end: Optional[str] = None) -> Dict[str, Any]:
        """获取返佣明细下载链接。"""
        params = {}
        if type is not None:
            params["type"] = type
        if begin is not None:
            params["begin"] = begin
        if end is not None:
            params["end"] = end
        return await self._client._request_with_params(GET, FD_REBATE_PER_ORDERS, params)
