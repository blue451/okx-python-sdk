"""
基本使用示例
演示如何使用 OKX Python SDK 进行基本操作
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rest_api import RestAPI


def main():
    """基本使用示例"""
    
    # 配置你的API密钥（请使用环境变量或配置文件）
    API_KEY = 'your_api_key_here'
    SECRET_KEY = 'your_secret_key_here'
    PASSPHRASE = 'your_passphrase_here'
    
    # 使用模拟盘进行测试
    FLAG = '1'  # '0'=实盘, '1'=模拟盘
    
    # 方式1: 手动管理连接
    print("=== 方式1: 手动管理连接 ===")
    api = RestAPI(
        api_key=API_KEY,
        api_secret_key=SECRET_KEY,
        passphrase=PASSPHRASE,
        flag=FLAG,
        debug=True
    )
    
    try:
        # 获取账户余额
        print("获取账户余额...")
        balance = api.account.get_account_balance()
        print(f"账户余额: {balance}")
        
        # 获取持仓信息
        print("\n获取持仓信息...")
        positions = api.account.get_positions()
        print(f"持仓信息: {positions}")
        
        # 获取市场数据
        print("\n获取BTC-USDT行情...")
        ticker = api.market_data.get_ticker(instId='BTC-USDT')
        print(f"BTC-USDT行情: {ticker}")
        
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 关闭连接
        api.close()
    
    print("\n" + "="*50 + "\n")
    
    # 方式2: 使用上下文管理器（推荐）
    print("=== 方式2: 使用上下文管理器 ===")
    try:
        with RestAPI(
            api_key=API_KEY,
            api_secret_key=SECRET_KEY,
            passphrase=PASSPHRASE,
            flag=FLAG,
            debug=True
        ) as api:
            # 获取交易对信息
            print("获取交易对信息...")
            instruments = api.public_data.get_instruments(instType='SPOT')
            if instruments and 'data' in instruments:
                btc_usdt = next((inst for inst in instruments['data'] if inst['instId'] == 'BTC-USDT'), None)
                if btc_usdt:
                    print(f"BTC-USDT交易对信息: {btc_usdt}")
            
            # 获取K线数据
            print("\n获取BTC-USDT K线数据...")
            candles = api.market_data.get_candles(
                instId='BTC-USDT',
                bar='1H',
                limit='10'
            )
            print(f"K线数据: {candles}")
            
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    print("OKX Python SDK 基本使用示例")
    print("注意: 请先配置你的API密钥")
    print("建议使用模拟盘进行测试\n")
    
    main()