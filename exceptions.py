# okx/exceptions.py
# coding=utf-8
import sys

if sys.version_info >= (3, 12):
    from typing import override
else:

    def override(func):
        """Python 3.12之前的兼容性装饰器"""
        return func


from typing import override


class OkxAPIException(Exception):
    """
    自定义API异常，用于封装来自OKX API的错误响应。
    """

    @override
    def __init__(self, response):
        """
        :param response: httpx.Response 对象
        """
        self.code = "N/A"
        self.message = "An unknown error occurred"
        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, "request", None)

        try:
            # 尝试从JSON响应中解析错误码和信息
            json_res = response.json()
            if "code" in json_res and "msg" in json_res:
                self.code = json_res["code"]
                self.message = json_res["msg"]
            else:
                # 如果JSON格式不符合预期，使用HTTP Body作为信息
                self.message = response.text
        except ValueError:
            # 如果响应不是有效的JSON
            self.message = f"Invalid JSON error message from okxx: {response.text}"

    @override
    def __str__(self):
        # 使用更现代的 f-string 格式
        return f"API Request Error(http_status={self.status_code}, error_code='{self.code}'): {self.message}"


class OkxRequestException(Exception):
    """
    当网络请求层面发生问题时（如连接超时）抛出的异常。
    """

    def __init__(self, message):
        self.message = message

    @override
    def __str__(self):
        return f"OkxRequestException: {self.message}"


class OkxParamsException(Exception):
    """
    当客户端参数校验失败时（预留）抛出的异常。
    """

    def __init__(self, message):
        self.message = message

    @override
    def __str__(self):
        return f"OkxParamsException: {self.message}"
