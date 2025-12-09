"""
Logger Setup
Configures logging for the application.
"""

import sys
from pathlib import Path
from loguru import logger


def setup_logger(log_dir: str = 'logs', log_level: str = 'INFO', log_format: str = None):
    """
    Configure application logger.

    Args:
        log_dir: Directory for log files
        log_level: Logging level
        log_format: Custom log format
    """
    # Create log directory
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Remove default handler
    logger.remove()

    # Default format
    if log_format is None:
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

    # Console handler
    logger.add(
        sys.stdout,
        format=log_format,
        level=log_level,
        colorize=True
    )

    # File handler - all logs
    logger.add(
        f"{log_dir}/app.log",
        format=log_format,
        level=log_level,
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )

    # File handler - errors only
    logger.add(
        f"{log_dir}/error.log",
        format=log_format,
        level="ERROR",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )

    logger.info(f"Logger initialized with level: {log_level}")
