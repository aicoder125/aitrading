# AI Trading System

A professional quantitative trading system with backtesting and live trading capabilities using Backtrader and Interactive Brokers.

## Features

- **Backtesting Engine**: Test strategies on historical data using Backtrader
- **Live Trading**: Execute trades in real-time via Interactive Brokers (IBKR)
- **Strategy Framework**: Extensible strategy base classes
- **Data Management**: Fetch data from Yahoo Finance and other sources
- **Performance Analysis**: Comprehensive performance metrics and visualization
- **Configuration Management**: YAML and environment variable configuration
- **Logging**: Structured logging with Loguru

## Project Structure

```
aitrading/
├── src/                    # Source code
│   ├── backtest/          # Backtesting engine and analyzers
│   ├── live/              # Live trading and IBKR connection
│   ├── strategies/        # Trading strategies
│   ├── data/              # Data fetching and processing
│   ├── config/            # Configuration management
│   └── utils/             # Utility functions
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── scripts/              # Executable scripts
├── data/                 # Data storage
│   ├── raw/             # Raw data
│   ├── processed/       # Processed data
│   └── cache/           # Cached data
├── logs/                # Log files
├── docs/                # Documentation
├── notebooks/           # Jupyter notebooks
├── config.yaml          # Configuration file
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd aitrading
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Install TA-Lib (optional)**
   ```bash
   # macOS
   brew install ta-lib

   # Ubuntu/Debian
   sudo apt-get install ta-lib

   # Then uncomment ta-lib in requirements.txt and install
   pip install ta-lib
   ```

## Quick Start

### Run a Backtest

```bash
python scripts/run_backtest.py
```

### Run Live Trading

```bash
# Make sure IBKR TWS or Gateway is running
python scripts/run_live.py
```

### Using Python API

```python
from datetime import datetime
from src.backtest import BacktestEngine, PerformanceAnalyzer
from src.strategies import SMACrossover
from src.data import YahooFinanceLoader

# Load data
loader = YahooFinanceLoader()
data = loader.fetch_data('AAPL', datetime(2020, 1, 1), datetime(2024, 1, 1))

# Run backtest
engine = BacktestEngine(initial_cash=100000)
engine.add_strategy(SMACrossover, fast_period=10, slow_period=30)
engine.add_data(data)
engine.add_analyzers()

results = engine.run()

# Analyze results
analyzer = PerformanceAnalyzer(results)
analyzer.print_metrics()
engine.plot()
```

## Configuration

Edit `config.yaml` to customize settings:

```yaml
backtest:
  initial_cash: 100000.0
  commission: 0.001

ibkr:
  host: "127.0.0.1"
  port: 7497  # 7497 for paper, 7496 for live
  client_id: 1
```

## Creating Custom Strategies

```python
from src.strategies import BaseStrategy
import backtrader as bt

class MyStrategy(BaseStrategy):
    params = (
        ('period', 20),
    )

    def __init__(self):
        super().__init__()
        self.sma = bt.indicators.SMA(period=self.params.period)

    def next(self):
        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                self.sell()
```

## Interactive Brokers Setup

1. **Download TWS or IB Gateway**
   - Download from [Interactive Brokers](https://www.interactivebrokers.com)

2. **Enable API Access**
   - Open TWS/Gateway
   - Go to Edit > Global Configuration > API > Settings
   - Enable "Enable ActiveX and Socket Clients"
   - Set Socket port to 7497 (paper) or 7496 (live)

3. **Configure Connection**
   - Update `config.yaml` or `.env` with your settings
   - Use port 7497 for paper trading
   - Use port 7496 for live trading

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/
```

## Logging

Logs are stored in the `logs/` directory:
- `app.log`: All application logs
- `error.log`: Error logs only

## Data Sources

- **Yahoo Finance**: Default data source via `yfinance`
- **IBKR**: Live market data (requires connection)

## Risk Warning

This software is for educational purposes only. Trading involves substantial risk of loss. Always test strategies thoroughly in paper trading before using real money.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
