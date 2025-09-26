"""
Models API routes - for managing available LLM models
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.database import get_db
from app.services.llm_adapters import LLMRouter, OpenAIAdapter, AnthropicAdapter, GoogleAdapter
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[Dict[str, Any]])
async def list_available_models():
    """List all available LLM models"""
    
    # Initialize router with available adapters
    llm_router = LLMRouter()
    
    # Register adapters (only if API keys are available)
    if settings.OPENAI_API_KEY:
        llm_router.register_adapter("gpt-4", OpenAIAdapter(settings.OPENAI_API_KEY, "gpt-4"))
        llm_router.register_adapter("gpt-3.5-turbo", OpenAIAdapter(settings.OPENAI_API_KEY, "gpt-3.5-turbo"))
    
    if settings.ANTHROPIC_API_KEY:
        llm_router.register_adapter("claude-3-sonnet", AnthropicAdapter(settings.ANTHROPIC_API_KEY, "claude-3-sonnet-20240229"))
        llm_router.register_adapter("claude-3-haiku", AnthropicAdapter(settings.ANTHROPIC_API_KEY, "claude-3-haiku-20240307"))
    
    if settings.GOOGLE_API_KEY:
        llm_router.register_adapter("gemini-pro", GoogleAdapter(settings.GOOGLE_API_KEY, "gemini-pro"))
        llm_router.register_adapter("gemini-pro-vision", GoogleAdapter(settings.GOOGLE_API_KEY, "gemini-pro-vision"))
    
    return llm_router.list_available_models()


@router.get("/{model_name}/info", response_model=Dict[str, Any])
async def get_model_info(model_name: str):
    """Get detailed information about a specific model"""
    
    # Initialize router
    llm_router = LLMRouter()
    
    # Register adapters
    if settings.OPENAI_API_KEY:
        llm_router.register_adapter("gpt-4", OpenAIAdapter(settings.OPENAI_API_KEY, "gpt-4"))
        llm_router.register_adapter("gpt-3.5-turbo", OpenAIAdapter(settings.OPENAI_API_KEY, "gpt-3.5-turbo"))
    
    if settings.ANTHROPIC_API_KEY:
        llm_router.register_adapter("claude-3-sonnet", AnthropicAdapter(settings.ANTHROPIC_API_KEY, "claude-3-sonnet-20240229"))
        llm_router.register_adapter("claude-3-haiku", AnthropicAdapter(settings.ANTHROPIC_API_KEY, "claude-3-haiku-20240307"))
    
    if settings.GOOGLE_API_KEY:
        llm_router.register_adapter("gemini-pro", GoogleAdapter(settings.GOOGLE_API_KEY, "gemini-pro"))
        llm_router.register_adapter("gemini-pro-vision", GoogleAdapter(settings.GOOGLE_API_KEY, "gemini-pro-vision"))
    
    adapter = llm_router.get_adapter(model_name)
    if not adapter:
        return {"error": f"Model {model_name} not found"}
    
    return adapter.get_model_info()


@router.post("/{model_name}/estimate-cost")
async def estimate_cost(
    model_name: str,
    messages: List[Dict[str, str]]
):
    """Estimate the cost of a request to a specific model"""
    
    # Initialize router
    llm_router = LLMRouter()
    
    # Register adapters
    if settings.OPENAI_API_KEY:
        llm_router.register_adapter("gpt-4", OpenAIAdapter(settings.OPENAI_API_KEY, "gpt-4"))
        llm_router.register_adapter("gpt-3.5-turbo", OpenAIAdapter(settings.OPENAI_API_KEY, "gpt-3.5-turbo"))
    
    if settings.ANTHROPIC_API_KEY:
        llm_router.register_adapter("claude-3-sonnet", AnthropicAdapter(settings.ANTHROPIC_API_KEY, "claude-3-sonnet-20240229"))
        llm_router.register_adapter("claude-3-haiku", AnthropicAdapter(settings.ANTHROPIC_API_KEY, "claude-3-haiku-20240307"))
    
    if settings.GOOGLE_API_KEY:
        llm_router.register_adapter("gemini-pro", GoogleAdapter(settings.GOOGLE_API_KEY, "gemini-pro"))
        llm_router.register_adapter("gemini-pro-vision", GoogleAdapter(settings.GOOGLE_API_KEY, "gemini-pro-vision"))
    
    adapter = llm_router.get_adapter(model_name)
    if not adapter:
        return {"error": f"Model {model_name} not found"}
    
    # Convert messages to LLMMessage format
    from app.services.llm_adapters import LLMMessage, MessageRole
    llm_messages = [
        LLMMessage(role=MessageRole(msg["role"]), content=msg["content"])
        for msg in messages
    ]
    
    cost = adapter.estimate_cost(llm_messages)
    carbon_footprint = adapter.estimate_carbon_footprint(llm_messages)
    
    return {
        "model": model_name,
        "estimated_cost": f"${cost:.6f}",
        "estimated_carbon_footprint": f"{carbon_footprint:.6f}g CO2",
        "message_count": len(messages)
    }
