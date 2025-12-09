"""
Base Strategy
Abstract base class for all trading strategies.
"""

import backtrader as bt


class BaseStrategy(bt.Strategy):
    """
    Abstract base strategy class.

    This class provides common functionality for all trading strategies
    and defines the interface that subclasses must implement.

    Subclasses MUST override the next() method to implement their
    trading logic. Attempting to use BaseStrategy directly will raise
    NotImplementedError.
    """

    params = (
        ('printlog', True),
    )

    def __init__(self):
        """Initialize strategy."""
        self.dataclose = self.datas[0].close
        self.order = None
        self.buy_price = None
        self.buy_comm = None

    def log(self, txt, dt=None):
        """Logging function."""
        if self.params.printlog:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()} {txt}')

    def notify_order(self, order):
        """Receive order notifications."""
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'BUY EXECUTED, Price: {order.executed.price:.2f}, '
                    f'Cost: {order.executed.value:.2f}, '
                    f'Comm: {order.executed.comm:.2f}'
                )
                self.buy_price = order.executed.price
                self.buy_comm = order.executed.comm
            else:
                self.log(
                    f'SELL EXECUTED, Price: {order.executed.price:.2f}, '
                    f'Cost: {order.executed.value:.2f}, '
                    f'Comm: {order.executed.comm:.2f}'
                )

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        """Receive trade notifications."""
        if not trade.isclosed:
            return

        self.log(f'OPERATION PROFIT, GROSS: {trade.pnl:.2f}, NET: {trade.pnlcomm:.2f}')

    def next(self):
        """
        Define strategy logic (must be implemented by subclasses).

        This method is called on each bar of data during backtesting.
        Subclasses must override this method to implement their specific
        trading logic.

        Raises:
            NotImplementedError: If subclass does not implement this method
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement the next() method. "
            "This method should contain the strategy's trading logic."
        )
