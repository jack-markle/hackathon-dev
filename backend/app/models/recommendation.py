"""Pydantic models for recommendation API"""
from typing import Dict, List
from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    """Request model for pricing recommendation endpoint"""
    origin_zone: str = Field(..., description="Origin geographic zone (e.g., 'downtown', 'suburbs')")
    destination_zone: str = Field(..., description="Destination geographic zone (e.g., 'airport_corridor', 'downtown')")
    scenarios: List[str] = Field(..., description="List of applicable scenarios (e.g., ['storm', 'road_closure'])")
    scenario: str = Field(..., description="Primary/selected scenario (e.g., 'storm', 'road_closure', 'emergency')")
    time: str = Field(..., description="ISO timestamp for the pricing request")
    loyalty_segment: str | None = Field(None, description="Customer loyalty tier (e.g., 'standard', 'gold', 'platinum')")
    notes: str | None = Field(None, description="Optional free-text notes about the scenario")
    corporate_revenue_goal: float | None = Field(None, description="Target revenue uplift percentage (e.g., 0.15 for 15%)")
    corporate_strategy_notes: str | None = Field(None, description="Free-text description of corporate strategy")
    # New fields from CSV gap analysis (Priority 1 & 2)
    number_of_riders: int | None = Field(None, ge=0, description="Current number of riders requesting rides in the area")
    number_of_drivers: int | None = Field(None, ge=0, description="Current number of available drivers in the area")
    historical_cost_of_ride: float | None = Field(None, ge=0.0, description="Historical cost for similar rides")
    vehicle_type: str | None = Field(None, pattern="^(Premium|Economy)$", description="Vehicle type requested (Premium or Economy)")
    expected_ride_duration: int | None = Field(None, ge=0, description="Expected ride duration in minutes")

    class Config:
        json_schema_extra = {
            "example": {
                "origin_zone": "downtown",
                "destination_zone": "airport_corridor",
                "scenarios": ["storm", "road_closure"],
                "scenario": "storm",
                "time": "2024-01-15T14:30:00.000Z",
                "loyalty_segment": "gold",
                "notes": "Storm expected to reduce driver availability by 40%.",
                "corporate_revenue_goal": 0.03,
                "corporate_strategy_notes": "Q4 revenue push",
                "number_of_riders": 90,
                "number_of_drivers": 45,
                "historical_cost_of_ride": 284.26,
                "vehicle_type": "Premium",
                "expected_ride_duration": 90
            }
        }


class FactorReasoning(BaseModel):
    """Structured reasoning summaries for individual factors"""
    environment: str | None = Field(None, description="Agent's reasoning about environmental factors")
    supply_demand: str | None = Field(None, description="Agent's reasoning about supply and demand factors")
    loyalty: str | None = Field(None, description="Agent's reasoning about loyalty factors")
    historical: str | None = Field(None, description="Agent's reasoning about historical patterns")
    corporate_pressure: str | None = Field(None, description="Agent's reasoning about corporate pressure factors")


class RecommendationResponse(BaseModel):
    """Response model for pricing recommendation endpoint"""
    recommended_adjustment: float = Field(..., description="Recommended price adjustment as a multiplier (e.g., 0.10 for +10%)")
    goodness: float = Field(..., description="Goodness score between 0.0 and 1.0")
    factors: Dict[str, str] = Field(..., description="Summary of each factor's contribution from tool outputs")
    overall_reasoning: str = Field(..., description="Overall natural language explanation of the recommendation")
    factor_reasoning: FactorReasoning = Field(..., description="Individual reasoning summaries for each factor from the agent")

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
                "overall_reasoning": "Based on current conditions, a +10% price adjustment is recommended. The combination of road closures, peak demand, and corporate revenue goals supports this pricing level while respecting loyalty discounts.",
                "factor_reasoning": {
                    "environment": "The road closure significantly impacts travel time and driver availability, justifying the 5% environmental adjustment.",
                    "supply_demand": "Evening rush hour combined with airport destination creates high demand pressure, supporting the 15% surge.",
                    "loyalty": "Gold tier members receive preferential pricing treatment, softening the overall surge impact.",
                    "historical": "Historical data shows similar routes during evening hours have successfully accepted pricing at this level.",
                    "corporate_pressure": "Corporate revenue goals provide upward pressure, but remain within ethical guardrails."
                }
            }
        }

