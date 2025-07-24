# okx/ws/private.py
import asyncio
import logging
from typing import Callable, Dict, List, Optional

from okxx.ws import utils
from okxx.ws.base import WsBaseAsync

logger = logging.getLogger(__name__)


class WsPrivateAsync(WsBaseAsync):
    """OKX私有WebSocket客户端（账户、交易），处理登录认证"""

    def __init__(
        self,
        api_key: str,
        passphrase: str,
        secret_key: str,
        url: str = "wss://ws.okx.com:8443/ws/v5/private",
        use_server_time: bool = False,
        ping_interval: Optional[int] = None,
        ping_timeout: Optional[int] = None,
    ):
        super().__init__(url, ping_interval, ping_timeout)
        self.api_key = api_key
        self.passphrase = passphrase
        self.secret_key = secret_key
        self.use_server_time = use_server_time

        self.logged_in = False
        self._login_future: Optional[asyncio.Future] = None

        # 扩展事件处理器以包含登录响应
        self._event_handlers["login"] = self._handle_login_response
        logger.info("🔑 Private channel client initialized.")

    async def login(self) -> bool:
        """执行非阻塞登录，并等待结果"""
        if not self.factory.is_connected():
            logger.error("Cannot log in, not connected.")
            return False

        if self.logged_in:
            return True

        logger.info("🔐 Attempting to log in...")

        try:
            login_payload = await utils.generate_login_payload(
                self.api_key, self.passphrase, self.secret_key, self.use_server_time
            )

            self._login_future = asyncio.get_running_loop().create_future()

            await self.factory.websocket.send(login_payload)

            # 等待登录结果，设置10秒超时
            result = await asyncio.wait_for(self._login_future, timeout=10)
            self.logged_in = result

            if result:
                logger.info("✅ Login successful.")
            else:
                logger.error("❌ Login failed. Check API credentials and permissions.")

            return result

        except asyncio.TimeoutError:
            logger.error("❌ Login timed out. No response from server.")
            self.logged_in = False
            return False
        except Exception as e:
            logger.exception(f"An unexpected error occurred during login: {e}")
            self.logged_in = False
            return False
        finally:
            self._login_future = None

    def _handle_login_response(self, msg_data: dict):
        """处理登录事件，并设置Future的结果"""
        if self._login_future and not self._login_future.done():
            # OKX v5 successful login has code "0"
            if msg_data.get("code") == "0":
                self._login_future.set_result(True)
            else:
                logger.error(f"Login failed with server message: {msg_data}")
                self._login_future.set_result(False)

    async def _handle_reconnect(self):
        """重连后，先登录再恢复订阅"""
        if await self.factory.reconnect():
            self.logged_in = False  # 重连后需要重新登录
            if await self.login():
                await self._resubscribe_all()
            else:
                logger.error(
                    "Failed to log in after reconnect, subscriptions not restored."
                )
        else:
            logger.error("Failed to reconnect, will retry consumer loop.")
            await asyncio.sleep(5)

    async def subscribe(self, params: List[Dict[str, str]], callback: Callable):
        """订阅私有频道前确保已登录"""
        if not self.logged_in:
            if not await self.login():
                logger.error("Cannot subscribe to private channels, login failed.")
                return

        await super().subscribe(params, callback)
