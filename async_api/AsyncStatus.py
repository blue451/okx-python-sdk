from typing import Optional, Dict, Any
from okx.consts import *

class AsyncStatusAPI:
    """
    系统状态相关的API - 异步版本
    """

    def __init__(self, client):
        self._client = client

    async def status(self, state: Optional[str] = None) -> Dict[str, Any]:
        """获取系统状态。"""
        params = {}
        if state is not None:
            params["state"] = state
        return await self._client._request_with_params(GET, STATUS, params)
