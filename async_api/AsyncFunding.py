# okx/async_api/AsyncFunding.py
from typing import Optional, List, Dict, Any
from okxx.consts import *


class AsyncFundingAPI:
    """
    资金账户相关的API - 异步版本
    """

    def __init__(self, client):
        self._client = client

    async def get_non_tradable_assets(
        self, ccy: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取不可交易资产。"""
        params = {}
        if ccy is not None:
            params["ccy"] = ccy
        return await self._client._request_with_params(GET, NON_TRADABLE_ASSETS, params)

    async def get_deposit_address(self, ccy: str) -> Dict[str, Any]:
        """获取充值地址。"""
        params = {"ccy": ccy}
        return await self._client._request_with_params(GET, DEPOSIT_ADDRESS, params)

    async def transfer_state(
        self, transId: str, type: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取资金划转状态。"""
        params = {"transId": transId}
        if type is not None:
            params["type"] = type
        return await self._client._request_with_params(GET, TRANSFER_STATE, params)

    async def get_balances(self, ccy: Optional[str] = None) -> Dict[str, Any]:
        """获取资金账户余额。"""
        params = {}
        if ccy is not None:
            params["ccy"] = ccy
        return await self._client._request_with_params(GET, GET_BALANCES, params)

    async def funds_transfer(
        self,
        ccy: str,
        amt: str,
        from_: str,
        to: str,
        type: Optional[str] = None,
        subAcct: Optional[str] = None,
        instId: Optional[str] = None,
        toInstId: Optional[str] = None,
        loanTrans: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """资金划转。"""
        params = {"ccy": ccy, "amt": amt, "from": from_, "to": to}
        if type is not None:
            params["type"] = type
        if subAcct is not None:
            params["subAcct"] = subAcct
        if instId is not None:
            params["instId"] = instId
        if toInstId is not None:
            params["toInstId"] = toInstId
        if loanTrans is not None:
            params["loanTrans"] = loanTrans
        return await self._client._request_with_params(POST, FUNDS_TRANSFER, params)

    async def withdrawal(
        self,
        ccy: str,
        amt: str,
        dest: str,
        toAddr: str,
        fee: str,
        chain: Optional[str] = None,
        areaCode: Optional[str] = None,
        clientId: Optional[str] = None,
    ) -> Dict[str, Any]:
        """提币。"""
        params = {"ccy": ccy, "amt": amt, "dest": dest, "toAddr": toAddr, "fee": fee}
        if chain is not None:
            params["chain"] = chain
        if areaCode is not None:
            params["areaCode"] = areaCode
        if clientId is not None:
            params["clientId"] = clientId
        return await self._client._request_with_params(POST, WITHDRAWAL_COIN, params)

    async def get_deposit_history(
        self,
        ccy: Optional[str] = None,
        type: Optional[str] = None,
        state: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
        txId: Optional[str] = None,
        depId: Optional[str] = None,
        fromWdId: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取充值历史。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return await self._client._request_with_params(GET, DEPOSIT_HISTORY, params)

    async def get_currencies(self, ccy: Optional[str] = None) -> Dict[str, Any]:
        """获取币种列表。"""
        params = {}
        if ccy is not None:
            params["ccy"] = ccy
        return await self._client._request_with_params(GET, CURRENCY_INFO, params)

    async def purchase_redempt(
        self, ccy: str, amt: str, side: str, rate: str
    ) -> Dict[str, Any]:
        """余币宝申购/赎回。"""
        params = {"ccy": ccy, "amt": amt, "side": side, "rate": rate}
        return await self._client._request_with_params(POST, PURCHASE_REDEMPT, params)

    async def get_bills(
        self,
        ccy: Optional[str] = None,
        type: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取资金流水。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return await self._client._request_with_params(GET, BILLS_INFO, params)

    async def get_deposit_lightning(
        self, ccy: str, amt: str, to: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取闪电网络充值信息。"""
        params = {"ccy": ccy, "amt": amt}
        if to is not None:
            params["to"] = to
        return await self._client._request_with_params(GET, DEPOSIT_LIGHTNING, params)

    async def withdrawal_lightning(
        self, ccy: str, invoice: str, memo: Optional[str] = None
    ) -> Dict[str, Any]:
        """闪电网络提币。"""
        params = {"ccy": ccy, "invoice": invoice}
        if memo is not None:
            params["memo"] = memo
        return await self._client._request_with_params(
            POST, WITHDRAWAL_LIGHTNING, params
        )

    async def cancel_withdrawal(self, wdId: str) -> Dict[str, Any]:
        """撤销提币。"""
        params = {"wdId": wdId}
        return await self._client._request_with_params(POST, CANCEL_WITHDRAWAL, params)

    async def convert_dust_assets(self, ccy: List[str]) -> Dict[str, Any]:
        """小额资产兑换。"""
        params = {"ccy": ccy}
        return await self._client._request_with_params(
            POST, CONVERT_DUST_ASSETS, params
        )

    async def get_asset_valuation(self, ccy: Optional[str] = None) -> Dict[str, Any]:
        """获取资产估值。"""
        params = {}
        if ccy is not None:
            params["ccy"] = ccy
        return await self._client._request_with_params(GET, ASSET_VALUATION, params)

    async def get_deposit_withdraw_status(
        self,
        wdId: Optional[str] = None,
        txId: Optional[str] = None,
        ccy: Optional[str] = None,
        to: Optional[str] = None,
        chain: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取充提状态。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return await self._client._request_with_params(
            GET, GET_DEPOSIT_WITHDRAW_STATUS, params
        )

    async def get_withdrawal_history(
        self,
        ccy: Optional[str] = None,
        wdId: Optional[str] = None,
        clientId: Optional[str] = None,
        txId: Optional[str] = None,
        type: Optional[str] = None,
        state: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取提币历史。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return await self._client._request_with_params(GET, WITHDRAWAL_HISTORY, params)
