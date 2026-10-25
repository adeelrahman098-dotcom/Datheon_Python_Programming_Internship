# Task 3: Automated File Organizer & Cleanup Utility

An autonomous desktop automation utility built in Python that inspects file extensions, dynamically creates categorized subdirectories, and safely relocates files while handling permission exceptions and naming collisions.

## 👤 Author
- **Name:** Adeel Rahman
- **Role:** Python Programming Intern

## Features
- **Extension-to-Category Mapping**: Automatically sorts files into `/Documents`, `/Images`, `/Videos`, `/Archives`, `/Code`, `/Audio`, and `/Others` based on file extensions.
- **Fast Directory Scanning**: Uses `os.scandir()` and `pathlib` for efficient filesystem traversal while ignoring subdirectories and protected script files.
- **Collision Resolution**: Prevents accidental file overwrites by automatically appending incremental suffixes (e.g., `report_1.pdf`, `report_2.pdf`) when duplicate filenames exist in the destination folder.
- **Exception Handling**: Implements `try-except` blocks to safely catch and report `PermissionError`, `FileExistsError`, and general OS errors without crashing.
- **Built-in Safe Demo Sandbox**: Includes an interactive option to auto-generate a `sample_cluttered_folder/` with 15 dummy files across various formats for instant, risk-free testing.
- **Formatted Execution Summary**: Displays real-time file relocation logs and a complete category breakdown in the console.

## File Organization
- `organizer.py`: Main desktop automation and directory sorting script.
- `sample_cluttered_folder/`: Auto-generated sandbox directory demonstrating organized category subfolders.
- `README.md`: Task documentation.

## How to Run

```bash
# From repository root
python Task-3/organizer.py

# Or from inside the task folder
cd Task-3
python organizer.py