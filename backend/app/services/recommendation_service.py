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
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import pandas as pd

from app.models.recommendation import RecommendationRequest, RecommendationResponse

logger = logging.getLogger(__name__)

# ===== DATA LOADER =====

class DataLoader:
    """
    Loads and caches mock data files and historical CSV data.
    Data is loaded once at module initialization and cached for performance.
    """
    def __init__(self):
        self.loyalty_data: Optional[Dict[str, Any]] = None
        self.corporate_strategies: Optional[Dict[str, Any]] = None
        self.zone_patterns: Optional[Dict[str, Any]] = None
        self.historical_df: Optional[pd.DataFrame] = None
        self._load_data()
    
    def _get_data_path(self, filename: str) -> Path:
        """Get absolute path to data file relative to backend directory."""
        # backend/app/services/recommendation_service.py -> backend -> project root -> data
        backend_dir = Path(__file__).parent.parent.parent
        project_root = backend_dir.parent
        return project_root / "data" / filename
    
    def _load_data(self):
        """Load all data files and cache them."""
        try:
            # Load loyalty distributions JSON
            loyalty_path = self._get_data_path("mock_data/loyalty_distributions.json")
            if loyalty_path.exists():
                with open(loyalty_path, 'r') as f:
                    self.loyalty_data = json.load(f)
                logger.info(f"Loaded loyalty distributions from {loyalty_path}")
            else:
                logger.warning(f"Loyalty distributions file not found: {loyalty_path}")
            
            # Load corporate strategies JSON
            corporate_path = self._get_data_path("mock_data/corporate_strategies.json")
            if corporate_path.exists():
                with open(corporate_path, 'r') as f:
                    self.corporate_strategies = json.load(f)
                logger.info(f"Loaded corporate strategies from {corporate_path}")
            else:
                logger.warning(f"Corporate strategies file not found: {corporate_path}")
            
            # Load zone historical patterns JSON
            zone_patterns_path = self._get_data_path("mock_data/zone_historical_patterns.json")
            if zone_patterns_path.exists():
                with open(zone_patterns_path, 'r') as f:
                    self.zone_patterns = json.load(f)
                logger.info(f"Loaded zone historical patterns from {zone_patterns_path}")
            else:
                logger.warning(f"Zone historical patterns file not found: {zone_patterns_path}")
            
            # Load historical CSV
            csv_path = self._get_data_path("dynamic_pricing - dynamic_pricing.csv")
            if csv_path.exists():
                self.historical_df = pd.read_csv(csv_path)
                logger.info(f"Loaded historical CSV with {len(self.historical_df)} records from {csv_path}")
            else:
                logger.warning(f"Historical CSV file not found: {csv_path}")
                
        except Exception as e:
            logger.error(f"Error loading data files: {e}", exc_info=True)
            # Continue with None values - functions will fall back to hardcoded logic
    
    def get_loyalty_discounts(self) -> Dict[str, float]:
        """Get loyalty discount mappings from loaded data."""
        if self.loyalty_data and "loyalty_discounts" in self.loyalty_data:
            return self.loyalty_data["loyalty_discounts"]
        return {}
    
    def get_corporate_strategy(self, strategy_key: str) -> Optional[Dict[str, Any]]:
        """Get corporate strategy by key from loaded data."""
        if self.corporate_strategies and "strategies" in self.corporate_strategies:
            return self.corporate_strategies["strategies"].get(strategy_key)
        return None
    
    def get_zone_pattern(self, zone: str) -> Optional[Dict[str, Any]]:
        """Get historical pattern for a zone from loaded data."""
        if self.zone_patterns and "zones" in self.zone_patterns:
            return self.zone_patterns["zones"].get(zone.lower())
        return None
    
    def get_historical_dataframe(self) -> Optional[pd.DataFrame]:
        """Get the loaded historical CSV DataFrame."""
        return self.historical_df


# Initialize data loader at module level (cached)
_data_loader = DataLoader()


# ===== FACTOR COMPUTATION FUNCTIONS =====

def compute_environment_factor(req: RecommendationRequest) -> Dict[str, Any]:
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


