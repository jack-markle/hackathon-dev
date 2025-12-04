"""Recommendation API endpoint"""
from fastapi import APIRouter, HTTPException
from app.models.recommendation import RecommendationRequest, RecommendationResponse
from app.orchestration.orchestrator import orchestrate_pricing_recommendation

router = APIRouter(tags=["recommendation"])


@router.post("/recommendation", response_model=RecommendationResponse)
async def get_recommendation(payload: RecommendationRequest) -> RecommendationResponse:
    """
    Get a pricing recommendation based on current conditions.
    
    This endpoint orchestrates:
    - 5 conceptual agents (Environment, Supply/Demand, Loyalty, Historical, Corporate)
    - Guardrail application
    - LangChain-based reasoning generation
    
    Returns a recommended price adjustment, goodness score, factor breakdown, and reasoning.
    """
    try:
        # Call the orchestrator (which handles Agents + LangChain)
        recommendation = await orchestrate_pricing_recommendation(payload)
        return recommendation
    except Exception as e:
        import traceback
        traceback.print_exc() # For debugging
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
