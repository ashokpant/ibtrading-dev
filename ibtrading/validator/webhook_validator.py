"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 06/03/2025
"""
from ibtrading.domain import WebhookPayload


def validate_webhook_request(req: WebhookPayload):
    if req.action is None:
        raise ValueError("action is required")
