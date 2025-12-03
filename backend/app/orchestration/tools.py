from typing import Dict, Any, List, Optional
from langchain_core.tools import tool
from app.services.recommendation_service import combine_factors, apply_guardrails

@tool
def calculate_pricing_outcome_tool(
    environment_factor: Dict[str, Any],
    supply_demand_factor: Dict[str, Any],
    loyalty_factor: Dict[str, Any],
    historical_factor: Dict[str, Any],
    corporate_pressure_factor: Dict[str, Any],
    scenario: str,
    loyalty_segment: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculate final pricing outcome by combining factors and applying guardrails.
    
    Args:
        environment_factor: Output from environment_tool
        supply_demand_factor: Output from supply_demand_tool
        loyalty_factor: Output from loyalty_tool
        historical_factor: Output from historical_tool
        corporate_pressure_factor: Output from corporate_pressure_tool
        scenario: The scenario string (e.g. "Heavy Rain")
        loyalty_segment: The loyalty segment string (e.g. "Gold Tier") or None
        
    Returns:
        A dictionary containing:
        - final_adjustment: The final calculated price adjustment
        - goodness: The goodness score
        - guardrail_flags: List of guardrail warnings applied
        - raw_adjustment: The adjustment before guardrails
    """
    
    # 1. Combine factors
    combination = combine_factors(
        environment_factor,
        supply_demand_factor,
        loyalty_factor,
        historical_factor,
        corporate_pressure_factor
    )
    
    raw_adjustment = combination["recommended_adjustment"]
    goodness = combination["goodness"]
    
    # 2. Prepare all_factors dict for guardrails
    all_factors = {
        "environment": environment_factor,
        "supply_demand": supply_demand_factor,
        "loyalty": loyalty_factor,
        "historical": historical_factor,
        "corporate_pressure": corporate_pressure_factor
    }
    
    # 3. Apply Guardrails
    guardrail_result = apply_guardrails(
        raw_adjustment,
        scenario,
        loyalty_segment,
        all_factors
    )
    
    final_adjustment = guardrail_result["adjusted_value"]
    guardrail_flags = guardrail_result["flags"]
    
    # 4. Adjust goodness if guardrails significantly modified the value
    if abs(final_adjustment - raw_adjustment) > 0.05:
        if guardrail_result["guardrail_applied"] == "emergency":
            goodness = max(goodness, 0.85)  # Ethical pricing is good
        elif guardrail_flags:
            goodness = max(0.60, goodness - 0.10)  # Tension exists
            
    return {
        "final_adjustment": final_adjustment,
        "goodness": goodness,
        "guardrail_flags": guardrail_flags,
        "raw_adjustment": raw_adjustment
    }

