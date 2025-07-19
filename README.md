# OKX Python SDK

OKX交易所的Python SDK，支持REST API和WebSocket。

## 快速开始

### 安装依赖

```bash
pip install httpx loguru
```

### 基本使用

```python
from rest_api import RestAPI

# 创建API客户端
api = RestAPI(
    api_key='your_api_key',
    api_secret_key='your_secret_key', 
    passphrase='your_passphrase',
    flag='1'  # '0'=实盘, '1'=模拟盘
)

# 获取账户余额
balance = api.account.get_account_balance()
print(balance)

# 获取持仓信息
positions = api.account.get_positions()
print(positions)

# 下单
order = api.trade.place_order(
    instId='BTC-USDT',
    tdMode='cash',
    side='buy',
    ordType='limit',
    sz='0.01',
    px='30000'
)
print(order)

# 关闭客户端
api.close()
```

### 使用上下文管理器（推荐）

```python
from rest_api import RestAPI

with RestAPI(api_key='...', api_secret_key='...', passphrase='...', flag='1') as api:
    balance = api.account.get_account_balance()
    print(balance)
# 自动关闭连接
```

## API模块

- `api.account` - 账户相关API
- `api.trade` - 交易相关API  
- `api.market_data` - 市场数据API
- `api.finance` - 金融服务API
- `api.funding` - 资金相关API
- `api.convert` - 兑换API
- `api.copy_trading` - 跟单API
- `api.grid` - 网格交易API
- `api.block_trading` - 大宗交易API
- `api.spread_trading` - 价差交易API
- `api.public_data` - 公共数据API
- `api.status` - 系统状态API
- `api.sub_account` - 子账户API
- `api.trading_data` - 交易数据API

## 异步支持

```python
from async_rest import AsyncRestAPI
import asyncio

async def main():
    async with AsyncRestAPI(api_key='...', ...) as api:
        balance = await api.account.get_account_balance()
        print(balance)

asyncio.run(main())
```

## 配置说明

- `api_key`: OKX API Key
- `api_secret_key`: OKX Secret Key  
- `passphrase`: OKX API Passphrase
- `flag`: 交易环境 ('0'=实盘, '1'=模拟盘)
- `domain`: API域名 (默认: https://www.okx.com)
- `debug`: 调试模式 (默认: False)
- `proxy`: 代理设置 (可选)

## 注意事项

1. 请妥善保管您的API密钥
2. 建议在测试环境先使用模拟盘 (`flag='1'`)
3. 生产环境使用时请注意API调用频率限制
4. 使用完毕后记得调用 `api.close()` 或使用上下文管理器