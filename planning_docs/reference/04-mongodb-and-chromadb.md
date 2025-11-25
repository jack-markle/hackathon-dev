### MongoDB & ChromaDB – Reference

This document outlines how we might use **MongoDB** and **ChromaDB** in the project, even if the hackathon implementation uses mostly mock data.

---

### 1. Role in Our Architecture

- **MongoDB** (document DB):
  - Potential home for historical ride/pricing data.
  - Could store user profiles, loyalty tiers, or scenario logs.
- **ChromaDB** (vector store):
  - Potential store for **embedding-based lookups** (e.g., similar historical scenarios, policies, or pricing guidelines).

For the hackathon MVP, we may simulate these with in-memory or static data, but we still want patterns that would scale to real stores.

---

### 2. MongoDB Usage Pattern (Conceptual)

- Keep MongoDB access **behind a repository or service layer**:

```python
# backend/app/repositories/historical_repository.py
from typing import Any, Dict, List


class HistoricalRepository:
    """
    Conceptual repository for historical pricing/ride data.
    Implementation can be MongoDB, mock data, or another source.
    """

    def __init__(self, client: Any):
        self._client = client

    def find_similar_trips(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Returns mock or real records of historically similar trips.
        """
        ...
```

- This keeps the rest of the code agnostic to the chosen backend (real Mongo vs. mock).

---

### 3. ChromaDB Usage Pattern (Conceptual)

- ChromaDB would typically be used via LangChain’s **vector store** APIs, for example:
  - Storing text like “historic scenarios + outcomes” as embeddings.
  - Querying “similar situations” to inform the historical factor or explanation.
- For this hackathon, we can:
  - Stub or simplify this to static lookups.
  - Leave clear extension points if the sponsor wants real vector search later.

Conceptual pattern:

```python
from typing import List, Dict, Any


def query_similar_scenarios(embedding_client: Any, query_vector: List[float]) -> List[Dict[str, Any]]:
    """
    Wraps a ChromaDB or similar vector search client.
    Returns high-level scenario summaries instead of raw vectors.
    """
    ...
```

---

### 4. Best Practices for This Project

- Keep **data access behind interfaces** (repositories, utility functions) rather than sprinkling DB calls throughout agents.
- Given hackathon time:
  - Prefer **in-memory or file-backed mock data** with clear docstrings saying “replace with MongoDB/ChromaDB later”.
- Keep models and responses **independent** of specific storage technology:
  - The rest of the system should not care whether data came from MongoDB, CSV, or ChromaDB.
- If we do add real drivers:
  - Store connection URIs, credentials, and collection names in configuration (env vars / `config.py`), not inline constants.

---

### 5. Example Cursor Rule Snippet (MongoDB & ChromaDB)

Example `.cursor/rules/data-stores.mdc` content:

```text
When editing data access related to MongoDB or ChromaDB:
- Hide DB or vector-store specifics behind repository or helper functions.
- Favor simple mock or in-memory data sources for the hackathon, but document how they would map to real MongoDB/ChromaDB.
- Do not couple Pydantic models or API contracts directly to MongoDB schemas or ChromaDB internals.
- Keep all connection details and credentials in config/environment, never hard-coded in source files.
```

Use this rule when prompting in any `repositories/`, `data`, or `historical`-related modules.


