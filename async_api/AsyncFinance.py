# okx/async_api/AsyncFinance.py
from okxx.consts import *


class AsyncFinanceAPI:
    """
    封装了金融服务相关的API的异步版本。
    """

    def __init__(self, client):
        self._client = client

    # =================
    # Staking / DeFi
    # =================

    async def get_defi_offers(self, productId="", protocolType="", ccy=""):
        params = {"productId": productId, "protocolType": protocolType, "ccy": ccy}
        return await self._client._request_with_params(GET, STACK_DEFI_OFFERS, params)

    async def defi_purchase(self, productId="", investData=[], term="", tag=""):
        params = {"productId": productId, "investData": investData}
        if term:
            params["term"] = term
        if tag:
            params["tag"] = tag
        return await self._client._request_with_params(
            POST, STACK_DEFI_PURCHASE, params
        )

    async def defi_redeem(self, ordId="", protocolType="", allowEarlyRedeem=""):
        params = {
            "ordId": ordId,
            "protocolType": protocolType,
            "allowEarlyRedeem": allowEarlyRedeem,
        }
        return await self._client._request_with_params(POST, STACK_DEFI_REDEEM, params)

    async def defi_cancel(self, ordId="", protocolType=""):
        params = {"ordId": ordId, "protocolType": protocolType}
        return await self._client._request_with_params(POST, STACK_DEFI_CANCEL, params)

    async def get_defi_active_orders(
        self, productId="", protocolType="", ccy="", state=""
    ):
        params = {
            "productId": productId,
            "protocolType": protocolType,
            "ccy": ccy,
            "state": state,
        }
        return await self._client._request_with_params(
            GET, STACK_DEFI_ORDERS_ACTIVITY, params
        )

    async def get_defi_orders_history(
        self, productId="", protocolType="", ccy="", after="", before="", limit=""
    ):
        params = {
            "productId": productId,
            "protocolType": protocolType,
            "ccy": ccy,
            "after": after,
            "before": before,
            "limit": limit,
        }
        return await self._client._request_with_params(
            GET, STACK_DEFI_ORDERS_HISTORY, params
        )

    # =================
    # ETH Staking
    # =================

    async def get_eth_product_info(self):
        return await self._client._request_without_params(GET, STACK_ETH_PRODUCT_INFO)

    async def eth_purchase(self, amt=""):
        params = {"amt": amt}
        return await self._client._request_with_params(POST, STACK_ETH_PURCHASE, params)

    async def eth_redeem(self, amt=""):
        params = {"amt": amt}
        return await self._client._request_with_params(POST, STACK_ETH_REDEEM, params)

    async def get_eth_balance(self):
        return await self._client._request_without_params(GET, STACK_ETH_BALANCE)

    async def get_eth_purchase_redeem_history(
        self, type="", status="", after="", before="", limit=""
    ):
        params = {}
        if type:
            params["type"] = type
        if status:
            params["status"] = status
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if limit:
            params["limit"] = limit
        return await self._client._request_with_params(
            GET, STACK_ETH_PURCHASE_REDEEM_HISTORY, params
        )

    async def get_eth_apy_history(self, days):
        params = {"days": days}
        return await self._client._request_with_params(
            GET, STACK_ETH_APY_HISTORY, params
        )

    # =================
    # SOL Staking
    # =================

    async def sol_purchase(self, amt):
        params = {"amt": amt}
        return await self._client._request_with_params(POST, STACK_SOL_PURCHASE, params)

    async def sol_redeem(self, amt=""):
        params = {"amt": amt}
        return await self._client._request_with_params(POST, STACK_SOL_REDEEM, params)

    async def get_sol_balance(self):
        return await self._client._request_without_params(GET, STACK_SOL_BALANCE)

    async def get_sol_purchase_redeem_history(
        self, type="", status="", after="", before="", limit=""
    ):
        params = {}
        if type:
            params["type"] = type
        if status:
            params["status"] = status
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if limit:
            params["limit"] = limit
        return await self._client._request_with_params(
            GET, STACK_SOL_PURCHASE_REDEEM_HISTORY, params
        )

    async def get_sol_apy_history(self, days):
        params = {"days": days}
        return await self._client._request_with_params(
            GET, STACK_SOL_APY_HISTORY, params
        )

    # =================
    # Savings (Simple Earn)
    # =================

    async def get_saving_balance(self, ccy=""):
        params = {"ccy": ccy}
        return await self._client._request_with_params(GET, GET_SAVING_BALANCE, params)

    async def savings_purchase_redemption(self, ccy="", amt="", side="", rate=""):
        params = {"ccy": ccy, "amt": amt, "side": side, "rate": rate}
        return await self._client._request_with_params(
            POST, SAVING_PURCHASE_REDEMPTION, params
        )

    async def set_lending_rate(self, ccy="", rate=""):
        params = {"ccy": ccy, "rate": rate}
        return await self._client._request_with_params(POST, SET_LENDING_RATE, params)

    async def get_lending_history(self, ccy="", after="", before="", limit=""):
        params = {"ccy": ccy, "after": after, "before": before, "limit": limit}
        return await self._client._request_with_params(GET, GET_LENDING_HISTORY, params)

    async def get_public_borrow_info(self, ccy=""):
        params = {"ccy": ccy}
        return await self._client._request_with_params(
            GET, GET_PUBLIC_BORROW_INFO, params
        )

    async def get_public_borrow_history(self, ccy="", after="", before="", limit=""):
        params = {"ccy": ccy, "after": after, "before": before, "limit": limit}
        return await self._client._request_with_params(
            GET, GET_PUBLIC_BORROW_HISTORY, params
        )

    # =================
    # Flexible Loan
    # =================

    async def get_loan_currencies(self):
        return await self._client._request_without_params(
            GET, FINANCE_BORROW_CURRENCIES
        )

    async def get_collateral_assets(self, ccy=""):
        params = {}
        if ccy:
            params["ccy"] = ccy
        return await self._client._request_with_params(
            GET, FINANCE_COLLATERAL_ASSETS, params
        )

    async def get_max_loan(self, borrowCcy="", supCollateral=[]):
        params = {
            "borrowCcy": borrowCcy,
            "supCollateral": supCollateral,
        }
        return await self._client._request_with_params(POST, FINANCE_MAX_LOAN, params)

    async def get_max_collateral_redeem_amount(self, ccy=""):
        params = {}
        if ccy:
            params["ccy"] = ccy
        return await self._client._request_with_params(GET, FINANCE_MAX_REDEEM, params)

    async def adjust_collateral(self, type="", collateralCcy="", collateralAmt=""):
        params = {
            "type": type,
            "collateralCcy": collateralCcy,
            "collateralAmt": collateralAmt,
        }
        return await self._client._request_with_params(
            POST, FINANCE_ADJUST_COLLATERAL, params
        )

    async def get_loan_info(self):
        return await self._client._request_without_params(GET, FINANCE_LOAN_INFO)

    async def get_loan_history(self, type="", after="", before="", limit=""):
        params = {}
        if type:
            params["type"] = type
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if limit:
            params["limit"] = limit
        return await self._client._request_with_params(
            GET, FINANCE_LOAN_HISTORY, params
        )

    async def get_interest_accrued(self, ccy="", after="", before="", limit=""):
        params = {}
        if ccy:
            params["ccy"] = ccy
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if limit:
            params["limit"] = limit
        return await self._client._request_with_params(
            GET, FINANCE_INTEREST_ACCRUED, params
        )
