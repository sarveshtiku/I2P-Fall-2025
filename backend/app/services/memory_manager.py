"""
Memory Manager - Handles conversation state and context reconstruction
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.llm_adapters import LLMMessage, MessageRole
from sentence_transformers import SentenceTransformer
import json


class MemoryManager:
    """Manages conversation memory and context reconstruction"""
    
    def __init__(self, db: Session):
        self.db = db
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    async def store_message(
        self, 
        conversation_id: int, 
        role: str, 
        content: str, 
        model_used: str,
        token_count: int = 0,
        cost: float = 0.0,
        carbon_footprint: float = 0.0
    ) -> Message:
        """Store a new message in the conversation"""
        
        # Generate embedding for semantic search
        embedding = self.embedding_model.encode(content).tolist()
        
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            model_used=model_used,
            token_count=token_count,
            cost=str(cost),
            carbon_footprint=str(carbon_footprint),
            embedding_vector=embedding
        )
        
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        
        return message
    
    async def get_conversation_context(
        self, 
        conversation_id: int, 
        max_messages: int = 10,
        include_compressed: bool = True
    ) -> List[LLMMessage]:
        """Get conversation context for LLM input"""
        
        # Get recent messages
        messages = (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(max_messages)
            .all()
        )
        
        # Convert to LLMMessage format
        context = []
        for msg in reversed(messages):  # Reverse to get chronological order
            role = MessageRole(msg.role)
            content = msg.content
            
            # If message is compressed, we might want to expand it
            if msg.is_context_compressed and not include_compressed:
                # TODO: Implement context expansion
                pass
            
            context.append(LLMMessage(
                role=role,
                content=content,
                metadata={
                    "message_id": msg.id,
                    "model_used": msg.model_used,
                    "created_at": msg.created_at.isoformat(),
                    "is_compressed": msg.is_context_compressed
                }
            ))
        
        return context
    
    async def compress_context(
        self, 
        conversation_id: int, 
        target_ratio: float = 0.3
    ) -> List[Message]:
        """Compress conversation context to reduce token usage"""
        
        # Get all messages in the conversation
        messages = (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )
        
        if len(messages) <= 5:  # Don't compress if conversation is short
            return messages
        
        # Simple compression strategy: keep first and last few messages
        keep_count = max(2, int(len(messages) * target_ratio))
        
        # Mark messages for compression
        messages_to_compress = messages[2:-2]  # Keep first 2 and last 2
        
        for msg in messages_to_compress:
            if not msg.is_context_compressed:
                # Create a summary of the message
                summary = await self._summarize_message(msg)
                msg.content = f"[COMPRESSED] {summary}"
                msg.is_context_compressed = True
                msg.compression_ratio = str(target_ratio)
        
        self.db.commit()
        return messages
    
    async def _summarize_message(self, message: Message) -> str:
        """Summarize a message for compression"""
        # Simple summarization - in production, use a proper summarization model
        content = message.content
        if len(content) > 200:
            return content[:200] + "..."
        return content
    
    async def search_similar_messages(
        self, 
        query: str, 
        conversation_id: Optional[int] = None,
        limit: int = 5
    ) -> List[Message]:
        """Search for similar messages using semantic similarity"""
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Get all messages (or from specific conversation)
        query_obj = self.db.query(Message)
        if conversation_id:
            query_obj = query_obj.filter(Message.conversation_id == conversation_id)
        
        messages = query_obj.all()
        
        # Calculate similarities
        similarities = []
        for msg in messages:
            if msg.embedding_vector:
                # Calculate cosine similarity
                similarity = self._cosine_similarity(query_embedding, msg.embedding_vector)
                similarities.append((msg, similarity))
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [msg for msg, _ in similarities[:limit]]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        import numpy as np
        
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        return dot_product / (norm1 * norm2)
    
    async def get_conversation_summary(self, conversation_id: int) -> Dict[str, Any]:
        """Get a summary of the conversation"""
        
        conversation = self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            return {}
        
        messages = (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )
        
        total_tokens = sum(msg.token_count for msg in messages)
        total_cost = sum(float(msg.cost) for msg in messages)
        total_carbon = sum(float(msg.carbon_footprint) for msg in messages)
        
        return {
            "conversation_id": conversation_id,
            "title": conversation.title,
            "message_count": len(messages),
            "total_tokens": total_tokens,
            "total_cost": f"{total_cost:.4f}",
            "total_carbon": f"{total_carbon:.4f}",
            "models_used": list(set(msg.model_used for msg in messages if msg.model_used)),
            "created_at": conversation.created_at.isoformat(),
            "last_updated": conversation.updated_at.isoformat() if conversation.updated_at else None
        }
