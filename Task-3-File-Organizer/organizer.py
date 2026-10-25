import os
import shutil
from pathlib import Path
from datetime import datetime

# 1. Extension-to-Category Mapping Dictionary
EXTENSION_MAP = {
    # Documents
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".xlsx": "Documents",
    ".csv": "Documents",
    ".pptx": "Documents",
    ".md": "Documents",
    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".svg": "Images",
    ".webp": "Images",
    ".bmp": "Images",
    # Videos
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    ".mov": "Videos",
    ".wmv": "Videos",
    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".7z": "Archives",
    # Code
    ".py": "Code",
    ".js": "Code",
    ".html": "Code",
    ".css": "Code",
    ".cpp": "Code",
    ".c": "Code",
    ".java": "Code",
    ".json": "Code",
    ".sql": "Code",
    # Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".flac": "Audio",
    ".aac": "Audio"
}

PROTECTED_FILES = {"organizer.py", "readme.md", "cleanup_log.txt"}


def create_sample_test_folder(base_dir: Path) -> Path:
    """
    Creates a safe 'sample_cluttered_folder' populated with dummy files
    so the user can test the file organizer immediately and safely.
    """
    sample_dir = base_dir / "sample_cluttered_folder"
    sample_dir.mkdir(exist_ok=True)

    dummy_files = [
        "project_proposal.pdf",
        "financial_report.xlsx",
        "meeting_notes.txt",
        "vacation_photo.jpg",
        "ui_screenshot.png",
        "company_logo.svg",
        "lecture_recording.mp4",
        "demo_tutorial.mov",
        "backup_dataset.zip",
        "source_archive.tar",
        "data_analysis.py",
        "index_template.html",
        "styles.css",
        "podcast_episode.mp3",
        "unidentified_file.xyz"
    ]

    created_count = 0
    for filename in dummy_files:
        file_path = sample_dir / filename
        if not file_path.exists():
            file_path.write_text(f"Dummy content for {filename}\n", encoding="utf-8")
            created_count += 1

    print(f"✅ Prepared test folder: '{sample_dir.name}' ({created_count} new sample files created).")
    return sample_dir


def resolve_collision(dest_folder: Path, filename: str) -> Path:
    """
    Checks if a file with the same name already exists in dest_folder.
    If a collision is detected, appends an incremental counter (e.g., file_1.pdf).
    """
    target_path = dest_folder / filename
    if not target_path.exists():
        return target_path

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1

    while True:
        new_name = f"{stem}_{counter}{suffix}"
        candidate_path = dest_folder / new_name
        if not candidate_path.exists():
            return candidate_path
        counter += 1


def organize_directory(target_dir: Path) -> dict:
    """
    Scans target_dir using os.scandir(), dynamically creates category folders,
    and safely relocates files using shutil.move() with exception handling.
    """
    stats = {
        "moved": 0,
        "skipped": 0,
        "collisions_resolved": 0,
        "errors": 0,
        "category_counts": {},
        "details": []
    }

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"❌ Error: Directory '{target_dir}' does not exist or is not a valid folder.")
        return stats

    print(f"\n🔍 Scanning directory: {target_dir}\n" + "-" * 72)

    try:
        with os.scandir(target_dir) as entries:
            for entry in entries:
                # Skip subdirectories
                if not entry.is_file():
                    continue

                filename = entry.name

                # Protect script and documentation files if run in the current folder
                if filename.lower() in PROTECTED_FILES or filename.startswith("."):
                    stats["skipped"] += 1
                    continue

                ext = Path(filename).suffix.lower()
                category = EXTENSION_MAP.get(ext, "Others")

                dest_folder = target_dir / category
                src_path = Path(entry.path)

                try:
                    # Dynamically create the category subfolder
                    dest_folder.mkdir(exist_ok=True)

                    # Handle naming collisions safely
                    final_dest_path = resolve_collision(dest_folder, filename)
                    collision_occurred = final_dest_path.name != filename

                    if collision_occurred:
                        stats["collisions_resolved"] += 1

                    # Move file using shutil.move()
                    shutil.move(str(src_path), str(final_dest_path))

                    stats["moved"] += 1
                    stats["category_counts"][category] = stats["category_counts"].get(category, 0) + 1
                    stats["details"].append({
                        "original": filename,
                        "destination": f"/{category}/{final_dest_path.name}",
                        "status": "Renamed & Moved" if collision_occurred else "Moved"
                    })

                    print(f"  ✔ {filename:<28} ──►  /{category}/{final_dest_path.name}")

                except PermissionError:
                    stats["errors"] += 1
                    print(f"  ❌ PermissionError: Locked or restricted file '{filename}'. Skipped.")
                except FileExistsError:
                    stats["errors"] += 1
                    print(f"  ❌ FileExistsError: Could not overwrite '{filename}'. Skipped.")
                except Exception as e:
                    stats["errors"] += 1
                    print(f"  ❌ Error moving '{filename}': {e}")

    except PermissionError:
        print(f"❌ PermissionError: Access denied when scanning '{target_dir}'.")

    return stats


def display_execution_summary(target_dir: Path, stats: dict):
    """Prints a formatted execution summary and saves a log file."""
    print("\n" + "=" * 72)
    print(f"{'📊 AUTOMATED FILE ORGANIZER EXECUTION SUMMARY':^72}")
    print("=" * 72)
    print(f"Target Directory     : {target_dir}")
    print(f"Timestamp            : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 72)
    print(f"Total Files Relocated: {stats['moved']}")
    print(f"Collisions Resolved  : {stats['collisions_resolved']}")
    print(f"Protected / Skipped  : {stats['skipped']}")
    print(f"Permission / Errors  : {stats['errors']}")
    print("-" * 72)

    if stats["category_counts"]:
        print("Category Breakdown:")
        for category, count in sorted(stats["category_counts"].items()):
            print(f"  • /{category:<12} : {count} file(s)")
    else:
        print("ℹ️  No eligible loose files found to organize.")

    print("=" * 72)


def main():
    script_dir = Path(__file__).resolve().parent

    print("\n========================================================================")
    print("             🗂️  AUTOMATED FILE ORGANIZER & CLEANUP UTILITY              ")
    print("========================================================================")
    print("Choose an option:")
    print("  [1] Create & Organize a Safe Demo Folder ('sample_cluttered_folder')")
    print("  [2] Enter a Custom Directory Path to Organize (e.g., Downloads)")
    print("========================================================================")

    choice = input("Select option (1 or 2): ").strip()

    if choice == "1":
        target_dir = create_sample_test_folder(script_dir)
    elif choice == "2":
        raw_path = input("Enter full directory path to organize: ").strip().strip('"').strip("'")
        target_dir = Path(raw_path).expanduser().resolve()
    else:
        print("ℹ️  Defaulting to Option 1 (Safe Demo Folder).")
        target_dir = create_sample_test_folder(script_dir)

    stats = organize_directory(target_dir)
    display_execution_summary(target_dir, stats)


if __name__ == "__main__":
    main()