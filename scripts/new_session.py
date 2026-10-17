"""Create a private, offline lab notebook without overwriting existing files."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ("machine.md", "report.md", "credentials.md", "progress.md", "tool-inventory.md")
TEMPLATES_BY_MODE = {
    "exam": TEMPLATES,
    "pentest": ("machine.md", "client-report.md", "engagement.md", "credentials.md", "tool-inventory.md"),
}


def create_session(destination, mode="exam"):
    if mode not in TEMPLATES_BY_MODE:
        raise ValueError(f"Unknown notebook mode: {mode}")
    selected_templates = TEMPLATES_BY_MODE[mode]
    destination = Path(destination).expanduser()
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Destination already exists: {destination}")
    destination = destination.resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise ValueError("Choose a private destination outside this repository.")
    for name in selected_templates:
        if not (ROOT / "templates" / name).is_file():
            raise FileNotFoundError(f"Missing template: {name}")
    destination.mkdir(parents=True, mode=0o700)
    for name in selected_templates:
        shutil.copyfile(ROOT / "templates" / name, destination / name)
    for name in ("scans", "evidence", "files", "notes"):
        (destination / name).mkdir()
    (destination / "README.md").write_text(
        f"# Private {mode} notebook\n\n"
        "Keep this directory out of public repositories. Store evidence and credentials "
        "according to your lab rules. This directory is not encrypted; review filesystem "
        "permissions and backups before storing secrets.\n", encoding="utf-8"
    )
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--mode", choices=tuple(TEMPLATES_BY_MODE), default="exam", help="choose exam evidence/report or client engagement/finding templates")
    args = parser.parse_args()
    try:
        print(f"Created private notebook: {create_session(args.destination, mode=args.mode)}")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
