import shutil
from pathlib import Path


def _merge_dir(source: Path, target: Path) -> None:
    """Recursively merge source directory into target using copy-if-missing logic.

    Files and directories that already exist in target are left untouched,
    preserving any user customizations. Only missing items are added.

    Args:
        source: Master template directory inside the installed package.
        target: Destination directory in the user's project.
    """
    target.mkdir(parents=True, exist_ok=True)

    for item in source.iterdir():
        dest = target / item.name

        if item.is_dir():
            # Recurse so we can add missing files inside existing directories.
            _merge_dir(item, dest)
        elif dest.exists():
            print(f"  skipped  : {dest.relative_to(Path.cwd())} (already exists)")
        else:
            shutil.copy2(item, dest)
            print(f"  added    : {dest.relative_to(Path.cwd())}")


def main():
    pkg_path = Path(__file__).parent
    template_path = pkg_path / "templates" / ".claude"
    target_path = Path.cwd() / ".claude"

    print("--- Syncing .claude configuration ---")

    is_new = not target_path.exists()
    _merge_dir(template_path, target_path)

    if is_new:
        print(f"\nCreated {target_path} with standard configuration.")
    else:
        print("\nSync complete. Existing customizations were not modified.")