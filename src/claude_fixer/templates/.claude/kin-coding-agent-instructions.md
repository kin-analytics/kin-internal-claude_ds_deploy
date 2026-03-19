# Kin Analytics — Coding Agent Instructions (v1.0)

Use this file as **hard requirements** when generating or modifying code for Kin Analytics projects.

## 0) Non‑negotiables
- Prefer **readability over brevity**.
- Follow **standard industry conventions** (no Hungarian notation/prefixes).
- No secrets in code or logs.
- All executions must be traceable via **Correlation ID**.

---

## 1) Repository structure
Use (and don’t fight) this baseline layout:

- `/src` — application source code  
- `.env, .env.staging, .env.production, .env.development` — environment-specific configuration (**must not contain secrets**)  
- `/tests` — unit + integration tests  
- `/docs` — technical docs and API references  
- `/logs` — local execution logs (**must be git-ignored**)

---

## 2) Execution context: Correlation ID
### Rule
**Every execution** (API request, background job, script) must generate a **unique Correlation ID** and pass it through **all layers**.

### Requirements
- Generate a Correlation ID at the entry point if one is not provided.
- Propagate it through:
  - controllers/handlers
  - services/use-cases
  - repositories/DB calls
  - external API clients
  - queue/event messages (as metadata/headers)
  - logs and error handling
- Include Correlation ID in every log entry and in error logs.

---

## 3) Clean code & naming conventions
### Naming standards
- **Classes:** `PascalCase` (e.g., `CustomerRepository`)
- **Methods/Functions:** `camelCase` and must be **verbs/actions** (e.g., `calculateTotalRevenue`)
- **Variables:** `camelCase` and descriptive  
  - Bad: `d`, `flag`, `list`  
  - Good: `daysSinceLogin`, `isValidUser`, `pendingOrders`
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_RETRY_ATTEMPTS`)

### Core principles
1. **SRP (Single Responsibility):** One reason to change. Split monoliths into smaller, testable units.  
2. **DRY (Don’t Repeat Yourself):** If logic appears twice, refactor into a shared utility/service.  
3. **Self‑Documenting Code:** Comments explain **why**, not **what**. Structure and naming must make the code readable.

---

## 4) Secure by design
### Input validation
- Never trust input.
- Validate **types, length, format** at the application entry point.

### Secrets management
- **Never** hardcode or print credentials, passwords, connection strings, or API keys.
- Use **environment variables (.env)** or a **Secret Manager** vault.

### Least privilege
- Run with minimal permissions required (e.g., read-only DB user for reporting services).

---

## 5) Exception handling & logging
### Try/Catch/Finally pattern
All business logic must be wrapped in exception handling:

- **Try:** business logic  
- **Catch:** handle exceptions and **log**:
  - stack trace
  - line number (where feasible)
  - correlation ID
- **Finally:** always release resources (DB connections, file streams, etc.)

### Logging standards
Prefer **structured logs (JSON)**.

#### Levels
- `INFO`: milestones (e.g., “Request received”, “Calculation started”)
- `WARN`: non-blocking issues (e.g., “API response slow”, “Deprecated method used”)
- `ERROR`: exceptions caught; include stack trace + line number
- `SUCCESS`: major transaction completed successfully
- `FAILED`: business failure (e.g., “Payment declined”) distinct from system crash

#### Required log fields
`[Timestamp] | [Level] | [CorrelationID] | [Service/Module] | [Message]`

#### Retention
Implement log rotation (e.g., `nLogRetention` logic) so logs older than the configured threshold are deleted.

---

## 6) Testing strategy
### Testing pyramid
1. **Unit tests (Required)**
   - Test functions/classes in isolation.
   - Mock external dependencies (DB, APIs).
   - Cover happy path + edge cases (null, empty lists, etc.).
2. **Integration tests (Required)**
   - Verify module interaction (e.g., controller ↔ DB).
   - Verify configuration/env variables are loaded correctly.
3. **E2E tests (Recommended)**
   - Simulate full user flows end-to-end.

### Testing standards
- Use **AAA** pattern: `Arrange`, `Act`, `Assert`
- No production PII in tests; use fixtures/factories
- Tests must not leave side effects; use teardown/cleanup

---

## 7) Quality checklist (must pass before merge)
- **Modularity:** large functions split into single responsibilities (SRP)
- **Scalability:** avoid obvious inefficiencies (e.g., N+1 queries)
- **Reusability:** duplicated logic extracted (DRY)
- **Security:** no credentials/keys in repo; inputs validated against injection
- **Readability:** naming is unambiguous; code is self-documenting
- **Cleanup:** connections/streams released in `finally`
- **Reliability:** external calls wrapped with try/catch
- **Testing:** unit tests include edge cases; integration tests cover config loading
- **Observability:** correlation ID present in all logs
- **Config:** URLs/timeouts read from env/config, not hardcoded

---

## 8) Critical failure protocol
For services: implement **graceful shutdown**:
- Handle termination signals (e.g., `SIGTERM`)
- Finish in-flight requests when possible
- Close DB pools safely before exiting

---

## 9) Agent output expectations
When generating code:
- Keep functions small and composable.
- Prefer pure functions for business rules when possible.
- Ensure correlation ID propagation is explicit (context/headers/metadata).
- Add/modify tests that validate happy path + edge cases.
- Never introduce secrets; use env variables and safe logging.

If a requirement conflicts with an existing codebase constraint, document the **why** and provide the safest compliant alternative.
