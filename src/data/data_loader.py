"""
Data Loader
Abstract base class for data loaders.
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional
from datetime import datetime


class DataLoader(ABC):
    """Abstract base class for data loaders."""

    @abstractmethod
    def fetch_data(self,
                   symbol: str,
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None,
                   **kwargs) -> pd.DataFrame:
        """
        Fetch historical price data.

        Args:
            symbol: Stock ticker symbol
            start_date: Start date for data
            end_date: End date for data
            **kwargs: Additional parameters

        Returns:
            DataFrame with OHLCV data
        """
        pass

    @staticmethod
    def validate_data(df: pd.DataFrame) -> bool:
        """
        Validate OHLCV data structure.

        Args:
            df: DataFrame to validate

        Returns:
            True if valid
        """
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        return all(col in df.columns for col in required_columns)

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess data.

        Args:
            df: Raw DataFrame

        Returns:
            Cleaned DataFrame
        """
        # Remove NaN values
        df = df.dropna()

        # Ensure datetime index
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)

        # Sort by date
        df = df.sort_index()

        return df
