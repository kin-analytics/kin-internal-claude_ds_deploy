import shutil
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path


def _get_version() -> str:
    try:
        return version("claude-ds-tools")
    except PackageNotFoundError:
        return "unknown"


def _merge_dir(source: Path, target: Path) -> None:
    """Recursively sync source directory into target.

    Files that exist in the master template are always updated (admin-owned).
    Files that exist only in the target are left untouched (DS custom files).

    Args:
        source: Master template directory inside the installed package.
        target: Destination directory in the user's project.
    """
    target.mkdir(parents=True, exist_ok=True)

    for item in source.iterdir():
        dest = target / item.name

        if item.is_dir():
            _merge_dir(item, dest)
        elif dest.exists():
            shutil.copy2(item, dest)
            print(f"  updated  : {dest.relative_to(Path.cwd())}")
        else:
            shutil.copy2(item, dest)
            print(f"  added    : {dest.relative_to(Path.cwd())}")


def main():
    pkg_path = Path(__file__).parent
    template_path = pkg_path / "templates" / ".claude"
    target_path = Path.cwd() / ".claude"
    pkg_version = _get_version()

    print(f"--- Syncing .claude configuration (v{pkg_version}) ---")

    is_new = not target_path.exists()
    _merge_dir(template_path, target_path)

    # Write version file so DS users can verify what's installed
    version_file = target_path / "VERSION"
    version_file.write_text(f"claude-ds-tools=={pkg_version}\n")

    if is_new:
        print(f"\nCreated {target_path} with standard configuration (v{pkg_version}).")
    else:
        print(f"\nSync complete. Standard files updated to v{pkg_version}. Custom-only files were not modified.")