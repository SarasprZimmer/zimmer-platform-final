from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    knowledge_entries = relationship("KnowledgeEntry", back_populates="client")
    tickets = relationship("Ticket", foreign_keys="Ticket.user_id", back_populates="user")
    ticket_messages = relationship("TicketMessage", back_populates="user")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user")
    kb_status_history = relationship("KBStatusHistory", back_populates="user") 