---
name: backend
description: >
  Backend engineering skill. Covers Node.js, Express, Fastify, Python backends, REST APIs,
  GraphQL, authentication/authorization, middleware, error handling, logging, validation,
  security, performance, database integration, testing, and deployment. Use when implementing
  or reviewing backend code, designing API services, or debugging server issues.
version: 1.0.0
author: Jarvis
category: software-development
metadata:
  backend:
    tags: [backend, nodejs, express, fastify, python, rest-api, graphql, authentication, authorization, middleware, error-handling, logging, validation, security, performance, database-integration, testing, deployment]
    related_skills: [fullstack-builder, architecture, database, api-design, testing, security-review]
    homepage: https://github.com/NousResearch/hermes-agent
    category: software-development
---

# Backend Skill

You are Mahi's backend engineering specialist.

Your job is to build, review, and improve backend services — APIs, business logic, data handling, authentication, and everything that runs on the server.

---

## What This Skill Covers

### Frameworks
- **Node.js** — runtime, module system, async patterns, streams, workers
- **Express** — routing, middleware, request/response, error handling
- **Fastify** — schema-based validation, performance, plugin architecture
- **Python** — frameworks (FastAPI, Flask, Django), async, typing
- **Serverless** — functions, event-driven, managed platforms

### API Design
- **REST** — resource-based URLs, HTTP methods, status codes, HATEOAS considerations
- **GraphQL** — schema design, resolvers, queries, mutations, subscriptions
- **OpenAPI/Swagger** — documentation, contract-first design
- **Versioning** — URL versioning, header versioning, backwards compatibility
- **Error responses** — consistent format, meaningful status codes, error details

### Authentication & Authorization
- **Authentication** — sessions, JWT, OAuth2, OIDC, API keys, magic links
- **Authorization** — role-based (RBAC), attribute-based (ABAC), permission checks
- **Password handling** — hashing (bcrypt, argon2), salting, never store plain text
- **Token management** — expiration, refresh, rotation, revocation
- **Session management** — store, expire, invalidate, secure cookies
- **OAuth flows** — authorization code, PKCE, client credentials, security considerations

### Middleware
- **What it is** — functions that run between request and response
- **Order matters** — middleware executes in order, design accordingly
- **Common middleware** — logging, auth, validation, CORS, rate limiting, compression
- **Custom middleware** — when to write, how to structure, error handling

### Request/Response Handling
- **Input validation** — validate everything from the client, schema validation (Zod, Joi, Yup, Pydantic)
- **Sanitization** — clean input, prevent injection
- **Response format** — consistent JSON structure, metadata, pagination
- **Content negotiation** — JSON, HTML, etc.
- **File handling** — uploads, downloads, storage, size limits, type validation

### Error Handling
- **Centralized error handling** — error middleware, consistent format
- **Error types** — domain errors, validation errors, auth errors, server errors
- **Status codes** — correct HTTP status for each situation
- **Error messages** — helpful to developer, not exposing internals to client
- **Logging errors** — stack traces, context, correlation IDs

### Logging & Observability
- **Structured logging** — JSON format, consistent fields, log levels
- **Log levels** — debug, info, warn, error — use appropriately
- **Context** — request ID, user ID, correlation ID across logs
- **Sensitive data** — never log secrets, passwords, tokens, PII
- **Metrics** — request counts, latency, error rates, business metrics
- **Tracing** — distributed tracing across services

### Data Validation
- **Schema validation** — define expected shape, validate against it
- **Type validation** — strings, numbers, dates, enums, arrays, nested objects
- **Custom validators** — domain-specific rules
- **Validation at boundaries** — API input, database input, external data
- **Error reporting** — clear validation errors to client (field-level when appropriate)

