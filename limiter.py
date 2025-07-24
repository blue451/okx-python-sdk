# okx/limiter.py
import asyncio
import time
import threading
from collections import deque, defaultdict
from typing import Dict, Any, List
from loguru import logger

# 导入所有API路径常量
from okxx import consts as c

# ==============================================================================
# 异步限速器 (Async Version)
# ==============================================================================


class AsyncTokenBucketLimiter:
    """
    一个基于异步的令牌桶速率限制器。
    """

    def __init__(self, rate: int, period_seconds: int, name: str = "default"):
        if rate <= 0 or period_seconds <= 0:
            raise ValueError("Rate and period must be positive.")

        # 按照要求，不使用元组赋值
        self.rate_limit = rate
        self.period = period_seconds
        self.name = name

        self._timestamps = deque()
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            while True:
                now = time.monotonic()
                window_start = now - self.period
                while self._timestamps and self._timestamps[0] <= window_start:
                    self._timestamps.popleft()

                if len(self._timestamps) < self.rate_limit:
                    self._timestamps.append(now)
                    return

                earliest_request_time = self._timestamps[0]
                wait_time = (earliest_request_time + self.period) - now
                if wait_time > 0:
                    logger.trace(
                        f"Async Rate limiter '{self.name}' triggered. Waiting for {wait_time:.3f} seconds."
                    )
                    await asyncio.sleep(wait_time)


# ==============================================================================
# 同步限速器 (Sync Version)
# ==============================================================================


class SyncTokenBucketLimiter:
    """
    一个基于线程安全的同步令牌桶速率限制器。
    """

    def __init__(self, rate: int, period_seconds: int, name: str = "default"):
        if rate <= 0 or period_seconds <= 0:
            raise ValueError("Rate and period must be positive.")

        # 按照要求，不使用元组赋值
        self.rate_limit = rate
        self.period = period_seconds
        self.name = name

        self._timestamps = deque()
        self._lock = threading.Lock()

    def acquire(self):
        with self._lock:
            while True:
                now = time.monotonic()
                window_start = now - self.period
                while self._timestamps and self._timestamps[0] <= window_start:
                    self._timestamps.popleft()

                if len(self._timestamps) < self.rate_limit:
                    self._timestamps.append(now)
                    return

                earliest_request_time = self._timestamps[0]
                wait_time = (earliest_request_time + self.period) - now
                if wait_time > 0:
                    logger.trace(
                        f"Sync Rate limiter '{self.name}' triggered. Waiting for {wait_time:.3f} seconds."
                    )
                    time.sleep(wait_time)


# ==============================================================================
# 通用限速规则配置和管理器
# ==============================================================================


