# Strategy Development Guide

## Overview

This guide explains how to develop and test trading strategies in the AI Trading System.

## Strategy Structure

All strategies inherit from `BaseStrategy` which provides common functionality:

```python
from src.strategies import BaseStrategy
import backtrader as bt

class MyStrategy(BaseStrategy):
    params = (
        ('param1', default_value),
    )

    def __init__(self):
        super().__init__()
        # Initialize indicators here

    def next(self):
        # Strategy logic here
        pass
```

## Example: Simple Moving Average Strategy

```python
import backtrader as bt
from src.strategies import BaseStrategy

class SMACrossover(BaseStrategy):
    params = (
        ('fast_period', 10),
        ('slow_period', 30),
        ('printlog', True),
    )

    def __init__(self):
        super().__init__()
        self.sma_fast = bt.indicators.SMA(period=self.params.fast_period)
        self.sma_slow = bt.indicators.SMA(period=self.params.slow_period)
        self.crossover = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.crossover > 0:
                self.buy()
        else:
            if self.crossover < 0:
                self.sell()
```

## Available Indicators

Backtrader provides many built-in indicators:

- Moving Averages: SMA, EMA, WMA
- Oscillators: RSI, MACD, Stochastic
- Volatility: Bollinger Bands, ATR
- Volume: OBV, Volume
- And many more...

See [Backtrader Indicators](https://www.backtrader.com/docu/indautoref/) for complete list.

## Testing Your Strategy

1. **Create test script**
2. **Load historical data**
3. **Run backtest**
4. **Analyze results**

```python
from datetime import datetime
from src.backtest import BacktestEngine
from src.data import YahooFinanceLoader

# Load data
loader = YahooFinanceLoader()
data = loader.fetch_data('AAPL', datetime(2020, 1, 1), datetime(2024, 1, 1))

# Run backtest
engine = BacktestEngine()
engine.add_strategy(MyStrategy)
engine.add_data(data)
engine.add_analyzers()
results = engine.run()
```

## Best Practices

1. **Start Simple**: Begin with simple strategies and add complexity gradually
2. **Avoid Overfitting**: Don't optimize too many parameters
3. **Test Robustness**: Test on different time periods and instruments
4. **Consider Costs**: Include realistic commissions and slippage
5. **Risk Management**: Always include stop losses and position sizing
6. **Paper Trade First**: Test in paper trading before going live

## Common Patterns

### Entry on Indicator Cross
```python
if self.indicator1[0] > self.indicator2[0]:
    self.buy()
```

### Exit on Stop Loss
```python
if self.position:
    if self.dataclose[0] < self.buy_price * 0.95:  # 5% stop loss
        self.sell()
```

### Position Sizing
```python
size = int(self.broker.cash * 0.02 / self.dataclose[0])  # Risk 2% per trade
self.buy(size=size)
```

## Debugging Strategies

Use the built-in logging:

```python
def next(self):
    self.log(f'Close: {self.dataclose[0]:.2f}')
    self.log(f'Position: {self.position.size}')
```

## Next Steps

- Review existing strategies in `src/strategies/`
- Read Backtrader documentation
- Experiment with different indicators
- Optimize parameters systematically