def compute_supply_demand_factor(req: RecommendationRequest) -> Dict[str, Any]:
    """
    Compute supply/demand impact on pricing.
    
    Considers: time of day, day of week, driver availability patterns.
    If number_of_riders and number_of_drivers are provided, uses them for data-driven calculation.
    Returns a factor adjustment and summary.
    """
    # Priority: Use real-time rider/driver data if available
    if req.number_of_riders is not None and req.number_of_drivers is not None:
        if req.number_of_drivers > 0:
            demand_supply_ratio = req.number_of_riders / req.number_of_drivers
            
            # High demand: ratio > 1.5 (more riders than drivers)
            if demand_supply_ratio > 2.0:
                factor = 0.20
                summary = f"Critical supply shortage: {req.number_of_riders} riders vs {req.number_of_drivers} drivers (ratio {demand_supply_ratio:.2f}) (+20%)."
            elif demand_supply_ratio > 1.5:
                factor = 0.15
                summary = f"High demand pressure: {req.number_of_riders} riders vs {req.number_of_drivers} drivers (ratio {demand_supply_ratio:.2f}) (+15%)."
            elif demand_supply_ratio > 1.0:
                factor = 0.10
                summary = f"Moderate demand pressure: {req.number_of_riders} riders vs {req.number_of_drivers} drivers (ratio {demand_supply_ratio:.2f}) (+10%)."
            elif demand_supply_ratio > 0.7:
                factor = 0.05
                summary = f"Balanced supply/demand: {req.number_of_riders} riders vs {req.number_of_drivers} drivers (ratio {demand_supply_ratio:.2f}) (+5%)."
            else:
                factor = 0.0
                summary = f"Surplus supply: {req.number_of_riders} riders vs {req.number_of_drivers} drivers (ratio {demand_supply_ratio:.2f}) (no adjustment)."
            
            # Apply vehicle type and duration modifiers if available
            vehicle_modifier = 0.0
            duration_modifier = 0.0
            
            if req.vehicle_type == "Premium":
                vehicle_modifier = 0.03  # Premium vehicles command higher pricing
                summary += f" Premium vehicle adds +3%."
            
            if req.expected_ride_duration is not None and req.expected_ride_duration > 45:
                duration_modifier = 0.02  # Longer rides justify slight premium
                summary += f" Extended duration ({req.expected_ride_duration} min) adds +2%."
            
            return {
                "factor": factor + vehicle_modifier + duration_modifier,
                "summary": summary
            }
        else:
            # Zero drivers - critical shortage
            return {
                "factor": 0.25,
                "summary": f"Critical driver shortage: {req.number_of_riders} riders but no available drivers (+25%)."
            }
    
    # Fallback to time-based logic if rider/driver data not available
    try:
        # Parse time to determine demand patterns
        time_obj = datetime.fromisoformat(req.time.replace('Z', '+00:00'))
        hour = time_obj.hour
        weekday = time_obj.weekday()  # 0 = Monday, 6 = Sunday
    except:
        # Default to moderate if we can't parse time
        base_factor = 0.05
        summary = "Moderate demand expected (default) (+5%)."
        
        # Still apply vehicle/duration modifiers if available
        vehicle_modifier = 0.0
        duration_modifier = 0.0
        
        if req.vehicle_type == "Premium":
            vehicle_modifier = 0.03
            summary += " Premium vehicle adds +3%."
        
        if req.expected_ride_duration is not None and req.expected_ride_duration > 45:
            duration_modifier = 0.02
            summary += f" Extended duration ({req.expected_ride_duration} min) adds +2%."
        
        return {
            "factor": base_factor + vehicle_modifier + duration_modifier,
            "summary": summary
        }
    
    # Consider both origin and destination zones for supply/demand
    origin_zone = req.origin_zone.lower()
    destination_zone = req.destination_zone.lower()
    
    # Peak hours (7-9 AM, 5-7 PM on weekdays)
    is_weekday = weekday < 5
    is_morning_rush = 7 <= hour <= 9
    is_evening_rush = 17 <= hour <= 19
    
    base_factor = 0.0
    summary = ""
    
    if is_weekday and (is_morning_rush or is_evening_rush):
        # High-demand zones: airport or downtown in either origin or destination
        base_factor = 0.15 if ("airport" in origin_zone or "airport" in destination_zone or 
                          "downtown" in origin_zone or "downtown" in destination_zone) else 0.10
        summary = f"Peak commute hours with high demand ({'+15%' if base_factor == 0.15 else '+10%'})."
    elif hour >= 23 or hour <= 4:
        base_factor = 0.12
        summary = "Late night hours with limited driver availability (+12%)."
    elif weekday in [4, 5] and (hour >= 20 or hour <= 2):  # Friday/Saturday 8 PM - 2 AM
        base_factor = 0.18
        summary = "Weekend night with high entertainment demand (+18%)."
    elif not is_weekday and 10 <= hour <= 18:
        base_factor = 0.05
        summary = "Weekend leisure travel - moderate demand (+5%)."
    else:
        base_factor = 0.0
        summary = "Off-peak hours with balanced supply and demand (no adjustment)."
    
    # Apply vehicle type and duration modifiers if available
    vehicle_modifier = 0.0
    duration_modifier = 0.0
    
    if req.vehicle_type == "Premium":
        vehicle_modifier = 0.03
        summary += " Premium vehicle adds +3%."
    
    if req.expected_ride_duration is not None and req.expected_ride_duration > 45:
        duration_modifier = 0.02
        summary += f" Extended duration ({req.expected_ride_duration} min) adds +2%."
    
    return {
        "factor": base_factor + vehicle_modifier + duration_modifier,
        "summary": summary
    }


