"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 28/01/2025
"""
from pydantic import BaseModel, Field


class ApiErrorResponse(BaseModel):
    success: bool = Field(..., description="Success")
    code: int = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
