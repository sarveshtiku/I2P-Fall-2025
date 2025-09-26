"""
Memory API routes - for context management and search
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from app.core.database import get_db
from app.services.memory_manager import MemoryManager

router = APIRouter()


class SearchRequest(BaseModel):
    """Request model for memory search"""
    query: str
    conversation_id: Optional[int] = None
    limit: int = 5


class SearchResponse(BaseModel):
    """Response model for memory search"""
    message_id: int
    content: str
    role: str
    similarity_score: float
    created_at: str
    conversation_id: int


class CompressRequest(BaseModel):
    """Request model for context compression"""
    conversation_id: int
    target_ratio: float = 0.3


@router.post("/search", response_model=List[SearchResponse])
async def search_memory(
    search_request: SearchRequest,
    db: Session = Depends(get_db)
):
    """Search for similar messages in memory"""
    
    memory_manager = MemoryManager(db)
    
    # Search for similar messages
    messages = await memory_manager.search_similar_messages(
        query=search_request.query,
        conversation_id=search_request.conversation_id,
        limit=search_request.limit
    )
    
    # Convert to response format
    results = []
    for i, msg in enumerate(messages):
        # Calculate similarity score (simplified)
        similarity_score = 1.0 - (i * 0.1)  # Mock similarity score
        
        results.append(SearchResponse(
            message_id=msg.id,
            content=msg.content,
            role=msg.role,
            similarity_score=similarity_score,
            created_at=msg.created_at.isoformat(),
            conversation_id=msg.conversation_id
        ))
    
    return results


@router.post("/compress")
async def compress_context(
    compress_request: CompressRequest,
    db: Session = Depends(get_db)
):
    """Compress conversation context to reduce token usage"""
    
    memory_manager = MemoryManager(db)
    
    # Compress the context
    messages = await memory_manager.compress_context(
        conversation_id=compress_request.conversation_id,
        target_ratio=compress_request.target_ratio
    )
    
    compressed_count = sum(1 for msg in messages if msg.is_context_compressed)
    
    return {
        "conversation_id": compress_request.conversation_id,
        "total_messages": len(messages),
        "compressed_messages": compressed_count,
        "compression_ratio": compress_request.target_ratio,
        "status": "success"
    }


@router.get("/conversation/{conversation_id}/summary")
async def get_conversation_summary(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """Get a summary of a conversation"""
    
    memory_manager = MemoryManager(db)
    
    summary = await memory_manager.get_conversation_summary(conversation_id)
    
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return summary


@router.get("/conversation/{conversation_id}/context")
async def get_conversation_context(
    conversation_id: int,
    max_messages: int = 10,
    include_compressed: bool = True,
    db: Session = Depends(get_db)
):
    """Get conversation context for LLM input"""
    
    memory_manager = MemoryManager(db)
    
    context = await memory_manager.get_conversation_context(
        conversation_id=conversation_id,
        max_messages=max_messages,
        include_compressed=include_compressed
    )
    
    return {
        "conversation_id": conversation_id,
        "context": [
            {
                "role": msg.role.value,
                "content": msg.content,
                "metadata": msg.metadata
            }
            for msg in context
        ],
        "message_count": len(context)
    }
