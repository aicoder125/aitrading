"""
Settings
System-wide settings and configuration.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class BacktestSettings:
    """Backtesting configuration."""
    initial_cash: float = 100000.0
    commission: float = 0.001
    slippage: float = 0.0
    stake: int = 100  # Number of shares per trade


@dataclass
class IBKRSettings:
    """Interactive Brokers configuration."""
    host: str = '127.0.0.1'
    port: int = 7497  # 7497 for paper, 7496 for live
    client_id: int = 1
    account: Optional[str] = None


@dataclass
class DataSettings:
    """Data fetching configuration."""
    default_source: str = 'yahoo'
    cache_enabled: bool = True
    cache_dir: str = 'data/cache'


@dataclass
class LogSettings:
    """Logging configuration."""
    level: str = 'INFO'
    log_dir: str = 'logs'
    format: str = '{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}'


@dataclass
class Settings:
    """Main settings container."""
    backtest: BacktestSettings = None
    ibkr: IBKRSettings = None
    data: DataSettings = None
    log: LogSettings = None

    def __post_init__(self):
        """Initialize nested settings."""
        if self.backtest is None:
            self.backtest = BacktestSettings()
        if self.ibkr is None:
            self.ibkr = IBKRSettings()
        if self.data is None:
            self.data = DataSettings()
        if self.log is None:
            self.log = LogSettings()
