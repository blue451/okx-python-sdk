# okx/async_api/AsyncPublicData.py
from typing import Optional, Dict, Any
from okx.consts import *

class AsyncPublicAPI:
    """
    公共数据相关的API - 异步版本
    """

    def __init__(self, client):
        self._client = client

    async def get_instruments(self, instType: str, uly: Optional[str] = None, instId: Optional[str] = None, instFamily: Optional[str] = None) -> Dict[str, Any]:
        """获取交易产品基础信息。"""
        params = {"instType": instType}
        if uly is not None:
            params["uly"] = uly
        if instId is not None:
            params["instId"] = instId
        if instFamily is not None:
            params["instFamily"] = instFamily
        return await self._client._request_with_params(GET, INSTRUMENT_INFO, params)

    async def get_delivery_exercise_history(self, instType: str, uly: Optional[str] = None, after: Optional[str] = None, before: Optional[str] = None, limit: Optional[str] = None, instFamily: Optional[str] = None) -> Dict[str, Any]:
        """获取交割/行权历史。"""
        params = {"instType": instType}
        if uly is not None:
            params["uly"] = uly
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if limit is not None:
            params["limit"] = limit
        if instFamily is not None:
            params["instFamily"] = instFamily
        return await self._client._request_with_params(GET, DELIVERY_EXERCISE, params)

    async def get_open_interest(self, instType: str, uly: Optional[str] = None, instId: Optional[str] = None, instFamily: Optional[str] = None) -> Dict[str, Any]:
        """获取合约/期权全量持仓信息。"""
        params = {"instType": instType}
        if uly is not None:
            params["uly"] = uly
        if instId is not None:
            params["instId"] = instId
        if instFamily is not None:
            params["instFamily"] = instFamily
        return await self._client._request_with_params(GET, OPEN_INTEREST, params)

    async def get_funding_rate(self, instId: str) -> Dict[str, Any]:
        """获取合约资金费率。"""
        params = {"instId": instId}
        return await self._client._request_with_params(GET, FUNDING_RATE, params)

    async def funding_rate_history(self, instId: str, after: Optional[str] = None, before: Optional[str] = None, limit: Optional[str] = None) -> Dict[str, Any]:
        """获取合约资金费率历史。"""
        params = {"instId": instId}
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if limit is not None:
            params["limit"] = limit
        return await self._client._request_with_params(GET, FUNDING_RATE_HISTORY, params)

    async def get_price_limit(self, instId: str) -> Dict[str, Any]:
        """获取产品限价。"""
        params = {"instId": instId}
        return await self._client._request_with_params(GET, PRICE_LIMIT, params)

    async def get_opt_summary(self, uly: Optional[str] = None, expTime: Optional[str] = None, instFamily: Optional[str] = None) -> Dict[str, Any]:
        """获取期权公共成交数据。"""
        params = {}
        if uly is not None:
            params["uly"] = uly
        if expTime is not None:
            params["expTime"] = expTime
        if instFamily is not None:
            params["instFamily"] = instFamily
        return await self._client._request_with_params(GET, OPT_SUMMARY, params)

    async def get_estimated_price(self, instId: str) -> Dict[str, Any]:
        """获取期权估算交割/行权价格。"""
        params = {"instId": instId}
        return await self._client._request_with_params(GET, ESTIMATED_PRICE, params)

    async def discount_interest_free_quota(self, ccy: Optional[str] = None) -> Dict[str, Any]:
        """获取交易产品免息额度。"""
        params = {}
        if ccy is not None:
            params["ccy"] = ccy
        return await self._client._request_with_params(GET, DISCOUNT_INTEREST_INFO, params)

    async def get_system_time(self) -> Dict[str, Any]:
        """获取系统时间。"""
        return await self._client._request_without_params(GET, SYSTEM_TIME)

    async def get_mark_price(self, instType: str, uly: Optional[str] = None, instId: Optional[str] = None, instFamily: Optional[str] = None) -> Dict[str, Any]:
        """获取产品标记价格。"""
        params = {"instType": instType}
        if uly is not None:
            params["uly"] = uly
        if instId is not None:
            params["instId"] = instId
        if instFamily is not None:
            params["instFamily"] = instFamily
        return await self._client._request_with_params(GET, MARK_PRICE, params)

    async def get_position_tiers(self, instType: str, tdMode: str, uly: Optional[str] = None, instId: Optional[str] = None, ccy: Optional[str] = None, tier: Optional[str] = None, instFamily: Optional[str] = None) -> Dict[str, Any]:
        """获取产品档位信息。"""
        params = {"instType": instType, "tdMode": tdMode}
        if uly is not None:
            params["uly"] = uly
        if instId is not None:
            params["instId"] = instId
        if ccy is not None:
            params["ccy"] = ccy
        if tier is not None:
            params["tier"] = tier
        if instFamily is not None:
            params["instFamily"] = instFamily
        return await self._client._request_with_params(GET, TIER, params)

    async def get_interest_rate_loan_quota(self) -> Dict[str, Any]:
        """获取借币利率和限额。"""
        return await self._client._request_without_params(GET, INTEREST_LOAN)

    async def get_vip_interest_rate_loan_quota(self) -> Dict[str, Any]:
        """获取VIP借币利率和限额。"""
        return await self._client._request_without_params(GET, VIP_INTEREST_RATE_LOAN_QUOTA)

    async def get_underlying(self, instType: Optional[str] = None) -> Dict[str, Any]:
        """获取标的指数。"""
        params = {}
        if instType is not None:
            params["instType"] = instType
        return await self._client._request_with_params(GET, UNDERLYING, params)

    async def get_insurance_fund(self, instType: Optional[str] = None, type: Optional[str] = None, uly: Optional[str] = None, ccy: Optional[str] = None, before: Optional[str] = None, after: Optional[str] = None, limit: Optional[str] = None, instFamily: Optional[str] = None) -> Dict[str, Any]:
        """获取风险准备金余额。"""
        params = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._client._request_with_params(GET, INSURANCE_FUND, params)

    async def get_convert_contract_coin(self, type: Optional[str] = None, instId: Optional[str] = None, sz: Optional[str] = None, px: Optional[str] = None, unit: Optional[str] = None) -> Dict[str, Any]:
        """获取合约币种转换信息。"""
        params = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._client._request_with_params(GET, CONVERT_CONTRACT_COIN, params)

    async def get_option_tick_bands(self, instType: Optional[str] = None, instFamily: Optional[str] = None) -> Dict[str, Any]:
        """获取期权价格限制。"""
        params = {}
        if instType is not None:
            params["instType"] = instType
        if instFamily is not None:
            params["instFamily"] = instFamily
        return await self._client._request_with_params(GET, GET_OPTION_TICKBANDS, params)

    async def get_option_trades(self, instId: Optional[str] = None, instFamily: Optional[str] = None, optType: Optional[str] = None) -> Dict[str, Any]:
        """获取期权最新成交数据。"""
        params = {}
        if instId is not None:
            params["instId"] = instId
        if instFamily is not None:
            params["instFamily"] = instFamily
        if optType is not None:
            params["optType"] = optType
        return await self._client._request_with_params(GET, GET_OPTION_TRADES, params)
