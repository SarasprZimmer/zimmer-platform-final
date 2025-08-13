from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TicketMessageCreate(BaseModel):
    ticket_id: int
    message: str
    attachment_path: Optional[str] = None
    is_internal: bool = False

class TicketMessageUpdate(BaseModel):
    message: Optional[str] = None
    attachment_path: Optional[str] = None

class TicketMessageOut(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    message: str
    attachment_path: Optional[str] = None
    is_internal: bool
    created_at: datetime
    user_name: Optional[str] = None
    user_email: Optional[str] = None

    class Config:
        from_attributes = True

class TicketMessageListResponse(BaseModel):
    total_count: int
    messages: List[TicketMessageOut] 