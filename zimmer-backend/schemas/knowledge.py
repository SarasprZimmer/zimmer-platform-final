from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class KnowledgeCreate(BaseModel):
    client_id: int
    category: str
    answer: str

class KnowledgeOut(BaseModel):
    id: int
    category: str
    answer: str
    created_at: datetime
    client_name: str

    class Config:
        from_attributes = True

class KnowledgeListResponse(BaseModel):
    total_count: int
    knowledge_entries: List[KnowledgeOut] 