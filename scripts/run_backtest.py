#!/usr/bin/env python3
"""
Run Backtest Script
SMA Crossover strategy backtest for TSLA and QQQ.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.backtest import BacktestEngine, PerformanceAnalyzer
from src.strategies import SMACrossover
from src.data import YahooFinanceLoader


def run_backtest_for_symbol(symbol: str, data_loader: YahooFinanceLoader):
    """
    Run backtest for a single symbol.

    Args:
        symbol: Stock ticker symbol
        data_loader: Data loader instance
    """
    print("\n" + "="*70)
    print(f"BACKTESTING {symbol}")
    print("="*70)

    # Fetch data
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 12, 1)

    print(f"Fetching data for {symbol} from {start_date.date()} to {end_date.date()}...")
    data = data_loader.fetch_data(symbol, start_date, end_date)

    if data.empty:
        print(f"No data fetched for {symbol}. Skipping.")
        return

    print(f"Loaded {len(data)} bars of data")

    # Initialize backtest engine
    engine = BacktestEngine(
        initial_cash=100000.0,
        commission=0.001  # 0.1% commission
    )

    # Add SMA Crossover strategy
    engine.add_strategy(
        SMACrossover,
        fast_period=10,    # Fast SMA period
        slow_period=30,    # Slow SMA period
        printlog=True      # Print trade logs
    )

    # Add data
    engine.add_data(data, name=symbol)

    # Add analyzers (Sharpe Ratio, Drawdown, etc.)
    engine.add_analyzers()

    # Run backtest
    print(f"\nRunning backtest for {symbol}...")
    results = engine.run()

    # Analyze and print results
    print("\n" + "="*70)
    print(f"PERFORMANCE SUMMARY FOR {symbol}")
    print("="*70)

    try:
        analyzer = PerformanceAnalyzer(results)
        analyzer.print_metrics()
    except Exception as e:
        print(f"Note: Detailed metrics not available ({e})")
        print("Basic results shown above (Portfolio Value and Total Return)")

    # Note: Plotting disabled to avoid display issues in headless environments
    # To enable plotting, uncomment the lines below:
    # try:
    #     print(f"\nGenerating equity curve for {symbol}...")
    #     engine.plot()
    # except Exception as e:
    #     print(f"Note: Could not generate plot: {e}")

    print(f"Backtest for {symbol} completed!\n")


def main():
    """Run backtest for TSLA and QQQ."""
    print("\n" + "="*70)
    print("SMA CROSSOVER STRATEGY BACKTEST")
    print("Strategy: Buy on Golden Cross (Fast SMA > Slow SMA)")
    print("          Sell on Death Cross (Fast SMA < Slow SMA)")
    print("="*70)

    # Initialize data loader
    data_loader = YahooFinanceLoader()

    # List of symbols to backtest
    symbols = ['TSLA', 'QQQ']

    # Run backtest for each symbol
    for symbol in symbols:
        try:
            run_backtest_for_symbol(symbol, data_loader)
        except Exception as e:
            print(f"\nError running backtest for {symbol}: {e}\n")
            continue

    print("="*70)
    print("ALL BACKTESTS COMPLETED")
    print("="*70)


if __name__ == '__main__':
    main()
