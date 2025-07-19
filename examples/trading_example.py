"""
交易示例
演示如何使用 OKX Python SDK 进行交易操作
"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rest_api import RestAPI


def trading_example():
    """交易示例"""
    
    # 配置API密钥
    API_KEY = 'your_api_key_here'
    SECRET_KEY = 'your_secret_key_here'
    PASSPHRASE = 'your_passphrase_here'
    FLAG = '1'  # 使用模拟盘
    
    with RestAPI(
        api_key=API_KEY,
        api_secret_key=SECRET_KEY,
        passphrase=PASSPHRASE,
        flag=FLAG,
        debug=True
    ) as api:
        
        # 1. 获取当前BTC价格
        print("=== 获取当前BTC价格 ===")
        ticker = api.market_data.get_ticker(instId='BTC-USDT')
        if ticker and 'data' in ticker and ticker['data']:
            current_price = float(ticker['data'][0]['last'])
            print(f"BTC当前价格: ${current_price}")
        else:
            print("无法获取价格信息")
            return
        
        # 2. 下限价买单
        print("\n=== 下限价买单 ===")
        buy_price = current_price * 0.99  # 比当前价格低1%
        buy_order = api.trade.place_order(
            instId='BTC-USDT',
            tdMode='cash',  # 现货交易
            side='buy',
            ordType='limit',
            sz='0.001',  # 买入0.001 BTC
            px=str(buy_price)
        )
        print(f"买单结果: {buy_order}")
        
        if buy_order and 'data' in buy_order and buy_order['data']:
            buy_order_id = buy_order['data'][0]['ordId']
            print(f"买单ID: {buy_order_id}")
            
            # 3. 查询订单状态
            print("\n=== 查询订单状态 ===")
            time.sleep(1)  # 等待1秒
            order_info = api.trade.get_order(
                instId='BTC-USDT',
                ordId=buy_order_id
            )
            print(f"订单信息: {order_info}")
            
            # 4. 取消订单（如果还未成交）
            print("\n=== 取消订单 ===")
            cancel_result = api.trade.cancel_order(
                instId='BTC-USDT',
                ordId=buy_order_id
            )
            print(f"取消订单结果: {cancel_result}")
        
        # 5. 下市价单示例（小心使用）
        print("\n=== 市价单示例 ===")
        print("注意: 这是模拟交易，实盘请谨慎操作")
        
        # 获取账户余额
        balance = api.account.get_account_balance()
        print(f"账户余额: {balance}")
        
        # 6. 获取历史订单
        print("\n=== 获取历史订单 ===")
        history_orders = api.trade.get_orders_history(
            instType='SPOT',
            limit='10'
        )
        print(f"历史订单: {history_orders}")


def batch_orders_example():
    """批量下单示例"""
    
    API_KEY = 'your_api_key_here'
    SECRET_KEY = 'your_secret_key_here'
    PASSPHRASE = 'your_passphrase_here'
    FLAG = '1'
    
    with RestAPI(
        api_key=API_KEY,
        api_secret_key=SECRET_KEY,
        passphrase=PASSPHRASE,
        flag=FLAG
    ) as api:
        
        print("=== 批量下单示例 ===")
        
        # 获取当前价格
        ticker = api.market_data.get_ticker(instId='BTC-USDT')
        if not (ticker and 'data' in ticker and ticker['data']):
            print("无法获取价格信息")
            return
            
        current_price = float(ticker['data'][0]['last'])
        
        # 准备批量订单
        orders = [
            {
                'instId': 'BTC-USDT',
                'tdMode': 'cash',
                'side': 'buy',
                'ordType': 'limit',
                'sz': '0.001',
                'px': str(current_price * 0.98)  # 低于市价2%
            },
            {
                'instId': 'BTC-USDT',
                'tdMode': 'cash',
                'side': 'buy',
                'ordType': 'limit',
                'sz': '0.001',
                'px': str(current_price * 0.97)  # 低于市价3%
            }
        ]
        
        # 批量下单
        batch_result = api.trade.place_multiple_orders(orders)
        print(f"批量下单结果: {batch_result}")


if __name__ == "__main__":
    print("OKX Python SDK 交易示例")
    print("警告: 这些示例使用模拟盘，实盘交易请谨慎操作！")
    print("请确保已正确配置API密钥\n")
    
    try:
        trading_example()
        print("\n" + "="*50 + "\n")
        batch_orders_example()
    except Exception as e:
        print(f"示例执行出错: {e}")
        print("请检查API密钥配置和网络连接")