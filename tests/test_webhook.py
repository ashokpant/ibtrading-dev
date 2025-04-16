"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 29/11/2024
"""
from unittest import TestCase

import requests


class TestWebhookAPI(TestCase):
    # API_HOST = 'http://localhost:8008'
    API_HOST = "https://grossly-prepared-cobra.ngrok-free.app"

    def test_webhook_success(self):
        payload = {'action': 'sell', 'contracts': '1', 'symbol': 'NQ1!', 'position_size': '0',
                   'market_position': 'flat', 'market_position_size': '0', 'time': '2024-11-29T08:03:00Z',
                   'close': '20900.50', 'open': '20899.00', 'high': '20901.50', 'low': '20899.00', 'volume': '42',
                   'timeframe': '1', 'exchange': 'CME_MINI_DL', 'timenow': '2024-11-29T08:13:20Z', 'currency': 'USD'}

        url = f"{self.API_HOST}/api/v1/webhook"
        response = requests.post(url, json=payload)
        print(response.json())
        self.assertEqual(response.status_code, 200)
