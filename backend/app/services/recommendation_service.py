"""
Core pricing recommendation service with factor computations and guardrails.

This module implements the five conceptual pricing factors:
- Environment (weather, disasters, road closures)
- Supply & Demand (driver availability, time of day)
- Loyalty (customer tier discounts)
- Historical (past pricing patterns)
- Corporate Pressure (revenue goals and strategy)

It also applies ethical and market-based guardrails.
"""
from typing import Dict
from datetime import datetime
from app.models.recommendation import RecommendationRequest, RecommendationResponse


# ===== FACTOR COMPUTATION FUNCTIONS =====

def compute_environment_factor(req: RecommendationRequest) -> Dict[str, any]:
    """
    Compute environmental impact on pricing.
    
    Considers: weather, road closures, disasters, emergencies.
    Returns a factor adjustment and summary.
    """
    scenario = req.scenario.lower()
    # Consider both origin and destination zones for environmental factors
    origin_zone = req.origin_zone.lower()
    destination_zone = req.destination_zone.lower()
    
    # Emergency scenarios get special treatment (guardrails will handle pricing)
    if scenario in ["emergency", "natural_disaster", "disaster"]:
        return {
            "factor": 0.0,
            "summary": "Emergency situation detected - applying ethical guardrails (no surge)."
        }
    
    # Road closures add complexity and travel time
    if scenario == "road_closure":
        return {
            "factor": 0.05,
            "summary": "Road closure adds moderate travel time and complexity (+5%)."
        }
    
    # Storm/weather conditions
    if scenario in ["storm", "heavy_rain", "snow"]:
        return {
            "factor": 0.08,
            "summary": f"Weather conditions ({scenario}) increase difficulty and demand (+8%)."
        }
    
    # Special events
    if scenario in ["concert", "sports_event", "festival"]:
        return {
            "factor": 0.12,
            "summary": f"High-demand event ({scenario}) in the area (+12%)."
        }
    
    # Holiday periods
    if scenario in ["holiday", "new_year", "thanksgiving"]:
        return {
            "factor": 0.10,
            "summary": "Holiday period with increased demand (+10%)."
        }
    
    # Normal day
    return {
        "factor": 0.0,
        "summary": "Normal environmental conditions (no adjustment)."
    }


def compute_supply_demand_factor(req: RecommendationRequest) -> Dict[str, any]:
    """
    Compute supply/demand impact on pricing.
    
    Considers: time of day, day of week, driver availability patterns.
    Returns a factor adjustment and summary.
    """
    try:
        # Parse time to determine demand patterns
        time_obj = datetime.fromisoformat(req.time.replace('Z', '+00:00'))
        hour = time_obj.hour
        weekday = time_obj.weekday()  # 0 = Monday, 6 = Sunday
    except:
        # Default to moderate if we can't parse time
        return {
            "factor": 0.05,
            "summary": "Moderate demand expected (default) (+5%)."
        }
    
    # Consider both origin and destination zones for supply/demand
    origin_zone = req.origin_zone.lower()
    destination_zone = req.destination_zone.lower()
    
    # Peak hours (7-9 AM, 5-7 PM on weekdays)
    is_weekday = weekday < 5
    is_morning_rush = 7 <= hour <= 9
    is_evening_rush = 17 <= hour <= 19
    
    if is_weekday and (is_morning_rush or is_evening_rush):
        # High-demand zones: airport or downtown in either origin or destination
        factor = 0.15 if ("airport" in origin_zone or "airport" in destination_zone or 
                          "downtown" in origin_zone or "downtown" in destination_zone) else 0.10
        return {
            "factor": factor,
            "summary": f"Peak commute hours with high demand ({'+15%' if factor == 0.15 else '+10%'})."
        }
    
    # Late night hours (11 PM - 4 AM) - lower supply
    if hour >= 23 or hour <= 4:
        return {
            "factor": 0.12,
            "summary": "Late night hours with limited driver availability (+12%)."
        }
    
    # Weekend nights (Friday/Saturday 8 PM - 2 AM)
    if weekday in [4, 5] and 20 <= hour <= 26:  # 26 to handle past midnight
        return {
            "factor": 0.18,
            "summary": "Weekend night with high entertainment demand (+18%)."
        }
    
    # Weekend days
    if not is_weekday and 10 <= hour <= 18:
        return {
            "factor": 0.05,
            "summary": "Weekend leisure travel - moderate demand (+5%)."
        }
    
    # Off-peak hours
    return {
        "factor": 0.0,
        "summary": "Off-peak hours with balanced supply and demand (no adjustment)."
    }


