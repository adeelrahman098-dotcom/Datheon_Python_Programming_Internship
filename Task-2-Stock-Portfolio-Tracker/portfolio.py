import csv
from pathlib import Path
from datetime import datetime

# Sample current market prices (USD) for popular S&P 500 tickers
SAMPLE_MARKET_PRICES = {
    "AAPL": 225.50,
    "MSFT": 430.20,
    "GOOGL": 180.75,
    "GOOG": 182.10,
    "AMZN": 205.10,
    "NVDA": 135.80,
    "TSLA": 250.00,
    "META": 585.40,
    "BRK.B": 455.10,
    "JPM": 225.30,
    "V": 290.15,
    "JNJ": 158.90,
    "WMT": 82.40,
    "PG": 170.25,
    "MA": 505.60,
    "UNH": 565.00,
    "HD": 395.80,
    "DIS": 96.50,
    "NFLX": 755.20,
    "AMD": 155.40,
    "INTC": 23.50,
    "ADBE": 495.00,
    "ABBV": 188.50,
    "ABT": 116.20,
    "ACN": 345.80,
    "MMM": 130.40,
    "ABNB": 135.25
}


def load_sp500_constituents(script_dir: Path, filename="constituents.csv") -> dict:
    """
    Loads S&P 500 company metadata (Symbol, Security, GICS Sector) from constituents.csv.
    """
    constituents = {}
    file_path = script_dir / filename

    # If saved under a slightly different .csv name, look for it automatically
    if not file_path.exists():
        csv_candidates = [
            f for f in script_dir.glob("*.csv")
            if f.name.lower() != "portfolio_summary.csv"
        ]
        if csv_candidates:
            file_path = csv_candidates[0]

    if not file_path.exists():
        print(f"ℹ️  '{filename}' not found in folder. Using built-in S&P 500 ticker lookup.")
        return constituents

    try:
        with open(file_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row.get("Symbol", "").strip().upper()
                if symbol:
                    constituents[symbol] = {
                        "company": row.get("Security", "Unknown Company").strip(),
                        "sector": row.get("GICS Sector", "Unknown Sector").strip()
                    }
        print(f"✅ Loaded {len(constituents)} S&P 500 companies from '{file_path.name}'.")
    except Exception as e:
        print(f"⚠️  Error reading '{file_path.name}': {e}")

    return constituents


def get_positive_float(prompt: str) -> float:
    """Prompts user until a valid positive number is entered."""
    while True:
        try:
            val = float(input(prompt).strip())
            if val <= 0:
                print("❌ Value must be greater than 0. Please try again.")
                continue
            return val
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")


def collect_portfolio_positions(constituents: dict, market_prices: dict) -> dict:
    """
    Allows the user to enter stock ticker symbols, buy prices, and share quantities.
    Stores positions in a dictionary structure.
    """
    portfolio = {}

    print("\n================================================================")
    print("            📈 STOCK PORTFOLIO PERFORMANCE TRACKER              ")
    print("================================================================")
    print("Sample Tickers with Pre-loaded Prices: AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, AMD, ADBE, MMM")
    print("Enter your stock holdings below (type 'done' when finished).\n")

    while True:
        ticker = input("Enter Stock Ticker Symbol (or 'done' to finish): ").strip().upper()

        if ticker == "DONE":
            if not portfolio:
                print("⚠️  Your portfolio is empty! Please add at least one stock holding.")
                continue
            break

        if not ticker or not ticker.replace(".", "").replace("-", "").isalnum():
            print("❌ Invalid ticker symbol. Example valid symbols: AAPL, MSFT, GOOGL.")
            continue

        # Identify company metadata from constituents.csv if available
        if ticker in constituents:
            company_name = constituents[ticker]["company"]
            sector = constituents[ticker]["sector"]
            print(f"   🏢 Company: {company_name} ({sector})")
        else:
            company_name = "Custom / Unlisted"
            sector = "N/A"
            if constituents:
                print(f"   ℹ️  Note: '{ticker}' is not listed in the S&P 500 constituents file.")

        # Look up current price
        if ticker in market_prices:
            current_price = market_prices[ticker]
            print(f"   💵 Current Market Price for {ticker}: ${current_price:,.2f}")
        else:
            print(f"   ℹ️  No pre-loaded market price for '{ticker}'.")
            current_price = get_positive_float(f"   Enter current market price for {ticker} ($): ")
            market_prices[ticker] = current_price

        buy_price = get_positive_float(f"   Enter your buy price for {ticker} ($): ")
        quantity = get_positive_float(f"   Enter share quantity for {ticker}: ")

        # Aggregate if the user enters the same ticker multiple times
        if ticker in portfolio:
            old_qty = portfolio[ticker]["quantity"]
            old_cost = portfolio[ticker]["buy_price"] * old_qty
            new_qty = old_qty + quantity
            new_avg_buy = (old_cost + (buy_price * quantity)) / new_qty

            portfolio[ticker]["quantity"] = new_qty
            portfolio[ticker]["buy_price"] = new_avg_buy
            print(f"   ✅ Updated {ticker}: {new_qty:g} total shares @ Avg Buy ${new_avg_buy:,.2f}\n")
        else:
            portfolio[ticker] = {
                "company": company_name,
                "sector": sector,
                "buy_price": buy_price,
                "current_price": current_price,
                "quantity": quantity
            }
            print(f"   ✅ Added {ticker} ({quantity:g} shares @ ${buy_price:,.2f})\n")

    return portfolio


def calculate_portfolio_performance(portfolio: dict) -> tuple[list, dict]:
    """
    Computes total invested capital, current market value, and percentage gain/loss per holding.
    """
    records = []
    total_invested = 0.0
    total_market_value = 0.0

    for ticker, data in portfolio.items():
        buy_price = data["buy_price"]
        current_price = data["current_price"]
        quantity = data["quantity"]

        invested_capital = buy_price * quantity
        market_value = current_price * quantity
        profit_loss = market_value - invested_capital
        gain_loss_pct = ((current_price - buy_price) / buy_price) * 100

        total_invested += invested_capital
        total_market_value += market_value

        records.append({
            "Ticker": ticker,
            "Company": data["company"],
            "Sector": data["sector"],
            "Shares": round(quantity, 4),
            "Buy_Price": round(buy_price, 2),
            "Current_Price": round(current_price, 2),
            "Invested_Capital": round(invested_capital, 2),
            "Market_Value": round(market_value, 2),
            "Profit_Loss": round(profit_loss, 2),
            "Gain_Loss_Pct": round(gain_loss_pct, 2)
        })

    total_profit_loss = total_market_value - total_invested
    total_return_pct = ((total_profit_loss / total_invested) * 100) if total_invested > 0 else 0.0

    summary = {
        "total_invested": round(total_invested, 2),
        "total_market_value": round(total_market_value, 2),
        "total_profit_loss": round(total_profit_loss, 2),
        "total_return_pct": round(total_return_pct, 2)
    }

    return records, summary


def display_console_report(records: list, summary: dict):
    """Displays a formatted summary table in the terminal."""
    print("\n" + "=" * 105)
    print(f"{'PORTFOLIO PERFORMANCE & VALUATION SUMMARY':^105}")
    print("=" * 105)
    print(
        f"{'Ticker':<7} | {'Company':<22} | {'Shares':>8} | {'Buy ($)':>9} | "
        f"{'Curr ($)':>9} | {'Invested ($)':>12} | {'Market Val ($)':>14} | {'Gain/Loss':>10}"
    )
    print("-" * 105)

    for r in records:
        sign = "+" if r["Gain_Loss_Pct"] >= 0 else ""
        pct_str = f"{sign}{r['Gain_Loss_Pct']:.2f}%"
        comp_short = (r["Company"][:19] + "...") if len(r["Company"]) > 22 else r["Company"]
        print(
            f"{r['Ticker']:<7} | {comp_short:<22} | {r['Shares']:>8.2f} | {r['Buy_Price']:>9,.2f} | "
            f"{r['Current_Price']:>9,.2f} | {r['Invested_Capital']:>12,.2f} | "
            f"{r['Market_Value']:>14,.2f} | {pct_str:>10}"
        )

    print("-" * 105)
    pl_sign = "+" if summary["total_profit_loss"] >= 0 else ""
    print(f"Total Invested Capital : ${summary['total_invested']:,.2f}")
    print(f"Current Market Value   : ${summary['total_market_value']:,.2f}")
    print(
        f"Total Net Profit/Loss  : {pl_sign}${summary['total_profit_loss']:,.2f} "
        f"({pl_sign}{summary['total_return_pct']:.2f}%)"
    )
    print("=" * 105)


def save_to_csv(records: list, summary: dict, output_file: Path):
    """Persists the portfolio performance log to 'portfolio_summary.csv'."""
    fieldnames = [
        "Ticker",
        "Company",
        "Sector",
        "Shares",
        "Buy_Price",
        "Current_Price",
        "Invested_Capital",
        "Market_Value",
        "Profit_Loss",
        "Gain_Loss_Pct",
        "Timestamp"
    ]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(output_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for r in records:
                row = r.copy()
                row["Timestamp"] = timestamp
                writer.writerow(row)

            # Summary row at bottom
            writer.writerow({
                "Ticker": "TOTAL",
                "Company": "PORTFOLIO SUMMARY",
                "Sector": "",
                "Shares": "",
                "Buy_Price": "",
                "Current_Price": "",
                "Invested_Capital": summary["total_invested"],
                "Market_Value": summary["total_market_value"],
                "Profit_Loss": summary["total_profit_loss"],
                "Gain_Loss_Pct": summary["total_return_pct"],
                "Timestamp": timestamp
            })

        print(f"\n💾 Portfolio summary successfully logged to: '{output_file.name}'")
    except Exception as e:
        print(f"\n❌ Error writing CSV file: {e}")


def main():
    script_dir = Path(__file__).resolve().parent
    output_csv = script_dir / "portfolio_summary.csv"

    constituents = load_sp500_constituents(script_dir, "constituents.csv")
    market_prices = SAMPLE_MARKET_PRICES.copy()

    portfolio = collect_portfolio_positions(constituents, market_prices)
    records, summary = calculate_portfolio_performance(portfolio)

    display_console_report(records, summary)
    save_to_csv(records, summary, output_csv)


if __name__ == "__main__":
    main()