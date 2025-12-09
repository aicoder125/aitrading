"""
IBKR Connector
Handles connection and communication with Interactive Brokers.
"""

from ib_insync import IB, Stock, MarketOrder, LimitOrder, util
from typing import List, Optional
import asyncio
from loguru import logger


class IBKRConnector:
    """Interactive Brokers connection manager."""

    def __init__(self,
                 host: str = '127.0.0.1',
                 port: int = 7497,
                 client_id: int = 1):
        """
        Initialize IBKR connector.

        Args:
            host: TWS/Gateway host
            port: TWS/Gateway port (7497 for paper, 7496 for live)
            client_id: Unique client identifier
        """
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ib = IB()

    def connect(self) -> bool:
        """
        Connect to IBKR TWS/Gateway.

        Returns:
            True if connection successful
        """
        try:
            self.ib.connect(self.host, self.port, clientId=self.client_id)
            logger.info(f"Connected to IBKR at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to IBKR: {e}")
            return False

    def disconnect(self):
        """Disconnect from IBKR."""
        if self.ib.isConnected():
            self.ib.disconnect()
            logger.info("Disconnected from IBKR")

    def get_account_summary(self) -> dict:
        """
        Get account summary information.

        Returns:
            Dictionary with account information
        """
        if not self.ib.isConnected():
            logger.error("Not connected to IBKR")
            return {}

        account_values = self.ib.accountValues()
        summary = {}

        for av in account_values:
            if av.tag in ['NetLiquidation', 'TotalCashValue', 'BuyingPower']:
                summary[av.tag] = float(av.value)

        return summary

    def get_positions(self) -> List:
        """
        Get current positions.

        Returns:
            List of Position objects
        """
        if not self.ib.isConnected():
            logger.error("Not connected to IBKR")
            return []

        return self.ib.positions()

    def create_stock_contract(self, symbol: str, exchange: str = 'SMART', currency: str = 'USD') -> Stock:
        """
        Create a stock contract.

        Args:
            symbol: Stock ticker symbol
            exchange: Exchange name
            currency: Currency

        Returns:
            Stock contract object
        """
        return Stock(symbol, exchange, currency)

    def place_market_order(self, contract, quantity: int, action: str = 'BUY'):
        """
        Place a market order.

        Args:
            contract: Contract object
            quantity: Number of shares
            action: 'BUY' or 'SELL'

        Returns:
            Trade object
        """
        if not self.ib.isConnected():
            logger.error("Not connected to IBKR")
            return None

        order = MarketOrder(action, quantity)
        trade = self.ib.placeOrder(contract, order)
        logger.info(f"Placed {action} market order for {quantity} shares of {contract.symbol}")

        return trade

    def place_limit_order(self, contract, quantity: int, limit_price: float, action: str = 'BUY'):
        """
        Place a limit order.

        Args:
            contract: Contract object
            quantity: Number of shares
            limit_price: Limit price
            action: 'BUY' or 'SELL'

        Returns:
            Trade object
        """
        if not self.ib.isConnected():
            logger.error("Not connected to IBKR")
            return None

        order = LimitOrder(action, quantity, limit_price)
        trade = self.ib.placeOrder(contract, order)
        logger.info(f"Placed {action} limit order for {quantity} shares of {contract.symbol} at ${limit_price}")

        return trade

    def get_market_data(self, contract):
        """
        Request market data for a contract.

        Args:
            contract: Contract object

        Returns:
            Market data ticker
        """
        if not self.ib.isConnected():
            logger.error("Not connected to IBKR")
            return None

        self.ib.qualifyContracts(contract)
        ticker = self.ib.reqMktData(contract)
        self.ib.sleep(2)  # Wait for data to populate

        return ticker
