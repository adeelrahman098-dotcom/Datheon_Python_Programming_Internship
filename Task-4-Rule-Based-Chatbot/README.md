# Task 4: Rule-Based Interactive Terminal Assistant / Chatbot

A responsive conversational terminal assistant built in Python featuring multi-intent recognition, regular expression keyword extraction, JSON knowledge base loading, and conversational state management.

## 👤 Author
- **Name:** Adeel Rahman
- **Role:** Python Programming Intern

## Features
- **JSON Knowledge Base Integration**: Dynamically loads greetings and FAQ question-answer pairs from `faq.json` with built-in fallback protection.
- **Input Normalization & Regex Extraction**: Cleans user queries (lowercasing, whitespace stripping) and extracts keywords using Python's `re` module.
- **Multi-Intent Recognition**: Capable of detecting and answering multiple intents within a single compound user query (e.g., greeting + business hours + certificate inquiry).
- **Conversational State Management**: Tracks session states (`GREETING` → `INTENT_IDENTIFICATION` → `RESOLUTION` / `FALLBACK` → `EXIT`).
- **Graceful Fallback & Clean Exit**: Provides helpful topic suggestions when query confidence is low and supports clean termination commands (`bye`, `exit`, `quit`).

## File Organization
- `chatbot.py`: Main interactive chatbot script.
- `faq.json`: External JSON dataset containing greetings and FAQ entries.
- `README.md`: Task documentation.

## How to Run

```bash
# From repository root
python Task-4/chatbot.py

# Or from inside the task folder
cd Task-4
python chatbot.py