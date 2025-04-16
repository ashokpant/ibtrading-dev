"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 31/01/2025
"""

from ibtrading.domain import ListTradeResponse, ListOrderResponse, ListPortfolioResponse, ListPositionResponse, \
    ListAccountResponse, AccountData, \
    ListContractResponse
from ibtrading.domain import WebhookPayload
from ibtrading.domain.webhook import ListWebhookPayloadResponse
from ibtrading.repo.order_repo import OrderRepo
from ibtrading.service.auth_service import AuthService
from ibtrading.service.service_base import ServiceBase


class OrderService(ServiceBase):
    def __init__(self, order_repo: OrderRepo, auth_service: AuthService):
        super().__init__(auth_service=auth_service)
        self.order_repo = order_repo

    async def list_trades(self) -> ListTradeResponse:
        return ListTradeResponse(trades=self.order_repo.list_trades())

    async def list_orders(self) -> ListOrderResponse:
        return ListOrderResponse(orders=self.order_repo.list_orders())

    async def list_portfolio(self) -> ListPortfolioResponse:
        return ListPortfolioResponse(portfolios=self.order_repo.list_portfolio())

    async def list_position(self) -> ListPositionResponse:
        return ListPositionResponse(positions=self.order_repo.list_position())

    async def list_account_summary(self) -> ListAccountResponse:
        values = self.order_repo.list_account_summary()
        accounts = {}
        for value in values:
            account = accounts.get(value.account_id, None)
            if account is None:
                accounts[value.account_id] = []
            accounts[value.account_id].append(value)
        data = []
        for account_id, values in accounts.items():
            account = AccountData(account_id=account_id, values=values)
            data.append(account)
        return ListAccountResponse(accounts=data)

    async def list_contracts(self) -> ListContractResponse:
        return ListContractResponse(contracts=self.order_repo.list_contracts())

    async def list_webhook_logs(self) -> ListWebhookPayloadResponse:
        return ListWebhookPayloadResponse(webhooks=self.order_repo.list_webhook_logs())

    def get_last_webhook(self, req) -> WebhookPayload:
        return self.order_repo.get_last_webhook(req)
