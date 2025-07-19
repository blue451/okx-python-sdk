from typing import Optional, Dict, Any
from okx.consts import *

class AsyncTradingDataAPI:
    """
    交易大数据相关的API - 异步版本
    """

    def __init__(self, client):
        self._client = client

    async def get_support_coin(self) -> Dict[str, Any]:
        """获取支持的币种列表。"""
        return await self._client._request_without_params(GET, SUPPORT_COIN)

    async def get_taker_volume(self, ccy: str, instType: str, begin: Optional[str] = None, end: Optional[str] = None, period: Optional[str] = None) -> Dict[str, Any]:
        """获取Taker交易量。"""
        params = {"ccy": ccy, "instType": instType}
        if begin is not None:
            params["begin"] = begin
        if end is not None:
            params["end"] = end
        if period is not None:
            params["period"] = period
        return await self._client._request_with_params(GET, TAKER_VOLUME, params)

    async def get_margin_lending_ratio(self, ccy: str, begin: Optional[str] = None, end: Optional[str] = None, period: Optional[str] = None) -> Dict[str, Any]:
        """获取杠杆借币与持仓比率。"""
        params = {"ccy": ccy}
        if begin is not None:
            params["begin"] = begin
        if end is not None:
            params["end"] = end
        if period is not None:
            params["period"] = period
        return await self._client._request_with_params(GET, MARGIN_LENDING_RATIO, params)

    async def get_long_short_ratio(self, ccy: str, begin: Optional[str] = None, end: Optional[str] = None, period: Optional[str] = None) -> Dict[str, Any]:
        """获取多空持仓人数比。"""
        params = {"ccy": ccy}
        if begin is not None:
            params["begin"] = begin
        if end is not None:
            params["end"] = end
        if period is not None:
            params["period"] = period
        return await self._client._request_with_params(GET, LONG_SHORT_RATIO, params)

    async def get_contracts_interest_volume(self, ccy: str, begin: Optional[str] = None, end: Optional[str] = None, period: Optional[str] = None) -> Dict[str, Any]:
        """获取合约持仓量和交易量。"""
        params = {"ccy": ccy}
        if begin is not None:
            params["begin"] = begin
        if end is not None:
            params["end"] = end
        if period is not None:
            params["period"] = period
        return await self._client._request_with_params(GET, CONTRACTS_INTEREST_VOLUME, params)

    async def get_options_interest_volume(self, ccy: str, period: Optional[str] = None) -> Dict[str, Any]:
        """获取期权持仓量和交易量。"""
        params = {"ccy": ccy}
        if period is not None:
            params["period"] = period
        return await self._client._request_with_params(GET, OPTIONS_INTEREST_VOLUME, params)

    async def get_put_call_ratio(self, ccy: str, period: Optional[str] = None) -> Dict[str, Any]:
        """获取期权看涨看跌比。"""
        params = {"ccy": ccy}
        if period is not None:
            params["period"] = period
        return await self._client._request_with_params(GET, PUT_CALL_RATIO, params)

    async def get_interest_volume_expiry(self, ccy: str, period: Optional[str] = None) -> Dict[str, Any]:
        """获取期权到期日持仓量和交易量。"""
        params = {"ccy": ccy}
        if period is not None:
            params["period"] = period
        return await self._client._request_with_params(GET, OPEN_INTEREST_VOLUME_EXPIRY, params)

    async def get_interest_volume_strike(self, ccy: str, expTime: str, period: Optional[str] = None) -> Dict[str, Any]:
        """获取期权行权价持仓量和交易量。"""
        params = {"ccy": ccy, "expTime": expTime}
        if period is not None:
            params["period"] = period
        return await self._client._request_with_params(GET, INTEREST_VOLUME_STRIKE, params)

    async def get_taker_block_volume(self, ccy: str, period: Optional[str] = None) -> Dict[str, Any]:
        """获取Taker大宗交易量。"""
        params = {"ccy": ccy}
        if period is not None:
            params["period"] = period
        return await self._client._request_with_params(GET, TAKER_FLOW, params)
