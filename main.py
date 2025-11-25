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
    TARGETS = ["AAPL", "TSLA", "NVDA", "BTC-USD", "ETH-USD"]
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

    if not RECIPIENT_EMAIL:
        print("Error: RECIPIENT_EMAIL not set in environment variables.")
        sys.exit(1)

    print(f"Starting daily report for: {', '.join(TARGETS)}")

    final_report_html = "<html><body><h1>Daily Market Report</h1>"
    
    for ticker in TARGETS:
        print(f"\nProcessing {ticker}...")
        try:
            # 1. Fetch Data
            market = MarketData(ticker)
            data = market.get_data()
            
            if not data:
                print(f"⚠️ Skipping {ticker}: No data found.")
                continue

            # 2. Analyze Data
            analyst = AIAnalyst()
            analysis_text = analyst.analyze_stock(data)
            
            # 3. Append to Report
            stock_html = f"""
            <div style="margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px;">
                <h2>{ticker}</h2>
                <p><strong>Price:</strong> ${data['last_close']} <span style="color: {'green' if data['change_percent'] >= 0 else 'red'}">({data['change_percent']}%)</span></p>
                <h3>Analysis</h3>
                <p>{analysis_text}</p>
                <h3>Headlines</h3>
                <ul>
                    {''.join([f'<li>{h}</li>' for h in data['headlines']])}
                </ul>
            </div>
            """
            final_report_html += stock_html
            print(f"✅ {ticker} processed successfully.")

        except Exception as e:
            print(f"❌ Error processing {ticker}: {e}")
            continue

    final_report_html += "</body></html>"

    # 4. Send Email
    print("\nSending aggregated email report...")
    try:
        notifier = EmailService()
        notifier.send_html_email(RECIPIENT_EMAIL, "Daily Market Report", final_report_html)
    except Exception as e:
        print(f"Notification failed: {e}")
        sys.exit(1)

    print("Daily report completed successfully.")

if __name__ == "__main__":
    main()
