# okx/rest/Account.py
from typing import Optional, List, Dict, Any
from okxx.consts import *


class AccountAPI:
    """
    封装了账户相关的API。
    """

    def __init__(self, client):
        self._client = client

    def get_position_risk(self, instType: Optional[str] = None) -> Dict[str, Any]:
        """获取账户的仓位风险信息。"""
        params = {}
        if instType:
            params["instType"] = instType
        return self._client._request_with_params(GET, POSITION_RISK, params)

    def get_account_balance(self, ccy: Optional[str] = None) -> Dict[str, Any]:
        """获取账户余额信息。"""
        params = {}
        if ccy:
            params["ccy"] = ccy
        return self._client._request_with_params(GET, ACCOUNT_INFO, params)

    def get_positions(
        self, instType: Optional[str] = None, instId: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取持仓信息。"""
        params = {}
        if instType:
            params["instType"] = instType
        if instId:
            params["instId"] = instId
        return self._client._request_with_params(GET, POSITION_INFO, params)

    def get_account_bills(
        self,
        instType: Optional[str] = None,
        ccy: Optional[str] = None,
        mgnMode: Optional[str] = None,
        ctType: Optional[str] = None,
        type: Optional[str] = None,
        subType: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取最近7天的账单流水。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, BILLS_DETAIL, params)

    def get_account_bills_archive(
        self,
        instType: Optional[str] = None,
        ccy: Optional[str] = None,
        mgnMode: Optional[str] = None,
        ctType: Optional[str] = None,
        type: Optional[str] = None,
        subType: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
        begin: Optional[str] = None,
        end: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取最近3个月的账单流水。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, BILLS_ARCHIVE, params)

    def get_account_config(self) -> Dict[str, Any]:
        """获取账户配置。"""
        return self._client._request_without_params(GET, ACCOUNT_CONFIG)

    def set_position_mode(self, posMode: str) -> Dict[str, Any]:
        """设置持仓模式。"""
        params = {"posMode": posMode}
        return self._client._request_with_params(POST, POSITION_MODE, params)

    def set_leverage(
        self,
        lever: str,
        mgnMode: str,
        instId: Optional[str] = None,
        ccy: Optional[str] = None,
        posSide: Optional[str] = None,
    ) -> Dict[str, Any]:
        """设置杠杆倍数。"""
        params = {"lever": lever, "mgnMode": mgnMode}
        if instId:
            params["instId"] = instId
        if ccy:
            params["ccy"] = ccy
        if posSide:
            params["posSide"] = posSide
        return self._client._request_with_params(POST, SET_LEVERAGE, params)

    def get_max_order_size(
        self,
        instId: str,
        tdMode: str,
        ccy: Optional[str] = None,
        px: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取最大可买卖数量。"""
        params = {"instId": instId, "tdMode": tdMode}
        if ccy:
            params["ccy"] = ccy
        if px:
            params["px"] = px
        return self._client._request_with_params(GET, MAX_TRADE_SIZE, params)

    def get_max_avail_size(
        self,
        instId: str,
        tdMode: str,
        ccy: Optional[str] = None,
        reduceOnly: Optional[str] = None,
        unSpotOffset: Optional[str] = None,
        quickMgnType: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取最大可用数量。

        Args:
            instId: 产品ID，如 BTC-USDT
            tdMode: 交易模式 cross：全仓 isolated：逐仓 cash：非保证金 spot_isolated：现货逐仓
            ccy: 保证金币种，适用于逐仓杠杆及合约模式下的全仓杠杆
            reduceOnly: 是否为只减仓模式，仅适用于币币杠杆 ("true"/"false")
            unSpotOffset: 现货对冲数量 ("true"/"false")
            quickMgnType: 一键借币类型 manual：手动，auto_borrow：自动借币，auto_repay：自动还币
        """
        params = {"instId": instId, "tdMode": tdMode}
        if ccy:
            params["ccy"] = ccy
        if reduceOnly:
            params["reduceOnly"] = reduceOnly
        if unSpotOffset:
            params["unSpotOffset"] = unSpotOffset
        if quickMgnType:
            params["quickMgnType"] = quickMgnType
        return self._client._request_with_params(GET, MAX_AVAIL_SIZE, params)

    def adjustment_margin(
        self,
        instId: str,
        posSide: str,
        type: str,
        amt: str,
        loanTrans: Optional[str] = None,
    ) -> Dict[str, Any]:
        """增加或减少保证金。

        Args:
            instId: 产品ID
            posSide: 持仓方向
            type: 增加或减少保证金
            amt: 保证金数量
            loanTrans: 是否支持跨币种保证金模式或组合保证金模式 ("true"/"false")
        """
        params = {"instId": instId, "posSide": posSide, "type": type, "amt": amt}
        if loanTrans:
            params["loanTrans"] = loanTrans
        return self._client._request_with_params(POST, ADJUSTMENT_MARGIN, params)

    def get_leverage(
        self, mgnMode: str, ccy: Optional[str] = None, instId: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取杠杆倍数。"""
        params = {"mgnMode": mgnMode}
        if ccy:
            params["ccy"] = ccy
        if instId:
            params["instId"] = instId
        return self._client._request_with_params(GET, GET_LEVERAGE, params)

    def get_max_loan(
        self, instId: str, mgnMode: str, mgnCcy: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取最大可借币量。"""
        params = {"instId": instId, "mgnMode": mgnMode}
        if mgnCcy:
            params["mgnCcy"] = mgnCcy
        return self._client._request_with_params(GET, MAX_LOAN, params)

    def get_fee_rates(
        self,
        instType: str,
        instId: Optional[str] = None,
        uly: Optional[str] = None,
        category: Optional[str] = None,
        instFamily: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取手续费率。"""
        params = {"instType": instType}
        if instId:
            params["instId"] = instId
        if uly:
            params["uly"] = uly
        if category:
            params["category"] = category
        if instFamily:
            params["instFamily"] = instFamily
        return self._client._request_with_params(GET, FEE_RATES, params)

    def get_interest_accrued(
        self,
        instId: Optional[str] = None,
        ccy: Optional[str] = None,
        mgnMode: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取计息记录。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, INTEREST_ACCRUED, params)

    def get_interest_rate(self, ccy: Optional[str] = None) -> Dict[str, Any]:
        """获取借币利率。"""
        params = {}
        if ccy:
            params["ccy"] = ccy
        return self._client._request_with_params(GET, INTEREST_RATE, params)

    def set_greeks(self, greeksType: str) -> Dict[str, Any]:
        """设置希腊字母展示方式。"""
        params = {"greeksType": greeksType}
        return self._client._request_with_params(POST, SET_GREEKS, params)

    def set_isolated_mode(self, isoMode: str, type: str) -> Dict[str, Any]:
        """设置逐仓交易模式。"""
        params = {"isoMode": isoMode, "type": type}
        return self._client._request_with_params(POST, SET_ISOLATED_MODE, params)

    def get_max_withdrawal(self, ccy: Optional[str] = None) -> Dict[str, Any]:
        """获取最大可提币量。"""
        params = {}
        if ccy:
            params["ccy"] = ccy
        return self._client._request_with_params(GET, MAX_WITHDRAWAL, params)

    def borrow_repay(
        self, ccy: str, side: str, amt: str, ordId: Optional[str] = None
    ) -> Dict[str, Any]:
        """资金借还。"""
        params = {"ccy": ccy, "side": side, "amt": amt}
        if ordId:
            params["ordId"] = ordId
        return self._client._request_with_params(POST, BORROW_REPAY, params)

    def get_borrow_repay_history(
        self,
        ccy: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取借还历史记录。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, BORROW_REPAY_HISTORY, params)

    def get_interest_limits(
        self, type: str, ccy: Optional[str] = None
    ) -> Dict[str, Any]:
        """获取尊享借币利率和借币限额。"""
        params = {"type": type}
        if ccy:
            params["ccy"] = ccy
        return self._client._request_with_params(GET, INTEREST_LIMITS, params)

    def get_simulated_margin(
        self,
        instType: Optional[str] = None,
        inclRealPos: Optional[str] = None,
        spotOffsetType: Optional[str] = None,
        simPos: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """获取模拟保证金。

        Args:
            instType: 产品类型
            inclRealPos: 是否包含真实持仓 ("true"/"false")
            spotOffsetType: 现货对冲类型
            simPos: 模拟持仓列表
        """
        params = {}
        if instType:
            params["instType"] = instType
        if inclRealPos:
            params["inclRealPos"] = inclRealPos
        if spotOffsetType:
            params["spotOffsetType"] = spotOffsetType
        if simPos:
            params["simPos"] = simPos
        return self._client._request_with_params(POST, SIMULATED_MARGIN, params)

    def get_greeks(self, ccy: Optional[str] = None) -> Dict[str, Any]:
        """获取希腊字母。"""
        params = {}
        if ccy:
            params["ccy"] = ccy
        return self._client._request_with_params(GET, GREEKS, params)

    def get_account_position_risk(self) -> Dict[str, Any]:
        """获取账户仓位风险。"""
        return self._client._request_without_params(GET, ACCOUNT_RISK)

    def get_positions_history(
        self,
        instType: Optional[str] = None,
        instId: Optional[str] = None,
        mgnMode: Optional[str] = None,
        type: Optional[str] = None,
        posId: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取仓位历史记录。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, POSITIONS_HISTORY, params)

    def get_account_position_tiers(
        self,
        instType: Optional[str] = None,
        uly: Optional[str] = None,
        instFamily: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取账户仓位等级。"""
        params = {}
        if instType:
            params["instType"] = instType
        if uly:
            params["uly"] = uly
        if instFamily:
            params["instFamily"] = instFamily
        return self._client._request_with_params(GET, GET_PM_LIMIT, params)

    def get_vip_interest_accrued_data(
        self,
        ccy: Optional[str] = None,
        ordId: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取VIP借币计息记录。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(
            GET, GET_VIP_INTEREST_ACCRUED_DATA, params
        )

    def get_vip_interest_deducted_data(
        self,
        ccy: Optional[str] = None,
        ordId: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取VIP借币扣息记录。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(
            GET, GET_VIP_INTEREST_DEDUCTED_DATA, params
        )

    def get_vip_loan_order_list(
        self,
        ordId: Optional[str] = None,
        state: Optional[str] = None,
        ccy: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取VIP借币订单列表。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, GET_VIP_LOAN_ORDER_LIST, params)

    def get_vip_loan_order_detail(
        self,
        ccy: Optional[str] = None,
        ordId: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取VIP借币订单详情。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, GET_VIP_LOAN_ORDER_DETAIL, params)

    def set_risk_offset_type(self, type: str) -> Dict[str, Any]:
        """设置风险对冲类型。"""
        params = {"type": type}
        return self._client._request_with_params(POST, SET_RISK_OFFSET_TYPE, params)

    def set_auto_loan(self, autoLoan: str) -> Dict[str, Any]:
        """设置自动借币。"""
        params = {"autoLoan": autoLoan}
        return self._client._request_with_params(POST, SET_AUTO_LOAN, params)

    def set_account_level(self, acctLv: str) -> Dict[str, Any]:
        """设置账户等级。"""
        params = {"acctLv": acctLv}
        return self._client._request_with_params(POST, SET_ACCOUNT_LEVEL, params)

    def activate_option(self) -> Dict[str, Any]:
        """开通期权。"""
        return self._client._request_without_params(POST, ACTIVATE_OPTION)

    def get_fixed_loan_borrowing_limit(self) -> Dict[str, Any]:
        """获取定期借款额度。"""
        return self._client._request_without_params(GET, BORROWING_LIMIT)

    def get_fixed_loan_borrowing_quote(
        self,
        type: Optional[str] = None,
        ccy: Optional[str] = None,
        amt: Optional[str] = None,
        maxRate: Optional[str] = None,
        term: Optional[str] = None,
        ordId: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取定期借款报价。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, BORROWING_QUOTE, params)

    def place_fixed_loan_borrowing_order(
        self,
        ccy: str,
        amt: str,
        maxRate: str,
        term: str,
        reborrow: Optional[str] = None,
        reborrowRate: Optional[str] = None,
    ) -> Dict[str, Any]:
        """下单定期借款。

        Args:
            ccy: 借币币种
            amt: 借币数量
            maxRate: 最大利率
            term: 借币期限
            reborrow: 是否自动续借 ("true"/"false")
            reborrowRate: 续借利率
        """
        params = {"ccy": ccy, "amt": amt, "maxRate": maxRate, "term": term}
        if reborrow:
            params["reborrow"] = reborrow
        if reborrowRate:
            params["reborrowRate"] = reborrowRate
        return self._client._request_with_params(POST, PLACE_BORROWING_ORDER, params)

    def amend_fixed_loan_borrowing_order(
        self,
        ordId: str,
        reborrow: Optional[str] = None,
        renewMaxRate: Optional[str] = None,
    ) -> Dict[str, Any]:
        """修改定期借款订单。

        Args:
            ordId: 订单ID
            reborrow: 是否自动续借 ("true"/"false")
            renewMaxRate: 续借最大利率
        """
        params = {"ordId": ordId}
        if reborrow:
            params["reborrow"] = reborrow
        if renewMaxRate:
            params["renewMaxRate"] = renewMaxRate
        return self._client._request_with_params(POST, AMEND_BORROWING_ORDER, params)

    def fixed_loan_manual_reborrow(
        self, ordId: str, maxRate: Optional[str] = None
    ) -> Dict[str, Any]:
        """手动续借。"""
        params = {"ordId": ordId}
        if maxRate:
            params["maxRate"] = maxRate
        return self._client._request_with_params(POST, MANUAL_REBORROW, params)

    def repay_fixed_loan_borrowing_order(self, ordId: str) -> Dict[str, Any]:
        """归还定期借款。"""
        params = {"ordId": ordId}
        return self._client._request_with_params(POST, REPAY_BORROWING_ORDER, params)

    def get_fixed_loan_borrowing_orders_list(
        self,
        ordId: Optional[str] = None,
        ccy: Optional[str] = None,
        state: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取定期借款订单列表。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, BORROWING_ORDERS_LIST, params)

    def spot_manual_borrow_repay(self, ccy: str, side: str, amt: str) -> Dict[str, Any]:
        """现货手动借还。"""
        params = {"ccy": ccy, "side": side, "amt": amt}
        return self._client._request_with_params(POST, MANUAL_BORROW_REPAY, params)

    def set_auto_repay(self, autoRepay: str) -> Dict[str, Any]:
        """设置自动还款。

        Args:
            autoRepay: 是否自动还款 ("true"/"false")
        """
        params = {"autoRepay": autoRepay}
        return self._client._request_with_params(POST, SET_AUTO_REPAY, params)

    def get_spot_borrow_repay_history(
        self,
        ccy: Optional[str] = None,
        type: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """获取现货借还历史。"""
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, GET_BORROW_REPAY_HISTORY, params)
