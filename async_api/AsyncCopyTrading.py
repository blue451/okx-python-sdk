# okx/async_api/AsyncCopyTrading.py
from typing import Optional, Dict, Any
from okxx.consts import *


class AsyncCopyTradingAPI:
    """
    跟单交易相关的API - 异步版本
    """

    def __init__(self, client):
        self._client = client

    async def get_existing_leading_positions(
        self, instId: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取当前带单仓位。"""
        params = {}
        if instId is not None:
            params["instId"] = instId
        return await self._client._request_with_params(
            GET, GET_EXISTING_LEADING_POSITIONS, params
        )

    async def get_leading_position_history(
        self,
        instId: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取历史带单仓位。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return await self._client._request_with_params(
            GET, GET_LEADING_POSITIONS_HISTORY, params
        )

    async def place_leading_stop_order(
        self,
        subPosId: str,
        tpTriggerPx: Optional[str] = None,
        slTriggerPx: Optional[str] = None,
        tpTriggerPxType: Optional[str] = None,
        slTriggerPxType: Optional[str] = None,
    ) -> Dict[str, Any]:
        """为带单仓位设置止盈止损。"""
        params = {"subPosId": subPosId}
        if tpTriggerPx is not None:
            params["tpTriggerPx"] = tpTriggerPx
        if slTriggerPx is not None:
            params["slTriggerPx"] = slTriggerPx
        if tpTriggerPxType is not None:
            params["tpTriggerPxType"] = tpTriggerPxType
        if slTriggerPxType is not None:
            params["slTriggerPxType"] = slTriggerPxType
        return await self._client._request_with_params(
            POST, PLACE_LEADING_STOP_ORDER, params
        )

    async def close_leading_position(self, subPosId: str) -> Dict[str, Any]:
        """平掉一个带单仓位。"""
        params = {"subPosId": subPosId}
        return await self._client._request_with_params(
            POST, CLOSE_LEADING_POSITIONS, params
        )

    async def get_leading_instruments(self) -> Dict[str, Any]:
        """获取交易员的带单合约。"""
        return await self._client._request_without_params(GET, GET_LEADING_INSTRUMENTS)

    async def amend_leading_instruments(self, instId: str) -> Dict[str, Any]:
        """修改交易员的带单合约。"""
        params = {"instId": instId}
        return await self._client._request_with_params(
            POST, AMEND_LEADING_INSTRUMENTS, params
        )

    async def get_profit_sharing_details(
        self,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取分润明细。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return await self._client._request_with_params(
            GET, GET_PROFIT_SHARING_DETAILS, params
        )

    async def get_total_profit_sharing(self) -> Dict[str, Any]:
        """获取总分润。"""
        return await self._client._request_without_params(GET, GET_TOTAL_PROFIT_SHARING)

    async def get_unrealized_profit_sharing_details(self) -> Dict[str, Any]:
        """获取未实现分润明细。"""
        return await self._client._request_without_params(
            GET, GET_UNREALIZED_PROFIT_SHARING_DETAILS
        )
