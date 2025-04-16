"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 29/11/2024
"""

import os

import pytz
from dotenv import load_dotenv

load_dotenv()


class Settings:
    TV_WEBHOOK_API_HOST: str = os.getenv("TV_WEBHOOK_API_HOST", "0.0.0.0")
    TV_WEBHOOK_API_PORT: int = int(os.getenv("TV_WEBHOOK_API_PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "")

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    IBKR_HOST: str = os.getenv("IBKR_HOST", "127.0.0.1")
    IBKR_PORT: int = int(os.getenv("IBKR_PORT", 7497))  # 7496 for Real, 7497 for Paper Workstation
    # IBKR_PORT: int = int(os.getenv("IBKR_PORT", 4002))  # 4001 for Real , 4002 for Paper Gateway
    IBKR_CLIENT_ID: int = int(os.getenv("IBKR_CLIENT_ID", 1))
    IBKR_ACCOUNT_ID: str = os.getenv("IBKR_ACCOUNT_ID", None)
    IBKR_MARKET_DATA_TYPE: int = os.getenv("IBKR_MARKET_DATA_TYPE", 1)

    NGROK_URL: str = os.getenv("NGROK_URL", "grossly-prepared-cobra.ngrok-free.app")
    HOME_DIR = os.getenv("HOME")
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{HOME_DIR}/algotrade_data/algotrade.db")

    TIMEZONE_STR = os.getenv("TIMEZONE", "America/New_York")
    TIMEZONE = pytz.timezone(TIMEZONE_STR)
    JOIN_SYMBOL: str = "-"
