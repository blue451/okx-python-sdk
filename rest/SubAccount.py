# okx/rest/SubAccount.py
from typing import Optional, List, Dict, Any
from okx.consts import *

class SubAccountAPI:
    """
    封装了子账户相关的API。
    """

    def __init__(self, client):
        self._client = client

    def get_account_balance(self, subAcct: str) -> Dict[str, Any]:
        """获取子账户余额。"""
        params = {"subAcct": subAcct}
        return self._client._request_with_params(GET, BALANCE, params)

    def get_bills(self, ccy: Optional[str] = None, type: Optional[str] = None, subAcct: Optional[str] = None, after: Optional[str] = None, before: Optional[str] = None, limit: Optional[str] = None) -> Dict[str, Any]:
        """获取子账户账单流水。"""
        params = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return self._client._request_with_params(GET, BILLS, params)

    def reset_subaccount_apikey(self, subAcct: str, apiKey: str, label: Optional[str] = None, perm: Optional[str] = None, ip: Optional[str] = None) -> Dict[str, Any]:
        """重置子账户APIKey。"""
        params = {"subAcct": subAcct, "apiKey": apiKey}
        if label is not None:
            params["label"] = label
        if perm is not None:
            params["perm"] = perm
        if ip is not None:
            params["ip"] = ip
        return self._client._request_with_params(POST, RESET, params)

    def get_subaccount_list(self, enable: Optional[str] = None, subAcct: Optional[str] = None, after: Optional[str] = None, before: Optional[str] = None, limit: Optional[str] = None) -> Dict[str, Any]:
        """获取子账户列表。"""
        params = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return self._client._request_with_params(GET, VIEW_LIST, params)

    def sub_account_transfer(self, ccy: str, amt: str, froms: str, to: str, fromSubAccount: str, toSubAccount: str, loanTrans: Optional[bool] = None, omitPosRisk: Optional[bool] = None) -> Dict[str, Any]:
        """子账户资金划转。"""
        params = {
            "ccy": ccy,
            "amt": amt,
            "from": froms,
            "to": to,
            "fromSubAccount": fromSubAccount,
            "toSubAccount": toSubAccount,
        }
        if loanTrans is not None:
            params["loanTrans"] = loanTrans
        if omitPosRisk is not None:
            params["omitPosRisk"] = omitPosRisk
        return self._client._request_with_params(POST, SUBACCOUNT_TRANSFER, params)

    def get_entrust_subaccount_list(self, subAcct: Optional[str] = None) -> Dict[str, Any]:
        """获取托管子账户列表。"""
        params = {}
        if subAcct is not None:
            params["subAcct"] = subAcct
        return self._client._request_with_params(GET, ENTRUST_SUBACCOUNT_LIST, params)

    def set_permission_transfer_out(self, subAcct: str, canTransOut: bool) -> Dict[str, Any]:
        """设置子账户转出权限。"""
        params = {"subAcct": subAcct, "canTransOut": canTransOut}
        return self._client._request_with_params(POST, SET_TRANSFER_OUT, params)

    def get_funding_balance(self, subAcct: Optional[str] = None, ccy: Optional[str] = None) -> Dict[str, Any]:
        """获取子账户资金余额。"""
        params = {}
        if subAcct is not None:
            params["subAcct"] = subAcct
        if ccy is not None:
            params["ccy"] = ccy
        return self._client._request_with_params(GET, GET_ASSET_SUBACCOUNT_BALANCE, params)

    def set_sub_accounts_vip_loan(self, enable: bool, alloc: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """设置子账户VIP借币额度。"""
        params = {"enable": enable}
        if alloc is not None:
            params["alloc"] = alloc
        return self._client._request_with_params(POST, SET_SUB_ACCOUNTS_VIP_LOAN, params)

    def get_sub_account_borrow_interest_and_limit(self, subAcct: Optional[str] = None, ccy: Optional[str] = None) -> Dict[str, Any]:
        """获取子账户借币利息和限额。"""
        params = {}
        if subAcct is not None:
            params["subAcct"] = subAcct
        if ccy is not None:
            params["ccy"] = ccy
        return self._client._request_with_params(GET, GET_SUB_ACCOUNT_BORROW_INTEREST_AND_LIMIT, params)
