# Task 2: Stock Portfolio Performance Tracker

A command-line investment portfolio tracking utility built in Python that computes real-time portfolio valuation, percentage gain/loss per holding, and persists performance logs to an external CSV file.

## 👤 Author
- **Name:** Adeel Rahman
- **Role:** Python Programming Intern

## Features
- **S&P 500 Dataset Integration**: Automatically reads ticker symbols, company names, and GICS sectors from `constituents.csv`.
- **Position Aggregation**: Supports multiple entries of the same stock ticker by computing the weighted average buy price.
- **Valuation & Performance Metrics**: Calculates Invested Capital, Current Market Value, Net Profit/Loss ($), and Percentage Return (%) per holding and across the entire portfolio.
- **Formatted Console Report**: Outputs an aligned financial performance table directly in the terminal.
- **CSV Persistence**: Exports detailed holding records and total portfolio summary with timestamps to `portfolio_summary.csv` using Python's built-in `csv` module.

## File Organization
- `portfolio.py`: Main portfolio tracker script.
- `constituents.csv`: S&P 500 company metadata dataset.
- `portfolio_summary.csv`: Generated output file logging portfolio performance.
- `README.md`: Task documentation.

## How to Run

```bash
# From repository root
python Task-2-Stock-Portfolio-Tracker/portfolio.py

# Or from inside the task folder
cd Task-2-Stock-Portfolio-Tracker
python portfolio.py