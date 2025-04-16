"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 29/11/2024
"""
import argparse
import os
import sys

from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.getcwd())

import uvicorn
import nest_asyncio

nest_asyncio.apply()

from fastapi import FastAPI
from pyngrok import ngrok

from ibtrading.api import health_router, auth_router, trade_router, trade_router_v2
from ibtrading.settings import Settings
from ibtrading.utils import loggerutil

logger = loggerutil.get_logger(__name__)
app = FastAPI(
    title="IB Trading API",
    description="Tradingview Webhook API for IB Trading",
    version="1.0.0",
    author="Ashok Kumar Pant",
    email="ashok@treeleaf.ai",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health_router.router, prefix="")
app.include_router(auth_router.router, prefix="")
app.include_router(trade_router.router, prefix="")
app.include_router(trade_router_v2.router)


def setup_ngrok():
    try:
        # ngrok.set_auth_token('YOUR_NGROK_AUTH_TOKEN')
        tunnel = ngrok.connect(Settings.TV_WEBHOOK_API_PORT,
                               url=Settings.NGROK_URL)
        logger.debug(f"Public URL: {tunnel.public_url}")
    except Exception as e:
        logger.exception(f"Error setting up ngrok: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IB Trading API")
    parser.add_argument('--enable-ngrok', action='store_true', help="Enable ngrok tunnel")
    args = parser.parse_args()
    loggerutil.setup_logging()
    if args.enable_ngrok:
        setup_ngrok()

    uvicorn.run(
        "main:app",
        host=Settings.TV_WEBHOOK_API_HOST,
        port=Settings.TV_WEBHOOK_API_PORT,
        reload=Settings.DEBUG,
        loop="asyncio",
    )
