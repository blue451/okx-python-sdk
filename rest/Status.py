from typing import Optional, Dict, Any
from okx.consts import *

class StatusAPI:
    """
    封装了获取系统状态的API。
    """

    def __init__(self, client):
        self._client = client

    def status(self, state: Optional[str] = None) -> Dict[str, Any]:
        """获取系统状态。"""
        params = {}
        if state is not None:
            params["state"] = state
        return self._client._request_with_params(GET, STATUS, params)
