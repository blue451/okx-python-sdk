from typing import Optional, Dict, Any
from okxx.consts import *


class MarketAPI:
    """
    封装了市场行情数据相关的API。
    这些通常是公开数据接口，无需API Key即可调用。
    """

    def __init__(self, client):
        """
        初始化
        :param client: 一个 OkxClient 实例
        """
        self._client = client

    def get_tickers(
        self, instType: str, uly: Optional[str] = None, instFamily: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取所有产品行情信息。

        Args:
            instType (str): 产品类型。
            uly (Optional[str]): 标的指数。
            instFamily (Optional[str]): 交易品种。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"instType": instType}
        if uly is not None:
            params["uly"] = uly
        if instFamily is not None:
            params["instFamily"] = instFamily
        return self._client._request_with_params(GET, TICKERS_INFO, params)

    def get_ticker(self, instId: str) -> Dict[str, Any]:
        """
        获取单个产品行情信息。

        Args:
            instId (str): 产品ID。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"instId": instId}
        return self._client._request_with_params(GET, TICKER_INFO, params)

    def get_index_tickers(
        self, quoteCcy: Optional[str] = None, instId: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取指数行情信息。

        Args:
            quoteCcy (Optional[str]): 计价币种。
            instId (Optional[str]): 指数ID。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {}
        if quoteCcy is not None:
            params["quoteCcy"] = quoteCcy
        if instId is not None:
            params["instId"] = instId
        return self._client._request_with_params(GET, INDEX_TICKERS, params)

    def get_orderbook(self, instId: str, sz: Optional[str] = None) -> Dict[str, Any]:
        """
        获取产品深度数据。

        Args:
            instId (str): 产品ID。
            sz (Optional[str]): 深度档位数量。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"instId": instId}
        if sz is not None:
            params["sz"] = sz
        return self._client._request_with_params(GET, ORDER_BOOKS, params)

    def get_candlesticks(
        self,
        instId: str,
        after: Optional[str] = None,
        before: Optional[str] = None,
        bar: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取K线数据。

        Args:
            instId (str): 产品ID。
            after (Optional[str]): 查询起始时间戳。
            before (Optional[str]): 查询结束时间戳。
            bar (Optional[str]): K线周期。
            limit (Optional[str]): 返回结果的数量。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"instId": instId}
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if bar is not None:
            params["bar"] = bar
        if limit is not None:
            params["limit"] = limit
        return self._client._request_with_params(GET, MARKET_CANDLES, params)

    def get_history_candlesticks(
        self,
        instId: str,
        after: Optional[str] = None,
        before: Optional[str] = None,
        bar: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取历史K线数据（仅支持部分币种）。

        Args:
            instId (str): 产品ID。
            after (Optional[str]): 查询起始时间戳。
            before (Optional[str]): 查询结束时间戳。
            bar (Optional[str]): K线周期。
            limit (Optional[str]): 返回结果的数量。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"instId": instId}
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if bar is not None:
            params["bar"] = bar
        if limit is not None:
            params["limit"] = limit
        return self._client._request_with_params(GET, HISTORY_CANDLES, params)

    def get_index_candlesticks(
        self,
        instId: str,
        after: Optional[str] = None,
        before: Optional[str] = None,
        bar: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取指数K线数据。

        Args:
            instId (str): 指数ID。
            after (Optional[str]): 查询起始时间戳。
            before (Optional[str]): 查询结束时间戳。
            bar (Optional[str]): K线周期。
            limit (Optional[str]): 返回结果的数量。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"instId": instId}
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if bar is not None:
            params["bar"] = bar
        if limit is not None:
            params["limit"] = limit
        return self._client._request_with_params(GET, INDEX_CANDLES, params)

    def get_mark_price_candlesticks(
        self,
        instId: str,
        after: Optional[str] = None,
        before: Optional[str] = None,
        bar: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取标记价格K线数据。

        Args:
            instId (str): 产品ID。
            after (Optional[str]): 查询起始时间戳。
            before (Optional[str]): 查询结束时间戳。
            bar (Optional[str]): K线周期。
            limit (Optional[str]): 返回结果的数量。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"instId": instId}
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if bar is not None:
            params["bar"] = bar
        if limit is not None:
            params["limit"] = limit
        return self._client._request_with_params(GET, MARKPRICE_CANDLES, params)

    def get_trades(self, instId: str, limit: Optional[str] = None) -> Dict[str, Any]:
        """
        获取最新成交数据。

        Args:
            instId (str): 产品ID。
            limit (Optional[str]): 返回结果的数量。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"instId": instId}
        if limit is not None:
            params["limit"] = limit
        return self._client._request_with_params(GET, MARKET_TRADES, params)

    def get_volume(self) -> Dict[str, Any]:
        """
        获取平台24小时交易量。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        return self._client._request_without_params(GET, PLATFORM_24_VOLUME)

    def get_tier(
        self,
        instType: Optional[str] = None,
        tdMode: Optional[str] = None,
        uly: Optional[str] = None,
        instId: Optional[str] = None,
        ccy: Optional[str] = None,
        tier: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取产品档位信息。

        Args:
            instType (Optional[str]): 产品类型。
            tdMode (Optional[str]): 交易模式。
            uly (Optional[str]): 标的指数。
            instId (Optional[str]): 产品ID。
            ccy (Optional[str]): 保证金币种。
            tier (Optional[str]): 档位。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {k: v for k, v in locals().items() if v is not None and k != "self"}
        return self._client._request_with_params(GET, TIER, params)

    def get_index_components(self, index: str) -> Dict[str, Any]:
        """
        获取指数成分数据。

        Args:
            index (str): 指数ID。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"index": index}
        return self._client._request_with_params(GET, INDEX_COMPONENTS, params)

    def get_exchange_rate(self) -> Dict[str, Any]:
        """
        获取法币汇率。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        return self._client._request_without_params(GET, EXCHANGE_RATE)

    def get_history_trades(
        self,
        instId: str,
        type: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        获取历史成交数据。

        Args:
            instId (str): 产品ID。
            type (Optional[str]): 成交类型。
            after (Optional[str]): 查询起始时间戳。
            before (Optional[str]): 查询结束时间戳。
            limit (Optional[str]): 返回结果的数量。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"instId": instId}
        if type is not None:
            params["type"] = type
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before
        if limit is not None:
            params["limit"] = limit
        return self._client._request_with_params(GET, HISTORY_TRADES, params)

    def get_block_ticker(self, instId: str) -> Dict[str, Any]:
        """
        获取大宗交易产品行情信息。

        Args:
            instId (str): 产品ID。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"instId": instId}
        return self._client._request_with_params(GET, BLOCK_TICKER, params)

    def get_block_tickers(
        self, instType: str, uly: Optional[str] = None, instFamily: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取大宗交易所有产品行情信息。

        Args:
            instType (str): 产品类型。
            uly (Optional[str]): 标的指数。
            instFamily (Optional[str]): 交易品种。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"instType": instType}
        if uly is not None:
            params["uly"] = uly
        if instFamily is not None:
            params["instFamily"] = instFamily
        return self._client._request_with_params(GET, BLOCK_TICKERS, params)

    def get_block_trades(self, instId: str) -> Dict[str, Any]:
        """
        获取大宗交易最新成交数据。

        Args:
            instId (str): 产品ID。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"instId": instId}
        return self._client._request_with_params(GET, BLOCK_TRADES, params)

    def get_order_lite_book(self, instId: str) -> Dict[str, Any]:
        """
        获取精简深度数据。

        Args:
            instId (str): 产品ID。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"instId": instId}
        return self._client._request_with_params(GET, GET_ORDER_LITE_BOOK, params)

    def get_option_trades(self, instFamily: str) -> Dict[str, Any]:
        """
        获取期权最新成交数据。

        Args:
            instFamily (str): 交易品种。

        Returns:
            Dict[str, Any]: API响应数据。
        """
        params = {"instFamily": instFamily}
        return self._client._request_with_params(
            GET, GET_OPTION_INSTRUMENT_FAMILY_TRADES, params
        )
