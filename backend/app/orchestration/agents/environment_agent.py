from typing import Dict, Any
from app.models.recommendation import RecommendationRequest
from app.services.recommendation_service import compute_environment_factor

def evaluate_environment(req: RecommendationRequest) -> Dict[str, Any]:
    """
    Evaluate environmental factors.
    Wrapper for recommendation_service.compute_environment_factor.
    """
    return compute_environment_factor(req)
