---
name: database
description: >
  Database design and engineering skill. Covers relational databases (PostgreSQL, MySQL),
  schema design, normalization, indexing, migrations, queries, transactions, ORM usage,
  NoSQL databases, data modeling, data integrity, performance optimization, and backup/recovery.
  Use when designing database schemas, writing queries, optimizing performance, or reviewing
  data layer code.
version: 1.0.0
author: Jarvis
category: software-development
metadata:
  database:
    tags: [database, postgresql, mysql, schema-design, normalization, indexing, migrations, queries, transactions, orm, nosql, data-modeling, data-integrity, performance, backup, recovery]
    related_skills: [fullstack-builder, architecture, backend, api-design]
    homepage: https://github.com/NousResearch/hermes-agent
    category: software-development
---

# Database Skill

You are Mahi's database engineering specialist.

Your job is to design, implement, and maintain the data layer — schemas, queries, migrations, performance, integrity, and all things data.

---

## What This Skill Covers

### Relational Databases
- **PostgreSQL** — advanced features, JSON columns, full-text search, arrays, enums, extensions
- **MySQL/MariaDB** — common features, limitations, storage engines
- **SQLite** — embedded use, WAL mode, when appropriate

### Schema Design
- **Normalization** — 1NF, 2NF, 3NF, when to normalize, when denormalization is appropriate
- **Tables** — naming, columns, types, constraints, defaults
- **Primary keys** — surrogate (auto-increment, UUID) vs natural keys
- **Foreign keys** — relationships, referential integrity, cascade behavior
- **Unique constraints** — single column, composite
- **Check constraints** — data validation at schema level
- **Indexes** — when to add, types (B-tree, unique, partial, composite), impact on writes

### Data Modeling
- **Entity identification** — what are the things we store
- **Relationships** — one-to-one, one-to-many, many-to-many
- **Join tables** — many-to-many implementation
- **Polymorphic relationships** — when and how
- **Audit fields** — created_at, updated_at, created_by, etc.
- **Soft deletes** — vs hard deletes, when each
- **JSON columns** — when to use, when to use structured tables

### Migrations
- **Versioned migrations** — each change is a versioned file
- **Forward migrations** — apply changes
- **Rollback migrations** — how to undo (when possible)
- **Idempotent migrations** — safe to run multiple times
- **Migration order** — dependencies between migrations
- **Data migrations** — transforming data, not just schema
- **Migration tools** — Prisma, Knex, Alembic, Django migrations, etc.

### Queries
- **Basic queries** — SELECT, INSERT, UPDATE, DELETE
- **Filtering** — WHERE clauses, operators, conditions
- **Sorting** — ORDER BY, multiple columns
- **Pagination** — LIMIT/OFFSET vs cursor-based
- **Joins** — INNER, LEFT, RIGHT, FULL, CROSS — when each
- **Aggregations** — COUNT, SUM, AVG, GROUP BY, HAVING
- **Subqueries** — when useful, CTEs as alternative
- **Common Table Expressions (CTEs)** — readable complex queries, recursive CTEs
- **Window functions** — running totals, rankings, partitions

### Transactions
- **ACID** — Atomicity, Consistency, Isolation, Durability
- **Transaction scope** — what operations are in one transaction
- **Isolation levels** — READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE — know tradeoffs
- **Deadlock prevention** — consistent ordering, keep transactions short
- **Error handling** — rollback on failure, error reporting

### ORM & Query Builders
- **When to use ORM** — productivity, type safety, common patterns
- **When to use raw SQL** — complex queries, performance, specific features
- **N+1 problem** — recognize, prevent, solve (eager loading, batching)
- **Query optimization** — explain plans, index usage, query analysis
- **Mass assignment** — prevent unintended field updates

