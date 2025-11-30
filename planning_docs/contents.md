### Milestones (`planning_docs/milestones`)

- **`01-architecture-and-project-setup.md`**: Defines overall architecture (console → orchestrator → agents → corporate pressure tool → n8n), repo layout (backend/frontend/orchestration/infra), core models (including corporate pressure fields), dev-lane split for 5 developers, and “definition of done” for initial setup.
- **`02-backend-recommendation-logic.md`**: Specifies how `/recommendation` computes environment, supply/demand, loyalty, historical, and corporate pressure factors, combines them into `recommended_adjustment` + `goodness`, and enforces guardrails (emergencies, loyal customers, corporate pressure as a soft influence).
- **`03-orchestrator-and-agents-langchain.md`**: Describes an orchestrator function that calls conceptual agents (including corporate pressure), aggregates factors, invokes a LangChain explanation chain, and returns a fully populated `RecommendationResponse` with aligned goodness and reasoning.
- **`04-frontend-pricing-analyst-console.md`**: Outlines the Next.js console UI (form + results layout), including corporate strategy inputs, API wiring, and UX for showing adjustment, goodness, and AI reasoning with loading/error/empty states.
- **`05-n8n-integration-and-alerting.md`**: Details the n8n webhook workflow, payload/flag shape (including `corporate_overruled_by_guardrails`), when and how the backend should POST alerts (low goodness / risk flags), and config via `N8N_WEBHOOK_URL`.
- **`06-polish-testing-and-demo-prep.md`**: Covers final UX polish, prompt refinement (including how corporate goals are described vs guardrails), scripted demo scenarios, light testing, and presentation/demo preparation.

### User stories (`planning_docs/user_stories`)

- **`dev_1_stories.md`**: Dev 1’s stories for backend core pricing logic – implementing factor functions (including corporate pressure), guardrails, numeric combination, and baseline tests.
- **`dev_2_stories.md`**: Dev 2’s stories for orchestrator, conceptual agents (environment, supply/demand, loyalty, historical, corporate pressure), and the LangChain explanation chain.
- **`dev_3_stories.md`**: Dev 3’s stories for the Next.js Pricing Analyst Console UI, including scenario form, corporate strategy inputs, API wiring, and result rendering.
- **`dev_4_stories.md`**: Dev 4’s stories for n8n workflow design, backend n8n integration utilities, alert triggering logic, and non-blocking behavior.
- **`dev_5_stories.md`**: Dev 5’s stories for mock data, scripted demo scenarios (with corporate pressure), cross-cutting testing/sanity checks, and presentation/demo scripting.

### Reference (`planning_docs/reference`)

- **`01-fastapi-backend.md`**: How we use FastAPI (structure, patterns, best practices) with a sample Cursor rule for backend work.
- **`02-nextjs-frontend.md`**: How we use Next.js App Router for the console (structure, UX patterns, fetch usage) plus a Cursor rule.
- **`03-langchain-orchestrator-and-agents.md`**: Patterns for agents + orchestrator + LangChain chain, with prompting guidance and a Cursor rule.
- **`04-mongodb-and-chromadb.md`**: Conceptual use of MongoDB/ChromaDB via repositories/helpers (mock-friendly), with a data-access Cursor rule.
- **`05-n8n-workflows-and-alerting.md`**: Expected n8n workflow shape, FastAPI integration, config, and an alerting Cursor rule.