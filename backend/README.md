# AI Pricing Monitor & Advisor - Backend

FastAPI backend for the AI Pricing Monitor & Advisor hackathon project.

## Developer: Dev 1 - Backend Core Pricing Logic

This implementation covers:
- ✅ Five factor computation functions (environment, supply/demand, loyalty, historical, corporate pressure)
- ✅ Factor combination and goodness score calculation
- ✅ Ethical and market-based guardrails
- ✅ Main recommendation orchestration function
- ✅ FastAPI REST API endpoint

## Quick Start

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration (optional for basic usage)
```

### 3. Run the Server

```bash
# From backend directory
uvicorn app.main:app --reload

# Or use the main file directly
python app/main.py
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### POST /api/v1/recommendation

Get a pricing recommendation based on current conditions.

**Request Body:**
```json
{
  "zone": "airport_corridor",
  "scenario": "road_closure",
  "time": "2025-11-27T18:00:00Z",
  "loyalty_segment": "gold",
  "notes": "evening commute, partial freeway closure",
  "corporate_revenue_goal": 0.15,
  "corporate_strategy_notes": "End-of-quarter revenue push"
}
```

**Response:**
```json
{
  "recommended_adjustment": 0.1,
  "goodness": 0.78,
  "factors": {
    "environment": "Road closure adds moderate travel time (+5%).",
    "supply_demand": "Peak commute hours with high demand (+15%).",
    "loyalty": "Gold member receives loyalty discount (-5%).",
    "historical": "Historical data shows airport trips typically succeed at 1.05x",
    "corporate_pressure": "Moderate corporate revenue goal (15%) nudges pricing upward"
  },
  "reasoning": "Detailed explanation..."
}
```

## Example Scenarios

### Scenario 1: Emergency Situation
```bash
curl -X POST http://localhost:8000/api/v1/recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "zone": "downtown",
    "scenario": "emergency",
    "time": "2025-12-01T14:00:00Z",
    "loyalty_segment": "standard"
  }'
```
**Expected:** Zero surge due to emergency guardrails, high goodness score

### Scenario 2: Concert Event with Corporate Pressure
```bash
curl -X POST http://localhost:8000/api/v1/recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "zone": "stadium",
    "scenario": "concert",
    "time": "2025-12-01T20:00:00Z",
    "loyalty_segment": "platinum",
    "corporate_revenue_goal": 0.20
  }'
```
**Expected:** Moderate surge justified by event, softened by platinum loyalty

### Scenario 3: Storm with Gold Member
```bash
curl -X POST http://localhost:8000/api/v1/recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "zone": "airport_corridor",
    "scenario": "storm",
    "time": "2025-12-01T07:30:00Z",
    "loyalty_segment": "gold",
    "corporate_revenue_goal": 0.10
  }'
```
**Expected:** Weather + morning rush + airport justify surge, gold loyalty softens it

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app factory
│   ├── api/
│   │   └── v1/
│   │       └── recommendation.py  # API routes
│   ├── core/
│   │   └── config.py              # Settings
│   ├── models/
│   │   └── recommendation.py      # Pydantic schemas
│   ├── services/
│   │   └── recommendation_service.py  # Core pricing logic (Dev 1)
│   └── integrations/
│       └── n8n_notifier.py        # N8N integration (Dev 4)
├── requirements.txt
├── .env.example
└── README.md
```

## Factor Computation Logic

### 1. Environment Factor
- Emergency/disaster: 0% (guardrails override)
- Road closure: +5%
- Storm/weather: +8%
- Concerts/events: +12%
- Holiday: +10%
- Normal: 0%

### 2. Supply/Demand Factor
- Peak commute (weekday 7-9am, 5-7pm): +10-15%
- Late night (11pm-4am): +12%
- Weekend nights: +18%
- Off-peak: 0%

### 3. Loyalty Factor
- Platinum: -10%
- Gold: -5%
- Silver: -3%
- Standard: 0%

### 4. Historical Factor
- Based on zone and scenario patterns
- Range: 0% to +15%

### 5. Corporate Pressure Factor
- Soft influence from revenue goals
- Capped at +8% to prevent overriding market physics
- Cannot override emergency guardrails

## Guardrails

1. **Emergency Protocol**: Zero surge during emergencies/disasters
2. **Loyalty Protection**: Additional caps for loyal customers (15-18% max)
3. **Maximum Surge**: Never exceed 100% increase (2.0x multiplier)
4. **Minimum Floor**: Never negative pricing
5. **Corporate Constraints**: Revenue goals cannot override ethics/market physics

## Goodness Score

The goodness score (0.0-1.0) reflects:
- **High (0.8-1.0)**: Balanced pricing respecting market, loyalty, ethics
- **Medium (0.5-0.8)**: Acceptable with some tension
- **Low (0.0-0.5)**: Aggressive pricing or conflicts

Factors:
- ✅ Moderate adjustments are better
- ✅ Strong market justification increases score
- ✅ Loyalty discounts increase score
- ❌ Excessive surge decreases score
- ❌ Corporate pressure without market support decreases score

## Integration Points

### For Dev 2 (Orchestrator & LangChain)
- Import `build_recommendation()` from `app.services.recommendation_service`
- Replace placeholder reasoning with LLM-generated text
- Optionally wrap factor functions as "agents"

### For Dev 3 (Frontend)
- API endpoint: `POST /api/v1/recommendation`
- CORS enabled for all origins (restrict in production)
- Full OpenAPI docs at `/docs`

### For Dev 4 (n8n)
- Add n8n webhook calls after recommendation generation
- Use `app/integrations/n8n_notifier.py` (to be created)
- Alert on low goodness scores or guardrail flags

### For Dev 5 (Data & Testing)
- Add scenario test cases
- Mock historical data patterns
- Validate factor ranges and guardrail behavior

## Testing

Run lightweight tests:
```bash
pytest
```

## Notes for Team

- All numeric factors return percentage adjustments (e.g., 0.10 = +10%)
- Guardrails are applied AFTER factor combination
- Corporate pressure is intentionally soft (max 8% influence)
- Emergency scenarios always result in 0% surge
- The `reasoning` field is currently a placeholder; Dev 2 will replace with LLM output

## Next Steps

- [ ] Dev 2: Integrate LangChain for natural language reasoning
- [ ] Dev 3: Build frontend console to consume this API
- [ ] Dev 4: Add n8n webhook integration for alerts
- [ ] Dev 5: Add comprehensive test scenarios and mock data

