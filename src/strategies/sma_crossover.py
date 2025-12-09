"""
SMA Crossover Strategy
Simple Moving Average crossover strategy example.
"""

import backtrader as bt
from .base_strategy import BaseStrategy


class SMACrossover(BaseStrategy):
    """
    Simple Moving Average Crossover Strategy.

    Buy when fast SMA crosses above slow SMA.
    Sell when fast SMA crosses below slow SMA.
    """

    params = (
        ('fast_period', 10),
        ('slow_period', 30),
        ('printlog', True),
    )

    def __init__(self):
        """Initialize indicators."""
        super().__init__()

        # Add moving average indicators
        self.sma_fast = bt.indicators.SimpleMovingAverage(
            self.datas[0].close, period=self.params.fast_period
        )
        self.sma_slow = bt.indicators.SimpleMovingAverage(
            self.datas[0].close, period=self.params.slow_period
        )

        # Crossover signal
        self.crossover = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)

    def next(self):
        """Execute strategy logic."""
        # Check if an order is pending
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Not in market, look for buy signal
            if self.crossover > 0:  # Fast MA crosses above Slow MA
                self.log(f'BUY SIGNAL, Close: {self.dataclose[0]:.2f}')
                self.order = self.buy()

        else:
            # In market, look for sell signal
            if self.crossover < 0:  # Fast MA crosses below Slow MA
                self.log(f'SELL SIGNAL, Close: {self.dataclose[0]:.2f}')
                self.order = self.sell()