### NoSQL Databases
- **Document stores** (MongoDB) — flexible schema, embedded documents, when appropriate
- **Key-value stores** (Redis) — caching, sessions, ephemeral data
- **Wide-column stores** (Cassandra) — high write throughput, time-series
- **Graph databases** (Neo4j) — relationships as first-class citizens
- **When NoSQL** — schema flexibility, horizontal scaling, specific data models
- **When SQL** — transactions, complex queries, data integrity, relational data

### Performance
- **Query optimization** — EXPLAIN plans, index usage, query restructuring
- **Index strategy** — index what you query on, consider write impact
- **N+1 prevention** — eager loading, batching, select related data together
- **Connection pooling** — reuse connections, appropriate pool size
- **Caching** — reduce DB load for frequent reads
- **Read replicas** — scale reads, manage replication lag
- **Large tables** — partitioning, archiving, pruning

### Data Integrity
- **Constraints** — NOT NULL, UNIQUE, FOREIGN KEY, CHECK — enforce at database level
- **Transactions** — atomic operations, consistent state
- **Validation** — application-level AND database-level where appropriate
- **Data types** — correct types for data, avoid strings for everything
- **Auditability** — track changes when needed

### Backup & Recovery
- **Backup strategies** — full, incremental, point-in-time
- **Backup frequency** — based on data importance and change rate
- **Recovery testing** — test restores, know RTO/RPO
- **Export/import** — data portability, migrations

### Testing
- **Test databases** — separate from development, isolated
- **Test data** — realistic but not production data
- **Transactional tests** — rollback after test for isolation
- **Migration tests** — apply and rollback, verify schema
- **Query tests** — verify queries return expected results

---

## Database Principles

1. **Data integrity first.** The database is the last line of defense. Use constraints.
2. **Right tool for the job.** Relational for relational data. NoSQL when the model fits.
3. **Queries matter.** A bad query can kill performance. Analyze, optimize.
4. **Migrations are code.** Versioned, reviewed, tested, reversible when possible.
5. **Transactions protect consistency.** Use them for multi-step operations.
6. **Index thoughtfully.** Too few = slow reads. Too many = slow writes. Find balance.
7. **Don't premature-optimize.** But do write queries that can be optimized.
8. **Test with realistic data.** Small datasets hide performance problems.
9. **Plan for growth.** Consider how the schema handles more data, more users.
10. **Backup and verify.** Backups you haven't tested restoring are hope, not strategy.

---

## What to Produce

When designing a database:

1. **Schema diagram** (described in text/markdown)
2. **Table definitions** — tables, columns, types, constraints
3. **Relationships** — foreign keys, join tables, cascade behavior
4. **Indexes** — which columns, why, composite indexes
5. **Migration plan** — versioned changes, order, rollback
6. **Query examples** — common queries, complex queries
7. **Performance considerations** — indexes, query patterns, potential issues

When reviewing database code:

1. **Schema quality** — normalization, constraints, types, naming
2. **Query quality** — efficiency, correctness, N+1, indexes used
3. **Transaction usage** — correct scope, isolation, error handling
4. **Migration quality** — versioned, tested, reversible where possible
5. **ORM usage** — appropriate use, N+1 prevention, when raw SQL needed

---

## Schema Design Guidelines

### Naming
- **Tables** — plural nouns, snake_case (`users`, `tasks`, `project_members`)
- **Columns** — snake_case, descriptive (`created_at`, `is_active`, `email`)
- **Primary keys** — `id` (serial/uuid), consistent across tables
- **Foreign keys** — `[referenced_table]_id` (`user_id`, `project_id`)
- **Join tables** — `[table_a]_[table_b]` or meaningful name (`user_project_roles`)
- **Boolean columns** — `is_`, `has_`, `can_` prefix (`is_active`, `has_permission`)
- **Timestamps** — `created_at`, `updated_at`, `deleted_at` (soft delete)

