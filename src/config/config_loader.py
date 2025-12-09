"""
Configuration Loader
Loads configuration from files and environment variables.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any
from loguru import logger
from dotenv import load_dotenv
from .settings import Settings, BacktestSettings, IBKRSettings, DataSettings, LogSettings


def load_config(config_file: str = None) -> Settings:
    """
    Load configuration from file and environment variables.

    Args:
        config_file: Path to configuration file (JSON or YAML)

    Returns:
        Settings object
    """
    # Load environment variables
    load_dotenv()

    # Default settings
    settings = Settings()

    # Load from file if provided
    if config_file and os.path.exists(config_file):
        config_data = _load_config_file(config_file)
        settings = _parse_config(config_data)

    # Override with environment variables
    settings = _override_from_env(settings)

    return settings


def _load_config_file(file_path: str) -> Dict[str, Any]:
    """Load configuration file (JSON or YAML)."""
    try:
        with open(file_path, 'r') as f:
            if file_path.endswith('.json'):
                return json.load(f)
            elif file_path.endswith(('.yaml', '.yml')):
                return yaml.safe_load(f)
            else:
                logger.warning(f"Unknown config file format: {file_path}")
                return {}
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        return {}


def _parse_config(config_data: Dict[str, Any]) -> Settings:
    """Parse configuration dictionary into Settings object."""
    backtest = BacktestSettings(**config_data.get('backtest', {}))
    ibkr = IBKRSettings(**config_data.get('ibkr', {}))
    data = DataSettings(**config_data.get('data', {}))
    log = LogSettings(**config_data.get('log', {}))

    return Settings(
        backtest=backtest,
        ibkr=ibkr,
        data=data,
        log=log
    )


def _override_from_env(settings: Settings) -> Settings:
    """Override settings with environment variables."""
    # IBKR settings
    if os.getenv('IBKR_HOST'):
        settings.ibkr.host = os.getenv('IBKR_HOST')
    if os.getenv('IBKR_PORT'):
        settings.ibkr.port = int(os.getenv('IBKR_PORT'))
    if os.getenv('IBKR_CLIENT_ID'):
        settings.ibkr.client_id = int(os.getenv('IBKR_CLIENT_ID'))

    # Backtest settings
    if os.getenv('INITIAL_CASH'):
        settings.backtest.initial_cash = float(os.getenv('INITIAL_CASH'))
    if os.getenv('COMMISSION'):
        settings.backtest.commission = float(os.getenv('COMMISSION'))

    # Log settings
    if os.getenv('LOG_LEVEL'):
        settings.log.level = os.getenv('LOG_LEVEL')

    return settings
