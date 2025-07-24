# okx/__init__.py
"""
Python SDK for the OKX API v5
同时提供同步 (RestAPI) 和异步 (AsyncRestAPI) 客户端。
"""

__version__ = "0.5.1"

# 同步入口
from okxx.rest_api import RestAPI

# 异步入口
from okxx.async_rest import AsyncRestAPI
