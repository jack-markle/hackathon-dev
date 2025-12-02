from typing import Dict, Any
from app.models.recommendation import RecommendationRequest
from app.services.recommendation_service import compute_corporate_pressure_factor

def evaluate_corporate_pressure(req: RecommendationRequest) -> Dict[str, Any]:
    """
    Evaluate corporate pressure factors.
    Wrapper for recommendation_service.compute_corporate_pressure_factor.
    """
    return compute_corporate_pressure_factor(req)
