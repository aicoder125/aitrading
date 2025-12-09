"""
Strategies Module
Trading strategy implementations.
"""

from .base_strategy import BaseStrategy
from .sma_crossover import SMACrossover

__all__ = ['BaseStrategy', 'SMACrossover']
