# Datheon Python Programming Internship

A collection of Python projects completed as part of the
Datheon Python Programming Internship.

## About the Repository

This repository contains practical Python programming tasks
designed to improve problem-solving, programming logic,
modular coding, and software development skills.

## Tasks

### Task 1: Hangman Word Guessing Game
- **Status:** Completed
- **Language:** Python 3
- **Type:** Console application
- **Concepts:** Random module, strings, sets, loops,
  conditionals, functions, file handling, and input validation.

A terminal-based word guessing game where players try to
discover a hidden word within six incorrect guesses, featuring dynamic ASCII art and categorized clues.

**Folder:** `Task-1-Hangman-Game/`

### Task 2: Stock Portfolio Performance Tracker
- **Status:** Completed
- **Language:** Python 3
- **Type:** Console application & CSV logger
- **Concepts:** Dictionaries, `csv` module, File I/O, `pathlib`,
  data aggregation, financial calculations, and formatted console tables.

An investment portfolio tracking utility that allows users to enter stock ticker symbols, buy prices, and share quantities, computes total portfolio value and percentage gain/loss per holding, and automatically logs the transaction summary to an external CSV file.

**Folder:** `Task-2/`

### Task 3: Automated File Organizer & Cleanup Utility
- **Status:** Completed
- **Language:** Python 3
- **Type:** Desktop automation script
- **Concepts:** `os.scandir()`, `shutil.move()`, `pathlib`, dictionary mapping,
  collision handling, and `try-except` exception handling (`PermissionError`, `FileExistsError`).

An autonomous desktop automation utility that organizes cluttered directories by inspecting file extensions, dynamically creating category subfolders (`/Documents`, `/Images`, `/Videos`, `/Archives`, `/Code`, `/Audio`, `/Others`), and safely relocating files while resolving naming collisions.

**Folder:** `Task-3/`

### Task 4: Rule-Based Interactive Terminal Assistant / Chatbot
- **Status:** Completed
- **Language:** Python 3
- **Type:** Interactive CLI chatbot
- **Concepts:** Regular expressions (`re`), `json` module, text normalization,
  multi-intent recognition, conversational state management, and fallback handling.

A rule-based customer support and internship FAQ assistant that parses user input using keywords and regular expressions, handles queries regarding business hours, project submissions, and certificates from an external JSON dataset, and manages conversational state transitions with graceful fallbacks and clean exit commands (`bye`, `exit`, `quit`).

**Folder:** `Task-4/`

## Technologies Used

- Python 3
- Visual Studio Code
- Git and GitHub

## How to Run the Tasks

### Task 1: Hangman Game
1. Install Python 3.
2. Open the Task 1 folder (`Task-1-Hangman-Game/`) in your terminal.
3. Run:

    `python hangman.py`

### Task 2: Stock Portfolio Tracker
1. Open the Task 2 folder (`Task-2/`) in your terminal.
2. Run:

    `python portfolio.py`

### Task 3: Automated File Organizer
1. Open the Task 3 folder (`Task-3/`) in your terminal.
2. Run:

    `python organizer.py`

### Task 4: Rule-Based Interactive Chatbot
1. Open the Task 4 folder (`Task-4/`) in your terminal.
2. Run:

    `python chatbot.py`

On Windows, you can also use `py hangman.py`, `py portfolio.py`, `py organizer.py`, or `py chatbot.py`.

## Author

Adeel Rahman

## Internship

Datheon Python Programming Internship