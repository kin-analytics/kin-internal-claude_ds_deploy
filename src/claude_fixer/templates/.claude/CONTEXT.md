# CONTEXT.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About Kin Analytics

Data analytics consultancy delivering predictive models, ML pipelines, ETL processes,
APIs, and dashboards. Clients span Equipment Finance / Lending, Consumer Goods & Retail,
and other verticals. SOC certified and GDPR compliant — data privacy is non-negotiable.

Primary languages: Python, R, SQL. Cloud: AWS, GCP, and Azure depending on the project.

## Toolkit Structure

```
.claude/
├── CONTEXT.md                           ← this file
├── kin-coding-agent-instructions.md     ← hard requirements for code generation (always active)
├── agents/
│   ├── code-reviewer.md                 ← code review checklist and feedback format
│   ├── debugger.md                      ← root-cause debugging protocol and common patterns
│   ├── doc-writer.md                    ← docstring, notebook, and README standards
│   └── security-checker.md             ← pre-commit scan: secrets, PII, and compliance
└── rules/
    ├── python.md                        ← Python style, naming, DataFrames, SQL, error handling
    └── security.md                      ← 7 security rules + incident response
```

All agent and rule files contain general rules ready to use as-is.
For project-specific details (compliance scope, PII fields, data sources), document them
in the project's own `CLAUDE.md` at the root of the client repo.

> **Important:** existing files in `agents/` and `rules/` must not be deleted.
> If a project needs additional conventions, add new files — never change the ones already here.

## Core Conventions

### Code Quality
- Clarity over cleverness — the team has mixed levels; readable beats smart
- Functions do one thing and have a docstring
- Descriptive variable names — `loan_applications`, not `df2` or `temp`
- SQL uses CTEs, not nested subqueries
- Never assume data is clean — validate inputs explicitly

### Documentation
- **All documentation must be written in English** — docstrings, READMEs, notebook Markdown cells, inline comments, and any other written content in the codebase
- Docstring format: **Google style** (see `agents/doc-writer.md`)
- Notebooks follow: context → setup → exploration → analysis → conclusion
- Strip notebook output before committing, or audit it for PII first

### Naming Conventions
- Python: `snake_case` for functions and variables, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants — follow `rules/python.md`
- Other languages (JS, TS, etc.): `camelCase` for methods/functions, `PascalCase` for classes — follow `kin-coding-agent-instructions.md`
- When in doubt, match the language's standard convention; `rules/python.md` takes precedence for Python code

### Observability (always enforced)
- Every execution (API request, background job, script) must generate a **Correlation ID** at the entry point and propagate it through all layers: controllers, services, DB calls, external clients, queue messages, and logs
- Use structured JSON logs with the format: `[Timestamp] | [Level] | [CorrelationID] | [Service/Module] | [Message]`
- Log levels: `INFO` for milestones, `WARN` for non-blocking issues, `ERROR` for exceptions (include stack trace + Correlation ID), `SUCCESS`/`FAILED` for business outcomes
- Implement log rotation; delete logs older than the configured threshold

### Exception Handling (always enforced)
- Wrap all business logic in try/catch/finally: try → business logic, catch → log stack trace + line + Correlation ID, finally → release DB connections and file streams
- Catch specific exceptions — never bare `except:` or `except Exception:`
- External calls (APIs, DBs) must always be wrapped

### Testing (always enforced)
- Unit tests and integration tests are required; E2E tests are recommended
- Follow the AAA pattern: Arrange, Act, Assert
- No production PII in tests — use fixtures or synthetic data (`faker`)
- Tests must not leave side effects; use teardown/cleanup

### Security (always enforced, regardless of project)
- No hardcoded secrets, API keys, or credentials — ever
- No PII in logs, error messages, or committed notebook output
- Client data files must always be in `.gitignore`
- Validate types, length, and format at every application entry point
- Run with least privilege — read-only DB users for reporting services
- See `rules/security.md` for the full ruleset

## Agents — When to Use Each

| Agent | Invoke when... |
|---|---|
| `agents/code-reviewer.md` | Reviewing a PR, auditing a module, inspecting a function |
| `agents/debugger.md` | Fixing an error, tracing a bug, investigating unexpected output |
| `agents/doc-writer.md` | Writing docstrings, documenting a notebook, generating a README |
| `agents/security-checker.md` | Pre-commit scan, auditing a file for secrets or PII exposure |
| `kin-coding-agent-instructions.md` | Always active — hard requirements applied to every code generation task |

## Common Commands

These are the reference commands for the typical DS stack. Adapt paths and tool choices per project.

### Testing
```bash
pytest tests/ -v                          # run all tests
pytest tests/ -v --cov=src --cov-report=term-missing  # with coverage
pytest tests/unit/ -v                     # unit tests only
pytest tests/integration/ -v             # integration tests only
```

### Code Quality
```bash
ruff check src/                           # lint
ruff format src/                          # format
ruff check src/ --fix                     # auto-fix lint issues
mypy src/                                 # type checking (if configured)
```

### Dependency Management
```bash
pip audit                                 # scan for known CVEs
pip install -r requirements.txt
pip freeze > requirements.txt             # pin current environment
```

---

## What to Avoid

- Overly complex solutions — minimum complexity for the current task
- Ignoring nulls, outliers, or type mismatches in data
- Suggesting new tools or frameworks without flagging them explicitly
- Hardcoded file paths, credentials, or environment-specific values
- Committing client data or PII in any form


## Important Coding Agent Instructions

- Before generating code, always follow the guidelines described in kin-coding-agent-instructions.md file.