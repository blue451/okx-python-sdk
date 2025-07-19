# okx/async_rest.py
"""
此文件定义了SDK的异步统一入口点 AsyncRestAPI。
用户应从此文件导入并实例化 AsyncRestAPI 类来进行高性能的异步API交互。
"""

from okx.async_okxclient import AsyncOkxClient
from okx.async_api.AsyncAccount import AsyncAccountAPI
from okx.async_api.AsyncBlockTrading import AsyncBlockTradingAPI
from okx.async_api.AsyncConvert import AsyncConvertAPI
from okx.async_api.AsyncCopyTrading import AsyncCopyTradingAPI
from okx.async_api.AsyncFDBroker import AsyncFDBrokerAPI
from okx.async_api.AsyncFinance import AsyncFinanceAPI
from okx.async_api.AsyncFunding import AsyncFundingAPI
from okx.async_api.AsyncGrid import AsyncGridAPI
from okx.async_api.AsyncMarketData import AsyncMarketAPI
from okx.async_api.AsyncPublicData import AsyncPublicAPI
from okx.async_api.AsyncSpreadTrading import AsyncSpreadTradingAPI
from okx.async_api.AsyncStatus import AsyncStatusAPI
from okx.async_api.AsyncSubAccount import AsyncSubAccountAPI
from okx.async_api.AsyncTrade import AsyncTradeAPI
from okx.async_api.AsyncTradingData import AsyncTradingDataAPI

from okx.consts import API_URL
from typing import Optional

class AsyncRestAPI:
    """
    OKX Rest API 的异步统一入口。
    该类整合了所有独立的异步API功能模块，并共享一个底层的异步HTTP客户端实例。
    所有API调用都返回协程(coroutine)，需要使用 'await' 来执行。
    限速逻辑已由底层客户端自动处理。
    """

    def __init__(self, api_key: str = '-1', api_secret_key: str = '-1', passphrase: str = '-1', flag: str = '1',
                 domain: str = API_URL, debug: bool = False, proxy: Optional[str] = None):
        """
        初始化异步SDK客户端。
        参数与同步版本完全相同。
        """
        self._client = AsyncOkxClient(api_key, api_secret_key, passphrase, flag, domain, debug, proxy)

        # 实例化所有异步功能模块
        self.account = AsyncAccountAPI(self._client)
        self.block_trading = AsyncBlockTradingAPI(self._client)
        self.convert = AsyncConvertAPI(self._client)
        self.copy_trading = AsyncCopyTradingAPI(self._client)
        self.fd_broker = AsyncFDBrokerAPI(self._client)
        self.finance = AsyncFinanceAPI(self._client)
        self.funding = AsyncFundingAPI(self._client)
        self.grid = AsyncGridAPI(self._client)
        self.market_data = AsyncMarketAPI(self._client)
        self.public_data = AsyncPublicAPI(self._client)
        self.spread_trading = AsyncSpreadTradingAPI(self._client)
        self.status = AsyncStatusAPI(self._client)
        self.sub_account = AsyncSubAccountAPI(self._client)
        self.trade = AsyncTradeAPI(self._client)
        self.trading_data = AsyncTradingDataAPI(self._client)
    
    async def aclose(self):
        """
        优雅地关闭底层的 httpx.AsyncClient 连接池。
        强烈建议在应用程序退出前调用此方法，以释放网络资源。
        
        使用示例:
        api = AsyncRestAPI()
        try:
            # ... do async stuff
        finally:
            await api.aclose()
        """
        await self._client.aclose()
    
    async def __aenter__(self):
        """异步上下文管理器支持"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步资源清理"""
        await self.aclose()