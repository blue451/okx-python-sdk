# okx/async_api/AsyncConvert.py
from typing import Optional, Dict, Any
from okxx.consts import *


class AsyncConvertAPI:
    """
    闪兑相关的API - 异步版本
    """

    def __init__(self, client):
        self._client = client

    async def get_currencies(self) -> Dict[str, Any]:
        """获取闪兑币种列表。"""
        return await self._client._request_without_params(GET, GET_CURRENCIES)

    async def get_currency_pair(self, fromCcy: str, toCcy: str) -> Dict[str, Any]:
        """获取闪兑币对信息。"""
        params = {"fromCcy": fromCcy, "toCcy": toCcy}
        return await self._client._request_with_params(GET, GET_CURRENCY_PAIR, params)

    async def estimate_quote(
        self,
        baseCcy: str,
        quoteCcy: str,
        side: str,
        rfqSz: str,
        rfqSzCcy: str,
        clQReqId: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取闪兑预估报价。"""
        params = {
            "baseCcy": baseCcy,
            "quoteCcy": quoteCcy,
            "side": side,
            "rfqSz": rfqSz,
            "rfqSzCcy": rfqSzCcy,
        }
        if clQReqId is not None:
            params["clQReqId"] = clQReqId
        if tag is not None:
            params["tag"] = tag
        return await self._client._request_with_params(POST, ESTIMATE_QUOTE, params)

    async def convert_trade(
        self,
        quoteId: str,
        baseCcy: str,
        quoteCcy: str,
        side: str,
        sz: str,
        szCcy: str,
        clTReqId: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        """闪兑交易。"""
        params = {
            "quoteId": quoteId,
            "baseCcy": baseCcy,
            "quoteCcy": quoteCcy,
            "side": side,
            "sz": sz,
            "szCcy": szCcy,
        }
        if clTReqId is not None:
            params["clTReqId"] = clTReqId
        if tag is not None:
            params["tag"] = tag
        return await self._client._request_with_params(POST, CONVERT_TRADE, params)

    async def get_convert_history(
        self,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取闪兑历史记录。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return await self._client._request_with_params(GET, CONVERT_HISTORY, params)
