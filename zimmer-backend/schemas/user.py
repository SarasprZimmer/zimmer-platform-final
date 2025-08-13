from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserSignupRequest(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    password: str

class UserSignupResponse(BaseModel):
    message: str
    user_id: int
    email: str
    access_token: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    message: str
    access_token: str
    user_id: int
    email: str
    name: str

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone_number: Optional[str] = None
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserAutomationCreate(BaseModel):
    automation_id: int
    telegram_bot_token: Optional[str] = None
    tokens_remaining: Optional[int] = 0

class UserAutomationUpdate(BaseModel):
    telegram_bot_token: Optional[str] = None
    tokens_remaining: Optional[int] = None
    status: Optional[str] = None

class UserAutomationResponse(BaseModel):
    id: int
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

class UserDashboardResponse(BaseModel):
    user: UserResponse
    automations: list[UserAutomationResponse]
    total_demo_tokens: int
    total_paid_tokens: int
    has_active_demo: bool
    has_expired_demo: bool 