def compute_loyalty_factor(req: RecommendationRequest) -> Dict[str, any]:
    """
    Compute loyalty tier discount/adjustment.
    
    Loyal customers receive preferential treatment and softer surge pricing.
    Returns a factor adjustment (typically negative) and summary.
    """
    loyalty = (req.loyalty_segment or "standard").lower()
    
    # Platinum tier - highest loyalty
    if loyalty == "platinum":
        return {
            "factor": -0.10,
            "summary": "Platinum member receives premium loyalty discount (-10%)."
        }
    
    # Gold tier - strong loyalty
    if loyalty == "gold":
        return {
            "factor": -0.05,
            "summary": "Gold member receives loyalty discount and softened surge (-5%)."
        }
    
    # Silver tier - moderate loyalty
    if loyalty == "silver":
        return {
            "factor": -0.03,
            "summary": "Silver member receives moderate loyalty benefit (-3%)."
        }
    
    # Standard tier - no adjustment
    return {
        "factor": 0.0,
        "summary": "Standard customer tier (no loyalty adjustment)."
    }


def compute_historical_factor(req: RecommendationRequest) -> Dict[str, any]:
    """
    Compute adjustment based on historical pricing patterns.
    
    In production, this would query actual historical data.
    For the hackathon demo, we use heuristics based on zone and scenario.
    """
    origin_zone = req.origin_zone.lower()
    destination_zone = req.destination_zone.lower()
    scenario = req.scenario.lower()
    
    # Airport corridor historical patterns (check destination primarily)
    if "airport" in destination_zone:
        if scenario in ["normal", "road_closure"]:
            return {
                "factor": 0.05,
                "summary": "Historical data shows airport trips typically succeed at 1.05x base price."
            }
        return {
            "factor": 0.08,
            "summary": "Historical airport demand during events suggests +8% pricing."
        }
    
    # Downtown historical patterns (check both origin and destination)
    if "downtown" in origin_zone or "downtown" in destination_zone:
        if scenario in ["concert", "sports_event"]:
            return {
                "factor": 0.10,
                "summary": "Historical event data in downtown shows strong acceptance at +10%."
            }
        return {
            "factor": 0.03,
            "summary": "Historical downtown patterns suggest modest +3% adjustment."
        }
    
    # Stadium/venue zones (check both origin and destination)
    if "stadium" in origin_zone or "venue" in origin_zone or "stadium" in destination_zone or "venue" in destination_zone:
        if scenario in ["concert", "sports_event"]:
            return {
                "factor": 0.15,
                "summary": "Historical venue event data supports +15% pricing."
            }
        return {
            "factor": 0.0,
            "summary": "Historical data shows standard pricing for non-event periods."
        }
    
    # Suburban areas (check both origin and destination)
    if "suburb" in origin_zone or "suburb" in destination_zone:
        return {
            "factor": 0.0,
            "summary": "Historical suburban patterns show stable pricing (no adjustment)."
        }
    
    # Default for unrecognized zones
    return {
        "factor": 0.02,
        "summary": "Historical patterns suggest slight upward adjustment (+2%)."
    }


