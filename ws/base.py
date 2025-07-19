# okx/ws/base.py
import asyncio
import json
import logging
from collections import defaultdict
from typing import Callable, Dict, List, Optional

import websockets
from okx.ws.factory import WebSocketFactory

logger = logging.getLogger(__name__)


class WsBaseAsync:
    """WebSocket基础客户端，处理连接、订阅和消息分发"""

    def __init__(
        self,
        url: str,
        ping_interval: Optional[int] = None,
        ping_timeout: Optional[int] = None,
    ):
        self.factory = WebSocketFactory(url, ping_interval, ping_timeout)
        self.subscriptions = defaultdict(list)  # channel -> [param1, param2]
        self.callbacks = defaultdict(list)  # channel -> [callback1, callback2]
        self.auto_reconnect = True
        self.consumer_task = None

        # 事件处理器字典，用于优雅地处理非数据类消息
        self._event_handlers = {
            "subscribe": self._handle_subscribe_event,
            "unsubscribe": self._handle_unsubscribe_event,
            "error": self._handle_error_event,
        }

    async def start(self):
        """启动客户端，连接并开始消费消息"""
        logger.info("🚀 Starting WebSocket client...")
        if not await self.factory.connect():
            return  # 如果初始连接失败，则不启动消费任务
        self.consumer_task = asyncio.create_task(self._consume_messages())

    async def stop(self):
        """停止客户端，取消任务并关闭连接"""
        logger.info("🛑 Stopping WebSocket client...")
        self.auto_reconnect = False
        if self.consumer_task and not self.consumer_task.done():
            self.consumer_task.cancel()
            try:
                await self.consumer_task
            except asyncio.CancelledError:
                pass  # 任务取消是正常行为
        await self.factory.close()
        logger.info("WebSocket client stopped.")

    async def _consume_messages(self):
        """核心消息消费循环"""
        while self.auto_reconnect:
            try:
                async for message in self.factory.websocket:
                    try:
                        msg_data = json.loads(message)
                        event = msg_data.get("event")

                        # 优先处理系统事件
                        if event and event in self._event_handlers:
                            self._event_handlers[event](msg_data)
                            continue

                        # 分发数据消息到对应的回调
                        arg = msg_data.get("arg", {})
                        channel = arg.get("channel")
                        if channel and channel in self.callbacks:
                            for callback in self.callbacks[channel]:
                                try:
                                    await callback(msg_data)
                                except Exception as e:
                                    logger.error(
                                        f"Error in callback for channel {channel}: {e}"
                                    )
                        else:
                            # 记录但不过度干扰
                            if "event" not in msg_data and "data" not in msg_data:
                                logger.warning(
                                    f"Unhandled message or event: {message[:150]}..."
                                )

                    except json.JSONDecodeError:
                        logger.error(f"Invalid JSON received: {message[:150]}...")
                    except Exception as e:
                        logger.exception(f"Error processing message: {e}")

            except (
                websockets.ConnectionClosedError,
                websockets.ConnectionClosedOK,
            ) as e:
                logger.error(f"🚫 Connection closed: {e}. Auto-reconnecting...")
                if self.auto_reconnect:
                    await self._handle_reconnect()
                else:
                    break  # 退出循环
            except asyncio.CancelledError:
                logger.info("Message consumer task cancelled.")
                break
            except Exception as e:
                logger.exception(
                    f"❌ Unexpected error in consumer loop: {e}. Retrying after a delay."
                )
                await asyncio.sleep(5)

    async def _handle_reconnect(self):
        """处理断线重连逻辑"""
        if await self.factory.reconnect():
            await self._resubscribe_all()
        else:
            logger.error("Failed to reconnect, will retry consumer loop.")
            await asyncio.sleep(5)  # 等待一段时间再尝试下一次循环

    async def _resubscribe_all(self):
        """断线重连后，重新订阅所有之前已订阅的频道"""
        if not self.factory.is_connected():
            logger.error("Cannot resubscribe, no active connection.")
            return

        all_params = [
            param
            for params_list in self.subscriptions.values()
            for param in params_list
        ]
        if not all_params:
            logger.info("No active subscriptions to restore.")
            return

        logger.info(f"🔄 Restoring {len(all_params)} subscriptions...")
        # 去重，避免重复订阅
        unique_params = [dict(t) for t in {tuple(d.items()) for d in all_params}]
        await self._send_subscription_payload(unique_params, "subscribe")

    async def subscribe(self, params: List[Dict[str, str]], callback: Callable):
        """订阅一个或多个频道，并关联回调函数"""
        for param in params:
            channel = param.get("channel")
            if not channel:
                logger.warning(f"Subscription parameter missing 'channel': {param}")
                continue

            self.subscriptions[channel].append(param)
            if callback not in self.callbacks[channel]:
                self.callbacks[channel].append(callback)

        await self._send_subscription_payload(params, "subscribe")

    async def unsubscribe(self, params: List[Dict[str, str]]):
        """取消订阅一个或多个频道"""
        for param in params:
            channel = param.get("channel")
            if channel in self.subscriptions:
                # 从订阅列表中移除
                self.subscriptions[channel] = [
                    p for p in self.subscriptions[channel] if p != param
                ]
                # 如果该频道下没有订阅了，则清空
                if not self.subscriptions[channel]:
                    del self.subscriptions[channel]
                    del self.callbacks[channel]

        await self._send_subscription_payload(params, "unsubscribe")

    async def _send_subscription_payload(self, params: List[Dict[str, str]], op: str):
        """构建并发送(取消)订阅请求"""
        if not self.factory.is_connected():
            logger.error(f"Cannot {op}, not connected.")
            return

        payload = json.dumps({"op": op, "args": params})
        logger.info(f"📡 Sending {op} request: {payload}")
        try:
            await self.factory.websocket.send(payload)
        except websockets.ConnectionClosed as e:
            logger.error(f"Failed to send {op} request, connection closed: {e}")

    # --- Event Handlers ---
    def _handle_subscribe_event(self, msg_data: dict):
        logger.info(f"✅ Subscription confirmed for: {msg_data.get('arg')}")

    def _handle_unsubscribe_event(self, msg_data: dict):
        logger.info(f"✅ Unsubscription confirmed for: {msg_data.get('arg')}")

    def _handle_error_event(self, msg_data: dict):
        logger.error(f"🚨 Error message from server: {msg_data}")
