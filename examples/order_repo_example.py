"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 06/02/2025
"""

from ibtrading.repo import DataSource
from ibtrading.repo.order_repo import OrderRepo

if __name__ == '__main__':
    db = DataSource()
    order_repo = OrderRepo(db)
    wb = order_repo.get_webhook_by_id(1)

    print("Given", wb)
    last_webhook = order_repo.get_last_webhook(wb)

    print("Prev", last_webhook)
