---
name: codebase-memory-mcp
description: Use when exploring codebases with CBM graph tools.
---

# Codebase Memory MCP (CBM) Skill

## Overview
Codebase Memory MCP (CBM) is a high-performance code intelligence engine featuring:
- Fast tree-sitter AST indexing across 162 languages.
- Hybrid LSP semantic type resolution for 10 major languages.
- 15 MCP tools (`search_graph`, `trace_path` / `trace_call_path`, `query_graph` [Cypher], `get_code_snippet`, `get_architecture`, `check_index_coverage`, `detect_changes`, `semantic_query`, `manage_adr`, etc.).
- Built-in 3D graph visualization UI at `localhost:9749`.
- 120x fewer tokens, 10x fewer tool calls vs file-by-file search.
- Zero external runtime dependencies (no Docker, Python, Node, or API keys needed; uses compiled-in embeddings).

## Installation & Configuration on Windows 11
1. **Download / Build CBM binary**: Place the `cbm` executable in your PATH or project directory (e.g., `C:/Program Files/cbm` or project root).
2. **Initialize CBM in a Repository**:
   ```bash
   cbm init
   cbm index
   ```
3. **Configure MCP in Hermes / Client**:
   Add CBM to your MCP configuration:
   ```json
   {
     "mcpServers": {
       "codebase-memory": {
         "command": "cbm",
         "args": ["mcp"]
       }
     }
   }
   ```
4. **Launch 3D Graph UI**:
   ```bash
   cbm ui --port 9749
   ```

## Key Tools & Usage
- `search_graph`: Semantic & structural code search across symbols, functions, and types.
- `trace_call_path`: Trace execution and call graphs between entrypoints and functions.
- `query_graph`: Advanced Cypher queries over the codebase graph.
- `get_architecture`: High-level system architecture extraction and dependency mapping.
- `semantic_query`: Vector/semantic code retrieval using built-in `nomic-embed-code` 768-dim embeddings.
