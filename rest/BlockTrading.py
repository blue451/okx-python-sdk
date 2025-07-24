# okx/rest/BlockTrading.py
from typing import Optional, List, Dict, Any
from okxx.consts import *


class BlockTradingAPI:
    """
    封装了RFQ大宗交易相关的API。
    """

    def __init__(self, client):
        self._client = client

    def get_counterparties(self) -> Dict[str, Any]:
        """获取交易对手方列表。"""
        return self._client._request_without_params(GET, COUNTERPARTIES)

    def create_rfq(
        self,
        counterparties: List[str],
        legs: List[Dict],
        anonymous: bool = False,
        clRfqId: Optional[str] = None,
        tag: Optional[str] = None,
        allowPartialExecution: bool = False,
    ) -> Dict[str, Any]:
        """创建RFQ。"""
        params = {
            "counterparties": counterparties,
            "anonymous": anonymous,
            "allowPartialExecution": allowPartialExecution,
            "legs": legs,
        }
        if clRfqId is not None:
            params["clRfqId"] = clRfqId
        if tag is not None:
            params["tag"] = tag
        return self._client._request_with_params(POST, CREATE_RFQ, params)

    def cancel_rfq(
        self, rfqId: Optional[str] = None, clRfqId: Optional[str] = None
    ) -> Dict[str, Any]:
        """取消RFQ。"""
        params = {}
        if rfqId is not None:
            params["rfqId"] = rfqId
        if clRfqId is not None:
            params["clRfqId"] = clRfqId
        return self._client._request_with_params(POST, CANCEL_RFQ, params)

    def cancel_batch_rfqs(
        self, rfqIds: Optional[List[str]] = None, clRfqIds: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """批量取消RFQ。"""
        params = {}
        if rfqIds is not None:
            params["rfqIds"] = rfqIds
        if clRfqIds is not None:
            params["clRfqIds"] = clRfqIds
        return self._client._request_with_params(POST, CANCEL_BATCH_RFQS, params)

    def cancel_all_rfqs(self) -> Dict[str, Any]:
        """取消所有RFQ。"""
        return self._client._request_without_params(POST, CANCEL_ALL_RFQS)

    def execute_quote(
        self, rfqId: str, quoteId: str, legs: List[Dict]
    ) -> Dict[str, Any]:
        """执行报价。"""
        params = {"rfqId": rfqId, "quoteId": quoteId, "legs": legs}
        return self._client._request_with_params(POST, EXECUTE_QUOTE, params)

    def create_quote(
        self,
        rfqId: str,
        quoteSide: str,
        legs: List[Dict],
        clQuoteId: Optional[str] = None,
        tag: Optional[str] = None,
        anonymous: bool = False,
        expiresIn: Optional[str] = None,
    ) -> Dict[str, Any]:
        """创建报价。"""
        params = {
            "rfqId": rfqId,
            "quoteSide": quoteSide,
            "legs": legs,
            "anonymous": anonymous,
        }
        if clQuoteId is not None:
            params["clQuoteId"] = clQuoteId
        if tag is not None:
            params["tag"] = tag
        if expiresIn is not None:
            params["expiresIn"] = expiresIn
        return self._client._request_with_params(POST, CREATE_QUOTE, params)

    def cancel_quote(
        self, quoteId: Optional[str] = None, clQuoteId: Optional[str] = None
    ) -> Dict[str, Any]:
        """取消报价。"""
        params = {}
        if quoteId is not None:
            params["quoteId"] = quoteId
        if clQuoteId is not None:
            params["clQuoteId"] = clQuoteId
        return self._client._request_with_params(POST, CANCEL_QUOTE, params)

    def cancel_batch_quotes(
        self,
        quoteIds: Optional[List[str]] = None,
        clQuoteIds: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """批量取消报价。"""
        params = {}
        if quoteIds is not None:
            params["quoteIds"] = quoteIds
        if clQuoteIds is not None:
            params["clQuoteIds"] = clQuoteIds
        return self._client._request_with_params(POST, CANCEL_BATCH_QUOTES, params)

    def cancel_all_quotes(self) -> Dict[str, Any]:
        """取消所有报价。"""
        return self._client._request_without_params(POST, CANCEL_ALL_QUOTES)

    def get_rfqs(
        self,
        rfqId: Optional[str] = None,
        clRfqId: Optional[str] = None,
        state: Optional[str] = None,
        beginId: Optional[str] = None,
        endId: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取RFQ列表。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, GET_RFQS, params)

    def get_quotes(
        self,
        rfqId: Optional[str] = None,
        clRfqId: Optional[str] = None,
        quoteId: Optional[str] = None,
        clQuoteId: Optional[str] = None,
        state: Optional[str] = None,
        beginId: Optional[str] = None,
        endId: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取报价列表。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, GET_QUOTES, params)

    def get_trades(
        self,
        rfqId: Optional[str] = None,
        clRfqId: Optional[str] = None,
        quoteId: Optional[str] = None,
        clQuoteId: Optional[str] = None,
        state: Optional[str] = None,
        beginId: Optional[str] = None,
        endId: Optional[str] = None,
        beginTs: Optional[str] = None,
        endTs: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取大宗交易成交历史。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, GET_RFQ_TRADES, params)

    def get_public_trades(
        self,
        beginId: Optional[str] = None,
        endId: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取大宗交易公共成交数据。"""
        params = {}
        if beginId is not None:
            params["beginId"] = beginId
        if endId is not None:
            params["endId"] = endId
        if limit is not None:
            params["limit"] = limit
        return self._client._request_with_params(GET, GET_PUBLIC_TRADES, params)

    def reset_mmp(self) -> Dict[str, Any]:
        """重置MMP状态。"""
        return self._client._request_without_params(POST, MMP_RESET)

    def set_maker_instrument(self, params: List[Dict]) -> Dict[str, Any]:
        """设置MMP可报价的标的。"""
        return self._client._request_with_params(
            POST, MARKER_INSTRUMENT_SETTING, params
        )

    def get_quote_products(self) -> Dict[str, Any]:
        """获取可报价产品。"""
        return self._client._request_without_params(GET, MARKER_INSTRUMENT_SETTING)