def compute_corporate_pressure_factor(req: RecommendationRequest) -> Dict[str, any]:
    """
    Compute the influence of corporate revenue goals on pricing.
    
    This is a SOFT factor that nudges pricing but CANNOT override
    market physics (supply/demand) or ethical guardrails (emergencies).
    
    Returns a factor adjustment and summary.
    """
    if req.corporate_revenue_goal is None:
        return {
            "factor": 0.0,
            "summary": "No specific corporate revenue target set (no pressure adjustment)."
        }
    
    # Corporate goal is expressed as a target uplift (e.g., 0.15 = 15% revenue increase goal)
    goal = req.corporate_revenue_goal
    
    # Cap corporate pressure influence at reasonable levels
    # We don't let corporate pressure alone drive more than 8% adjustment
    capped_influence = min(goal, 0.08)
    
    # If there are strategy notes, include them in summary
    strategy_note = ""
    if req.corporate_strategy_notes:
        # Truncate if too long
        strategy_note = f" Strategy: {req.corporate_strategy_notes[:80]}..."
    
    if goal > 0.15:
        return {
            "factor": capped_influence,
            "summary": f"High corporate revenue target ({goal*100:.0f}%) encourages pricing increase, but capped at +{capped_influence*100:.0f}% to maintain market competitiveness.{strategy_note}"
        }
    elif goal > 0.08:
        return {
            "factor": capped_influence,
            "summary": f"Moderate corporate revenue goal ({goal*100:.0f}%) nudges pricing upward (+{capped_influence*100:.0f}%).{strategy_note}"
        }
    elif goal > 0.0:
        return {
            "factor": goal,
            "summary": f"Corporate revenue target ({goal*100:.0f}%) provides modest upward pressure.{strategy_note}"
        }
    else:
        return {
            "factor": 0.0,
            "summary": "No positive revenue target set (no corporate pressure).{strategy_note}"
        }


# ===== GUARDRAILS =====

def apply_guardrails(
    base_adjustment: float,
    scenario: str,
    loyalty_segment: str | None,
    factors: Dict[str, Dict[str, any]]
) -> Dict[str, any]:
    """
    Apply ethical and market-based guardrails to the recommended adjustment.
    
    Guardrails (in priority order):
    1. Emergency scenarios: NO surge pricing (cap at 0.0)
    2. Loyal customers: Soften any aggressive surge
    3. Corporate pressure: Cannot override emergency/ethics rules
    4. Maximum surge cap: Never exceed 2.0x (100% increase)
    
    Returns adjusted value and any flags/warnings.
    """
    scenario_lower = scenario.lower()
    adjusted = base_adjustment
    flags = []
    
    # GUARDRAIL 1: Emergency scenarios - NO SURGE
    if scenario_lower in ["emergency", "natural_disaster", "disaster"]:
        if base_adjustment > 0.0:
            flags.append("EMERGENCY_GUARDRAIL: Surge pricing blocked due to emergency situation.")
            adjusted = 0.0
        return {
            "adjusted_value": adjusted,
            "flags": flags,
            "guardrail_applied": "emergency"
        }
    
    # GUARDRAIL 2: Loyal customers get additional softening
    loyalty = (loyalty_segment or "standard").lower()
    if loyalty in ["platinum", "gold", "silver"]:
        # Already factored in compute_loyalty_factor, but we apply additional cap here
        if base_adjustment > 0.20:  # If surge is more than 20%
            loyalty_cap = 0.15 if loyalty == "platinum" else 0.18
            if adjusted > loyalty_cap:
                flags.append(f"LOYALTY_GUARDRAIL: Surge capped at {loyalty_cap*100:.0f}% for {loyalty} members.")
                adjusted = loyalty_cap
    
    # GUARDRAIL 3: Check if corporate pressure is pushing against ethics
    corp_factor = factors.get("corporate_pressure", {}).get("factor", 0.0)
    env_factor = factors.get("environment", {}).get("factor", 0.0)
    
    if corp_factor > 0.05 and scenario_lower in ["storm", "road_closure"]:
        flags.append("TENSION: Corporate revenue goals conflict with fair-pricing during disruption.")
    
    # GUARDRAIL 4: Absolute maximum surge cap
    MAX_SURGE = 1.0  # 100% increase maximum (2.0x multiplier)
    if adjusted > MAX_SURGE:
        flags.append(f"MAX_SURGE_GUARDRAIL: Adjustment capped at {MAX_SURGE*100:.0f}% to prevent excessive pricing.")
        adjusted = MAX_SURGE
    
    # GUARDRAIL 5: Never go negative (minimum 0% adjustment)
    if adjusted < 0.0:
        flags.append("FLOOR_GUARDRAIL: Negative pricing prevented (minimum 0%).")
        adjusted = 0.0
    
    guardrail_type = "none"
    if flags:
        guardrail_type = "active"
    
    return {
        "adjusted_value": adjusted,
        "flags": flags,
        "guardrail_applied": guardrail_type
    }


