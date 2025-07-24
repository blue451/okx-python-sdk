# okx/rest_api.py
"""
OKX REST API 同步客户端 - 主要入口

这是推荐的使用方式，包含所有API功能模块。

使用示例:
    from okxx import RestAPI

    # 创建API客户端
    api = RestAPI(
        api_key='your_api_key',
        api_secret_key='your_secret_key',
        passphrase='your_passphrase',
        flag='1',  # '0'=实盘, '1'=模拟盘
        debug=False  # 开启调试模式
    )

    # 账户相关
    balance = api.account.get_account_balance()
    positions = api.account.get_positions()

    # 交易相关
    order = api.trade.place_order(
        instId='BTC-USDT',
        tdMode='cash',
        side='buy',
        ordType='limit',
        sz='0.01',
        px='30000'
    )

    # 市场数据
    ticker = api.market_data.get_ticker('BTC-USDT')

    # 记得关闭客户端
    api.close()

    # 或使用上下文管理器
    with RestAPI(api_key='...', ...) as api:
        balance = api.account.get_account_balance()
"""

from okxx.okxclient import OkxClient
from okxx.rest.Account import AccountAPI
from okxx.rest.BlockTrading import BlockTradingAPI
from okxx.rest.Convert import ConvertAPI
from okxx.rest.CopyTrading import CopyTradingAPI
from okxx.rest.FDBroker import FDBrokerAPI
from okxx.rest.Finance import FinanceAPI
from okxx.rest.Funding import FundingAPI
from okxx.rest.Grid import GridAPI
from okxx.rest.MarketData import MarketAPI
from okxx.rest.PublicData import PublicAPI
from okxx.rest.SpreadTrading import SpreadTradingAPI
from okxx.rest.Status import StatusAPI
from okxx.rest.SubAccount import SubAccountAPI
from okxx.rest.Trade import TradeAPI
from okxx.rest.TradingData import TradingDataAPI

from okxx.consts import API_URL
from typing import Optional


class RestAPI:
    """
    OKX Rest API的同步统一入口。
    该类整合了所有独立的API功能模块，并共享一个底层的HTTP客户端实例。
    """

    def __init__(
        self,
        api_key: str = "-1",
        api_secret_key: str = "-1",
        passphrase: str = "-1",
        flag: str = "1",
        domain: str = API_URL,
        debug: bool = False,
        proxy: Optional[str] = None,
    ):
        """
        初始化SDK客户端。

        :param api_key: 您的API Key。对于公开接口，可以不填。
        :param api_secret_key: 您的API Secret。
        :param passphrase: 您的API Passphrase。
        :param flag: 交易模式标记。'0': 实盘, '1': 模拟盘。
        :param domain: API请求的域名。默认为 'https://www.okx.com'。
        :param debug: 是否开启调试模式，开启后会打印详细的请求日志。
        :param proxy: （可选）代理服务器地址，例如 'http://127.0.0.1:7890'。
        """
        # 创建一个共享的底层HTTP请求客户端
        self._client = OkxClient(
            api_key, api_secret_key, passphrase, flag, domain, debug, proxy
        )

        # 将各个功能模块实例化为RestAPI的属性
        self.account = AccountAPI(self._client)
        self.block_trading = BlockTradingAPI(self._client)
        self.convert = ConvertAPI(self._client)
        self.copy_trading = CopyTradingAPI(self._client)
        self.fd_broker = FDBrokerAPI(self._client)
        self.finance = FinanceAPI(self._client)
        self.funding = FundingAPI(self._client)
        self.grid = GridAPI(self._client)
        self.market_data = MarketAPI(self._client)
        self.public_data = PublicAPI(self._client)
        self.spread_trading = SpreadTradingAPI(self._client)
        self.status = StatusAPI(self._client)
        self.sub_account = SubAccountAPI(self._client)
        self.trade = TradeAPI(self._client)
        self.trading_data = TradingDataAPI(self._client)

    def close(self):
        """
        关闭内部持有的HTTP客户端，释放所有连接资源。
        """
        if self._client:
            self._client.close()

    def __enter__(self):
        """上下文管理器支持"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """自动资源清理"""
        self.close()
