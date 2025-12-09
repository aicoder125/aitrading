"""
Backtesting Engine
Core backtesting functionality using Backtrader.
"""

import backtrader as bt
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd


class BacktestEngine:
    """Backtesting engine wrapper for Backtrader."""

    def __init__(self,
                 initial_cash: float = 100000.0,
                 commission: float = 0.001,
                 slippage: float = 0.0):
        """
        Initialize backtesting engine.

        Args:
            initial_cash: Starting capital
            commission: Commission rate (0.001 = 0.1%)
            slippage: Slippage percentage
        """
        self.cerebro = bt.Cerebro()
        self.cerebro.broker.setcash(initial_cash)
        self.cerebro.broker.setcommission(commission=commission)
        self.initial_cash = initial_cash

    def add_strategy(self, strategy_class, **kwargs):
        """Add a strategy to the backtesting engine."""
        self.cerebro.addstrategy(strategy_class, **kwargs)

    def add_data(self, data: pd.DataFrame, name: str = 'data'):
        """
        Add price data to the backtesting engine.

        Args:
            data: DataFrame with OHLCV data
            name: Name for the data feed
        """
        data_feed = bt.feeds.PandasData(dataname=data)
        self.cerebro.adddata(data_feed, name=name)

    def add_analyzers(self):
        """Add standard analyzers to the backtesting engine."""
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        self.cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')

    def run(self) -> Dict[str, Any]:
        """
        Run the backtest.

        Returns:
            Dictionary containing backtest results
        """
        print(f'Starting Portfolio Value: {self.cerebro.broker.getvalue():.2f}')

        results = self.cerebro.run()
        final_value = self.cerebro.broker.getvalue()

        print(f'Final Portfolio Value: {final_value:.2f}')
        print(f'Total Return: {((final_value - self.initial_cash) / self.initial_cash * 100):.2f}%')

        # Extract strategy (first element of results)
        strat = results[0]

        # Extract analyzer data safely
        analyzer_results = {}
        if hasattr(strat, 'analyzers'):
            analyzers = strat.analyzers

            # SharpeRatio
            if hasattr(analyzers, 'sharpe'):
                try:
                    sharpe_analysis = analyzers.sharpe.get_analysis()
                    analyzer_results['sharpe_ratio'] = sharpe_analysis.get('sharperatio', None)
                except Exception as e:
                    analyzer_results['sharpe_ratio'] = None

            # DrawDown
            if hasattr(analyzers, 'drawdown'):
                try:
                    dd_analysis = analyzers.drawdown.get_analysis()
                    analyzer_results['max_drawdown'] = dd_analysis.get('max', {}).get('drawdown', None)
                    analyzer_results['max_drawdown_length'] = dd_analysis.get('max', {}).get('len', None)
                except Exception as e:
                    analyzer_results['max_drawdown'] = None

            # TradeAnalyzer
            if hasattr(analyzers, 'trades'):
                try:
                    trade_analysis = analyzers.trades.get_analysis()
                    analyzer_results['total_trades'] = trade_analysis.get('total', {}).get('total', 0)
                    analyzer_results['won_trades'] = trade_analysis.get('won', {}).get('total', 0)
                    analyzer_results['lost_trades'] = trade_analysis.get('lost', {}).get('total', 0)

                    # Win rate
                    if analyzer_results['total_trades'] > 0:
                        analyzer_results['win_rate'] = (analyzer_results['won_trades'] / analyzer_results['total_trades']) * 100
                    else:
                        analyzer_results['win_rate'] = 0

                    # Average win/loss
                    analyzer_results['avg_win'] = trade_analysis.get('won', {}).get('pnl', {}).get('average', None)
                    analyzer_results['avg_loss'] = trade_analysis.get('lost', {}).get('pnl', {}).get('average', None)
                except Exception as e:
                    analyzer_results['total_trades'] = 0

            # Returns
            if hasattr(analyzers, 'returns'):
                try:
                    returns_analysis = analyzers.returns.get_analysis()
                    analyzer_results['total_return_analyzer'] = returns_analysis.get('rtot', None)
                    analyzer_results['average_return'] = returns_analysis.get('ravg', None)
                except Exception as e:
                    pass

        return {
            'initial_value': self.initial_cash,
            'final_value': final_value,
            'return_pct': (final_value - self.initial_cash) / self.initial_cash * 100,
            'strategy_results': strat,
            'analyzers': analyzer_results
        }

    def plot(self, **kwargs):
        """Plot the backtest results."""
        self.cerebro.plot(**kwargs)
