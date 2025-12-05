# Gap Analysis: CSV Fields Missing from Application

This document identifies fields present in `data/dynamic_pricing - dynamic_pricing.csv` that are not currently part of the `RecommendationRequest` model.

## CSV Fields Not in Application

### 1. `Number_of_Riders`
- **Type**: Integer (e.g., 90, 58, 42)
- **Description**: Current number of riders requesting rides in the area
- **Potential Use**: Supply/demand factor calculation - higher rider count indicates higher demand
- **How to Add**: Add `number_of_riders: int | None` to `RecommendationRequest` in `backend/app/models/recommendation.py`

### 2. `Number_of_Drivers`
- **Type**: Integer (e.g., 45, 39, 31)
- **Description**: Current number of available drivers in the area
- **Potential Use**: Supply/demand factor calculation - driver-to-rider ratio is critical for surge pricing
- **How to Add**: Add `number_of_drivers: int | None` to `RecommendationRequest` in `backend/app/models/recommendation.py`

### 3. `Number_of_Past_Rides`
- **Type**: Integer (e.g., 13, 72, 0)
- **Description**: Customer's historical ride count with the platform
- **Potential Use**: Enhanced loyalty factor - could refine loyalty tier assignment or provide additional discount
- **How to Add**: Add `number_of_past_rides: int | None` to `RecommendationRequest` in `backend/app/models/recommendation.py`

### 4. `Average_Ratings`
- **Type**: Float (e.g., 4.47, 4.06, 3.99)
- **Description**: Average rating of the customer (or possibly driver/ride quality metric)
- **Potential Use**: Could influence pricing decisions for high-value customers or quality assurance
- **How to Add**: Add `average_ratings: float | None` to `RecommendationRequest` in `backend/app/models/recommendation.py`

### 5. `Vehicle_Type`
- **Type**: String enum (e.g., "Premium", "Economy")
- **Description**: Type of vehicle requested or used
- **Potential Use**: Vehicle type affects base pricing - Premium vehicles should have higher adjustments
- **How to Add**: Add `vehicle_type: str | None` with validation (e.g., `Field(None, pattern="^(Premium|Economy)$")`) to `RecommendationRequest`

### 6. `Expected_Ride_Duration`
- **Type**: Integer (minutes, e.g., 90, 43, 76)
- **Description**: Expected duration of the ride in minutes
- **Potential Use**: Longer rides could justify higher pricing adjustments; duration affects driver availability
- **How to Add**: Add `expected_ride_duration: int | None` to `RecommendationRequest` in `backend/app/models/recommendation.py`

### 7. `Historical_Cost_of_Ride`
- **Type**: Float (e.g., 284.26, 173.87, 329.80)
- **Description**: Historical cost/pricing for similar rides
- **Potential Use**: Primary metric for historical factor - compare current recommendation against historical costs
- **How to Add**: Add `historical_cost_of_ride: float | None` to `RecommendationRequest` in `backend/app/models/recommendation.py`

## Field Mapping (CSV → Application)

| CSV Field | Application Field | Mapping Notes |
|-----------|------------------|---------------|
| `Location_Category` | `origin_zone` / `destination_zone` | CSV has single location; app has origin/destination. CSV values: Urban, Suburban, Rural. App zones: downtown, airport_corridor, suburbs, stadium, venue. **Mapping needed**: Urban→downtown, Suburban→suburbs, Rural→(may need new zone or map to suburbs) |
| `Customer_Loyalty_Status` | `loyalty_segment` | CSV values: Silver, Gold, Regular. App values: standard, gold, platinum, silver. **Mapping needed**: Regular→standard, Silver→silver, Gold→gold (platinum not in CSV) |
| `Time_of_Booking` | `time` | CSV values: Night, Evening, Afternoon, Morning. App uses ISO timestamp. **Mapping needed**: Extract time period from ISO timestamp and map to CSV categories |

## Implementation Recommendations

### Priority 1 (High Impact)
1. **`Number_of_Riders` and `Number_of_Drivers`**: Critical for accurate supply/demand calculations
2. **`Historical_Cost_of_Ride`**: Essential for data-driven historical factor computation

### Priority 2 (Medium Impact)
3. **`Vehicle_Type`**: Affects base pricing and should be considered in adjustments
4. **`Expected_Ride_Duration`**: Influences pricing justification

### Priority 3 (Low Impact - Enhancement)
5. **`Number_of_Past_Rides`**: Could refine loyalty calculations
6. **`Average_Ratings`**: Nice-to-have for customer value assessment

## Example Model Update

```python
class RecommendationRequest(BaseModel):
    # ... existing fields ...
    
    # New fields from CSV
    number_of_riders: int | None = Field(None, description="Current number of riders requesting rides")
    number_of_drivers: int | None = Field(None, description="Current number of available drivers")
    number_of_past_rides: int | None = Field(None, description="Customer's historical ride count")
    average_ratings: float | None = Field(None, ge=0.0, le=5.0, description="Average customer rating")
    vehicle_type: str | None = Field(None, pattern="^(Premium|Economy)$", description="Vehicle type requested")
    expected_ride_duration: int | None = Field(None, ge=0, description="Expected ride duration in minutes")
    historical_cost_of_ride: float | None = Field(None, ge=0.0, description="Historical cost for similar rides")
```

## Notes

- All new fields should be optional (`| None`) to maintain backward compatibility with existing API consumers
- The CSV data can be used for historical analysis even without these fields in the request model
- Consider creating a separate "EnhancedRecommendationRequest" model if backward compatibility is critical

