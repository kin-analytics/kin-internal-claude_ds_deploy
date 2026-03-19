# Rules: Security & Data Privacy

These rules apply to all code and configuration in this project.
When in doubt, flag it — over-alerting is preferred over missing a real issue.

---

## Rule 1: No Hardcoded Secrets

**Never** embed the following directly in source code, notebooks, SQL files, or config files:

- Passwords and authentication tokens
- API keys and OAuth credentials
- Database connection strings with credentials
- Cloud provider keys (AWS `AKIA...`, GCP service account JSON, Azure SAS tokens / connection strings)
- Private keys or certificates
- Internal endpoint URLs that carry embedded tokens

**Correct pattern:**
```python
import os
db_password = os.environ["DB_PASSWORD"]          # from environment
api_key = get_secret("my-service/api-key")       # from secrets manager (e.g. AWS Secrets Manager)
```

**Wrong:**
```python
db_password = "s3cr3tP@ssword"                  # hardcoded — never do this
api_key = "sk-abc123..."                         # hardcoded — never do this
```

Secrets in comments (`# use this key: ...`) are also banned — they still end up in git history.

---

## Rule 2: Protect PII and Sensitive Data

Personal data (names, emails, national IDs, account numbers, dates of birth, financial records,
health data, or any field classified as sensitive for this project) must never appear in:

- Log statements (`print`, `logging`, `logger.info/debug/error`)
- Exception messages or stack traces written to files
- API responses beyond the minimum necessary fields
- Test fixtures or sample datasets committed to the repo
- Notebook output cells committed to version control

**Correct pattern for logging:**
```python
# Log the identifier, not the sensitive value
logger.info("Processing record id=%s", record_id)

# Wrong
logger.info("Processing record for %s, SSN=%s", full_name, ssn)
```

When building test data, use synthetic generation libraries (e.g. `faker`) or fully anonymized exports.
Never copy real client data into test fixtures.

---

## Rule 3: Version Control Hygiene

The following must always be in `.gitignore`:

```
# Secrets & credentials
.env
.env.*
*credentials*
*secrets*
*service_account*.json
*.pem
*.key

# Client & sensitive data
data/raw/
data/client/
data/external/
*.csv
*.parquet
*.xlsx

# Cloud provider artifacts
.aws/
.gcp/
```

Before every commit, verify:
- [ ] No secrets in staged files (`git diff --cached`)
- [ ] No PII in notebook output cells
- [ ] No client data files accidentally staged

---

## Rule 4: Input Validation

Validate all data at system entry points — do not trust external inputs.

- **SQL**: Always use parameterized queries or ORM. Never string-format user input into SQL.
- **File paths**: Sanitize paths from user input to prevent directory traversal attacks.
- **API inputs**: Validate types, ranges, and required fields before processing.
- **DataFrames from external sources**: Check schema, nulls, and expected value ranges
  before applying transformations.

```python
# Validate expected schema on load
EXPECTED_COLUMNS = {"loan_id", "amount", "application_date"}
missing = EXPECTED_COLUMNS - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {missing}")
```

---

## Rule 5: Dependency Management

- Pin exact dependency versions in `requirements.txt` or `pyproject.toml`.
- Do not install packages directly from GitHub URLs without a pinned commit hash.
- Review new dependencies for maintenance status, known CVEs, and community adoption before adding.
- Run `pip audit` (or equivalent) periodically to surface known vulnerabilities.

---

## Rule 6: Cloud & Infrastructure

- IAM roles and service accounts follow least-privilege — only the permissions needed, nothing more.
- No sensitive data in publicly accessible buckets, containers, or object stores.
- Storage buckets / containers holding confidential or restricted data must have:
  - Access logging enabled
  - Versioning enabled (for audit trail)
  - Encryption at rest
- Rotate credentials and access keys on a regular schedule aligned with compliance requirements.
- Terraform / IaC files must not contain embedded secrets — use variable injection at apply time.

---

## Rule 7: Compliance

Projects handling regulated data (SOC 2, GDPR, CCPA, PCI-DSS, HIPAA, or similar) must:

- Minimize data collection to only what is strictly necessary for the task
- Document the legal basis for processing personal data
- Implement data retention limits and deletion procedures
- Log access to sensitive data for audit trail purposes
- Notify the team lead and security contact immediately if a breach is suspected

When a code change could affect compliance (e.g., adding a new log field, changing data retention),
flag it explicitly in the PR description and loop in the project lead.

---

## Pre-Commit / Pre-Deploy Checklist

Run through this checklist before every commit to shared branches and before every deployment.

### Secrets & Credentials
- [ ] No hardcoded passwords, API keys, tokens, or connection strings in staged files (`git diff --cached`)
- [ ] `.env` and credential files are in `.gitignore` and not staged
- [ ] Cloud provider key files (`*service_account*.json`, `*.pem`, `*.key`) are git-ignored

### Data & PII
- [ ] Notebook output cells are stripped or audited — no PII, no raw client data
- [ ] No client data files staged (`*.csv`, `*.parquet`, `*.xlsx`, `data/raw/`, `data/client/`)
- [ ] Log statements do not contain PII (names, emails, national IDs, account numbers)
- [ ] Test fixtures use synthetic data — no production records

### Code Quality
- [ ] All external inputs (API, file, DB) are validated before processing
- [ ] SQL queries use parameterized statements — no string interpolation with user data
- [ ] Specific exceptions caught — no bare `except:` or `except Exception:`
- [ ] Correlation ID present in all log entries for execution traces

### Dependencies & Infrastructure
- [ ] `pip audit` run — no critical or high CVEs in dependencies
- [ ] New dependencies are pinned to an exact version in `requirements.txt` / `pyproject.toml`
- [ ] IAM roles / service accounts follow least privilege for the environment being deployed to
- [ ] Storage buckets with client data have access logging and encryption at rest enabled

### Compliance (for regulated projects)
- [ ] No new PII fields added to logs or API responses without review
- [ ] Data retention limits respected — no accumulation of expired records
- [ ] Any change affecting compliance scope flagged in the PR description

---

## Incident Response

If a secret or PII is discovered in the repository:

1. **Immediately** rotate the exposed credential — do not wait.
2. Remove the secret from git history using `git filter-branch` or `git filter-repo`.
3. Force-push the cleaned history (coordinate with the team to avoid conflicts).
4. Notify the team lead and security contact as soon as possible.
5. Document the incident: what was exposed, for how long, and remediation steps taken.

---

## Severity Reference

| Level | Example | Response |
|---|---|---|
| CRITICAL | Secret committed and pushed to remote | Rotate immediately, purge history, notify |
| HIGH | PII in log file on shared server | Remove log, audit access, patch code |
| MEDIUM | Missing input validation on internal API | Fix in current sprint |
| LOW | Unpinned dependency version | Log as tech debt, fix at next opportunity |