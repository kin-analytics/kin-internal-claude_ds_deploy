# claude-ds-tools

A CLI tool that safely syncs Kin Analytics' standard `.claude` configuration into any Data Science project — without overwriting custom files.

---

## Installation

```bash
pip install git+https://github.com/your-org/kin-internal-claude_ds_deploy.git
```

---

## Usage

Run inside the root of any project:

```bash
setup-claude
```

**What it does:**
- If `.claude/` does not exist → creates it with all standard files.
- If `.claude/` already exists → adds only the files and subdirectory entries that are missing. Your custom agents, rules, or prompts are never touched.

### Updating to the latest standard templates

```bash
pip install --upgrade git+https://github.com/your-org/kin-internal-claude_ds_deploy.git
setup-claude
```

---

## What gets synced

```
.claude/
├── CONTEXT.md                        # Project context & Kin Analytics conventions
├── settings.json                     # Claude Code permissions (read-only git, no destructive ops)
├── kin-coding-agent-instructions.md  # Hard coding requirements (always active)
├── rules/
│   ├── python.md                     # Python style guide
│   └── security.md                  # Security & data-privacy rules
└── agents/
    ├── code-reviewer.md              # Code review methodology
    ├── debugger.md                   # Root-cause debugging protocol
    ├── doc-writer.md                 # Documentation standards
    └── security-checker.md          # Pre-commit security scan
```

---

## Safe-merge behavior

The sync is **additive only**:

| Situation | Action |
|-----------|--------|
| File exists in standard template, missing from project | Copied |
| File exists in both standard template and project | Skipped (yours is kept) |
| File exists only in project (your custom agent, etc.) | Left untouched |
| New file added inside an existing standard subdirectory | Copied (recursive merge) |

---

## Project structure

```
kin-internal-claude_ds_deploy/
├── pyproject.toml
├── README.md
├── GOAL.md
└── src/
    └── claude_fixer/
        ├── cli.py               # Entry point logic
        └── templates/
            └── .claude/         # Master template files
```

---

## Contributing

Edit files inside `src/claude_fixer/templates/.claude/` to update the standard templates. Bump the version in `pyproject.toml`, push, and DS users will get the new files on their next `pip install --upgrade` + `setup-claude`.