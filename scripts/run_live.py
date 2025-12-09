#!/usr/bin/env python3
"""
Run Live Trading Script
Example script to run live trading.
"""

import sys
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.live import LiveTrader
from src.config import load_config
from src.utils import setup_logger
from loguru import logger


def main():
    """Run live trading example."""
    # Load configuration
    config = load_config('config.yaml')
    setup_logger(config.log.log_dir, config.log.level)

    logger.info("Starting live trading system...")

    # Initialize trader
    trader_config = {
        'ib_host': config.ibkr.host,
        'ib_port': config.ibkr.port,
        'ib_client_id': config.ibkr.client_id
    }

    trader = LiveTrader(trader_config)

    # Start trader
    if not trader.start():
        logger.error("Failed to start trader")
        return

    try:
        # Display positions
        positions = trader.get_positions()
        logger.info(f"Current positions: {len(positions)}")

        for pos in positions:
            logger.info(f"  {pos.contract.symbol}: {pos.position} shares @ ${pos.avgCost:.2f}")

        # Example: Place a market order (commented out for safety)
        # trader.execute_trade('AAPL', 10, 'BUY', 'MARKET')

        # Keep running
        logger.info("Trader is running. Press Ctrl+C to stop.")
        while True:
            time.sleep(60)

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        trader.stop()


if __name__ == '__main__':
    main()
