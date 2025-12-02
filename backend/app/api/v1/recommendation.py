"""Recommendation API endpoint"""
from fastapi import APIRouter, HTTPException
from app.models.recommendation import RecommendationRequest, RecommendationResponse
from app.services.recommendation_service import build_recommendation

router = APIRouter(tags=["recommendation"])


@router.post("/recommendation", response_model=RecommendationResponse)
async def get_recommendation(payload: RecommendationRequest) -> RecommendationResponse:
    """
    Get a pricing recommendation based on current conditions.
    
    This endpoint analyzes:
    - Environmental factors (weather, road closures, emergencies)
    - Supply and demand patterns (time, availability)
    - Customer loyalty tier
    - Historical pricing patterns
    - Corporate revenue goals and strategy
    
    Returns a recommended price adjustment, goodness score, factor breakdown, and reasoning.
    """
    try:
        # Call the recommendation service to build the response
        # Future: Dev 2 will enhance this with full orchestrator + LangChain integration
        recommendation = build_recommendation(payload)
        return recommendation
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendation: {str(e)}"
        )


@router.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Pricing Monitor & Advisor",
        "version": "1.0.0"
    }

