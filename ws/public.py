# okx/ws/public.py
import logging
from typing import Optional
from okx.ws.base import WsBaseAsync

logger = logging.getLogger(__name__)


class WsPublicAsync(WsBaseAsync):
    """
    OKX公共WebSocket客户端 (行情数据等).
    这是一个WsBaseAsync的直接子类，提供了清晰的语义。
    """
    
    def __init__(
        self, 
        url: str = "wss://ws.okx.com:8443/ws/v5/public",
        ping_interval: Optional[int] = None,
        ping_timeout: Optional[int] = None
    ):
        super().__init__(
            url, 
            ping_interval=ping_interval,
            ping_timeout=ping_timeout
        )
        logger.info("🌐 Public channel client initialized.")