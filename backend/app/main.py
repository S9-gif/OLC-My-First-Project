from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .api import haberler

# FastAPI app oluştur
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="OLC - Open Learn Close | AI-powered haber özet platformu",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (Frontend için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da kısıtlanacak
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
def root():
    """API root - health check"""
    return {
        "message": "OLC API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy"}

# API routers
app.include_router(haberler.router, prefix="/api/v1", tags=["haberler"])
