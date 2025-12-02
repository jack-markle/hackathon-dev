"""
Loyalty Agent - STUB for Dev 2

Responsibility: Calculate discount/adjustment based on customer loyalty tier.

Current state: Logic implemented in backend/app/services/recommendation_service.py
by Dev 1 as compute_loyalty_factor().
"""
from typing import Any, Dict


def evaluate_loyalty(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate loyalty tier impact on pricing.
    
    Args:
        context: Dictionary with loyalty_segment, etc.
    
    Returns:
        Dictionary with 'factor' (float) and 'summary' (str)
    """
    from app.models.recommendation import RecommendationRequest
    from app.services.recommendation_service import compute_loyalty_factor
    
    req = RecommendationRequest(**context)
    return compute_loyalty_factor(req)

