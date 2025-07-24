# okx/rest/Finance.py
from okxx.consts import *


class FinanceAPI:
    """
    封装了金融服务相关的API，包括赚币、借贷、质押等。
    """

    def __init__(self, client):
        self._client = client

    # =================
    # Staking / DeFi
    # =================

    def get_defi_offers(self, productId="", protocolType="", ccy=""):
        params = {"productId": productId, "protocolType": protocolType, "ccy": ccy}
        return self._client._request_with_params(GET, STACK_DEFI_OFFERS, params)

    def defi_purchase(self, productId="", investData=[], term="", tag=""):
        params = {"productId": productId, "investData": investData}
        if term:
            params["term"] = term
        if tag:
            params["tag"] = tag
        return self._client._request_with_params(POST, STACK_DEFI_PURCHASE, params)

    def defi_redeem(self, ordId="", protocolType="", allowEarlyRedeem=""):
        params = {
            "ordId": ordId,
            "protocolType": protocolType,
            "allowEarlyRedeem": allowEarlyRedeem,
        }
        return self._client._request_with_params(POST, STACK_DEFI_REDEEM, params)

    def defi_cancel(self, ordId="", protocolType=""):
        params = {"ordId": ordId, "protocolType": protocolType}
        return self._client._request_with_params(POST, STACK_DEFI_CANCEL, params)

    def get_defi_active_orders(self, productId="", protocolType="", ccy="", state=""):
        params = {
            "productId": productId,
            "protocolType": protocolType,
            "ccy": ccy,
            "state": state,
        }
        return self._client._request_with_params(
            GET, STACK_DEFI_ORDERS_ACTIVITY, params
        )

    def get_defi_orders_history(
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
        return self._client._request_with_params(GET, STACK_DEFI_ORDERS_HISTORY, params)

    # =================
    # ETH Staking
    # =================

    def get_eth_product_info(self):
        return self._client._request_without_params(GET, STACK_ETH_PRODUCT_INFO)

    def eth_purchase(self, amt=""):
        params = {"amt": amt}
        return self._client._request_with_params(POST, STACK_ETH_PURCHASE, params)

    def eth_redeem(self, amt=""):
        params = {"amt": amt}
        return self._client._request_with_params(POST, STACK_ETH_REDEEM, params)

    def get_eth_balance(self):
        return self._client._request_without_params(GET, STACK_ETH_BALANCE)

    def get_eth_purchase_redeem_history(
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
        return self._client._request_with_params(
            GET, STACK_ETH_PURCHASE_REDEEM_HISTORY, params
        )

    def get_eth_apy_history(self, days):
        params = {"days": days}
        return self._client._request_with_params(GET, STACK_ETH_APY_HISTORY, params)

    # =================
    # SOL Staking
    # =================

    def sol_purchase(self, amt):
        params = {"amt": amt}
        return self._client._request_with_params(POST, STACK_SOL_PURCHASE, params)

    def sol_redeem(self, amt=""):
        params = {"amt": amt}
        return self._client._request_with_params(POST, STACK_SOL_REDEEM, params)

    def get_sol_balance(self):
        return self._client._request_without_params(GET, STACK_SOL_BALANCE)

    def get_sol_purchase_redeem_history(
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
        return self._client._request_with_params(
            GET, STACK_SOL_PURCHASE_REDEEM_HISTORY, params
        )

    def get_sol_apy_history(self, days):
        params = {"days": days}
        return self._client._request_with_params(GET, STACK_SOL_APY_HISTORY, params)

    # =================
    # Savings (Simple Earn)
    # =================

    def get_saving_balance(self, ccy=""):
        params = {"ccy": ccy}
        return self._client._request_with_params(GET, GET_SAVING_BALANCE, params)

    def savings_purchase_redemption(self, ccy="", amt="", side="", rate=""):
        params = {"ccy": ccy, "amt": amt, "side": side, "rate": rate}
        return self._client._request_with_params(
            POST, SAVING_PURCHASE_REDEMPTION, params
        )

    def set_lending_rate(self, ccy="", rate=""):
        params = {"ccy": ccy, "rate": rate}
        return self._client._request_with_params(POST, SET_LENDING_RATE, params)

    def get_lending_history(self, ccy="", after="", before="", limit=""):
        params = {"ccy": ccy, "after": after, "before": before, "limit": limit}
        return self._client._request_with_params(GET, GET_LENDING_HISTORY, params)

    def get_public_borrow_info(self, ccy=""):
        params = {"ccy": ccy}
        return self._client._request_with_params(GET, GET_PUBLIC_BORROW_INFO, params)

    def get_public_borrow_history(self, ccy="", after="", before="", limit=""):
        params = {"ccy": ccy, "after": after, "before": before, "limit": limit}
        return self._client._request_with_params(GET, GET_PUBLIC_BORROW_HISTORY, params)

    # =================
    # Flexible Loan
    # =================

    def get_loan_currencies(self):
        return self._client._request_without_params(GET, FINANCE_BORROW_CURRENCIES)

    def get_collateral_assets(self, ccy=""):
        params = {}
        if ccy:
            params["ccy"] = ccy
        return self._client._request_with_params(GET, FINANCE_COLLATERAL_ASSETS, params)

    def get_max_loan(self, borrowCcy="", supCollateral=[]):
        params = {
            "borrowCcy": borrowCcy,
            "supCollateral": supCollateral,
        }
        return self._client._request_with_params(POST, FINANCE_MAX_LOAN, params)

    def get_max_collateral_redeem_amount(self, ccy=""):
        params = {}
        if ccy:
            params["ccy"] = ccy
        return self._client._request_with_params(GET, FINANCE_MAX_REDEEM, params)

    def adjust_collateral(self, type="", collateralCcy="", collateralAmt=""):
        params = {
            "type": type,
            "collateralCcy": collateralCcy,
            "collateralAmt": collateralAmt,
        }
        return self._client._request_with_params(
            POST, FINANCE_ADJUST_COLLATERAL, params
        )

    def get_loan_info(self):
        return self._client._request_without_params(GET, FINANCE_LOAN_INFO)

    def get_loan_history(self, type="", after="", before="", limit=""):
        params = {}
        if type:
            params["type"] = type
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if limit:
            params["limit"] = limit
        return self._client._request_with_params(GET, FINANCE_LOAN_HISTORY, params)

    def get_interest_accrued(self, ccy="", after="", before="", limit=""):
        params = {}
        if ccy:
            params["ccy"] = ccy
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if limit:
            params["limit"] = limit
        return self._client._request_with_params(GET, FINANCE_INTEREST_ACCRUED, params)
