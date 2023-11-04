import logging
from typing import *

from models import *

logger = logging.getLogger()

TF_EQUIV = {"1m": 60, "5m": 300, "15m": "900", "30m": 1800, "1h": 3600, "4h": 14400}


class Strategy:
    def __init__(self, contract: Contract, exchange: str, timeframe: str,
                 balance_pct: float, take_profit: float, stop_loss: float):

        self.contract = contract
        self.exchange = exchange
        self.tf = timeframe
        self.tf_equiv = TF_EQUIV[timeframe] * 1000
        self.balance_pct = balance_pct
        self.take_profit = take_profit
        self.stop_loss = stop_loss

        # Get Candles Historical Data
        self.candles: List[Candle] = []

    def parse_trades(self, price: float, size: float, timestamp: int) -> str:

        last_candle = self.candles[-1]

        # Update the same current candle

        if timestamp < last_candle.timestamp + self.tf_equiv:

            last_candle.close = price
            last_candle.volume += size

            if price > last_candle.high:
                last_candle.high = price
            elif price < last_candle.low:
                last_candle.low = price

            return "same_candle"

        # Missing Candle(s)

        elif timestamp >= last_candle.timestamp + 2 * self.tf_equiv:
            missing_candles = int((timestamp - last_candle.timestamp) / self.tf_equiv) - 1

            for missing in range(missing_candles):
                new_ts = last_candle.timestamp + self.tf_equiv
                candle_info = {'ts': new_ts, 'open': last_candle.close, 'high': last_candle.close,
                               'low': last_candle.close, 'close': last_candle.close, 'volume': 0}
                new_candle = Candle(candle_info, self.tf, "parse_trade")

                self.candles.append(new_candle)

                last_candle = new_candle

            new_ts = last_candle.timestamp + self.tf_equiv
            candle_info = {'ts': new_ts, 'open': price, 'high': price, 'low': price, 'close': price, 'volume': size}
            new_candle = Candle(candle_info, self.tf, "parse_trade")

            self.candles.append(new_candle)

            return "new_candle"


        # New Candle

        elif timestamp >= last_candle.timestamp + self.tf_equiv:
            new_ts = last_candle.timestamp + self.tf_equiv
            candle_info = {'ts': new_ts, 'open': price, 'high': price, 'low': price, 'close': price, 'volume': size}
            new_candle = Candle(candle_info, self.tf, "parse_trade")

            self.candles.append(new_candle)

            logger.info("%s New candle for %s %s", self.exchange, self.contract.symbol, self.tf)

            return "new_candle"


class TechnicalStrategy(Strategy):
    def __init__(self, contract: Contract, exchange: str, timeframe: str,
                 balance_pct: float, take_profit: float, stop_loss: float, other_params: Dict):
        super().__init__(contract, exchange, timeframe, balance_pct, take_profit, stop_loss)

        #Strategy Specific Atributes

        self._ema_fast = other_params['ema_fast']
        self._ema_slow = other_params['ema_slow']
        self._ema_signal = other_params['ema_signal']


class BreakoutStrategy(Strategy):
    def __init__(self, contract: Contract, exchange: str, timeframe: str,
                 balance_pct: float, take_profit: float, stop_loss: float, other_params: Dict):
        super().__init__(contract, exchange, timeframe, balance_pct, take_profit, stop_loss)

        #Strategy Specific Attributes

        self._min_volume = other_params['min_volume']

    def _check_signal(self) -> int:
        # High
        if self.candles[-1].close > self.candles[-2].high and self.candles[-1].volume > self._min_volume:
            return 1
        # Low
        elif self.candles[-1].close < self.candles[-2].low and self.candles[-1].volume > self._min_volume:
            return -1
        else:
            return 0

        # Inside Bar Pattern vs Outside Bar Pattern
        # if self.candles[-2].high < self.candles[-3].high and self.candles[-2].low > self.candles[-3].low:
        #    if self.candles[-1].close > self.candles[-3].high:
        #         Upside breakout
        #    elif self.candles[-1].close < self.candles[-3].low:
        #         Downside breakout




























