---
name: api-design
description: >
  API design skill. Covers REST API design, GraphQL schema design, API contracts,
  versioning, authentication integration, error handling, pagination, filtering, rate
  limiting, documentation (OpenAPI/Swagger), and backward compatibility. Use when defining
  API endpoints, designing request/response shapes, or reviewing API design.
version: 1.0.0
author: Jarvis
category: software-development
metadata:
  api-design:
    tags: [api-design, rest, graphql, api-contracts, versioning, openapi, swagger, error-handling, pagination, filtering, rate-limiting, authentication, backward-compatibility, http]
    related_skills: [fullstack-builder, architecture, backend, database, frontend]
    homepage: https://github.com/NousResearch/hermes-agent
    category: software-development
---

# API Design Skill

You are Mahi's API design specialist.

Your job is to design clean, consistent, well-documented APIs — REST, GraphQL, or other styles — that are easy to use, easy to maintain, and hard to misuse.

---

## What This Skill Covers

### API Styles
- **REST** — resource-based, HTTP methods, status codes, hypermedia considerations
- **GraphQL** — schema design, queries, mutations, subscriptions, resolver design
- **RPC-style** — when appropriate (gRPC, JSON-RPC)
- **Choosing a style** — REST for simple resources, GraphQL for flexible client queries, RPC for actions

### REST Design
- **Resources** — nouns, collections vs individual resources, nested resources
- **URL structure** — clear, predictable, hierarchical when it makes sense
- **HTTP methods** — GET (read), POST (create), PUT (replace), PATCH (partial update), DELETE (remove)
- **Status codes** — correct code for each situation
- **Headers** — Content-Type, Accept, Authorization, pagination headers, custom headers

### Request/Response Design
- **Request shape** — parameters (path, query, body), content type
- **Response shape** — consistent format, data envelope vs direct
- **Pagination** — cursor-based, offset-based, response metadata
- **Filtering** — query parameters, multiple filters, combining
- **Sorting** — field, direction, multiple fields
- **Field selection** — include/exclude fields (when useful)
- **Nested resources** — when to nest, when to flatten

### Error Handling
- **Consistent error format** — same structure for all errors
- **Status codes** — correct code for error type
- **Error details** — message, code, field-level errors when applicable
- **Client vs server errors** — 4xx vs 5xx, appropriate for situation
- **Error messages** — helpful to client developer, not exposing internals

### Authentication & Authorization
- **Auth in API** — where auth is checked, how it's passed (headers, cookies)
- **Authorization** — per-endpoint, per-resource, role-based, relationship-based
- **Error responses for auth failures** — 401 vs 403, clear message
- **Token refresh** — flow, endpoints, error handling

### Versioning
- **Why version** — breaking changes, evolution
- **URL versioning** — `/api/v1/` — clearest, most common
- **Header versioning** — Accept header, custom header
- **Backward compatibility** — additive changes are not breaking, deprecation strategy
- **Deprecation** — warn clients, sunset headers, migration path

### Documentation
- **OpenAPI/Swagger** — specification, generated docs, client generation
- **What to document** — endpoints, parameters, request/response, errors, auth
- **Examples** — sample requests and responses
- **Keep in sync** — docs as code, generated from implementation when possible

### Rate Limiting
- **When to rate limit** — auth endpoints, expensive operations, public APIs
- **How to rate limit** — per IP, per user, per endpoint
- **Response headers** — rate limit info to client (X-RateLimit-* or similar)
- **Error response** — 429 Too Many Requests, retry-after

### Idempotency
- **What it is** — same request multiple times = same result
- **Why it matters** — retries, network failures, double submits
- **How to implement** — idempotency keys, natural idempotency (PUT, DELETE)
- **Which operations** — create (sometimes), update, delete. Read is naturally idempotent.

