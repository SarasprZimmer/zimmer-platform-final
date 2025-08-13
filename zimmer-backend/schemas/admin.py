from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserListResponse(BaseModel):
    total_count: int
    users: List[dict]

class UserAutomationAdminResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    automation_id: int
    automation_name: str
    tokens_remaining: int
    demo_tokens: int
    is_demo_active: bool
    demo_expired: bool
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class PaymentResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    amount: float
    tokens_purchased: int
    method: str
    transaction_id: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class PaymentListResponse(BaseModel):
    total_count: int
    payments: List[PaymentResponse]

class TokenUsageResponse(BaseModel):
    id: int
    user_automation_id: int
    automation_name: str
    tokens_used: int
    usage_type: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class UserTokenUsageResponse(BaseModel):
    user_id: int
    user_name: str
    total_tokens_used: int
    total_cost: float
    usage_entries: List[TokenUsageResponse] 