# ===== COMBINATION AND GOODNESS SCORING =====

def combine_factors(
    env: Dict[str, any],
    supply_demand: Dict[str, any],
    loyalty: Dict[str, any],
    historical: Dict[str, any],
    corporate_pressure: Dict[str, any]
) -> Dict[str, float]:
    """
    Combine individual factors into a single recommended adjustment and goodness score.
    
    Strategy:
    - Add all factor values to get a raw adjustment
    - Environment and supply/demand are weighted most heavily (market physics)
    - Corporate pressure is treated as a soft nudge
    - Goodness score reflects balance between revenue, fairness, and ethical constraints
    
    Returns:
        - recommended_adjustment: float (percentage, e.g., 0.10 for +10%)
        - goodness: float (0.0 to 1.0, higher is better balance)
    """
    # Extract factor values
    env_factor = env["factor"]
    supply_demand_factor = supply_demand["factor"]
    loyalty_factor = loyalty["factor"]
    historical_factor = historical["factor"]
    corp_factor = corporate_pressure["factor"]
    
    # Weighted combination
    # Market physics (env + supply/demand) get full weight
    # Historical gets moderate weight
    # Corporate pressure gets soft weight
    # Loyalty is a direct discount (negative)
    
    raw_adjustment = (
        env_factor * 1.0 +           # Full weight - market physics
        supply_demand_factor * 1.0 + # Full weight - market physics
        historical_factor * 0.6 +     # Historical patterns are informative but not decisive
        corp_factor * 0.4 +          # Corporate pressure is soft influence
        loyalty_factor * 1.0         # Loyalty discount applied fully
    )
    
    # Calculate goodness score (0.0 to 1.0)
    # Higher goodness = better balance of revenue, fairness, ethics
    goodness = calculate_goodness_score(
        raw_adjustment,
        env_factor,
        supply_demand_factor,
        loyalty_factor,
        corp_factor
    )
    
    return {
        "recommended_adjustment": raw_adjustment,
        "goodness": goodness
    }


def calculate_goodness_score(
    adjustment: float,
    env_factor: float,
    supply_demand_factor: float,
    loyalty_factor: float,
    corp_factor: float
) -> float:
    """
    Calculate a 'goodness' score from 0.0 to 1.0.
    
    High goodness (0.8-1.0): Balanced pricing that respects market, loyalty, and ethics
    Medium goodness (0.5-0.8): Acceptable but some tension
    Low goodness (0.0-0.5): Aggressive pricing or conflicts with guardrails
    
    Factors that increase goodness:
    - Moderate adjustments (not too high, not negative)
    - Strong market justification (supply/demand, environment)
    - Loyalty discounts for valued customers
    - Alignment between corporate goals and market reality
    
    Factors that decrease goodness:
    - Excessive surge (>30%)
    - High corporate pressure without market justification
    - Negative total adjustment (underpricing)
    """
    base_goodness = 0.80  # Start optimistic
    
    # Penalty for excessive surge
    if adjustment > 0.30:
        base_goodness -= (adjustment - 0.30) * 0.5  # Each 10% over 30% reduces by 5%
    
    # Penalty for underpricing (negative adjustment)
    if adjustment < 0.0:
        base_goodness -= abs(adjustment) * 0.3
    
    # Bonus for moderate, justified pricing (10-20% range with market support)
    if 0.10 <= adjustment <= 0.20:
        market_justification = env_factor + supply_demand_factor
        if market_justification > 0.10:
            base_goodness += 0.10
    
    # Penalty if corporate pressure is high but market doesn't support it
    market_support = env_factor + supply_demand_factor
    if corp_factor > 0.05 and market_support < 0.05:
        base_goodness -= 0.15  # Corporate pushing without market justification
    
    # Bonus for loyalty considerations
    if loyalty_factor < 0.0:  # Negative = discount
        base_goodness += abs(loyalty_factor) * 0.5  # Rewarding loyal customers
    
    # Ensure goodness stays in [0.0, 1.0] range
    goodness = max(0.0, min(1.0, base_goodness))
    
    return round(goodness, 2)


# ===== MAIN ORCHESTRATION FUNCTION =====

