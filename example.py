#!/usr/bin/env python3
"""
OKX SDK 使用示例

这个文件展示了如何使用OKX Python SDK进行基本操作
"""

from okx.rest_api import RestAPI

def main():
    """主函数 - 展示基本用法"""
    
    # 配置API密钥 (请替换为您的真实密钥)
    API_KEY = 'your_api_key'
    SECRET_KEY = 'your_secret_key'
    PASSPHRASE = 'your_passphrase'
    
    # 创建API客户端
    # flag='1' 表示模拟盘，flag='0' 表示实盘
    with RestAPI(
        api_key=API_KEY,
        api_secret_key=SECRET_KEY,
        passphrase=PASSPHRASE,
        flag='1',  # 使用模拟盘进行测试
        debug=True  # 开启调试模式
    ) as api:
        
        try:
            # 1. 获取账户余额
            print("=== 获取账户余额 ===")
            balance = api.account.get_account_balance()
            print(f"账户余额: {balance}")
            
            # 2. 获取持仓信息
            print("\n=== 获取持仓信息 ===")
            positions = api.account.get_positions()
            print(f"持仓信息: {positions}")
            
            # 3. 获取市场行情
            print("\n=== 获取BTC-USDT行情 ===")
            ticker = api.market_data.get_ticker('BTC-USDT')
            print(f"BTC-USDT行情: {ticker}")
            
            # 4. 下单示例 (注意：这会实际下单，请谨慎使用)
            print("\n=== 下单示例 (模拟盘) ===")
            order = api.trade.place_order(
                instId='BTC-USDT',
                tdMode='cash',  # 现货交易
                side='buy',     # 买入
                ordType='limit', # 限价单
                sz='0.001',     # 数量
                px='30000'      # 价格
            )
            print(f"下单结果: {order}")
            
        except Exception as e:
            print(f"操作失败: {e}")

def async_example():
    """异步使用示例"""
    import asyncio
    from async_rest import AsyncRestAPI
    
    async def async_main():
        async with AsyncRestAPI(
            api_key='your_api_key',
            api_secret_key='your_secret_key',
            passphrase='your_passphrase',
            flag='1'
        ) as api:
            try:
                balance = await api.account.get_account_balance()
                print(f"异步获取余额: {balance}")
            except Exception as e:
                print(f"异步操作失败: {e}")
    
    # 运行异步示例
    asyncio.run(async_main())

if __name__ == "__main__":
    print("OKX SDK 使用示例")
    print("=" * 50)
    
    # 同步示例
    print("1. 同步API示例:")
    main()
    
    print("\n" + "=" * 50)
    
    # 异步示例
    print("2. 异步API示例:")
    async_example()
    
    print("\n使用完成！")