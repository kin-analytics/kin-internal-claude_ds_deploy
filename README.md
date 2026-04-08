# claude-ds-tools

A CLI tool that syncs Kin Analytics' standard `.claude` configuration into any Data Science project. Standard files are always kept up to date; files you created yourself are never touched.

---

## First-time setup

Install the package and run the command inside the root of your project:

```bash
pip install git+https://github.com/kin-analytics/kin-internal-claude_ds_deploy.git
setup-claude
```

This creates the `.claude/` folder with all standard files, including `CLAUDE.md` inside `.claude/`.

---

## Updating to the latest templates

When the team publishes new or updated templates, run these two commands to pull the latest version and apply it to your project:

```bash
pip install --force-reinstall git+https://github.com/kin-analytics/kin-internal-claude_ds_deploy.git
setup-claude
```

`--force-reinstall` ensures pip re-downloads the package even if the version number hasn't changed. `setup-claude` then overwrites the standard files with the latest versions — your custom files are never touched.

### Preview changes before applying (dry run)

Not sure what will change? Run this first:

```bash
setup-claude --dry-run
```

Shows exactly which files would be created or updated without writing anything to disk.

---

## What gets synced

```
.claude/
├── CLAUDE.md                         # Project-specific instructions (moved here or created)
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

### CLAUDE.md rules

| Situation | Action |
|-----------|--------|
| `CLAUDE.md` already in `.claude/` | Left untouched; import line added if missing |
| `CLAUDE.md` found at root or elsewhere | Moved to `.claude/CLAUDE.md`; import line added if missing |
| No `CLAUDE.md` anywhere | Created at `.claude/CLAUDE.md` with the import line |

The import line (`@.claude/CONTEXT.md`) is always ensured so Claude Code loads the standard Kin Analytics context automatically.

---

## Contributing

Edit files inside `src/claude_fixer/templates/.claude/`, bump the version in `pyproject.toml`, and push. DS users get the updates on their next reinstall + `setup-claude`.