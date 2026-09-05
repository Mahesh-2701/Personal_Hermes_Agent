# Architecture

```
                ┌────────────────────┐
                │      Hermes        │
                │  Agent / Router    │
                └─────────┬──────────┘
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
     GitHub API       Codex CLI         Playwright
          │               │                │
          ▼               ▼                ▼
       GitHub         Local Code       Browser
                          │
                          ▼
                       Tests
                          │
                          ▼
                      Review
```

## Data Flow
1. **Agent Router**: Determines intent and selects the appropriate mode (BUILD, RESEARCH, etc.).
2. **Tools/Skills**: Executes actions against external platforms (GitHub, Google Workspace, etc.).
3. **Environment**: Managed via `.env` and `config.yaml`.
4. **Memory**: Hybrid approach using local files and persistent context.
