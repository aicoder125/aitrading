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

    def add_optimization_strategy(self, strategy_class, **param_ranges):
        """
        Add a strategy for parameter optimization.

        Args:
            strategy_class: Strategy class to optimize
            **param_ranges: Parameter ranges for optimization
                Example: fast_period=range(5, 20), slow_period=range(25, 50)
        """
        self.cerebro.optstrategy(strategy_class, **param_ranges)

    def run_optimization(self) -> list:
        """
        Run parameter optimization.

        Returns:
            List of optimization results with parameters and metrics
        """
        print(f'Starting Parameter Optimization...')
        print(f'Initial Cash: {self.initial_cash:.2f}')

        # Run optimization (optreturn=False to get full strategy objects)
        opt_results = self.cerebro.run(optreturn=False)

        print(f'\nOptimization completed. Tested {len(opt_results)} parameter combinations.')

        # Extract results
        results_data = []
        for result in opt_results:
            strat = result[0]

            # Extract parameters
            params = {
                'fast_period': strat.params.fast_period,
                'slow_period': strat.params.slow_period,
            }

            # Extract analyzer data
            metrics = {}

            # Get final portfolio value from broker
            if hasattr(strat, 'broker'):
                final_value = strat.broker.getvalue()
                metrics['final_value'] = final_value
                metrics['total_return'] = ((final_value - self.initial_cash) / self.initial_cash) * 100
            else:
                metrics['final_value'] = self.initial_cash
                metrics['total_return'] = 0

            if hasattr(strat, 'analyzers'):
                analyzers = strat.analyzers

                # Sharpe Ratio
                if hasattr(analyzers, 'sharpe'):
                    try:
                        sharpe_analysis = analyzers.sharpe.get_analysis()
                        metrics['sharpe_ratio'] = sharpe_analysis.get('sharperatio', None)
                    except:
                        metrics['sharpe_ratio'] = None

                # DrawDown
                if hasattr(analyzers, 'drawdown'):
                    try:
                        dd_analysis = analyzers.drawdown.get_analysis()
                        metrics['max_drawdown'] = dd_analysis.get('max', {}).get('drawdown', None)
                    except:
                        metrics['max_drawdown'] = None

                # Trade Analysis
                if hasattr(analyzers, 'trades'):
                    try:
                        trade_analysis = analyzers.trades.get_analysis()
                        metrics['total_trades'] = trade_analysis.get('total', {}).get('total', 0)
                        metrics['won_trades'] = trade_analysis.get('won', {}).get('total', 0)

                        if metrics['total_trades'] > 0:
                            metrics['win_rate'] = (metrics['won_trades'] / metrics['total_trades']) * 100
                        else:
                            metrics['win_rate'] = 0
                    except:
                        metrics['total_trades'] = 0
                        metrics['win_rate'] = 0

            results_data.append({
                'params': params,
                'metrics': metrics
            })

        return results_data
