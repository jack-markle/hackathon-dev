# API Quick Reference Guide

## Endpoint
```
POST http://localhost:8000/api/v1/recommendation
```

## Example Requests

### 1. Emergency Scenario (Zero Surge)
```json
{
  "zone": "downtown",
  "scenario": "emergency",
  "time": "2025-12-01T14:00:00Z",
  "loyalty_segment": "standard"
}
```
**Expected:** 0% adjustment, high goodness

### 2. Concert with Corporate Pressure
```json
{
  "zone": "stadium",
  "scenario": "concert",
  "time": "2025-12-01T20:00:00Z",
  "loyalty_segment": "gold",
  "corporate_revenue_goal": 0.20,
  "corporate_strategy_notes": "End-of-quarter revenue push"
}
```
**Expected:** ~15-20% adjustment, moderate goodness

### 3. Storm Morning Rush at Airport
```json
{
  "zone": "airport_corridor",
  "scenario": "storm",
  "time": "2025-12-02T07:30:00Z",
  "loyalty_segment": "platinum",
  "corporate_revenue_goal": 0.15
}
```
**Expected:** ~15-25% adjustment, good balance

### 4. Weekend Night Downtown
```json
{
  "zone": "downtown",
  "scenario": "normal",
  "time": "2025-12-06T22:00:00Z",
  "loyalty_segment": "silver"
}
```
**Expected:** ~12-18% adjustment (weekend entertainment demand)

### 5. Road Closure Evening Commute
```json
{
  "zone": "airport_corridor",
  "scenario": "road_closure",
  "time": "2025-12-01T18:00:00Z",
  "loyalty_segment": "gold",
  "corporate_revenue_goal": 0.15
}
```
**Expected:** ~8-15% adjustment

## Response Format
```json
{
  "recommended_adjustment": 0.15,
  "goodness": 0.78,
  "factors": {
    "environment": "Storm adds difficulty (+8%)",
    "supply_demand": "Peak hours high demand (+15%)",
    "loyalty": "Platinum member discount (-10%)",
    "historical": "Historical patterns support +5%",
    "corporate_pressure": "Corporate goal 15% nudges upward"
  },
  "reasoning": "Natural language explanation..."
}
```

## Field Values

### Zones
- `"downtown"`
- `"airport_corridor"`
- `"stadium"`
- `"suburbs"`
- `"venue"`

### Scenarios
- `"normal"`
- `"emergency"` / `"disaster"` (triggers 0% surge)
- `"storm"` / `"heavy_rain"` / `"snow"`
- `"road_closure"`
- `"concert"` / `"sports_event"` / `"festival"`
- `"holiday"` / `"new_year"` / `"thanksgiving"`

### Loyalty Segments
- `"standard"` (0% discount)
- `"silver"` (-3%)
- `"gold"` (-5%)
- `"platinum"` (-10%)

### Time Format
ISO 8601: `"2025-12-01T18:00:00Z"`

### Corporate Revenue Goal
Float: `0.15` = 15% revenue increase target
- Typically 0.0 to 0.25 (0% to 25%)
- Capped at 8% actual influence

## cURL Examples

### Basic Request
```bash
curl -X POST http://localhost:8000/api/v1/recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "zone": "downtown",
    "scenario": "storm",
    "time": "2025-12-01T18:00:00Z",
    "loyalty_segment": "gold"
  }'
```

### With Corporate Pressure
```bash
curl -X POST http://localhost:8000/api/v1/recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "zone": "airport_corridor",
    "scenario": "concert",
    "time": "2025-12-01T20:00:00Z",
    "loyalty_segment": "platinum",
    "corporate_revenue_goal": 0.20,
    "corporate_strategy_notes": "Q4 revenue push for airport corridor"
  }'
```

## Testing Guardrails

### Test Emergency Override
```json
{
  "zone": "downtown",
  "scenario": "emergency",
  "time": "2025-12-01T14:00:00Z",
  "corporate_revenue_goal": 0.50
}
```
**Should:** Return 0% despite high corporate goal

### Test Loyalty Cap
```json
{
  "zone": "stadium",
  "scenario": "concert",
  "time": "2025-12-06T21:00:00Z",
  "loyalty_segment": "platinum",
  "corporate_revenue_goal": 0.25
}
```
**Should:** Cap adjustment lower for platinum member

## Health Check
```bash
curl http://localhost:8000/api/v1/health
```

## Interactive Docs
http://localhost:8000/docs

