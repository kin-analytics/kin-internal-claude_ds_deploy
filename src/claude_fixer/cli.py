import argparse
import shutil
try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError  # type: ignore[no-redef]
from pathlib import Path


CONTEXT_IMPORT = "@.claude/CONTEXT.md"


def _get_version() -> str:
    try:
        return version("claude-ds-tools")
    except PackageNotFoundError:
        return "unknown"


def _merge_dir(source: Path, target: Path, dry_run: bool = False) -> None:
    """Recursively sync source directory into target.

    Files that exist in the master template are always updated (admin-owned).
    Files that exist only in the target are left untouched (DS custom files).

    Args:
        source: Master template directory inside the installed package.
        target: Destination directory in the user's project.
        dry_run: If True, print what would happen without making any changes.
    """
    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)

    for item in source.iterdir():
        dest = target / item.name

        if item.is_dir():
            _merge_dir(item, dest, dry_run=dry_run)
        elif dest.exists():
            if not dry_run:
                shutil.copy2(item, dest)
            print(f"  updated  : {dest.relative_to(Path.cwd())}")
        else:
            if not dry_run:
                shutil.copy2(item, dest)
            print(f"  added    : {dest.relative_to(Path.cwd())}")


def _sync_claude_md(project_root: Path, target_path: Path, dry_run: bool = False) -> None:
    """Ensure CLAUDE.md exists inside .claude/ and references CONTEXT.md.

    Search order:
    1. CLAUDE.md already in .claude/ → just add the import line if missing.
    2. CLAUDE.md found elsewhere in the project → move it to .claude/, then add import.
    3. No CLAUDE.md anywhere → create one in .claude/ with the import line.

    Args:
        project_root: Root directory of the user's project.
        target_path: The .claude/ directory where CLAUDE.md should live.
        dry_run: If True, print what would happen without making any changes.
    """
    dest_claude_md = target_path / "CLAUDE.md"
    found = None

    if not dest_claude_md.exists():
        # Search for CLAUDE.md anywhere in the project (skip hidden dirs and venvs)
        skip_dirs = {".git", ".venv", "venv", "env", "__pycache__", "node_modules", "build", "dist", ".eggs"}
        found = None
        root_claude = project_root / "CLAUDE.md"
        if root_claude.exists():
            found = root_claude
        else:
            for candidate in project_root.rglob("CLAUDE.md"):
                if not any(part in skip_dirs for part in candidate.parts):
                    found = candidate
                    break

        if found:
            if not dry_run:
                shutil.move(str(found), dest_claude_md)
            print(f"  moved    : CLAUDE.md ({found.relative_to(project_root)} → .claude/CLAUDE.md)")
        else:
            if not dry_run:
                dest_claude_md.write_text("")
            print(f"  added    : .claude/CLAUDE.md (created)")

    # Check if import line is already present; in dry-run a moved file won't be at dest yet
    if dest_claude_md.exists():
        content = dest_claude_md.read_text()
    elif found:
        content = found.read_text()
    else:
        content = ""
    if CONTEXT_IMPORT not in content:
        if not dry_run:
            separator = "\n" if content and not content.endswith("\n") else ""
            dest_claude_md.write_text(content + separator + CONTEXT_IMPORT + "\n")
        print(f"  updated  : .claude/CLAUDE.md (added {CONTEXT_IMPORT})")
    else:
        print(f"  skipped  : .claude/CLAUDE.md (import already present)")


def main():
    parser = argparse.ArgumentParser(
        description="Sync Kin Analytics standard .claude configuration into a project."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be created or updated without making any changes.",
    )
    args = parser.parse_args()
    dry_run = args.dry_run

    pkg_path = Path(__file__).parent
    template_path = pkg_path / "templates" / ".claude"
    project_root = Path.cwd()
    target_path = project_root / ".claude"
    pkg_version = _get_version()

    if dry_run:
        print(f"--- Dry run: no files will be written (v{pkg_version}) ---")
    else:
        print(f"--- Syncing .claude configuration (v{pkg_version}) ---")

    is_new = not target_path.exists()
    _merge_dir(template_path, target_path, dry_run=dry_run)

    if not dry_run:
        # Write version file so DS users can verify what's installed
        (target_path / "VERSION").write_text(f"claude-ds-tools=={pkg_version}\n")

    _sync_claude_md(project_root, target_path, dry_run=dry_run)

    if dry_run:
        print(f"\nDry run complete. Run without --dry-run to apply these changes.")
    elif is_new:
        print(f"\nCreated {target_path} with standard configuration (v{pkg_version}).")
    else:
        print(f"\nSync complete. Standard files updated to v{pkg_version}. Custom-only files were not modified.")