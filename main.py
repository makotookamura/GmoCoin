import argparse
import logging
import traceback
from datetime import datetime

import cryptowatch as cw
import numpy as np
import pandas as pd

from gmocoin.common.dto import ExecutionType, SalesSide, Symbol, TimeInForce
from gmocoin.private.api import Client

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s- %(name)s - %(levelname)s - %(message)s')


def fetch_chart(query='kraken:btcjpy'):
    return cw.markets.get(query, ohlc=True)


def preprocess(chart):
    df = pd.DataFrame(chart.of_1d[-100:],
                      columns=['timestamp', 'open', 'high', 'low', 'close', 'volume_base', 'volume_quote'])
    df['datetime'] = df['timestamp'].apply(datetime.fromtimestamp)
    df['ema12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['ema26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['macd1226'] = df['ema12'] - df['ema26']
    df['signal12269'] = df['macd1226'].rolling(9).mean()
    return df


def macd_algorithm(macd, signal):
    if np.isnan(macd) or np.isnan(signal):
        return 'none'
    if macd >= signal:
        return 'buy'
    elif macd < signal:
        return 'sell'


def buy(client):
    res = client.order(symbol=Symbol.XRP_JPY, side=SalesSide.BUY, time_in_force=TimeInForce.FAK,
                       execution_type=ExecutionType.MARKET, size='1')
    logging.info(
        f'buy: status={res.status} orderId={res.orderId} price={res.price} losscutPrice={res.losscutPrice}')
    # ccl = client.cancel_order(res.orderId)
    # logging.info(f'cancel: status={ccl.status} orderId={res.orderId}')


def sell(client):
    res = client.order(symbol=Symbol.XRP_JPY, side=SalesSide.SELL, time_in_force=TimeInForce.FAK,
                       execution_type=ExecutionType.MARKET, size='1')
    logging.info(
        f'sell: status={res.status} orderId={res.orderId} price={res.price} losscutPrice={res.losscutPrice}')
    # ccl = client.cancel_order(res.orderId)
    # logging.info(f'cancel: status={ccl.status} orderId={res.orderId}')


def no_trade():
    logging.info('no trade')


def app(args):
    try:
        # chart
        chart = fetch_chart()
        df = preprocess(chart)
        today = df.tail(1).to_records()[0]

        # judge
        action = macd_algorithm(today['macd1226'], today['signal12269'])
        logging.info(f'action: {action}')

        # execute
        client = Client(args.api_key, args.secret_key)
        # logging.info(client.get_margin())
        # logging.info(client.get_assets())
        # logging.info(client.get_active_orders(symbol=Symbol.XRP_JPY))

        if action == 'buy':
            buy(client)
        elif action == 'sell':
            sell(client)
        else:
            no_trade()

    except Exception:
        logging.error(traceback.format_exc())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', type=str, required=True)
    parser.add_argument('--secret_key', type=str, required=True)
    args = parser.parse_args()
    app(args)