class _RateLimiterConfig:
    """
    OKX V5 REST API 完整限速规则配置中心。
    所有规则均根据官方文档整理，并使用原始的 consts.py 常量名。
    """

    RATE_CONFIGS: Dict[str, Dict[str, Any]] = {
        # === 账户 (Account) ===
        c.ACCOUNT_INFO: {"rate": 10, "period": 2, "key_by": ["user"]},
        c.POSITION_INFO: {"rate": 10, "period": 2, "key_by": ["user"]},
        c.POSITIONS_HISTORY: {"rate": 2, "period": 2, "key_by": ["user"]},
        c.POSITION_RISK: {"rate": 10, "period": 2, "key_by": ["user"]},
        c.BILLS_DETAIL: {"rate": 10, "period": 2, "key_by": ["user"]},
        c.BILLS_ARCHIVE: {
            "rate": 10,
            "period": 2,
            "key_by": ["user"],
        },  # Doc: get-bills-details-since-2021
        c.ACCOUNT_CONFIG: {"rate": 5, "period": 2, "key_by": ["user"]},
        c.POSITION_MODE: {"rate": 5, "period": 2, "key_by": ["user"]},
        c.SET_LEVERAGE: {"rate": 20, "period": 2, "key_by": ["user"]},
        c.MAX_TRADE_SIZE: {"rate": 20, "period": 2, "key_by": ["user", "instId"]},
        c.MAX_AVAIL_SIZE: {"rate": 20, "period": 2, "key_by": ["user", "instId"]},
        c.ADJUSTMENT_MARGIN: {"rate": 20, "period": 2, "key_by": ["user"]},
        c.GET_LEVERAGE: {"rate": 20, "period": 2, "key_by": ["user", "instId"]},
        c.MAX_LOAN: {"rate": 20, "period": 2, "key_by": ["user", "instId"]},
        c.FEE_RATES: {"rate": 5, "period": 2, "key_by": ["user"]},
        c.INTEREST_ACCRUED: {"rate": 5, "period": 2, "key_by": ["user"]},
        c.INTEREST_RATE: {"rate": 5, "period": 2, "key_by": ["user"]},
        c.SET_GREEKS: {"rate": 5, "period": 2, "key_by": ["user"]},
        c.MAX_WITHDRAWAL: {"rate": 10, "period": 2, "key_by": ["user"]},
        c.GET_INSTRUMENTS: {
            "rate": 20,
            "period": 2,
            "key_by": ["user", "instType"],
        },  # account/instruments
        # === 资金 (Asset/Funding) ===
        c.GET_BALANCES: {"rate": 10, "period": 2, "key_by": ["user"]},
        c.FUNDS_TRANSFER: {"rate": 2, "period": 2, "key_by": ["user"]},
        c.TRANSFER_STATE: {"rate": 2, "period": 2, "key_by": ["user"]},
        c.WITHDRAWAL_COIN: {"rate": 10, "period": 2, "key_by": ["user"]},
        c.CANCEL_WITHDRAWAL: {"rate": 10, "period": 2, "key_by": ["user"]},
        c.DEPOSIT_HISTORY: {"rate": 10, "period": 2, "key_by": ["user"]},
        c.WITHDRAWAL_HISTORY: {"rate": 10, "period": 2, "key_by": ["user"]},
        c.CURRENCY_INFO: {"rate": 10, "period": 2, "key_by": ["ip"]},
        c.DEPOSIT_ADDRESS: {"rate": 10, "period": 2, "key_by": ["user"]},
        # === 行情 (Market Data) ===
        c.TICKERS_INFO: {"rate": 20, "period": 2, "key_by": ["ip"]},
        c.TICKER_INFO: {"rate": 20, "period": 2, "key_by": ["ip"]},
        c.INDEX_TICKERS: {"rate": 20, "period": 2, "key_by": ["ip"]},
        c.ORDER_BOOKS: {"rate": 20, "period": 2, "key_by": ["ip"]},
        c.MARKET_CANDLES: {"rate": 40, "period": 2, "key_by": ["ip"]},
        c.HISTORY_CANDLES: {"rate": 20, "period": 2, "key_by": ["ip"]},
        c.INDEX_CANDLES: {"rate": 20, "period": 2, "key_by": ["ip"]},
        c.MARKPRICE_CANDLES: {"rate": 20, "period": 2, "key_by": ["ip"]},
        c.MARKET_TRADES: {"rate": 60, "period": 2, "key_by": ["ip"]},
        c.HISTORY_TRADES: {"rate": 20, "period": 2, "key_by": ["ip"]},
        # === 公共数据 (Public Data) ===
        c.INSTRUMENT_INFO: {
            "rate": 20,
            "period": 2,
            "key_by": ["ip", "instType"],
        },  # public/instruments
        c.OPEN_INTEREST: {"rate": 20, "period": 2, "key_by": ["ip"]},
        c.FUNDING_RATE: {"rate": 20, "period": 2, "key_by": ["ip"]},
        c.FUNDING_RATE_HISTORY: {"rate": 20, "period": 2, "key_by": ["ip"]},
        c.PRICE_LIMIT: {"rate": 20, "period": 2, "key_by": ["ip"]},
        c.OPT_SUMMARY: {"rate": 20, "period": 2, "key_by": ["ip"]},
        c.ESTIMATED_PRICE: {"rate": 10, "period": 2, "key_by": ["ip"]},
        c.SYSTEM_TIME: {"rate": 10, "period": 2, "key_by": ["ip"]},
        c.LIQUIDATION_ORDERS: {"rate": 20, "period": 2, "key_by": ["ip"]},
        c.MARK_PRICE: {"rate": 10, "period": 2, "key_by": ["ip"]},
        c.TIER: {"rate": 10, "period": 2, "key_by": ["ip"]},
        c.STATUS: {"rate": 10, "period": 2, "key_by": ["ip"]},
        # === 交易 (Trade) ===
        c.PLACE_ORDER: {"rate": 60, "period": 2, "key_by": ["user", "instId/family"]},
        c.BATCH_ORDERS: {"rate": 300, "period": 2, "key_by": ["user", "instType"]},
        c.CANCEL_ORDER: {"rate": 60, "period": 2, "key_by": ["user", "instId"]},
        c.CANCEL_BATCH_ORDERS: {
            "rate": 300,
            "period": 2,
            "key_by": ["user", "instType"],
        },
        c.AMEND_ORDER: {"rate": 60, "period": 2, "key_by": ["user", "instId"]},
        c.AMEND_BATCH_ORDER: {"rate": 300, "period": 2, "key_by": ["user", "instType"]},
        c.CLOSE_POSITION: {"rate": 20, "period": 2, "key_by": ["user", "mgnMode"]},
        c.ORDER_INFO: {"rate": 60, "period": 2, "key_by": ["user", "instId"]},
        c.ORDERS_PENDING: {"rate": 20, "period": 2, "key_by": ["user"]},
        c.ORDERS_HISTORY: {"rate": 40, "period": 2, "key_by": ["user"]},
        c.ORDERS_HISTORY_ARCHIVE: {"rate": 10, "period": 2, "key_by": ["user"]},
        c.ORDER_FILLS: {"rate": 20, "period": 2, "key_by": ["user"]},
        # === 子账户 (SubAccount) ===
        c.VIEW_LIST: {"rate": 2, "period": 2, "key_by": ["user"]},
        c.RESET: {"rate": 2, "period": 2, "key_by": ["user"]},
        c.BALANCE: {"rate": 10, "period": 2, "key_by": ["user"]},  # trading balance
        c.GET_ASSET_SUBACCOUNT_BALANCE: {
            "rate": 2,
            "period": 2,
            "key_by": ["user"],
        },  # funding balance
        c.BILLs: {"rate": 2, "period": 2, "key_by": ["user"]},
        c.SUBACCOUNT_TRANSFER: {"rate": 2, "period": 2, "key_by": ["user"]},
    }


