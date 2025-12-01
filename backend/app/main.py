"""
FastAPI application factory and entrypoint for AI Pricing Monitor & Advisor.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import recommendation
from app.core.config import settings


def create_app() -> FastAPI:
    """
    Application factory.
    
    Creates and configures the FastAPI application with routes,
    middleware, and settings.
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-powered pricing recommendation system for ride-hailing services"
    )
    
    # Configure CORS for frontend integration (Dev 3)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict to specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(
        recommendation.router,
        prefix=settings.api_v1_prefix
    )
    
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "AI Pricing Monitor & Advisor API",
            "version": settings.app_version,
            "docs": "/docs",
            "health": f"{settings.api_v1_prefix}/health"
        }
    
    return app


# Create the app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

