"""
Performance Analyzer
Analyzes and visualizes backtesting results.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
import matplotlib.pyplot as plt


class PerformanceAnalyzer:
    """Analyzes trading strategy performance."""

    def __init__(self, results: Dict[str, Any]):
        """
        Initialize analyzer with backtest results.

        Args:
            results: Results from BacktestEngine
        """
        self.results = results
        self.strategy = results.get('strategy_results')

    def get_metrics(self) -> Dict[str, float]:
        """
        Calculate performance metrics.

        Returns:
            Dictionary of performance metrics
        """
        metrics = {
            'initial_value': self.results.get('initial_value', 0),
            'final_value': self.results.get('final_value', 0),
            'total_return_pct': self.results.get('return_pct', 0),
        }

        # Add pre-extracted analyzer data if available
        analyzer_data = self.results.get('analyzers', {})

        if analyzer_data:
            # Add all analyzer metrics that were successfully extracted
            metrics.update(analyzer_data)
        else:
            # Fallback: try to extract from strategy object (old method)
            self.strategy = self.results.get('strategy_results')
            if self.strategy and hasattr(self.strategy, 'analyzers'):
                # Original code here as fallback
                if hasattr(self.strategy.analyzers, 'sharpe'):
                    try:
                        sharpe = self.strategy.analyzers.sharpe.get_analysis()
                        metrics['sharpe_ratio'] = sharpe.get('sharperatio', None)
                    except:
                        pass

                if hasattr(self.strategy.analyzers, 'drawdown'):
                    try:
                        dd = self.strategy.analyzers.drawdown.get_analysis()
                        metrics['max_drawdown'] = dd.get('max', {}).get('drawdown', 0)
                    except:
                        pass

                if hasattr(self.strategy.analyzers, 'trades'):
                    try:
                        trades = self.strategy.analyzers.trades.get_analysis()
                        metrics['total_trades'] = trades.get('total', {}).get('total', 0)
                        metrics['won_trades'] = trades.get('won', {}).get('total', 0)
                        metrics['lost_trades'] = trades.get('lost', {}).get('total', 0)

                        if metrics['total_trades'] > 0:
                            metrics['win_rate'] = metrics['won_trades'] / metrics['total_trades'] * 100
                    except:
                        pass

        return metrics

    def print_metrics(self):
        """Print performance metrics to console."""
        metrics = self.get_metrics()

        print("\n" + "="*50)
        print("PERFORMANCE METRICS")
        print("="*50)

        # Portfolio Performance
        print("\nPortfolio Performance:")
        print(f"  Initial Value: ${metrics.get('initial_value', 0):,.2f}")
        print(f"  Final Value: ${metrics.get('final_value', 0):,.2f}")
        print(f"  Total Return: {metrics.get('total_return_pct', 0):.2f}%")

        # Risk Metrics
        if 'sharpe_ratio' in metrics and metrics['sharpe_ratio'] is not None:
            print("\nRisk Metrics:")
            print(f"  Sharpe Ratio: {metrics['sharpe_ratio']:.3f}")

        if 'max_drawdown' in metrics and metrics['max_drawdown'] is not None:
            if 'sharpe_ratio' not in metrics or metrics['sharpe_ratio'] is None:
                print("\nRisk Metrics:")
            print(f"  Max Drawdown: {metrics['max_drawdown']:.2f}%")
            if 'max_drawdown_length' in metrics and metrics['max_drawdown_length'] is not None:
                print(f"  Max Drawdown Length: {metrics['max_drawdown_length']} bars")

        # Trade Statistics
        if 'total_trades' in metrics and metrics['total_trades'] > 0:
            print("\nTrade Statistics:")
            print(f"  Total Trades: {metrics['total_trades']}")
            print(f"  Winning Trades: {metrics.get('won_trades', 0)}")
            print(f"  Losing Trades: {metrics.get('lost_trades', 0)}")
            print(f"  Win Rate: {metrics.get('win_rate', 0):.2f}%")

            if 'avg_win' in metrics and metrics['avg_win'] is not None:
                print(f"  Average Win: ${metrics['avg_win']:.2f}")
            if 'avg_loss' in metrics and metrics['avg_loss'] is not None:
                print(f"  Average Loss: ${metrics['avg_loss']:.2f}")

        print("\n" + "="*50 + "\n")