def compute_loyalty_factor(req: RecommendationRequest) -> Dict[str, Any]:
    """
    Compute loyalty tier discount/adjustment.
    
    Loyal customers receive preferential treatment and softer surge pricing.
    Returns a factor adjustment (typically negative) and summary.
    Uses data from loyalty_distributions.json if available, falls back to hardcoded values.
    """
    loyalty = (req.loyalty_segment or "standard").lower()
    
    # Try to get discount from loaded data
    loyalty_discounts = _data_loader.get_loyalty_discounts()
    
    if loyalty_discounts and loyalty in loyalty_discounts:
        discount = loyalty_discounts[loyalty]
        discount_pct = abs(discount) * 100
        return {
            "factor": discount,
            "summary": f"{loyalty.capitalize()} member receives loyalty discount ({discount_pct:.0f}% reduction)."
        }
    
    # Fallback to hardcoded logic if data not available
    if loyalty == "platinum":
        return {
            "factor": -0.10,
            "summary": "Platinum member receives premium loyalty discount (-10%)."
        }
    
    if loyalty == "gold":
        return {
            "factor": -0.05,
            "summary": "Gold member receives loyalty discount and softened surge (-5%)."
        }
    
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


def _map_app_zone_to_csv_location(zone: str) -> Optional[str]:
    """Map application zone names to CSV Location_Category values."""
    zone_lower = zone.lower()
    if "airport" in zone_lower or "downtown" in zone_lower or "urban" in zone_lower:
        return "Urban"
    elif "suburb" in zone_lower or "suburban" in zone_lower:
        return "Suburban"
    elif "rural" in zone_lower:
        return "Rural"
    return None


def _extract_time_period_from_iso(time_str: str) -> Optional[str]:
    """Extract time period (Morning, Afternoon, Evening, Night) from ISO timestamp."""
    try:
        time_obj = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        hour = time_obj.hour
        
        if 6 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:  # 21-23 or 0-5
            return "Night"
    except:
        return None


