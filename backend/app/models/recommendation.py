"""Pydantic models for recommendation API"""
from typing import Dict
from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    """Request model for pricing recommendation endpoint"""
    zone: str = Field(..., description="Geographic zone (e.g., 'airport_corridor', 'downtown', 'suburbs')")
    scenario: str = Field(..., description="Current scenario (e.g., 'normal', 'storm', 'road_closure', 'emergency')")
    time: str = Field(..., description="ISO timestamp for the pricing request")
    loyalty_segment: str | None = Field(None, description="Customer loyalty tier (e.g., 'standard', 'gold', 'platinum')")
    notes: str | None = Field(None, description="Optional free-text notes about the scenario")
    corporate_revenue_goal: float | None = Field(None, description="Target revenue uplift percentage (e.g., 0.15 for 15%)")
    corporate_strategy_notes: str | None = Field(None, description="Free-text description of corporate strategy")

    class Config:
        json_schema_extra = {
            "example": {
                "zone": "airport_corridor",
                "scenario": "road_closure",
                "time": "2025-11-27T18:00:00Z",
                "loyalty_segment": "gold",
                "notes": "evening commute, partial freeway closure",
                "corporate_revenue_goal": 0.15,
                "corporate_strategy_notes": "End-of-quarter revenue push for airport corridor"
            }
        }


class RecommendationResponse(BaseModel):
    """Response model for pricing recommendation endpoint"""
    recommended_adjustment: float = Field(..., description="Recommended price adjustment as a multiplier (e.g., 0.10 for +10%)")
    goodness: float = Field(..., description="Goodness score between 0.0 and 1.0")
    factors: Dict[str, str] = Field(..., description="Summary of each factor's contribution")
    reasoning: str = Field(..., description="Natural language explanation of the recommendation")

    class Config:
        json_schema_extra = {
            "example": {
                "recommended_adjustment": 0.1,
                "goodness": 0.78,
                "factors": {
                    "environment": "Road closure near airport adds moderate travel time (+5%).",
                    "supply_demand": "Driver supply tight vs ride requests at 6pm (+10%).",
                    "loyalty": "Gold segment gets softened surge (-5%).",
                    "historical": "Similar airport evening trips succeed around 1.05x.",
                    "corporate_pressure": "Corporate target of +15% revenue nudges price upward within allowed guardrails."
                },
                "reasoning": "Based on current conditions, a +10% price adjustment is recommended..."
            }
        }

