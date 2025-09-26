"""
Context Pack model - represents shared context bundles for collaboration
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ContextPack(Base):
    """Context Pack model for shared context bundles"""
    
    __tablename__ = "context_packs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_public = Column(Boolean, default=False)
    version = Column(String(20), default="1.0.0")
    
    # Context data
    context_data = Column(JSON, nullable=True)  # Structured context information
    tags = Column(JSON, nullable=True)  # Array of tags for categorization
    access_level = Column(String(20), default="private")  # private, team, public
    
    # Collaboration
    collaborators = Column(JSON, nullable=True)  # Array of user IDs with access
    last_accessed = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    owner = relationship("User", back_populates="owned_context_packs")
    conversations = relationship("Conversation", back_populates="context_pack")
