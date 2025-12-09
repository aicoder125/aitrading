"""
Yahoo Finance Data Loader
Fetches historical price data from Yahoo Finance.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
from typing import Optional
from loguru import logger
from .data_loader import DataLoader


class YahooFinanceLoader(DataLoader):
    """Yahoo Finance data loader implementation."""

    def fetch_data(self,
                   symbol: str,
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None,
                   interval: str = '1d',
                   **kwargs) -> pd.DataFrame:
        """
        Fetch historical price data from Yahoo Finance.

        Args:
            symbol: Stock ticker symbol
            start_date: Start date for data
            end_date: End date for data
            interval: Data interval (1d, 1h, etc.)
            **kwargs: Additional yfinance parameters

        Returns:
            DataFrame with OHLCV data
        """
        try:
            logger.info(f"Fetching data for {symbol} from Yahoo Finance")

            ticker = yf.Ticker(symbol)
            df = ticker.history(
                start=start_date,
                end=end_date,
                interval=interval,
                **kwargs
            )

            if df.empty:
                logger.warning(f"No data retrieved for {symbol}")
                return pd.DataFrame()

            # Clean and validate
            df = self.clean_data(df)

            if not self.validate_data(df):
                logger.error(f"Invalid data structure for {symbol}")
                return pd.DataFrame()

            logger.info(f"Successfully fetched {len(df)} rows for {symbol}")
            return df

        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()

    def fetch_multiple(self,
                      symbols: list,
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None,
                      **kwargs) -> dict:
        """
        Fetch data for multiple symbols.

        Args:
            symbols: List of stock ticker symbols
            start_date: Start date for data
            end_date: End date for data
            **kwargs: Additional parameters

        Returns:
            Dictionary mapping symbols to DataFrames
        """
        data = {}
        for symbol in symbols:
            df = self.fetch_data(symbol, start_date, end_date, **kwargs)
            if not df.empty:
                data[symbol] = df

        return data