def build_recommendation(req: RecommendationRequest) -> RecommendationResponse:
    """
    Main orchestration function for building a pricing recommendation.
    
    This function:
    1. Computes all five factor dimensions
    2. Combines them into a raw adjustment
    3. Applies guardrails
    4. Calculates goodness score
    5. Returns a complete RecommendationResponse
    
    Note: The 'reasoning' field will be a placeholder until Dev 2 integrates LangChain.
    """
    # Step 1: Compute all factors
    env = compute_environment_factor(req)
    supply_demand = compute_supply_demand_factor(req)
    loyalty = compute_loyalty_factor(req)
    historical = compute_historical_factor(req)
    corporate_pressure = compute_corporate_pressure_factor(req)
    
    # Store factors for guardrail checking
    all_factors = {
        "environment": env,
        "supply_demand": supply_demand,
        "loyalty": loyalty,
        "historical": historical,
        "corporate_pressure": corporate_pressure
    }
    
    # Step 2: Combine factors
    combination = combine_factors(env, supply_demand, loyalty, historical, corporate_pressure)
    raw_adjustment = combination["recommended_adjustment"]
    goodness = combination["goodness"]
    
    # Step 3: Apply guardrails
    guardrail_result = apply_guardrails(
        raw_adjustment,
        req.scenario,
        req.loyalty_segment,
        all_factors
    )
    
    final_adjustment = guardrail_result["adjusted_value"]
    guardrail_flags = guardrail_result["flags"]
    
    # If guardrails changed the value significantly, adjust goodness
    if abs(final_adjustment - raw_adjustment) > 0.05:
        # Guardrails kicked in - this might affect goodness
        if guardrail_result["guardrail_applied"] == "emergency":
            goodness = max(goodness, 0.85)  # Ethical pricing is good
        elif guardrail_flags:
            goodness = max(0.60, goodness - 0.10)  # Some tension
    
    # Step 4: Build factor summaries for response
    factor_summaries = {
        "environment": env["summary"],
        "supply_demand": supply_demand["summary"],
        "loyalty": loyalty["summary"],
        "historical": historical["summary"],
        "corporate_pressure": corporate_pressure["summary"]
    }
    
    # Add guardrail info to summaries if any flags
    if guardrail_flags:
        factor_summaries["guardrails"] = " | ".join(guardrail_flags)
    
    # Step 5: Create reasoning (placeholder until LangChain integration by Dev 2)
    reasoning = _generate_placeholder_reasoning(
        req,
        final_adjustment,
        goodness,
        factor_summaries,
        guardrail_flags
    )
    
    # Step 6: Return complete response
    from app.models.recommendation import FactorReasoning
    
    return RecommendationResponse(
        recommended_adjustment=round(final_adjustment, 2),
        goodness=round(goodness, 2),
        factors=factor_summaries,
        overall_reasoning=reasoning,
        factor_reasoning=FactorReasoning()  # Empty factor reasoning for placeholder
    )


def _generate_placeholder_reasoning(
    req: RecommendationRequest,
    adjustment: float,
    goodness: float,
    factors: Dict[str, str],
    guardrail_flags: list
) -> str:
    """
    Generate a placeholder reasoning string until LangChain integration is complete.
    
    This will be replaced by Dev 2's LLM-generated explanation.
    """
    adjustment_pct = adjustment * 100
    
    reasoning_parts = [
        f"Pricing Analysis for {req.origin_zone} → {req.destination_zone} during {req.scenario}:",
        f"\nRecommended Adjustment: +{adjustment_pct:.0f}%",
        f"Confidence Score: {goodness:.2f}/1.00",
        f"\nFactor Breakdown:",
        f"• Environment: {factors['environment']}",
        f"• Supply/Demand: {factors['supply_demand']}",
        f"• Customer Loyalty: {factors['loyalty']}",
        f"• Historical Patterns: {factors['historical']}",
        f"• Corporate Strategy: {factors['corporate_pressure']}"
    ]
    
    if guardrail_flags:
        reasoning_parts.append(f"\n⚠️ Guardrails Applied:")
        for flag in guardrail_flags:
            reasoning_parts.append(f"• {flag}")
    
    reasoning_parts.append(
        f"\n[Note: This reasoning will be enhanced with natural language generation by the LangChain integration.]"
    )
    
    return "\n".join(reasoning_parts)