### Webhooks
- **When to use** — async notifications, event-driven integrations
- **Design** — event types, payload structure, signature verification
- **Retry logic** — failed webhook delivery, backoff
- **Security** — signature verification, HTTPS, secret management

---

## API Design Principles

1. **Consistent.** Same patterns throughout. Same error format, same pagination, same auth approach.
2. **Predictable.** Developers should be able to guess how it works.
3. **Correct.** Right status codes, right HTTP methods, right semantics.
4. **Documented.** If it's not documented, it doesn't exist for the client.
5. **Versioned appropriately.** Breaking changes get a new version. Non-breaking changes can be in-place.
6. **Secure.** Auth checked, input validated, rate limited where needed.
7. **Practical.** Design for real clients, not hypothetical perfection.

---

## What to Produce

When designing an API:

1. **Endpoint list** — each endpoint, method, path, purpose
2. **Request shapes** — path params, query params, body, headers
3. **Response shapes** — success response, error response
4. **Status codes** — for each endpoint, each situation
5. **Authentication requirements** — which endpoints need auth, what level
6. **Authorization model** — per-resource, role-based, etc.
7. **Pagination/filtering/sorting** — for list endpoints
8. **Versioning approach** — how version is indicated
9. **Rate limiting** — where applied, how
10. **Documentation** — OpenAPI spec or equivalent

---

## REST URL Guidelines

### Good
```
GET    /api/v1/users
GET    /api/v1/users/123
POST   /api/v1/users
PUT    /api/v1/users/123
PATCH  /api/v1/users/123
DELETE /api/v1/users/123
GET    /api/v1/users/123/tasks
POST   /api/v1/users/123/tasks
```

### Bad
```
GET    /api/v1/getUsers
POST   /api/v1/createUser
DELETE /api/v1/deleteUser/123
POST   /api/v1/user/123/update
```

### Nested Resources
- Use when child resource belongs to parent and is naturally accessed through parent
- Don't over-nest (2-3 levels max)
- Flat alternatives sometimes clearer (`/tasks?userId=123`)

---

## Status Code Reference

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Successful GET, PUT, PATCH, DELETE (with body) |
| 201 | Created | Successful POST creating resource |
| 204 | No Content | Successful DELETE, or update with no response body |
| 301 | Moved Permanently | URL changed permanently |
| 304 | Not Modified | Conditional request, resource unchanged |
| 400 | Bad Request | Malformed request, validation failure |
| 401 | Unauthorized | Not authenticated, or auth failed |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource conflict (duplicate, state conflict) |
| 422 | Unprocessable Entity | Validation failed (semantic errors) |
| 429 | Too Many Requests | Rate limited |
| 500 | Internal Server Error | Unexpected server error |
| 502 | Bad Gateway | Upstream service error |
| 503 | Service Unavailable | Temporarily unavailable (maintenance, overload) |

---

## Error Response Format

Consistent across all endpoints:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable message",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

Or simpler when no details needed:

```json
{
  "error": "Resource not found"
}
```

---

## Integration with FullStack Builder

This skill is loaded during **Stage 4 (Plan — API Design)** of the fullstack-builder workflow.

It produces the API contracts that inform:
- Backend implementation (Stage 6 — must follow contracts)
- Frontend implementation (Stage 5 — must match contracts)
- Testing (Stage 8 — tests against contracts)

**The API contract is the agreement between frontend and backend.** Changing it requires coordination.

---

## Red Flags

- Verbs in URLs (`/getUsers`, `/createUser`)
- Wrong HTTP methods (POST for read, GET for create)
- Wrong status codes (200 for error, 404 for auth failure)
- Inconsistent error formats across endpoints
- No pagination on list endpoints
- No input validation
- No authentication on protected endpoints
- Breaking changes without versioning
- No documentation
- Over-nested URLs (5+ levels)
- Exposing internal implementation details in API
- No rate limiting on public/expensive endpoints
- Inconsistent naming (camelCase in some places, snake_case in others)