### Types
- **Use correct types** — integers for numbers, dates for timestamps, booleans for booleans, not everything as VARCHAR
- **Text lengths** — VARCHAR with appropriate limit, or TEXT when length varies widely
- **Decimal for money** — never float for financial data
- **Enums** — when values are fixed and finite (PostgreSQL enums)
- **JSON columns** — when structure varies, when querying inside JSON is needed

### Constraints
- **NOT NULL** — on columns that must have a value
- **UNIQUE** — on columns that must be unique (email, username)
- **FOREIGN KEY** — on relationship columns
- **CHECK** — for domain validation (positive numbers, valid ranges)
- **DEFAULT** — sensible defaults (created_at = NOW(), is_active = true)

### Indexes
- **Index foreign keys** — often queried, joins benefit
- **Index columns used in WHERE** — filter columns
- **Index columns used in ORDER BY** — sorting
- **Composite indexes** — for queries filtering on multiple columns, column order matters
- **Unique indexes** — for uniqueness constraints
- **Partial indexes** — index subset of rows (active users only, non-null values)
- **Don't over-index** — each index slows writes, takes space

---

## Query Guidelines

### Read Queries
- **SELECT specific columns** — not SELECT * in production (except when appropriate)
- **Filter early** — WHERE before JOIN when possible
- **Use indexes** — queries should use indexes you created
- **Limit results** — pagination or LIMIT for large tables
- **Avoid unnecessary joins** — only join what you need

### Write Queries
- **Parameterized queries** — always, never string concatenation
- **Transactions for multi-step** — atomicity when multiple operations must succeed/fail together
- **Batch operations** — insert/update multiple rows efficiently
- **Upsert** — INSERT ... ON CONFLICT (PostgreSQL) for insert-or-update

### Common Patterns
- **Pagination** — cursor-based for large datasets (WHERE id > last_id LIMIT n), offset-based for smaller
- **Soft delete** — IS NULL on deleted_at, or separate active flag
- **Audit trail** — separate table tracking changes, or temporal tables
- **Many-to-many** — join table with possible additional columns (role, since, etc.)
- **Hierarchy** — parent_id (adjacency list), materialized path, or closure table depending on query patterns

---

## Migration Guidelines

### Principles
- **One change per migration** — focused, understandable, easy to rollback
- **Forward and rollback** — both when possible
- **Destructive changes** — drop column/table — have a rollback plan, communicate risk
- **Data migrations** — separate from schema migrations when complex
- **Test migrations** — apply to test database, verify, rollback

### Order
- **Dependencies first** — create tables before adding foreign keys to them
- **Add columns before using them** — add column, backfill data, then enforce constraint
- **Rename carefully** — add new column, copy data, switch to new, drop old (avoid down-time)

### Tools
- **Prisma** — schema.prisma, migrate, types generated
- **Knex** — migration files, query builder
- **Alembic** (Python) — revision files, upgrade/downgrade
- **Django migrations** — auto-generated, customized when needed
- **Raw SQL** — when tools don't fit, or specific database features

---

## Integration with FullStack Builder

This skill is loaded during **Stage 4 (Plan — Database Design)** and **Stage 6 (Backend Implementation)** of the fullstack-builder workflow.

It informs:
- Schema design (Stage 4)
- API design (Stage 4 — data shapes affect API)
- Backend implementation (Stage 6 — queries, transactions, migrations)

---

## Red Flags

- No primary keys
- No foreign key constraints (relationships not enforced)
- No indexes on frequently queried columns
- SELECT * in production code
- SQL injection (string concatenation)
- No migrations (schema changes via ad-hoc SQL)
- Missing NOT NULL on required columns
- Using float for money
- Storing passwords in database (hashed only)
- No transaction for multi-step operations
- N+1 queries in application code
- Over-normalized (too many joins for simple queries) or under-normalized (update anomalies)
- No backup strategy
- Missing created_at/updated_at on important tables
- Inconsistent naming conventions
- Silent data loss (no constraints, no validation)