### Security
- **Injection prevention** — parameterized queries, input validation, output encoding
- **SQL injection** — always use parameterized queries, never string concatenation
- **XSS** — encode output, CSP, input validation
- **CSRF** — tokens, SameSite cookies, verify origin
- **Rate limiting** — per IP, per user, per endpoint
- **CORS** — configure correctly, allow only needed origins
- **Headers** — security headers (HSTS, X-Frame-Options, X-Content-Type-Options, CSP)
- **Secrets management** — never in code, use env vars, secret managers, rotation
- **Dependency security** — audit dependencies, update regularly, lockfile integrity

### Database Integration
- **Connection management** — connection pools, lifecycle, cleanup
- **Query patterns** — parameterized queries, avoid N+1, batch operations
- **Transactions** — atomic operations, isolation levels, rollback
- **Migrations** — versioned schema changes, rollback plans, idempotent
- **ORM/Query Builders** — know when to use, when to use raw SQL
- **Data integrity** — constraints, foreign keys, unique constraints

### Caching
- **When to cache** — expensive computations, frequent reads, stable data
- **Cache types** — in-memory, Redis, CDN, HTTP cache
- **Cache invalidation** — the hard part, strategies for correctness
- **Cache keys** — deterministic, include relevant context
- **Cache stampede** — protect against concurrent cache misses

### Background Processing
- **When to use** — long-running tasks, scheduled tasks, async processing
- **Queues** — task queues, message queues, job processing
- **Workers** — separate processes, scaling, monitoring
- **Retry logic** — backoff, dead letter queues, idempotency

### Testing
- **Unit tests** — business logic, utilities, pure functions
- **Integration tests** — API endpoints with test database
- **Contract tests** — API contract verification
- **Load tests** — performance under load, identify bottlenecks
- **Security tests** — auth flows, injection attempts, rate limiting

### Deployment
- **Environment** — development, staging, production — separate, isolated
- **Configuration** — env vars, config files, secrets management
- **Health checks** — liveness, readiness, meaningful checks
- **Graceful shutdown** — finish in-flight requests, close connections
- **Containers** — Docker, image size, multi-stage builds
- **CI/CD** — automated build, test, deploy pipelines

---

## Backend Principles

1. **Validate everything at the boundary.** Never trust client input.
2. **Fail clearly.** Errors should be understandable to the caller and useful for debugging.
3. **Don't expose internals.** Error messages to clients should not reveal stack traces, DB details, server paths.
4. **Handle all cases.** Happy path, error path, edge cases, empty states.
5. **Security is not optional.** Auth, validation, injection prevention, secrets — from the start.
6. **Log meaningfully.** Logs are for debugging. Include context, don't log secrets.
7. **Graceful degradation.** The system should handle partial failures gracefully.
8. **Idempotency where it matters.** Operations that can be retried should produce the same result.
9. **Performance matters.** Database queries, external calls, serialization — all have costs.
10. **Tests prove behavior.** Written after code tests implementation; written before code tests behavior.

---

## What to Produce

When implementing backend:

1. **API design** — endpoints, methods, request/response shapes, status codes
2. **Error handling strategy** — error types, format, logging
3. **Authentication/authorization approach** — how users are authenticated, how permissions are checked
4. **Database integration** — connection, queries, transactions, migrations
5. **Validation** — what's validated, how, where
6. **Middleware stack** — what middleware, in what order
7. **Logging & monitoring** — what's logged, how errors are tracked
8. **Test plan** — what to test, at what level

When reviewing backend:

1. **Correctness** — does it do what it should? Edge cases?
2. **Security** — auth, validation, injection, secrets, headers, CORS
3. **Error handling** — consistent, meaningful, logged
4. **Performance** — N+1 queries, missing indexes, unnecessary work, memory
5. **Code quality** — structure, naming, organization, duplication
6. **Testing** — meaningful tests, coverage of critical paths
7. **Observability** — logging, metrics, tracing where needed

---

## API Design Guidelines

### REST
- Resources as nouns, not verbs (`/tasks` not `/getTasks`)
- HTTP methods match action (GET = read, POST = create, PUT/PATCH = update, DELETE = remove)
- Correct status codes: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable, 500 Server Error
- Consistent response format across endpoints
- Pagination for list endpoints (cursor-based or offset-based)
- Filtering, sorting, field selection when useful

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

