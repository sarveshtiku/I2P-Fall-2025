"""
Conversation model - represents a chat session
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Conversation(Base):
    """Conversation model representing a chat session"""
    
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    context_pack_id = Column(Integer, ForeignKey("context_packs.id"), nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Context management
    current_model = Column(String(100), default="gpt-4")
    total_tokens = Column(Integer, default=0)
    estimated_cost = Column(String(20), default="0.00")
    estimated_carbon = Column(String(20), default="0.00")  # in grams CO2
    
    # Relationships
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    user = relationship("User", back_populates="conversations")
    context_pack = relationship("ContextPack", back_populates="conversations")
