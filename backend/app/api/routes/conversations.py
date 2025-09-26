"""
Conversation API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.memory_manager import MemoryManager
from app.services.llm_adapters import LLMRouter, LLMMessage, MessageRole

router = APIRouter()


class MessageRequest(BaseModel):
    """Request model for sending a message"""
    content: str
    model: Optional[str] = "gpt-4"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None


class MessageResponse(BaseModel):
    """Response model for message"""
    id: int
    role: str
    content: str
    model_used: str
    token_count: int
    cost: str
    carbon_footprint: str
    created_at: str


class ConversationResponse(BaseModel):
    """Response model for conversation"""
    id: int
    title: Optional[str]
    current_model: str
    message_count: int
    total_tokens: int
    estimated_cost: str
    estimated_carbon: str
    created_at: str
    messages: List[MessageResponse]


@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    title: Optional[str] = None,
    initial_model: str = "gpt-4",
    db: Session = Depends(get_db)
):
    """Create a new conversation"""
    
    conversation = Conversation(
        title=title,
        current_model=initial_model
    )
    
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        current_model=conversation.current_model,
        message_count=0,
        total_tokens=conversation.total_tokens,
        estimated_cost=conversation.estimated_cost,
        estimated_carbon=conversation.estimated_carbon,
        created_at=conversation.created_at.isoformat(),
        messages=[]
    )


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """Get a conversation by ID"""
    
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Get messages
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )
    
    message_responses = [
        MessageResponse(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            model_used=msg.model_used or "",
            token_count=msg.token_count,
            cost=msg.cost,
            carbon_footprint=msg.carbon_footprint,
            created_at=msg.created_at.isoformat()
        )
        for msg in messages
    ]
    
    return ConversationResponse(
        id=conversation.id,
        title=conversation.title,
        current_model=conversation.current_model,
        message_count=len(messages),
        total_tokens=conversation.total_tokens,
        estimated_cost=conversation.estimated_cost,
        estimated_carbon=conversation.estimated_carbon,
        created_at=conversation.created_at.isoformat(),
        messages=message_responses
    )


@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def send_message(
    conversation_id: int,
    message_request: MessageRequest,
    db: Session = Depends(get_db)
):
    """Send a message to a conversation"""
    
    # Get conversation
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Initialize services
    memory_manager = MemoryManager(db)
    llm_router = LLMRouter()
    
    # TODO: Register adapters with actual API keys
    # For now, we'll create a mock response
    
    # Store user message
    user_message = await memory_manager.store_message(
        conversation_id=conversation_id,
        role="user",
        content=message_request.content,
        model_used="user",
        token_count=len(message_request.content.split()),
        cost=0.0,
        carbon_footprint=0.0
    )
    
    # Get conversation context
    context = await memory_manager.get_conversation_context(conversation_id)
    
    # Generate response (mock for now)
    # TODO: Implement actual LLM call
    assistant_content = f"Mock response to: {message_request.content}"
    
    # Store assistant response
    assistant_message = await memory_manager.store_message(
        conversation_id=conversation_id,
        role="assistant",
        content=assistant_content,
        model_used=message_request.model,
        token_count=len(assistant_content.split()),
        cost=0.01,
        carbon_footprint=0.001
    )
    
    # Update conversation totals
    conversation.total_tokens += user_message.token_count + assistant_message.token_count
    conversation.estimated_cost = str(float(conversation.estimated_cost) + 0.01)
    conversation.estimated_carbon = str(float(conversation.estimated_carbon) + 0.001)
    conversation.current_model = message_request.model
    
    db.commit()
    
    return MessageResponse(
        id=assistant_message.id,
        role=assistant_message.role,
        content=assistant_message.content,
        model_used=assistant_message.model_used or "",
        token_count=assistant_message.token_count,
        cost=assistant_message.cost,
        carbon_footprint=assistant_message.carbon_footprint,
        created_at=assistant_message.created_at.isoformat()
    )


@router.get("/", response_model=List[ConversationResponse])
async def list_conversations(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List all conversations"""
    
    conversations = (
        db.query(Conversation)
        .filter(Conversation.is_active == True)
        .order_by(Conversation.updated_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    result = []
    for conv in conversations:
        # Get message count
        message_count = db.query(Message).filter(Message.conversation_id == conv.id).count()
        
        result.append(ConversationResponse(
            id=conv.id,
            title=conv.title,
            current_model=conv.current_model,
            message_count=message_count,
            total_tokens=conv.total_tokens,
            estimated_cost=conv.estimated_cost,
            estimated_carbon=conv.estimated_carbon,
            created_at=conv.created_at.isoformat(),
            messages=[]  # Don't include messages in list view
        ))
    
    return result


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """Delete a conversation"""
    
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    conversation.is_active = False
    db.commit()
    
    return {"message": "Conversation deleted successfully"}
