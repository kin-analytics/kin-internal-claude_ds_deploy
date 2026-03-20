# claude-ds-tools

A CLI tool that syncs Kin Analytics' standard `.claude` configuration into any Data Science project. Standard files are always kept up to date; files you created yourself are never touched.

---

## Installation

```bash
pip install git+https://github.com/kin-analytics/kin-internal-claude_ds_deploy.git
```

---

## Usage

Run inside the root of any project:

```bash
setup-claude
```

**What it does:**
- If `.claude/` does not exist → creates it with all standard files.
- If `.claude/` already exists → updates all standard files to the latest version and leaves any custom files you created untouched.
- Writes a `.claude/VERSION` file so you can always check what version is installed.

### Updating to the latest standard templates

```bash
pip install --force-reinstall git+https://github.com/kin-analytics/kin-internal-claude_ds_deploy.git
setup-claude
```

---

## What gets synced

```
.claude/
├── CONTEXT.md                        # Project context & Kin Analytics conventions
├── settings.json                     # Claude Code permissions
├── kin-coding-agent-instructions.md  # Hard coding requirements (always active)
├── VERSION                           # Installed version (auto-generated)
├── rules/
│   ├── python.md                     # Python style guide
│   └── security.md                   # Security & data-privacy rules
└── agents/
    ├── code-reviewer.md              # Code review methodology
    ├── debugger.md                   # Root-cause debugging protocol
    ├── doc-writer.md                 # Documentation standards
    └── security-checker.md          # Pre-commit security scan
```

---

## Sync behavior

| Situation | Action |
|-----------|--------|
| File exists in standard template | Always updated to latest version |
| File exists only in your project (custom agent, etc.) | Left untouched |
| New file added to standard template | Copied to your project |

---

## Contributing

Edit files inside `src/claude_fixer/templates/.claude/`, bump the version in `pyproject.toml`, and push. DS users get the updates on their next reinstall + `setup-claude`.