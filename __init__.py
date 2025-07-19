# okx/__init__.py
"""
Python SDK for the OKX API v5
同时提供同步 (RestAPI) 和异步 (AsyncRestAPI) 客户端。
"""
__version__="0.5.0"

# 同步入口
from okx.rest_api import RestAPI

# 异步入口
from okx.async_rest import AsyncRestAPI