def _get_pattern_multiplier(zone_pattern: Dict[str, Any], time_period: str, scenario: str) -> float:
    """Get multiplier from zone patterns JSON based on time period and scenario."""
    if not zone_pattern:
        return 1.0
    
    # Get time-of-day multiplier
    time_multiplier = 1.0
    if "time_of_day_multipliers" in zone_pattern:
        for period_name, period_data in zone_pattern["time_of_day_multipliers"].items():
            if period_name.lower() == time_period.lower():
                time_multiplier = period_data.get("base_multiplier", 1.0)
                break
    
    # Get scenario multiplier
    scenario_multiplier = 1.0
    if "scenario_multipliers" in zone_pattern:
        scenario_multiplier = zone_pattern["scenario_multipliers"].get(scenario.lower(), 1.0)
    
    # Combine multipliers (cumulative as per JSON notes)
    combined_multiplier = time_multiplier * scenario_multiplier
    
    # Convert to adjustment factor (multiplier - 1.0)
    return combined_multiplier - 1.0


def compute_historical_factor(req: RecommendationRequest) -> Dict[str, Any]:
    """
    Compute adjustment based on historical pricing patterns.
    
    Uses zone_historical_patterns.json for pattern-based multipliers and
    dynamic_pricing.csv for data-driven historical analysis.
    Blends both sources for a comprehensive historical factor.
    """
    origin_zone = req.origin_zone.lower()
    destination_zone = req.destination_zone.lower()
    scenario = req.scenario.lower()
    
    # Step A: Get pattern-based multiplier from JSON
    pattern_factor = 0.0
    pattern_summary = ""
    
    # Try to get zone pattern (prefer destination zone, fallback to origin)
    zone_pattern = _data_loader.get_zone_pattern(destination_zone)
    if not zone_pattern:
        zone_pattern = _data_loader.get_zone_pattern(origin_zone)
    
    time_period = _extract_time_period_from_iso(req.time)
    
    if zone_pattern and time_period:
        pattern_factor = _get_pattern_multiplier(zone_pattern, time_period, scenario)
        pattern_summary = f"Pattern-based analysis suggests {pattern_factor*100:+.0f}% adjustment"
    else:
        # Fallback to hardcoded logic if patterns not available
        if "airport" in destination_zone:
            pattern_factor = 0.05 if scenario in ["normal", "road_closure"] else 0.08
            pattern_summary = "Airport corridor historical patterns"
        elif "downtown" in origin_zone or "downtown" in destination_zone:
            pattern_factor = 0.10 if scenario in ["concert", "sports_event"] else 0.03
            pattern_summary = "Downtown historical patterns"
        elif "stadium" in origin_zone or "venue" in origin_zone or "stadium" in destination_zone or "venue" in destination_zone:
            pattern_factor = 0.15 if scenario in ["concert", "sports_event"] else 0.0
            pattern_summary = "Stadium/venue historical patterns"
        elif "suburb" in origin_zone or "suburb" in destination_zone:
            pattern_factor = 0.0
            pattern_summary = "Suburban historical patterns"
        else:
            pattern_factor = 0.02
            pattern_summary = "Default historical patterns"
    
    # Step B: Get data-driven metric from CSV or use provided historical_cost_of_ride
    csv_factor = 0.0
    csv_summary = ""
    historical_df = _data_loader.get_historical_dataframe()
    
    # Priority: Use provided historical_cost_of_ride if available
    if req.historical_cost_of_ride is not None and req.historical_cost_of_ride > 0:
        # Compare provided historical cost against baseline
        baseline_cost = None
        
        if historical_df is not None and not historical_df.empty:
            try:
                # Try to get a relevant baseline from CSV
                origin_location = _map_app_zone_to_csv_location(req.origin_zone)
                dest_location = _map_app_zone_to_csv_location(req.destination_zone)
                
                filtered_df = historical_df.copy()
                
                # Filter by location if available
                if origin_location or dest_location:
                    location_filter = False
                    if origin_location:
                        location_filter = (filtered_df["Location_Category"] == origin_location)
                    if dest_location:
                        location_filter = location_filter | (filtered_df["Location_Category"] == dest_location)
                    filtered_df = filtered_df[location_filter]
                
                # Filter by time period if available
                if time_period:
                    filtered_df = filtered_df[filtered_df["Time_of_Booking"] == time_period]
                
                if not filtered_df.empty and "Historical_Cost_of_Ride" in filtered_df.columns:
                    baseline_cost = filtered_df["Historical_Cost_of_Ride"].mean()
                else:
                    # Fallback to global average
                    baseline_cost = historical_df["Historical_Cost_of_Ride"].mean()
            except Exception as e:
                logger.warning(f"Error processing CSV for baseline: {e}", exc_info=True)
                # Fallback to global average
                if historical_df is not None and "Historical_Cost_of_Ride" in historical_df.columns:
                    baseline_cost = historical_df["Historical_Cost_of_Ride"].mean()
        
        # If we have a baseline, calculate factor
        if baseline_cost is not None and baseline_cost > 0:
            csv_factor = (req.historical_cost_of_ride / baseline_cost) - 1.0
            csv_summary = f"Provided historical cost (${req.historical_cost_of_ride:.2f}) vs baseline (${baseline_cost:.2f}) suggests {csv_factor*100:+.1f}% adjustment"
        else:
            # No baseline available - use a conservative estimate
            csv_summary = f"Historical cost provided (${req.historical_cost_of_ride:.2f}) but no baseline available for comparison"
            csv_factor = 0.0
    
    # Fallback: Use CSV data if historical_cost_of_ride not provided
    elif historical_df is not None and not historical_df.empty:
        try:
            # Map zones to CSV Location_Category
            origin_location = _map_app_zone_to_csv_location(req.origin_zone)
            dest_location = _map_app_zone_to_csv_location(req.destination_zone)
            
            # Filter CSV data
            filtered_df = historical_df.copy()
            
            # Filter by location (check both origin and destination mappings)
            if origin_location or dest_location:
                location_filter = False
                if origin_location:
                    location_filter = (filtered_df["Location_Category"] == origin_location)
                if dest_location:
                    location_filter = location_filter | (filtered_df["Location_Category"] == dest_location)
                filtered_df = filtered_df[location_filter]
            
            # Filter by time period if available
            if time_period:
                filtered_df = filtered_df[filtered_df["Time_of_Booking"] == time_period]
            
            if not filtered_df.empty and "Historical_Cost_of_Ride" in filtered_df.columns:
                # Calculate average cost for matching rides
                avg_matching_cost = filtered_df["Historical_Cost_of_Ride"].mean()
                
                # Calculate average cost for all rides (baseline)
                avg_all_cost = historical_df["Historical_Cost_of_Ride"].mean()
                
                if avg_all_cost > 0:
                    # Calculate surge metric: (matching_avg / all_avg) - 1.0
                    csv_factor = (avg_matching_cost / avg_all_cost) - 1.0
                    csv_summary = f"CSV data shows {csv_factor*100:+.1f}% historical surge for similar rides"
                else:
                    csv_summary = "CSV data available but baseline cost is zero"
            else:
                csv_summary = "No matching CSV records found for this zone/time combination"
        except Exception as e:
            logger.warning(f"Error processing CSV data: {e}", exc_info=True)
            csv_summary = "CSV data processing error"
    
    # Step C: Blend pattern-based and CSV-based factors
    # Weight: 60% pattern (from JSON), 40% CSV data (or provided historical cost)
    blended_factor = (pattern_factor * 0.6) + (csv_factor * 0.4)
    
    # Build summary
    if csv_summary:
        summary = f"{pattern_summary}. {csv_summary}. Blended historical factor: {blended_factor*100:+.1f}%"
    else:
        summary = f"{pattern_summary}. Historical factor: {pattern_factor*100:+.1f}%"
    
    return {
        "factor": round(blended_factor, 3),
        "summary": summary
    }


