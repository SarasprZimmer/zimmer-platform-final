from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models.ticket import TicketStatus, TicketImportance

class TicketCreate(BaseModel):
    user_id: int
    subject: str
    message: str
    importance: TicketImportance = TicketImportance.MEDIUM
    attachment_path: Optional[str] = None

class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    assigned_to: Optional[int] = None
    message: Optional[str] = None

class TicketOut(BaseModel):
    id: int
    user_id: int
    subject: str
    message: str
    status: TicketStatus
    importance: TicketImportance
    attachment_path: Optional[str] = None
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    user_name: Optional[str] = None
    assigned_admin_name: Optional[str] = None

    class Config:
        from_attributes = True

class TicketListResponse(BaseModel):
    total_count: int
    tickets: List[TicketOut] 