# API Reference

## Backtest Module

### BacktestEngine

```python
from src.backtest import BacktestEngine

engine = BacktestEngine(
    initial_cash=100000.0,
    commission=0.001,
    slippage=0.0
)
```

**Methods:**
- `add_strategy(strategy_class, **kwargs)`: Add a strategy
- `add_data(data, name='data')`: Add price data
- `add_analyzers()`: Add performance analyzers
- `run()`: Run the backtest
- `plot(**kwargs)`: Plot results

### PerformanceAnalyzer

```python
from src.backtest import PerformanceAnalyzer

analyzer = PerformanceAnalyzer(results)
metrics = analyzer.get_metrics()
analyzer.print_metrics()
```

**Methods:**
- `get_metrics()`: Get performance metrics dict
- `print_metrics()`: Print metrics to console

## Live Trading Module

### LiveTrader

```python
from src.live import LiveTrader

config = {
    'ib_host': '127.0.0.1',
    'ib_port': 7497,
    'ib_client_id': 1
}
trader = LiveTrader(config)
```

**Methods:**
- `start()`: Start the trader
- `stop()`: Stop the trader
- `execute_trade(symbol, quantity, action, order_type, limit_price)`: Execute trade
- `get_positions()`: Get current positions

### IBKRConnector

```python
from src.live import IBKRConnector

connector = IBKRConnector(host='127.0.0.1', port=7497, client_id=1)
connector.connect()
```

**Methods:**
- `connect()`: Connect to IBKR
- `disconnect()`: Disconnect
- `get_account_summary()`: Get account info
- `get_positions()`: Get positions
- `create_stock_contract(symbol, exchange, currency)`: Create contract
- `place_market_order(contract, quantity, action)`: Place market order
- `place_limit_order(contract, quantity, limit_price, action)`: Place limit order
- `get_market_data(contract)`: Get market data

## Data Module

### YahooFinanceLoader

```python
from src.data import YahooFinanceLoader

loader = YahooFinanceLoader()
data = loader.fetch_data('AAPL', start_date, end_date)
```

**Methods:**
- `fetch_data(symbol, start_date, end_date, interval)`: Fetch data for symbol
- `fetch_multiple(symbols, start_date, end_date)`: Fetch data for multiple symbols

## Strategies Module

### BaseStrategy

```python
from src.strategies import BaseStrategy

class MyStrategy(BaseStrategy):
    def next(self):
        # Your logic here
        pass
```

**Methods:**
- `log(txt, dt)`: Log message
- `notify_order(order)`: Order notification handler
- `notify_trade(trade)`: Trade notification handler
- `next()`: Strategy logic (override this)

## Configuration Module

### Settings

```python
from src.config import load_config

settings = load_config('config.yaml')
```

**Properties:**
- `backtest`: BacktestSettings
- `ibkr`: IBKRSettings
- `data`: DataSettings
- `log`: LogSettings

## Utilities Module

### Logger

```python
from src.utils import setup_logger

setup_logger(log_dir='logs', log_level='INFO')
```

### Helpers

```python
from src.utils import validate_symbol, calculate_position_size

is_valid = validate_symbol('AAPL')
size = calculate_position_size(account_value=100000, risk_per_trade=0.02)
```