def compute_corporate_pressure_factor(req: RecommendationRequest, enable_guardrails: bool = True) -> Dict[str, Any]:
    """
    Compute the influence of corporate revenue goals on pricing.
    
    This is a SOFT factor that nudges pricing but CANNOT override
    market physics (supply/demand) or ethical guardrails (emergencies).
    
    Uses corporate_strategies.json if available to validate strategy notes and adjust factors.
    Returns a factor adjustment and summary.
    
    Args:
        enable_guardrails: If False, applies full corporate goal without 8% cap
    """
    if req.corporate_revenue_goal is None:
        return {
            "factor": 0.0,
            "summary": "No specific corporate revenue target set (no pressure adjustment)."
        }
    
    # Corporate goal is expressed as a target uplift (e.g., 0.15 = 15% revenue increase goal)
    goal = req.corporate_revenue_goal
    
    # Try to match strategy notes to a predefined strategy
    matched_strategy = None
    strategy_note = ""
    
    if req.corporate_strategy_notes:
        strategy_notes_lower = req.corporate_strategy_notes.lower()
        # Check if strategy notes match any predefined strategy key
        if _data_loader.corporate_strategies and "strategies" in _data_loader.corporate_strategies:
            for strategy_key, strategy_data in _data_loader.corporate_strategies["strategies"].items():
                # Check if strategy key or description appears in notes
                if strategy_key.replace("_", " ") in strategy_notes_lower or \
                   (isinstance(strategy_data, dict) and 
                    strategy_data.get("strategy_notes", "").lower() in strategy_notes_lower):
                    matched_strategy = strategy_data
                    break
        
        # Include strategy notes in summary (truncate if too long)
        strategy_note = f" Strategy: {req.corporate_strategy_notes[:80]}..."
    
    # If we matched a strategy, validate goal against strategy's typical range
    if matched_strategy and "typical_goal" in matched_strategy:
        typical_goal = matched_strategy["typical_goal"]
        # If provided goal is significantly different from typical, use typical as reference
        # but still respect the provided goal (just note the difference)
        if abs(goal - typical_goal) > 0.05:
            # Goal differs from typical - use provided goal but note it
            strategy_note += f" (Typical for this strategy: {typical_goal*100:.0f}%)"
    
    # Cap corporate pressure influence at reasonable levels (only when guardrails enabled)
    # We don't let corporate pressure alone drive more than 8% adjustment
    if enable_guardrails:
        capped_influence = min(goal, 0.08)
    else:
        capped_influence = goal  # Apply full goal when guardrails disabled
    
    if goal > 0.15:
        if enable_guardrails:
            return {
                "factor": capped_influence,
                "summary": f"High corporate revenue target ({goal*100:.0f}%) encourages pricing increase, but capped at +{capped_influence*100:.0f}% to maintain market competitiveness.{strategy_note}"
            }
        else:
            return {
                "factor": capped_influence,
                "summary": f"High corporate revenue target ({goal*100:.0f}%) applied fully (+{capped_influence*100:.0f}%) - guardrails disabled.{strategy_note}"
            }
    elif goal > 0.08:
        if enable_guardrails:
            return {
                "factor": capped_influence,
                "summary": f"Moderate corporate revenue goal ({goal*100:.0f}%) nudges pricing upward (+{capped_influence*100:.0f}%).{strategy_note}"
            }
        else:
            return {
                "factor": capped_influence,
                "summary": f"Moderate corporate revenue goal ({goal*100:.0f}%) applied fully (+{capped_influence*100:.0f}%) - guardrails disabled.{strategy_note}"
            }
    elif goal > 0.0:
        return {
            "factor": goal,
            "summary": f"Corporate revenue target ({goal*100:.0f}%) provides modest upward pressure.{strategy_note}"
        }
    else:
        return {
            "factor": 0.0,
            "summary": f"No positive revenue target set (no corporate pressure).{strategy_note}"
        }


