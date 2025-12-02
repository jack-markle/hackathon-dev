from typing import Dict, Any
from app.models.recommendation import RecommendationRequest
from app.services.recommendation_service import compute_loyalty_factor

def evaluate_loyalty(req: RecommendationRequest) -> Dict[str, Any]:
    """
    Evaluate loyalty factors.
    Wrapper for recommendation_service.compute_loyalty_factor.
    """
    return compute_loyalty_factor(req)
