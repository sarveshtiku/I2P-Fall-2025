"""
Message model - represents individual messages in a conversation
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Message(Base):
    """Message model representing individual messages in a conversation"""
    
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    
    # Message content
    role = Column(String(20), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    model_used = Column(String(100), nullable=True)  # Which LLM generated this message
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    token_count = Column(Integer, default=0)
    cost = Column(String(20), default="0.00")
    carbon_footprint = Column(String(20), default="0.00")  # in grams CO2
    
    # Context management
    is_context_compressed = Column(Boolean, default=False)
    compression_ratio = Column(String(10), default="1.0")  # e.g., "0.3" for 70% compression
    embedding_vector = Column(JSON, nullable=True)  # Store embedding for semantic search
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