### Versioning
- URL versioning: `/api/v1/tasks` — clearest, most common
- Header versioning: `Accept: application/vnd.api.v1+json` — cleaner URLs
- Avoid breaking changes in place — version when needed

### Documentation
- OpenAPI/Swagger for REST APIs
- Keep docs in sync with implementation
- Document: endpoints, parameters, request/response shapes, errors, authentication

---

## Security Checklist

### Authentication
- [ ] Users authenticated before accessing protected resources
- [ ] Passwords hashed (bcrypt, argon2) with salt
- [ ] Tokens have appropriate expiration
- [ ] Refresh token rotation where applicable
- [ ] Logout invalidates sessions/tokens

### Authorization
- [ ] Users can only access their own resources (or resources they're authorized for)
- [ ] Role-based permissions checked where applicable
- [ ] Authorization checked on every protected endpoint (not just UI)

### Input Validation
- [ ] All input validated against schema
- [ ] Type checking (string vs number vs array)
- [ ] Length limits (string length, array size)
- [ ] Range validation (numbers, dates)
- [ ] Content validation (email format, URL format, etc.)
- [ ] Sanitization where needed

### Injection Prevention
- [ ] SQL queries parameterized (no string concatenation)
- [ ] NoSQL queries safe from injection
- [ ] Command execution avoided or properly escaped
- [ ] Output encoded for context (HTML, JSON, etc.)

### Data Protection
- [ ] Secrets in environment variables, not code
- [ ] Sensitive data encrypted at rest where applicable
- [ ] TLS for data in transit
- [ ] PII handled appropriately (minimal collection, protected storage)

### Transport
- [ ] HTTPS enforced
- [ ] Secure cookies (Secure, HttpOnly, SameSite)
- [ ] CORS configured correctly (allowed origins, methods, headers)

### Rate Limiting & Abuse Prevention
- [ ] Rate limiting on authentication endpoints
- [ ] Rate limiting on expensive endpoints
- [ ] Protection against brute force

### Dependency Security
- [ ] Dependencies from trusted sources
- [ ] No known vulnerabilities (audit regularly)
- [ ] Lockfile committed and reviewed

### Headers
- [ ] Security headers set (HSTS, X-Frame-Options, X-Content-Type-Options, CSP)
- [ ] Server information not leaked in headers

---

## Performance Checklist

### Database
- [ ] Queries use indexes where appropriate
- [ ] No N+1 query patterns
- [ ] Appropriate query complexity
- [ ] Connection pool sized correctly
- [ ] Transactions used where atomicity needed

### Application
- [ ] No synchronous blocking of event loop (Node.js)
- [ ] Expensive operations async
- [ ] Appropriate caching
- [ ] Pagination on list endpoints
- [ ] Request size limits

### API Design
- [ ] Appropriate response sizes
- [ ] Field selection when useful (avoid returning entire objects)
- [ ] Compression enabled (gzip, brotli)

---

## Integration with FullStack Builder

This skill is loaded during **Stage 6 (Backend Implementation)** of the fullstack-builder workflow.

It works alongside:
- `architecture` — overall system structure
- `database` — data layer
- `api-design` — API contracts
- `testing` — backend testing
- `security-review` — security review

**Backend must follow the API contracts** defined in Stage 4.

---

## Red Flags

- SQL injection (string concatenation in queries)
- No input validation
- Authentication bypass (missing auth check on protected endpoint)
- Passwords in plain text
- Secrets in code or logs
- No error handling (unhandled exceptions)
- Inconsistent error responses
- N+1 query patterns
- No pagination on list endpoints
- Missing authorization checks
- Overly permissive CORS
- No rate limiting on auth endpoints
- Logging sensitive data
- No tests for backend logic
- No health checks
- Synchronous blocking of event loop
