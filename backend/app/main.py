"""
ContextLink - Universal AI Memory Fabric
Main FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.routes import conversations, models, memory
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="ContextLink API",
    description="Universal AI Memory Fabric for seamless LLM switching",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(conversations.router, prefix="/api/v1/conversations", tags=["conversations"])
app.include_router(models.router, prefix="/api/v1/models", tags=["models"])
app.include_router(memory.router, prefix="/api/v1/memory", tags=["memory"])


@app.get("/")
async def root():
    return {
        "message": "ContextLink API - Universal AI Memory Fabric",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
