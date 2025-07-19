# okx/ws/factory.py
import asyncio
import logging
import ssl

import certifi
import websockets
from websockets.protocol import State

logger = logging.getLogger(__name__)


class WebSocketFactory:
    """WebSocket 连接工厂
    
    :param url: WebSocket服务器地址
    :param ping_interval: Ping发送间隔（秒），None使用默认值
    :param ping_timeout: Ping响应超时（秒），None使用默认值
    """
    
    DEFAULT_PING_INTERVAL = 25
    DEFAULT_PING_TIMEOUT = 28
    
    def __init__(self, url, ping_interval=None, ping_timeout=None):
        self.url = url
        self.websocket: websockets.ClientConnection | None = None
        self.connected = False
        
        self.ping_interval = ping_interval or self.DEFAULT_PING_INTERVAL
        self.ping_timeout = ping_timeout or self.DEFAULT_PING_TIMEOUT
        
        logger.debug(f"WebSocketFactory initialized for {url} with heartbeat: "
                     f"interval={self.ping_interval}s, timeout={self.ping_timeout}s")
        
    async def connect(self, max_retries=5, retry_delay=3):
        """尝试连接WebSocket，并在失败时重试"""
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())
        
        retries = 0
        while retries < max_retries:
            try:
                # FIX: 明确传递更多参数给 websockets.connect，以规避其内部bug
                # 这些是 ClientConnection 的构造函数参数，提供合理的默认值
                self.websocket = await websockets.connect(
                    self.url, 
                    ssl=ssl_context,
                    ping_interval=self.ping_interval,
                    ping_timeout=self.ping_timeout,
                    close_timeout=10,  # 添加合理的关闭超时
                    # max_size=2**20,      # 默认1MB
                    # max_queue=32,        # 默认队列大小
                )
                self.connected = True
                logger.info(f"✅ WebSocket connection successful to {self.url}")
                return self.websocket
            except Exception as e:
                retries += 1
                # 在记录日志时，包含异常的类型和堆栈信息，便于调试
                logger.error(f"⚠️ Connection failed to {self.url} (attempt {retries}/{max_retries}): {e}", exc_info=True)
                if retries < max_retries:
                    await asyncio.sleep(retry_delay)
        
        logger.critical(f"🚨 Failed to connect to {self.url} after {max_retries} attempts.")
        self.connected = False
        return None

    async def reconnect(self, max_retries=5, retry_delay=3):
        """关闭现有连接并重新连接"""
        logger.info(f"Attempting to reconnect to {self.url}...")
        await self.close()
        return await self.connect(max_retries, retry_delay)

    async def close(self):
        """安全地关闭WebSocket连接"""
        if (
            self.websocket is not None and
            hasattr(self.websocket, 'protocol') and # 添加此行
            self.websocket.protocol.state not in (State.CLOSING, State.CLOSED)
        ):
            try:
                await self.websocket.close()
            except Exception as e:
                logger.warning(f"Exception during websocket.close(): {e}")

        self.connected = False
        self.websocket = None
        logger.info(f"🔌 WebSocket connection to {self.url} has been closed.")

    def is_connected(self):
        """检查连接是否处于活动状态"""
        return (
            self.connected and
            self.websocket is not None and
            self.websocket.protocol.state == State.OPEN
        )
    
    def update_heartbeat(self, ping_interval, ping_timeout):
        """更新心跳设置（仅影响后续的新连接或重连）"""
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        logger.info(f"🔄 Heartbeat settings updated: interval={ping_interval}s, timeout={ping_timeout}s. "
                    "Changes will apply on next connection.")