from typing import Dict, Any
from app.models.recommendation import RecommendationRequest
from app.services.recommendation_service import compute_historical_factor

def evaluate_historical(req: RecommendationRequest) -> Dict[str, Any]:
    """
    Evaluate historical pricing patterns.
    Wrapper for recommendation_service.compute_historical_factor.
    """
    return compute_historical_factor(req)
