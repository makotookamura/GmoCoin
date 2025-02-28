#!python3
from pprint import pprint
from enum import Enum
import time
import json
from decimal import Decimal
from datetime import datetime

from gmocoin.private.api import Client
from gmocoin.common.dto import AssetSymbol, Symbol, SalesSide, OrderType, ExecutionType, SettleType, \
    OrderStatus, TimeInForce
from .const import TestConst


class Test:

    @classmethod
    def setup_class(cls):
        with open(str('./tests/api_conf.json'), encoding='utf-8') as f:
            cls._api_conf = json.load(f)

    def test_get_margin(self):
        time.sleep(TestConst.API_CALL_INTERVAL)
        client = Client(
            api_key=self._api_conf['API_KEY'], secret_key=self._api_conf['SECRET_KEY'])
        res = client.get_margin()

        assert type(res.status) is int
        assert type(res.responsetime) is datetime
        assert type(res.data.actual_profit_loss) is Decimal
        assert type(res.data.available_amount) is Decimal
        assert type(res.data.margin) is Decimal
        assert type(res.data.margin_call_status) is str
        assert type(res.data.margin_ratio) is Decimal
        assert type(res.data.profit_loss) is Decimal

        print(res.status)
        print(res.responsetime)
        print(res.data.actual_profit_loss)
        print(res.data.available_amount)
        print(res.data.margin)
        print(res.data.profit_loss)

    def test_get_assets(self):
        time.sleep(TestConst.API_CALL_INTERVAL)
        client = Client(
            api_key=self._api_conf['API_KEY'], secret_key=self._api_conf['SECRET_KEY'])
        res = client.get_assets()

        assert type(res.status) is int
        assert type(res.responsetime) is datetime
        for d in res.data:
            assert type(d.amount) is Decimal
            assert type(d.available) is Decimal
            assert type(d.conversion_rate) is Decimal
            assert type(d.symbol) is AssetSymbol

        print(res.status)
        print(res.responsetime)
        for d in res.data:
            print(d.amount)
            print(d.available)
            print(d.conversion_rate)
            print(d.symbol)

    def test_get_active_orders(self):
        time.sleep(TestConst.API_CALL_INTERVAL)
        client = Client(
            api_key=self._api_conf['API_KEY'], secret_key=self._api_conf['SECRET_KEY'])

        res = client.order(symbol=Symbol.BTC_JPY,
                           side=SalesSide.BUY,
                           execution_type=ExecutionType.LIMIT,
                           time_in_force=TimeInForce.FAS,
                           price=str(TestConst.ORDER_PRICE),
                           size='0.01')
        order_id = res.data

        res = client.get_active_orders(symbol=Symbol.BTC_JPY)

        assert type(res.status) is int
        assert type(res.responsetime) is datetime
        assert type(res.data.pagination.current_page) is int
        assert type(res.data.pagination.count) is int
        for o in res.data.active_orders:
            assert type(o.root_order_id) is int
            assert type(o.order_id) is int
            assert type(o.symbol) is Symbol
            assert type(o.side) is SalesSide
            assert type(o.order_type) is OrderType
            assert type(o.execution_type) is ExecutionType
            assert type(o.settle_type) is SettleType
            assert type(o.size) is Decimal
            assert type(o.executed_size) is Decimal
            assert type(o.price) is Decimal
            assert type(o.losscut_price) is Decimal
            assert type(o.status) is OrderStatus
            assert type(o.time_in_force) is TimeInForce
            assert type(o.timestamp) is datetime

        print(res.status)
        print(res.responsetime)
        print(res.data.pagination.current_page)
        print(res.data.pagination.count)
        for o in res.data.active_orders:
            print(o.root_order_id)
            print(o.order_id)
            print(o.symbol)
            print(o.side)
            print(o.order_type)
            print(o.execution_type)
            print(o.settle_type)
            print(o.size)
            print(o.executed_size)
            print(o.price)
            print(o.losscut_price)
            print(o.status)
            print(o.time_in_force)
            print(o.timestamp)

        client.cancel_order(order_id)

        client.get_active_orders(symbol=Symbol.BTC)

    def test_get_latest_executions(self):
        time.sleep(TestConst.API_CALL_INTERVAL)
        client = Client(
            api_key=self._api_conf['API_KEY'], secret_key=self._api_conf['SECRET_KEY'])

        res = client.get_latest_executions(symbol=Symbol.BTC_JPY)

        assert type(res.status) is int
        assert type(res.responsetime) is datetime

        print(res.status)
        print(res.responsetime)

        # MEMO: 最新の約定が無い場合、以下の型テストを行わない。
        if res.data.pagination != None and res.data.latest_executions != None:
            assert type(res.data.pagination.current_page) is int
            assert type(res.data.pagination.count) is int
            for o in res.data.latest_executions:
                assert type(o.execution_id) is int
                assert type(o.order_id) is int
                assert type(o.symbol) is Symbol
                assert type(o.side) is SalesSide
                assert type(o.settle_type) is SettleType
                assert type(o.size) is Decimal
                assert type(o.price) is Decimal
                assert type(o.loss_gain) is Decimal
                assert type(o.fee) is Decimal
                assert type(o.timestamp) is datetime

            print(res.data.pagination.current_page)
            print(res.data.pagination.count)
            for o in res.data.latest_executions:
                print(o.execution_id)
                print(o.order_id)
                print(o.symbol)
                print(o.side)
                print(o.settle_type)
                print(o.size)
                print(o.price)
                print(o.loss_gain)
                print(o.fee)
                print(o.timestamp)

    def test_get_position_summary(self):
        time.sleep(TestConst.API_CALL_INTERVAL)
        client = Client(
            api_key=self._api_conf['API_KEY'], secret_key=self._api_conf['SECRET_KEY'])
        res = client.get_position_summary(symbol=Symbol.XRP_JPY)

        assert type(res.status) is int
        assert type(res.responsetime) is datetime
        if res.data.position_summarys is not None:
            for p in res.data.position_summarys:
                assert type(p.average_position_rate) is Decimal
                assert type(p.position_loss_gain) is Decimal
                assert type(p.side) is SalesSide
                assert type(p.sum_order_quantity) is Decimal
                assert type(p.sum_position_quantity) is Decimal
                assert type(p.symbol) is Symbol

        print(res.status)
        print(res.responsetime)
        if res.data.position_summarys is not None:
            for o in res.data.position_summarys:
                print(p.average_position_rate)
                print(p.position_loss_gain)
                print(p.side)
                print(p.sum_order_quantity)
                print(p.sum_position_quantity)
                print(p.symbol)

        client.get_position_summary(symbol=Symbol.LTC_JPY)

    def test_order_change_and_cancel(self):
        time.sleep(TestConst.API_CALL_INTERVAL)
        client = Client(
            api_key=self._api_conf['API_KEY'], secret_key=self._api_conf['SECRET_KEY'])
        res = client.order(symbol=Symbol.BTC_JPY,
                           side=SalesSide.BUY,
                           execution_type=ExecutionType.LIMIT,
                           time_in_force=TimeInForce.FAS,
                           price=str(TestConst.ORDER_PRICE),
                           size='0.01')
        order_id = res.data

        assert type(res.status) is int
        assert type(res.responsetime) is datetime
        assert type(res.data) is int
        print(res.status)
        print(res.responsetime)
        print(res.data)

        time.sleep(TestConst.API_CALL_INTERVAL)
        res = client.change_order(res.data, price=str(
            TestConst.ORDER_PRICE+10000), losscut_price=str(TestConst.ORDER_LOSSCUT_PRICE))
        assert type(res.status) is int
        assert type(res.responsetime) is datetime
        print(res.status)
        print(res.responsetime)

        time.sleep(TestConst.API_CALL_INTERVAL)
        res = client.cancel_order(order_id)
        assert type(res.status) is int
        assert type(res.responsetime) is datetime
        print(res.status)
        print(res.responsetime)

    def test_order_and_cancel(self):
        time.sleep(TestConst.API_CALL_INTERVAL)
        client = Client(
            api_key=self._api_conf['API_KEY'], secret_key=self._api_conf['SECRET_KEY'])
        res = client.order(symbol=Symbol.BTC_JPY,
                           side=SalesSide.BUY,
                           execution_type=ExecutionType.LIMIT,
                           time_in_force=TimeInForce.FAS,
                           price=str(TestConst.ORDER_PRICE),
                           size='0.01')

        assert type(res.status) is int
        assert type(res.responsetime) is datetime
        assert type(res.data) is int
        print(res.status)
        print(res.responsetime)
        print(res.data)

        time.sleep(TestConst.API_CALL_INTERVAL)
        res = client.cancel_order(res.data)
        assert type(res.status) is int
        assert type(res.responsetime) is datetime
        print(res.status)
        print(res.responsetime)

    def test_close_order(self):
        # 建玉が必要なためテスト省略
        pass

    def test_close_bulk_order(self):
        # 建玉が必要なためテスト省略
        pass
