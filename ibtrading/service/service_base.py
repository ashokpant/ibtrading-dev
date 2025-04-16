"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 20/03/2025
"""

from ibtrading.service.auth_service import AuthService


class ServiceBase:
    def __init__(self, auth_service: AuthService = None):
        if auth_service is None:
            auth_service = AuthService.get_instance()
        self.auth_service = auth_service
