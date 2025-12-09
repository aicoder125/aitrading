"""
Data Module
Handles data fetching, processing, and storage.
"""

from .data_loader import DataLoader
from .yfinance_loader import YahooFinanceLoader

__all__ = ['DataLoader', 'YahooFinanceLoader']
