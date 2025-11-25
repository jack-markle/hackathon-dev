### FastAPI Backend – Reference

This document summarizes how we intend to use **FastAPI** for the AI Pricing Monitor & Advisor backend, with recommended patterns and an example Cursor rule.

---

### 1. Role in Our Architecture

- Exposes the main **`POST /api/v1/recommendation`** endpoint.
- Hosts any additional internal endpoints (e.g., health checks).
- Integrates with the **orchestrator** and **LangChain** components.
- Optionally calls out to **n8n** for logging/alerts (webhook).

---

### 2. Recommended Project Structure

Keep FastAPI code modular and explicit:

```bash
backend/
  app/
    main.py              # FastAPI app factory & entrypoint
    api/
      v1/
        recommendation.py  # Versioned API routes
    models/
      recommendation.py  # Pydantic schemas
    services/
      recommendation_service.py  # Core pricing logic (no HTTP)
    integrations/
      n8n_notifier.py    # Outbound HTTP to n8n
    core/
      config.py          # Settings (env vars, etc.)
```

Key ideas:

- **Routes** should be thin (input/output & wiring only).
- **Services** contain business logic and orchestration calls.
- **Models** are strictly Pydantic schemas.

---

### 3. Implementation Notes & Patterns

- Use an **app factory**:

```python
from fastapi import FastAPI
from app.api.v1 import recommendation


def create_app() -> FastAPI:
    app = FastAPI(title="AI Pricing Monitor & Advisor")
    app.include_router(recommendation.router, prefix="/api/v1")
    return app


app = create_app()
```

- Always define **request/response models** (no plain dicts) so:
  - Frontend and docs have a stable contract.
  - Validation and OpenAPI docs come for free.
- Keep **async** endpoints (and any outbound IO like n8n calls) truly non-blocking.

---

### 4. Best Practices for This Project

- **Version your API** (`/api/v1/...`) even in the hackathon, to leave room for future change.
- Centralize **configuration** (e.g., `N8N_WEBHOOK_URL`, model keys) in `core/config.py`.
- Use descriptive **tags** on routers (e.g., `tags=["recommendation"]`) for clean Swagger UI sections.
- Prefer returning **domain-specific models** rather than generic error messages (e.g., a simple error wrapper model for custom error cases, if we add them).
- Keep the recommendation endpoint:
  - Idempotent for the same input.
  - Deterministic (no hidden randomness in numeric outputs).

---

### 5. Example Cursor Rule Snippet (FastAPI)

You can drop a rule like this into `.cursor/rules/fastapi.mdc`:

```text
When editing backend FastAPI code:
- Keep routes thin and delegate logic to services in app/services.
- Always use Pydantic models from app/models for request/response bodies.
- Preserve the /api/v1/recommendation contract (fields and types) unless explicitly asked to change it.
- Prefer async endpoints and non-blocking outbound calls (e.g., to n8n).
```

Use this rule when prompting in backend files to help the assistant follow our chosen patterns.


