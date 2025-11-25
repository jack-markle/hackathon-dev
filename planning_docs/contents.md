### Milestones (`planning_docs/milestones`)

- **`01-architecture-and-project-setup.md`**: Defines overall architecture (console → orchestrator → agents → n8n), repo layout (backend/frontend/orchestration/infra), skeleton files (FastAPI, Next.js, agents, chain), and “definition of done” for initial setup.
- **`02-backend-recommendation-logic.md`**: Specifies how `/recommendation` should compute environment, supply/demand, loyalty, and historical factors, combine them into `recommended_adjustment` + `goodness`, and enforce guardrails (emergencies, loyal customers).
- **`03-orchestrator-and-agents-langchain.md`**: Describes an orchestrator function that calls conceptual agents, aggregates factors, invokes a LangChain explanation chain, and returns a fully populated `RecommendationResponse`.
- **`04-frontend-pricing-analyst-console.md`**: Outlines the Next.js console UI (form + results layout), API wiring, and UX for showing adjustment, goodness, and AI reasoning with loading/error/empty states.
- **`05-n8n-integration-and-alerting.md`**: Details the n8n webhook workflow, when and how the backend should POST alerts (low goodness / risk flags), and config via `N8N_WEBHOOK_URL`.
- **`06-polish-testing-and-demo-prep.md`**: Covers final UX polish, prompt refinement, scripted demo scenarios, light testing, and presentation/demo preparation.

### User stories (`planning_docs/user_stories`)

- **`01-user-stories-architecture-and-setup.md`**: Stories for shared architecture understanding, repo skeletons, stable API contract, and local dev setup.
- **`02-user-stories-backend-recommendation.md`**: Stories for computing combined adjustment, factor functions, guardrails, and a simple goodness metric.
- **`03-user-stories-orchestrator-and-agents.md`**: Stories for a single orchestrator entrypoint, explicit agents, LangChain explanations, and consistency between goodness and explanation.
- **`04-user-stories-frontend-console.md`**: Stories for submitting scenarios, viewing recommendations/goodness, factor breakdown + reasoning, and robust UI states/layout.
- **`05-user-stories-n8n-integration.md`**: Stories for alerting on low-goodness/high-risk cases, non-blocking integration, configurable webhook, and a demonstrable alert scenario.
- **`06-user-stories-polish-and-demo.md`**: Stories for analyst-friendly UX, business-like explanations, scripted demo scenarios, basic stability/testing, and presentation narrative.

### Reference (`planning_docs/reference`)

- **`01-fastapi-backend.md`**: How we use FastAPI (structure, patterns, best practices) with a sample Cursor rule for backend work.
- **`02-nextjs-frontend.md`**: How we use Next.js App Router for the console (structure, UX patterns, fetch usage) plus a Cursor rule.
- **`03-langchain-orchestrator-and-agents.md`**: Patterns for agents + orchestrator + LangChain chain, with prompting guidance and a Cursor rule.
- **`04-mongodb-and-chromadb.md`**: Conceptual use of MongoDB/ChromaDB via repositories/helpers (mock-friendly), with a data-access Cursor rule.
- **`05-n8n-workflows-and-alerting.md`**: Expected n8n workflow shape, FastAPI integration, config, and an alerting Cursor rule.