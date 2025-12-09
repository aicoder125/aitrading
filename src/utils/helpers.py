"""
Helper Functions
Various utility functions.
"""

import re
from typing import Optional


def validate_symbol(symbol: str) -> bool:
    """
    Validate stock ticker symbol.

    Args:
        symbol: Ticker symbol

    Returns:
        True if valid
    """
    if not symbol:
        return False

    # Basic validation: 1-5 uppercase letters
    pattern = r'^[A-Z]{1,5}$'
    return bool(re.match(pattern, symbol.upper()))


def calculate_position_size(account_value: float,
                           risk_per_trade: float = 0.02,
                           stop_loss_pct: float = 0.05) -> int:
    """
    Calculate position size based on risk management.

    Args:
        account_value: Total account value
        risk_per_trade: Percentage of account to risk per trade (default 2%)
        stop_loss_pct: Stop loss percentage (default 5%)

    Returns:
        Number of shares to trade
    """
    if stop_loss_pct <= 0:
        return 0

    risk_amount = account_value * risk_per_trade
    position_size = int(risk_amount / stop_loss_pct)

    return max(position_size, 1)  # At least 1 share


def format_currency(value: float, currency: str = 'USD') -> str:
    """
    Format value as currency.

    Args:
        value: Numeric value
        currency: Currency code

    Returns:
        Formatted string
    """
    if currency == 'USD':
        return f'${value:,.2f}'
    else:
        return f'{value:,.2f} {currency}'


def calculate_returns(initial_value: float, final_value: float) -> dict:
    """
    Calculate various return metrics.

    Args:
        initial_value: Starting value
        final_value: Ending value

    Returns:
        Dictionary with return metrics
    """
    absolute_return = final_value - initial_value
    percentage_return = (absolute_return / initial_value) * 100 if initial_value > 0 else 0

    return {
        'absolute': absolute_return,
        'percentage': percentage_return,
        'initial': initial_value,
        'final': final_value
    }
