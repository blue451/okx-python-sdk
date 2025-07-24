from typing import Optional, List, Dict, Any
from okxx.consts import *


class AsyncTradeAPI:
    """
    交易相关的API - 异步版本
    """

    def __init__(self, client):
        self._client = client

    async def place_order(
        self,
        instId: str,
        tdMode: str,
        side: str,
        ordType: str,
        sz: str,
        ccy: Optional[str] = None,
        clOrdId: Optional[str] = None,
        tag: Optional[str] = None,
        posSide: Optional[str] = None,
        px: Optional[str] = None,
        reduceOnly: Optional[bool] = None,
        tgtCcy: Optional[str] = None,
        stpMode: Optional[str] = None,
        attachAlgoOrds: Optional[List[Dict]] = None,
        pxUsd: Optional[str] = None,
        pxVol: Optional[str] = None,
        banAmend: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """下单。"""
        params = {
            "instId": instId,
            "tdMode": tdMode,
            "side": side,
            "ordType": ordType,
            "sz": sz,
        }
        if ccy is not None:
            params["ccy"] = ccy
        if clOrdId is not None:
            params["clOrdId"] = clOrdId
        if tag is not None:
            params["tag"] = tag
        if posSide is not None:
            params["posSide"] = posSide
        if px is not None:
            params["px"] = px
        if reduceOnly is not None:
            params["reduceOnly"] = reduceOnly
        if tgtCcy is not None:
            params["tgtCcy"] = tgtCcy
        if stpMode is not None:
            params["stpMode"] = stpMode
        if attachAlgoOrds is not None:
            params["attachAlgoOrds"] = attachAlgoOrds
        if pxUsd is not None:
            params["pxUsd"] = pxUsd
        if pxVol is not None:
            params["pxVol"] = pxVol
        if banAmend is not None:
            params["banAmend"] = banAmend
        return await self._client._request_with_params(POST, PLACE_ORDER, params)

    async def place_multiple_orders(self, orders_data: List[Dict]) -> Dict[str, Any]:
        """批量下单。"""
        return await self._client._request_with_params(POST, BATCH_ORDERS, orders_data)

    async def cancel_order(
        self, instId: str, ordId: Optional[str] = None, clOrdId: Optional[str] = None
    ) -> Dict[str, Any]:
        """撤销订单。"""
        params = {"instId": instId}
        if ordId is not None:
            params["ordId"] = ordId
        if clOrdId is not None:
            params["clOrdId"] = clOrdId
        return await self._client._request_with_params(POST, CANCEL_ORDER, params)

    async def cancel_multiple_orders(self, orders_data: List[Dict]) -> Dict[str, Any]:
        """批量撤销订单。"""
        return await self._client._request_with_params(
            POST, CANCEL_BATCH_ORDERS, orders_data
        )

    async def amend_order(
        self,
        instId: str,
        cxlOnFail: Optional[bool] = None,
        ordId: Optional[str] = None,
        clOrdId: Optional[str] = None,
        reqId: Optional[str] = None,
        newSz: Optional[str] = None,
        newPx: Optional[str] = None,
        newTpTriggerPx: Optional[str] = None,
        newTpOrdPx: Optional[str] = None,
        newSlTriggerPx: Optional[str] = None,
        newSlOrdPx: Optional[str] = None,
        newTpTriggerPxType: Optional[str] = None,
        newSlTriggerPxType: Optional[str] = None,
        attachAlgoOrds: Optional[List[Dict]] = None,
        newTriggerPx: Optional[str] = None,
        newOrdPx: Optional[str] = None,
    ) -> Dict[str, Any]:
        """修改订单。"""
        params = {"instId": instId}
        if cxlOnFail is not None:
            params["cxlOnFail"] = cxlOnFail
        if ordId is not None:
            params["ordId"] = ordId
        if clOrdId is not None:
            params["clOrdId"] = clOrdId
        if reqId is not None:
            params["reqId"] = reqId
        if newSz is not None:
            params["newSz"] = newSz
        if newPx is not None:
            params["newPx"] = newPx
        if newTpTriggerPx is not None:
            params["newTpTriggerPx"] = newTpTriggerPx
        if newTpOrdPx is not None:
            params["newTpOrdPx"] = newTpOrdPx
        if newSlTriggerPx is not None:
            params["newSlTriggerPx"] = newSlTriggerPx
        if newSlOrdPx is not None:
            params["newSlOrdPx"] = newSlOrdPx
        if newTpTriggerPxType is not None:
            params["newTpTriggerPxType"] = newTpTriggerPxType
        if newSlTriggerPxType is not None:
            params["newSlTriggerPxType"] = newSlTriggerPxType
        if attachAlgoOrds is not None:
            params["attachAlgoOrds"] = attachAlgoOrds
        if newTriggerPx is not None:
            params["newTriggerPx"] = newTriggerPx
        if newOrdPx is not None:
            params["newOrdPx"] = newOrdPx
        return await self._client._request_with_params(POST, AMEND_ORDER, params)

    async def amend_multiple_orders(self, orders_data: List[Dict]) -> Dict[str, Any]:
        """批量修改订单。"""
        return await self._client._request_with_params(
            POST, AMEND_BATCH_ORDER, orders_data
        )

    async def close_positions(
        self,
        instId: str,
        mgnMode: str,
        posSide: Optional[str] = None,
        ccy: Optional[str] = None,
        autoCxl: Optional[bool] = None,
        clOrdId: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        """平仓。"""
        params = {"instId": instId, "mgnMode": mgnMode}
        if posSide is not None:
            params["posSide"] = posSide
        if ccy is not None:
            params["ccy"] = ccy
        if autoCxl is not None:
            params["autoCxl"] = autoCxl
        if clOrdId is not None:
            params["clOrdId"] = clOrdId
        if tag is not None:
            params["tag"] = tag
        return await self._client._request_with_params(POST, CLOSE_POSITION, params)

    async def get_order(
        self, instId: str, ordId: Optional[str] = None, clOrdId: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取订单信息。"""
        params = {"instId": instId}
        if ordId is not None:
            params["ordId"] = ordId
        if clOrdId is not None:
            params["clOrdId"] = clOrdId
        return await self._client._request_with_params(GET, ORDER_INFO, params)

    async def get_order_list(
        self,
        instType: Optional[str] = None,
        uly: Optional[str] = None,
        instId: Optional[str] = None,
        ordType: Optional[str] = None,
        state: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
        instFamily: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取未完成订单列表。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return await self._client._request_with_params(GET, ORDERS_PENDING, params)

    async def get_orders_history(
        self,
        instType: str,
        uly: Optional[str] = None,
        instId: Optional[str] = None,
        ordType: Optional[str] = None,
        state: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        begin: Optional[str] = None,
        end: Optional[str] = None,
        limit: Optional[str] = None,
        instFamily: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取订单历史（近7天）。"""
        params = {"instType": instType}
        if uly is not None:
            params["uly"] = uly
        if instId is not None:
            params["instId"] = instId
        if ordType is not None:
            params["ordType"] = ordType
        if state is not None:
            params["state"] = state
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if begin is not None:
            params["begin"] = begin
        if end is not None:
            params["end"] = end
        if limit is not None:
            params["limit"] = limit
        if instFamily is not None:
            params["instFamily"] = instFamily
        return await self._client._request_with_params(GET, ORDERS_HISTORY, params)

    async def get_orders_history_archive(
        self,
        instType: str,
        uly: Optional[str] = None,
        instId: Optional[str] = None,
        ordType: Optional[str] = None,
        state: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        begin: Optional[str] = None,
        end: Optional[str] = None,
        limit: Optional[str] = None,
        instFamily: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取订单历史（近3个月）。"""
        params = {"instType": instType}
        if uly is not None:
            params["uly"] = uly
        if instId is not None:
            params["instId"] = instId
        if ordType is not None:
            params["ordType"] = ordType
        if state is not None:
            params["state"] = state
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if begin is not None:
            params["begin"] = begin
        if end is not None:
            params["end"] = end
        if limit is not None:
            params["limit"] = limit
        if instFamily is not None:
            params["instFamily"] = instFamily
        return await self._client._request_with_params(
            GET, ORDERS_HISTORY_ARCHIVE, params
        )

    async def get_fills(
        self,
        instType: Optional[str] = None,
        uly: Optional[str] = None,
        instId: Optional[str] = None,
        ordId: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
        instFamily: Optional[str] = None,
        begin: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取成交明细。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return await self._client._request_with_params(GET, ORDER_FILLS, params)

    async def place_algo_order(
        self,
        instId: str,
        tdMode: str,
        side: str,
        ordType: str,
        sz: str,
        ccy: Optional[str] = None,
        posSide: Optional[str] = None,
        reduceOnly: Optional[bool] = None,
        tpTriggerPx: Optional[str] = None,
        tpOrdPx: Optional[str] = None,
        slTriggerPx: Optional[str] = None,
        slOrdPx: Optional[str] = None,
        triggerPx: Optional[str] = None,
        orderPx: Optional[str] = None,
        tgtCcy: Optional[str] = None,
        pxVar: Optional[str] = None,
        pxSpread: Optional[str] = None,
        szLimit: Optional[str] = None,
        pxLimit: Optional[str] = None,
        timeInterval: Optional[str] = None,
        tpTriggerPxType: Optional[str] = None,
        slTriggerPxType: Optional[str] = None,
        callbackRatio: Optional[str] = None,
        callbackSpread: Optional[str] = None,
        activePx: Optional[str] = None,
        tag: Optional[str] = None,
        triggerPxType: Optional[str] = None,
        closeFraction: Optional[str] = None,
        quickMgnType: Optional[str] = None,
        algoClOrdId: Optional[str] = None,
    ) -> Dict[str, Any]:
        """下单策略委托。"""
        params = {
            "instId": instId,
            "tdMode": tdMode,
            "side": side,
            "ordType": ordType,
            "sz": sz,
        }
        if ccy is not None:
            params["ccy"] = ccy
        if posSide is not None:
            params["posSide"] = posSide
        if reduceOnly is not None:
            params["reduceOnly"] = reduceOnly
        if tpTriggerPx is not None:
            params["tpTriggerPx"] = tpTriggerPx
        if tpOrdPx is not None:
            params["tpOrdPx"] = tpOrdPx
        if slTriggerPx is not None:
            params["slTriggerPx"] = slTriggerPx
        if slOrdPx is not None:
            params["slOrdPx"] = slOrdPx
        if triggerPx is not None:
            params["triggerPx"] = triggerPx
        if orderPx is not None:
            params["orderPx"] = orderPx
        if tgtCcy is not None:
            params["tgtCcy"] = tgtCcy
        if pxVar is not None:
            params["pxVar"] = pxVar
        if pxSpread is not None:
            params["pxSpread"] = pxSpread
        if szLimit is not None:
            params["szLimit"] = szLimit
        if pxLimit is not None:
            params["pxLimit"] = pxLimit
        if timeInterval is not None:
            params["timeInterval"] = timeInterval
        if tpTriggerPxType is not None:
            params["tpTriggerPxType"] = tpTriggerPxType
        if slTriggerPxType is not None:
            params["slTriggerPxType"] = slTriggerPxType
        if callbackRatio is not None:
            params["callbackRatio"] = callbackRatio
        if callbackSpread is not None:
            params["callbackSpread"] = callbackSpread
        if activePx is not None:
            params["activePx"] = activePx
        if tag is not None:
            params["tag"] = tag
        if triggerPxType is not None:
            params["triggerPxType"] = triggerPxType
        if closeFraction is not None:
            params["closeFraction"] = closeFraction
        if quickMgnType is not None:
            params["quickMgnType"] = quickMgnType
        if algoClOrdId is not None:
            params["algoClOrdId"] = algoClOrdId
        return await self._client._request_with_params(POST, PLACE_ALGO_ORDER, params)

    async def cancel_algo_order(self, params: List[Dict]) -> Dict[str, Any]:
        """撤销策略委托。"""
        return await self._client._request_with_params(POST, CANCEL_ALGOS, params)

    async def get_algo_order_list(
        self,
        ordType: Optional[str] = None,
        algoId: Optional[str] = None,
        instType: Optional[str] = None,
        instId: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取未完成策略委托列表。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return await self._client._request_with_params(GET, ORDERS_ALGO_PENDING, params)

    async def get_algo_order_history(
        self,
        ordType: str,
        state: Optional[str] = None,
        algoId: Optional[str] = None,
        instType: Optional[str] = None,
        instId: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取策略委托历史。"""
        params = {"ordType": ordType}
        if state is not None:
            params["state"] = state
        if algoId is not None:
            params["algoId"] = algoId
        if instType is not None:
            params["instType"] = instType
        if instId is not None:
            params["instId"] = instId
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if limit is not None:
            params["limit"] = limit
        return await self._client._request_with_params(GET, ORDERS_ALGO_HISTORY, params)

    async def get_fills_history(
        self,
        instType: str,
        uly: Optional[str] = None,
        instId: Optional[str] = None,
        ordId: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
        instFamily: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取成交明细历史。"""
        params = {"instType": instType}
        if uly is not None:
            params["uly"] = uly
        if instId is not None:
            params["instId"] = instId
        if ordId is not None:
            params["ordId"] = ordId
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if limit is not None:
            params["limit"] = limit
        if instFamily is not None:
            params["instFamily"] = instFamily
        return await self._client._request_with_params(
            GET, ORDERS_FILLS_HISTORY, params
        )

    async def get_easy_convert_currency_list(self) -> Dict[str, Any]:
        """获取一键兑换币种列表。"""
        return await self._client._request_without_params(
            GET, EASY_CONVERT_CURRENCY_LIST
        )

    async def easy_convert(self, fromCcy: List[str], toCcy: str) -> Dict[str, Any]:
        """一键兑换。"""
        params = {"fromCcy": fromCcy, "toCcy": toCcy}
        return await self._client._request_with_params(POST, EASY_CONVERT, params)

    async def get_easy_convert_history(
        self,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取一键兑换历史。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return await self._client._request_with_params(
            GET, CONVERT_EASY_HISTORY, params
        )

    async def get_oneclick_repay_list(
        self, debtType: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取一键还债币种列表。"""
        params = {}
        if debtType is not None:
            params["debtType"] = debtType
        return await self._client._request_with_params(
            GET, ONE_CLICK_REPAY_SUPPORT, params
        )

    async def oneclick_repay(self, debtCcy: List[str], repayCcy: str) -> Dict[str, Any]:
        """一键还债。"""
        params = {"debtCcy": debtCcy, "repayCcy": repayCcy}
        return await self._client._request_with_params(POST, ONE_CLICK_REPAY, params)

    async def oneclick_repay_history(
        self,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取一键还债历史。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return await self._client._request_with_params(
            GET, ONE_CLICK_REPAY_HISTORY, params
        )

    async def get_algo_order_details(
        self, algoId: Optional[str] = None, algoClOrdId: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取策略委托详情。"""
        params = {}
        if algoId is not None:
            params["algoId"] = algoId
        if algoClOrdId is not None:
            params["algoClOrdId"] = algoClOrdId
        return await self._client._request_with_params(
            GET, GET_ALGO_ORDER_DETAILS, params
        )

    async def amend_algo_order(
        self,
        instId: str,
        algoId: Optional[str] = None,
        algoClOrdId: Optional[str] = None,
        cxlOnFail: Optional[bool] = None,
        reqId: Optional[str] = None,
        newSz: Optional[str] = None,
        newTpTriggerPx: Optional[str] = None,
        newTpOrdPx: Optional[str] = None,
        newSlTriggerPx: Optional[str] = None,
        newSlOrdPx: Optional[str] = None,
        newTpTriggerPxType: Optional[str] = None,
        newSlTriggerPxType: Optional[str] = None,
    ) -> Dict[str, Any]:
        """修改策略委托。"""
        params = {"instId": instId}
        if algoId is not None:
            params["algoId"] = algoId
        if algoClOrdId is not None:
            params["algoClOrdId"] = algoClOrdId
        if cxlOnFail is not None:
            params["cxlOnFail"] = cxlOnFail
        if reqId is not None:
            params["reqId"] = reqId
        if newSz is not None:
            params["newSz"] = newSz
        if newTpTriggerPx is not None:
            params["newTpTriggerPx"] = newTpTriggerPx
        if newTpOrdPx is not None:
            params["newTpOrdPx"] = newTpOrdPx
        if newSlTriggerPx is not None:
            params["newSlTriggerPx"] = newSlTriggerPx
        if newSlOrdPx is not None:
            params["newSlOrdPx"] = newSlOrdPx
        if newTpTriggerPxType is not None:
            params["newTpTriggerPxType"] = newTpTriggerPxType
        if newSlTriggerPxType is not None:
            params["newSlTriggerPxType"] = newSlTriggerPxType
        return await self._client._request_with_params(POST, AMEND_ALGO_ORDER, params)

    async def get_oneclick_repay_list_v2(self) -> Dict[str, Any]:
        """获取一键还债币种列表V2。"""
        return await self._client._request_without_params(
            GET, ONE_CLICK_REPAY_SUPPORT_V2
        )

    async def oneclick_repay_v2(
        self, debtCcy: str, repayCcyList: List[str]
    ) -> Dict[str, Any]:
        """一键还债V2。"""
        params = {"debtCcy": debtCcy, "repayCcyList": repayCcyList}
        return await self._client._request_with_params(POST, ONE_CLICK_REPAY_V2, params)

    async def oneclick_repay_history_v2(
        self,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取一键还债历史V2。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return await self._client._request_with_params(
            GET, ONE_CLICK_REPAY_HISTORY_V2, params
        )