# ===== GUARDRAILS =====

def apply_guardrails(
    base_adjustment: float,
    scenario: str,
    loyalty_segment: str | None,
    factors: Dict[str, Dict[str, Any]],
    enable_guardrails: bool = True
) -> Dict[str, Any]:
    """
    Apply ethical and market-based guardrails to the recommended adjustment.
    
    Guardrails (in priority order):
    1. Emergency scenarios: NO surge pricing (cap at 0.0)
    2. Loyal customers: Soften any aggressive surge
    3. Corporate pressure: Cannot override emergency/ethics rules
    4. Maximum surge cap: Never exceed 2.0x (100% increase)
    
    Args:
        enable_guardrails: If False, returns raw adjustment without any guardrail modifications
    
    Returns adjusted value and any flags/warnings.
    """
    # If guardrails are disabled, return raw adjustment with no flags
    if not enable_guardrails:
        return {
            "adjusted_value": base_adjustment,
            "flags": [],
            "guardrail_applied": "disabled"
        }
    
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
    env: Dict[str, Any],
    supply_demand: Dict[str, Any],
    loyalty: Dict[str, Any],
    historical: Dict[str, Any],
    corporate_pressure: Dict[str, Any],
    enable_guardrails: bool = True
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
        corp_factor,
        enable_guardrails=enable_guardrails
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
    corp_factor: float,
    enable_guardrails: bool = True
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
    
    Args:
        enable_guardrails: If False, applies more aggressive penalties for high corporate pressure
    """
    if enable_guardrails:
        base_goodness = 0.80  # Start optimistic
    else:
        base_goodness = 0.70  # Start lower when guardrails disabled (more cautious)
    
    # Penalty for excessive surge
    if adjustment > 0.30:
        base_goodness -= (adjustment - 0.30) * 0.5  # Each 10% over 30% reduces by 5%
    
    # Penalty for underpricing (negative adjustment)
    if adjustment < 0.0:
        base_goodness -= abs(adjustment) * 0.3
    
    # Bonus for moderate, justified pricing (10-20% range with market support)
    # Only apply bonus when guardrails are enabled (ethical pricing is rewarded)
    if enable_guardrails and 0.10 <= adjustment <= 0.20:
        market_justification = env_factor + supply_demand_factor
        if market_justification > 0.10:
            base_goodness += 0.10
    
    # Penalty for corporate pressure - more aggressive when guardrails disabled
    market_support = env_factor + supply_demand_factor
    if enable_guardrails:
        # Standard penalty: corporate pressure without market support
        if corp_factor > 0.05 and market_support < 0.05:
            base_goodness -= 0.15  # Corporate pushing without market justification
    else:
        # Aggressive penalty when guardrails disabled: penalize high corporate pressure more
        if corp_factor > 0.10:  # High corporate pressure (>10%)
            # Penalty increases with corporate pressure level
            penalty = min(0.40, corp_factor * 2.0)  # Up to -40% penalty for very high pressure
            base_goodness -= penalty
            # Additional penalty if market doesn't support it
            if market_support < 0.10:
                base_goodness -= 0.20  # Extra penalty for pushing without market support
        elif corp_factor > 0.05:
            base_goodness -= 0.20  # Moderate corporate pressure still penalized
    
    # Bonus for loyalty considerations (only when guardrails enabled)
    if enable_guardrails and loyalty_factor < 0.0:  # Negative = discount
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
    enable_guardrails = req.enable_guardrails if req.enable_guardrails is not None else True
    env = compute_environment_factor(req)
    supply_demand = compute_supply_demand_factor(req)
    loyalty = compute_loyalty_factor(req)
    historical = compute_historical_factor(req)
    corporate_pressure = compute_corporate_pressure_factor(req, enable_guardrails=enable_guardrails)
    
    # Store factors for guardrail checking
    all_factors = {
        "environment": env,
        "supply_demand": supply_demand,
        "loyalty": loyalty,
        "historical": historical,
        "corporate_pressure": corporate_pressure
    }
    
    # Step 2: Combine factors
    combination = combine_factors(env, supply_demand, loyalty, historical, corporate_pressure, enable_guardrails=enable_guardrails)
    raw_adjustment = combination["recommended_adjustment"]
    goodness = combination["goodness"]
    
    # Step 3: Apply guardrails (if enabled)
    enable_guardrails = req.enable_guardrails if req.enable_guardrails is not None else True
    guardrail_result = apply_guardrails(
        raw_adjustment,
        req.scenario,
        req.loyalty_segment,
        all_factors,
        enable_guardrails=enable_guardrails
    )
    
    final_adjustment = guardrail_result["adjusted_value"]
    guardrail_flags = guardrail_result["flags"]
    
    # If guardrails changed the value significantly, adjust goodness (only when guardrails are enabled)
    if enable_guardrails and abs(final_adjustment - raw_adjustment) > 0.05:
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

