# Rules: Python

These rules apply to all Python code in this project.

---

## Style & Formatting

- Follow PEP 8. If a formatter (black or ruff format) is configured, let it enforce style — do not fight it.
- Max line length: 88 (black default). Adjust only if the project explicitly overrides it.
- Use double quotes for strings (consistent with black default).
- Imports: standard library → third-party → internal, each group separated by a blank line.
  ```python
  import os
  import sys

  import pandas as pd
  import numpy as np

  from myproject.utils import helper_function
  ```

---

## Naming Conventions

| Entity | Convention | Example |
|---|---|---|
| Functions & variables | `snake_case` | `calculate_risk_score` |
| Classes | `PascalCase` | `LoanPredictor` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_LOAN_AMOUNT` |
| Private helpers | `_leading_underscore` | `_normalize_features` |
| DataFrame columns | `snake_case` strings | `"application_date"` |

**Banned names:** `df2`, `temp`, `x`, `data2`, `result_final`, `new_df`.
Use descriptive names that reflect the domain: `loan_applications`, `credit_features`, `monthly_revenue`.

---

## Functions

- One function, one responsibility. If it does two things, split it.
- Every public function must have a docstring in Google style (see `doc-writer.md`).
- Use type hints for all function signatures:
  ```python
  def calculate_score(features: pd.DataFrame, threshold: float = 0.5) -> pd.Series:
  ```
- Default arguments must be immutable. Never `def f(x, data=[])` — use `None` and initialize inside.
- Functions longer than ~40 lines are a signal to refactor.

---

## Data & DataFrames

- Never iterate row-by-row with `.iterrows()` when a vectorized operation applies.
  Use `.apply()` only when truly necessary; prefer `.map()`, boolean masks, or numpy operations.
- Always validate inputs at function boundaries:
  ```python
  if df.empty:
      raise ValueError("Input DataFrame is empty — check upstream data source.")
  ```
- Check for nulls explicitly before operations that would silently propagate them:
  ```python
  assert df["key_column"].notna().all(), "Unexpected nulls in key_column"
  ```
- Column names must be consistent with the source schema. Document any renames.
- Use `.copy()` when modifying a slice to avoid `SettingWithCopyWarning`.

---

## SQL (via Python)

- Use parameterized queries — never string interpolation with user-supplied values:
  ```python
  # Correct
  cursor.execute("SELECT * FROM loans WHERE id = %s", (loan_id,))

  # Wrong — SQL injection risk
  cursor.execute(f"SELECT * FROM loans WHERE id = {loan_id}")
  ```
- For complex queries, write SQL in `.sql` files and load them; don't embed multi-line SQL in Python strings.
- Use CTEs for readability, not nested subqueries.

---

## Error Handling

- Catch specific exceptions, not bare `except:` or `except Exception:`.
- Error messages must be actionable: say what went wrong and where to look.
  ```python
  raise ValueError(f"Expected columns {required_cols} not found in {df.columns.tolist()}")
  ```
- Never suppress exceptions silently with empty `except` blocks.
- Do not log PII in error messages (see `security.md`).

---

## Notebooks

- Notebooks are for exploration and storytelling, not production pipelines.
- Reusable logic extracted from notebooks must be moved to `.py` modules.
- Strip output before committing (or audit output for PII first).
- Follow the narrative structure: context → setup → exploration → analysis → conclusion.
- See `doc-writer.md` for full notebook documentation standards.

---

## What to Avoid

- Overly "clever" one-liners that sacrifice readability.
- Silently ignoring data quality issues — always validate inputs.
- Hardcoded file paths — use config or environment variables.
- Hardcoded credentials — see `security.md`.
- `import *` — always import explicitly.
- Commenting out large blocks of code — delete them; git has history.