"""
User model - represents users of the system
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """User model representing system users"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile
    full_name = Column(String(100), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Preferences
    default_model = Column(String(100), default="gpt-4")
    carbon_budget = Column(String(20), default="1000.00")  # Monthly CO2 budget in grams
    cost_budget = Column(String(20), default="50.00")  # Monthly cost budget in USD
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user")
    owned_context_packs = relationship("ContextPack", back_populates="owner")
