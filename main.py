import os
import sys
from dotenv import load_dotenv
from src.data_fetcher import MarketData
from src.analyst import AIAnalyst
from src.notifier import EmailService

# Load environment variables
load_dotenv()

def main():
    # Configuration
    TICKER = "AAPL" # Default ticker, could be an env var or arg
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

    if not RECIPIENT_EMAIL:
        print("Error: RECIPIENT_EMAIL not set in environment variables.")
        sys.exit(1)

    print(f"Starting daily report for {TICKER}...")

    # 1. Fetch Data
    print("Fetching market data...")
    market = MarketData(TICKER)
    data = market.get_data()
    
    if not data:
        print("Failed to fetch data. Exiting.")
        sys.exit(1)

    # 2. Analyze Data
    print("Analyzing data with AI...")
    try:
        analyst = AIAnalyst()
        analysis_text = analyst.analyze_stock(data)
        data['analysis'] = analysis_text
    except Exception as e:
        print(f"Analysis failed: {e}")
        sys.exit(1)

    # 3. Send Email
    print("Sending email report...")
    try:
        notifier = EmailService()
        notifier.send_report(RECIPIENT_EMAIL, data)
    except Exception as e:
        print(f"Notification failed: {e}")
        sys.exit(1)

    print("Daily report completed successfully.")

if __name__ == "__main__":
    main()
