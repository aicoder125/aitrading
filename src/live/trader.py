"""
Live Trader
Executes trading strategies in real-time.
"""

from typing import Dict, Any
from loguru import logger
from .ib_connector import IBKRConnector


class LiveTrader:
    """Manages live trading execution."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize live trader.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.connector = IBKRConnector(
            host=config.get('ib_host', '127.0.0.1'),
            port=config.get('ib_port', 7497),
            client_id=config.get('ib_client_id', 1)
        )
        self.is_running = False

    def start(self) -> bool:
        """
        Start the live trader.

        Returns:
            True if started successfully
        """
        if not self.connector.connect():
            logger.error("Failed to start live trader")
            return False

        self.is_running = True
        logger.info("Live trader started")

        # Display account info
        account_info = self.connector.get_account_summary()
        logger.info(f"Account Summary: {account_info}")

        return True

    def stop(self):
        """Stop the live trader."""
        self.is_running = False
        self.connector.disconnect()
        logger.info("Live trader stopped")

    def execute_trade(self, symbol: str, quantity: int, action: str = 'BUY', order_type: str = 'MARKET', limit_price: float = None):
        """
        Execute a trade.

        Args:
            symbol: Stock ticker
            quantity: Number of shares
            action: 'BUY' or 'SELL'
            order_type: 'MARKET' or 'LIMIT'
            limit_price: Limit price (required for LIMIT orders)
        """
        if not self.is_running:
            logger.error("Trader is not running")
            return None

        contract = self.connector.create_stock_contract(symbol)

        if order_type == 'MARKET':
            trade = self.connector.place_market_order(contract, quantity, action)
        elif order_type == 'LIMIT':
            if limit_price is None:
                logger.error("Limit price required for LIMIT orders")
                return None
            trade = self.connector.place_limit_order(contract, quantity, limit_price, action)
        else:
            logger.error(f"Unknown order type: {order_type}")
            return None

        return trade

    def get_positions(self):
        """Get current positions."""
        if not self.is_running:
            logger.error("Trader is not running")
            return []

        return self.connector.get_positions()