def _build_dynamic_key(config: Dict, params: Dict, api_key: str) -> str:
    """通用函数：根据配置和请求上下文构建动态键"""
    key_parts: List[str] = []
    if "instId/family" in config["key_by"]:
        key_parts.append(api_key if "user" in config["key_by"] else "ip_shared")
        inst_id = params.get("instId", "")
        if "-C-" in inst_id or "-P-" in inst_id:
            inst_family = params.get("instFamily")
            if inst_family:
                key_parts.append(inst_family)
            else:
                try:
                    key_parts.append(inst_id.rsplit("-", 3)[0])
                except IndexError:
                    key_parts.append(inst_id)
        else:
            key_parts.append(inst_id)
        return ":".join(key_parts)
    for key_component in config["key_by"]:
        if key_component == "user":
            key_parts.append(api_key if api_key != "-1" else "public_user")
        elif key_component == "ip":
            key_parts.append("ip_shared")
        else:
            key_parts.append(str(params.get(key_component, "None")))
    return ":".join(key_parts)


class RateLimiterManager:
    """通用限速管理器基类"""

    def __init__(self):
        self._rate_configs = _RateLimiterConfig.RATE_CONFIGS


class AsyncRateLimiterManager(RateLimiterManager):
    """异步版本"""

    def __init__(self):
        super().__init__()
        self._limiters: Dict[str, Dict[str, AsyncTokenBucketLimiter]] = defaultdict(
            dict
        )
        self._lock = asyncio.Lock()

    async def acquire(self, request_path: str, params: Dict, api_key: str):
        config = self._rate_configs.get(request_path)
        if not config:
            return
        dynamic_key = _build_dynamic_key(config, params, api_key)
        if dynamic_key not in self._limiters[request_path]:
            async with self._lock:
                if dynamic_key not in self._limiters[request_path]:
                    rate = config["rate"]
                    period = config["period"]
                    limiter_name = f"{request_path}::{dynamic_key}"
                    self._limiters[request_path][dynamic_key] = AsyncTokenBucketLimiter(
                        rate, period, name=limiter_name
                    )
        limiter = self._limiters[request_path][dynamic_key]
        if limiter:
            await limiter.acquire()


class SyncRateLimiterManager(RateLimiterManager):
    """同步版本"""

    def __init__(self):
        super().__init__()
        self._limiters: Dict[str, Dict[str, SyncTokenBucketLimiter]] = defaultdict(dict)
        self._lock = threading.Lock()

    def acquire(self, request_path: str, params: Dict, api_key: str):
        config = self._rate_configs.get(request_path)
        if not config:
            return
        dynamic_key = _build_dynamic_key(config, params, api_key)
        if dynamic_key not in self._limiters[request_path]:
            with self._lock:
                if dynamic_key not in self._limiters[request_path]:
                    rate = config["rate"]
                    period = config["period"]
                    limiter_name = f"{request_path}::{dynamic_key}"
                    self._limiters[request_path][dynamic_key] = SyncTokenBucketLimiter(
                        rate, period, name=limiter_name
                    )
        limiter = self._limiters[request_path][dynamic_key]
        if limiter:
            limiter.acquire()
