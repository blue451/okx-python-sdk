from typing import Optional, List, Dict, Any
from okxx.consts import *


class SpreadTradingAPI:
    """
    封装了价差交易相关的API。
    """

    def __init__(self, client):
        self._client = client

    def place_order(
        self,
        sprdId: str,
        side: str,
        ordType: str,
        sz: str,
        clOrdId: Optional[str] = None,
        tag: Optional[str] = None,
        px: Optional[str] = None,
    ) -> Dict[str, Any]:
        """下单价差交易。"""
        params = {
            "sprdId": sprdId,
            "side": side,
            "ordType": ordType,
            "sz": sz,
        }
        if clOrdId is not None:
            params["clOrdId"] = clOrdId
        if tag is not None:
            params["tag"] = tag
        if px is not None:
            params["px"] = px
        return self._client._request_with_params(POST, SPREAD_PLACE_ORDER, params)

    def cancel_order(
        self, ordId: Optional[str] = None, clOrdId: Optional[str] = None
    ) -> Dict[str, Any]:
        """取消价差交易订单。"""
        params = {}
        if ordId is not None:
            params["ordId"] = ordId
        if clOrdId is not None:
            params["clOrdId"] = clOrdId
        return self._client._request_with_params(POST, SPREAD_CANCEL_ORDER, params)

    def cancel_all_orders(self, sprdId: Optional[str] = None) -> Dict[str, Any]:
        """取消所有价差交易订单。"""
        params = {}
        if sprdId is not None:
            params["sprdId"] = sprdId
        return self._client._request_with_params(POST, SPREAD_CANCEL_ALL_ORDERS, params)

    def get_order_details(
        self, ordId: Optional[str] = None, clOrdId: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取价差交易订单详情。"""
        params = {}
        if ordId is not None:
            params["ordId"] = ordId
        if clOrdId is not None:
            params["clOrdId"] = clOrdId
        return self._client._request_with_params(GET, SPREAD_GET_ORDER_DETAILS, params)

    def get_active_orders(
        self,
        sprdId: Optional[str] = None,
        ordType: Optional[str] = None,
        state: Optional[str] = None,
        beginId: Optional[str] = None,
        endId: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取未完成价差交易订单。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, SPREAD_GET_ACTIVE_ORDERS, params)

    def get_orders_history(
        self,
        sprdId: Optional[str] = None,
        ordType: Optional[str] = None,
        state: Optional[str] = None,
        beginId: Optional[str] = None,
        endId: Optional[str] = None,
        begin: Optional[str] = None,
        end: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取价差交易历史订单（近7天）。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, SPREAD_GET_ORDERS_HISTORY, params)

    def get_trades(
        self,
        sprdId: Optional[str] = None,
        tradeId: Optional[str] = None,
        ordId: Optional[str] = None,
        beginId: Optional[str] = None,
        endId: Optional[str] = None,
        begin: Optional[str] = None,
        end: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取价差交易成交明细（近7天）。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, SPREAD_GET_TRADES, params)

    def get_spreads(
        self,
        baseCcy: Optional[str] = None,
        instId: Optional[str] = None,
        sprdId: Optional[str] = None,
        state: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取价差交易产品信息（公共）。"""
        params = {}
        if baseCcy is not None:
            params["baseCcy"] = baseCcy
        if instId is not None:
            params["instId"] = instId
        if sprdId is not None:
            params["sprdId"] = sprdId
        if state is not None:
            params["state"] = state
        return self._client._request_with_params(GET, SPREAD_GET_SPREADS, params)

    def get_order_book(self, sprdId: str, sz: Optional[str] = None) -> Dict[str, Any]:
        """获取价差交易产品深度数据（公共）。"""
        params = {"sprdId": sprdId}
        if sz is not None:
            params["sz"] = sz
        return self._client._request_with_params(GET, SPREAD_GET_ORDER_BOOK, params)

    def get_ticker(self, sprdId: str) -> Dict[str, Any]:
        """获取价差交易产品行情信息（公共）。"""
        params = {"sprdId": sprdId}
        return self._client._request_with_params(GET, SPREAD_GET_TICKER, params)

    def get_public_trades(self, sprdId: str) -> Dict[str, Any]:
        """获取价差交易公共成交数据（公共）。"""
        params = {"sprdId": sprdId}
        return self._client._request_with_params(GET, SPREAD_GET_PUBLIC_TRADES, params)
