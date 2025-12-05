


How the backend combines parsed historical data with frontend user input:

## Data Flow Overview

### 1. **Frontend sends user input**
The frontend (`frontend/app/page.js`) sends a `RecommendationRequest` with:
- `origin_zone` and `destination_zone` (e.g., "downtown", "airport_corridor")
- `scenario` (e.g., "storm", "road_closure")
- `time` (ISO timestamp)
- `loyalty_segment` (e.g., "gold", "platinum")
- `corporate_revenue_goal` (e.g., 0.03 for 3%)
- `corporate_strategy_notes` (e.g., "Q4 revenue push")

### 2. **Backend loads historical data (cached)**
At startup, `DataLoader` loads and caches:
- `loyalty_distributions.json` → loyalty discount mappings
- `corporate_strategies.json` → predefined strategy templates
- `zone_historical_patterns.json` → zone/time multipliers
- `dynamic_pricing.csv` → 1000 historical ride records

### 3. **Combining user input with historical data**

#### **A. Loyalty Factor** (`compute_loyalty_factor`)
```python
# User provides: loyalty_segment = "gold"
# Historical data provides: loyalty_discounts["gold"] = -0.05

# Process:
1. Takes user's loyalty_segment from request
2. Looks up discount in loyalty_distributions.json
3. Returns factor based on historical discount data
```

#### **B. Corporate Pressure Factor** (`compute_corporate_pressure_factor`)
```python
# User provides: 
#   corporate_revenue_goal = 0.15 (15%)
#   corporate_strategy_notes = "Q4 revenue push"

# Historical data provides: corporate_strategies.json with strategy templates

# Process:
1. Takes user's corporate_strategy_notes
2. Matches it against predefined strategies in JSON (e.g., "q4_end_push")
3. Validates user's revenue_goal against typical_goal from matched strategy
4. Uses user's goal but adds context from historical strategy data
```

#### **C. Historical Factor** (`compute_historical_factor`) — most complex
This combines user input with two historical data sources:

**Step A: Pattern-based (from JSON)**
```python
# User provides: 
#   origin_zone = "downtown"
#   destination_zone = "airport_corridor"  
#   time = "2024-01-15T18:30:00Z" (evening)
#   scenario = "storm"

# Historical data provides: zone_historical_patterns.json

# Process:
1. Extracts time period from user's ISO timestamp → "Evening"
2. Looks up zone pattern for "airport_corridor" in JSON
3. Gets time_of_day_multiplier for "evening" = 1.12
4. Gets scenario_multiplier for "storm" = 1.15
5. Calculates: (1.12 * 1.15) - 1.0 = 0.288 (28.8% pattern factor)
```

**Step B: Data-driven (from CSV)**
```python
# User provides: same inputs as above

# Historical data provides: dynamic_pricing.csv with 1000 records

# Process:
1. Maps user's zones to CSV Location_Category:
   - "airport_corridor" → "Urban" (via _map_app_zone_to_csv_location)
   - "downtown" → "Urban"
2. Extracts time period from user's timestamp → "Evening"
3. Filters CSV DataFrame:
   - WHERE Location_Category IN ("Urban") 
   - AND Time_of_Booking = "Evening"
4. Calculates average cost of matching rides: e.g., $350.00
5. Calculates average cost of ALL rides (baseline): e.g., $300.00
6. Computes surge metric: (350/300) - 1.0 = 0.167 (16.7% CSV factor)
```

**Step C: Blending**
```python
# Combines both sources:
blended_factor = (pattern_factor * 0.6) + (csv_factor * 0.4)
                = (0.288 * 0.6) + (0.167 * 0.4)
                = 0.173 + 0.067
                = 0.24 (24% final historical factor)
```

### 4. **Final recommendation calculation**
All factors (including environment and supply/demand) are combined:
```python
final_adjustment = (
    environment_factor * 1.0 +
    supply_demand_factor * 1.0 +
    historical_factor * 0.6 +      # ← Uses blended historical data
    corporate_pressure_factor * 0.4 +
    loyalty_factor * 1.0
)
```

## Key Points

1. User input drives filtering: zones, time, scenario, and loyalty segment filter historical data.
2. Historical data provides context: JSON patterns and CSV averages inform adjustments.
3. Blending: The historical factor blends pattern-based (60%) and CSV-driven (40%) metrics.
4. Fallback: If historical data is missing, the system falls back to hardcoded logic.

This approach uses historical patterns while respecting current user inputs, producing data-informed recommendations.