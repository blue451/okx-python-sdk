# okx/async_api/AsyncGrid.py
from typing import Optional, List, Dict, Any
from okx.consts import *

class AsyncGridAPI:
    """
    策略交易相关的API - 异步版本
    """

    def __init__(self, client):
        self._client = client

    async def grid_order_algo(self, instId: str, algoOrdType: str, maxPx: str, minPx: str, gridNum: str, runType: str, tpTriggerPx: Optional[str] = None, slTriggerPx: Optional[str] = None, tag: Optional[str] = None, quoteSz: Optional[str] = None, baseSz: Optional[str] = None, sz: Optional[str] = None, direction: Optional[str] = None, lever: Optional[str] = None, basePos: Optional[str] = None) -> Dict[str, Any]:
        """下单策略委托。"""
        params = {
            "instId": instId,
            "algoOrdType": algoOrdType,
            "maxPx": maxPx,
            "minPx": minPx,
            "gridNum": gridNum,
            "runType": runType,
        }
        if tpTriggerPx is not None:
            params["tpTriggerPx"] = tpTriggerPx
        if slTriggerPx is not None:
            params["slTriggerPx"] = slTriggerPx
        if tag is not None:
            params["tag"] = tag
        if quoteSz is not None:
            params["quoteSz"] = quoteSz
        if baseSz is not None:
            params["baseSz"] = baseSz
        if sz is not None:
            params["sz"] = sz
        if direction is not None:
            params["direction"] = direction
        if lever is not None:
            params["lever"] = lever
        if basePos is not None:
            params["basePos"] = basePos
        return await self._client._request_with_params(POST, GRID_ORDER_ALGO, params)

    async def grid_amend_order_algo(self, algoId: str, instId: str, slTriggerPx: Optional[str] = None, tpTriggerPx: Optional[str] = None) -> Dict[str, Any]:
        """修改策略委托。"""
        params = {"algoId": algoId, "instId": instId}
        if slTriggerPx is not None:
            params["slTriggerPx"] = slTriggerPx
        if tpTriggerPx is not None:
            params["tpTriggerPx"] = tpTriggerPx
        return await self._client._request_with_params(POST, GRID_AMEND_ORDER_ALGO, params)

    async def grid_stop_order_algo(self, algoId: str, instId: str, algoOrdType: str, stopType: str) -> Dict[str, Any]:
        """停止策略委托。"""
        params = [
            {
                "algoId": algoId,
                "instId": instId,
                "algoOrdType": algoOrdType,
                "stopType": stopType,
            }
        ]
        return await self._client._request_with_params(POST, GRID_STOP_ORDER_ALGO, params)

    async def grid_orders_algo_pending(self, algoOrdType: Optional[str] = None, algoId: Optional[str] = None, instId: Optional[str] = None, instType: Optional[str] = None, after: Optional[str] = None, before: Optional[str] = None, limit: Optional[str] = None, instFamily: Optional[str] = None) -> Dict[str, Any]:
        """获取未完成策略委托列表。"""
        params = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._client._request_with_params(GET, GRID_ORDERS_ALGO_PENDING, params)

    async def grid_orders_algo_history(self, algoOrdType: Optional[str] = None, algoId: Optional[str] = None, instId: Optional[str] = None, instType: Optional[str] = None, after: Optional[str] = None, before: Optional[str] = None, limit: Optional[str] = None, instFamily: Optional[str] = None) -> Dict[str, Any]:
        """获取历史策略委托列表。"""
        params = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._client._request_with_params(GET, GRID_ORDERS_ALGO_HISTORY, params)

    async def grid_orders_algo_details(self, algoOrdType: str, algoId: str) -> Dict[str, Any]:
        """获取策略委托详情。"""
        params = {"algoOrdType": algoOrdType, "algoId": algoId}
        return await self._client._request_with_params(GET, GRID_ORDERS_ALGO_DETAILS, params)

    async def grid_sub_orders(self, algoId: str, algoOrdType: Optional[str] = None, type: Optional[str] = None, groupId: Optional[str] = None, after: Optional[str] = None, before: Optional[str] = None, limit: Optional[str] = None) -> Dict[str, Any]:
        """获取策略子订单。"""
        params = {"algoId": algoId}
        if algoOrdType is not None:
            params["algoOrdType"] = algoOrdType
        if type is not None:
            params["type"] = type
        if groupId is not None:
            params["groupId"] = groupId
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if limit is not None:
            params["limit"] = limit
        return await self._client._request_with_params(GET, GRID_SUB_ORDERS, params)

    async def grid_positions(self, algoOrdType: str, algoId: str) -> Dict[str, Any]:
        """获取策略持仓。"""
        params = {"algoOrdType": algoOrdType, "algoId": algoId}
        return await self._client._request_with_params(GET, GRID_POSITIONS, params)

    async def grid_withdraw_income(self, algoId: str) -> Dict[str, Any]:
        """提取策略收益。"""
        params = {"algoId": algoId}
        return await self._client._request_with_params(POST, GRID_WITHDRAW_INCOME, params)

    async def grid_compute_margin_balance(self, algoId: str, type: str, amt: str) -> Dict[str, Any]:
        """计算策略保证金。"""
        params = {"algoId": algoId, "type": type, "amt": amt}
        return await self._client._request_with_params(POST, GRID_COMPUTE_MARGIN_BALANCE, params)

    async def grid_adjust_margin_balance(self, algoId: str, type: str, amt: str, percent: Optional[str] = None) -> Dict[str, Any]:
        """调整策略保证金。"""
        params = {"algoId": algoId, "type": type, "amt": amt}
        if percent is not None:
            params["percent"] = percent
        return await self._client._request_with_params(POST, GRID_MARGIN_BALANCE, params)

    async def grid_ai_param(self, algoOrdType: str, instId: str, direction: Optional[str] = None, duration: Optional[str] = None) -> Dict[str, Any]:
        """获取策略AI参数。"""
        params = {"algoOrdType": algoOrdType, "instId": instId}
        if direction is not None:
            params["direction"] = direction
        if duration is not None:
            params["duration"] = duration
        return await self._client._request_with_params(GET, GRID_AI_PARAM, params)

    async def place_recurring_buy_order(self, stgyName: str, recurringList: List[Dict], period: str, recurringDay: str, recurringTime: str, timeZone: str, amt: str, investmentCcy: str, tdMode: str, algoClOrdId: Optional[str] = None, tag: Optional[str] = None) -> Dict[str, Any]:
        """下单定投策略。"""
        params = {
            "stgyName": stgyName,
            "recurringList": recurringList,
            "period": period,
            "recurringDay": recurringDay,
            "recurringTime": recurringTime,
            "timeZone": timeZone,
            "amt": amt,
            "investmentCcy": investmentCcy,
            "tdMode": tdMode,
        }
        if algoClOrdId is not None:
            params["algoClOrdId"] = algoClOrdId
        if tag is not None:
            params["tag"] = tag
        return await self._client._request_with_params(POST, PLACE_RECURRING_BUY_ORDER, params)

    async def amend_recurring_buy_order(self, algoId: str, stgyName: Optional[str] = None) -> Dict[str, Any]:
        """修改定投策略。"""
        params = {"algoId": algoId}
        if stgyName is not None:
            params["stgyName"] = stgyName
        return await self._client._request_with_params(POST, AMEND_RECURRING_BUY_ORDER, params)

    async def stop_recurring_buy_order(self, orders_data: List[Dict]) -> Dict[str, Any]:
        """停止定投策略。"""
        return await self._client._request_with_params(POST, STOP_RECURRING_BUY_ORDER, orders_data)

    async def get_recurring_buy_order_list(self, algoId: Optional[str] = None, after: Optional[str] = None, before: Optional[str] = None, limit: Optional[str] = None) -> Dict[str, Any]:
        """获取定投策略列表。"""
        params = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._client._request_with_params(GET, GET_RECURRING_BUY_ORDER_LIST, params)

    async def get_recurring_buy_order_history(self, algoId: Optional[str] = None, after: Optional[str] = None, before: Optional[str] = None, limit: Optional[str] = None) -> Dict[str, Any]:
        """获取定投策略历史。"""
        params = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._client._request_with_params(GET, GET_RECURRING_BUY_ORDER_HISTORY, params)

    async def get_recurring_buy_order_details(self, algoId: str) -> Dict[str, Any]:
        """获取定投策略详情。"""
        params = {"algoId": algoId}
        return await self._client._request_with_params(GET, GET_RECURRING_BUY_ORDER_DETAILS, params)

    async def get_recurring_buy_sub_orders(self, algoId: str, ordId: Optional[str] = None, after: Optional[str] = None, before: Optional[str] = None, limit: Optional[str] = None) -> Dict[str, Any]:
        """获取定投子订单。"""
        params = {"algoId": algoId}
        if ordId is not None:
            params["ordId"] = ordId
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if limit is not None:
            params["limit"] = limit
        return await self._client._request_with_params(GET, GET_RECURRING_BUY_SUB_ORDERS, params)
