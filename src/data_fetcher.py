import yfinance as yf
from typing import Dict, Optional, List

class MarketData:
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)

    def get_data(self) -> Optional[Dict]:
        """
        Fetches the last close price, percentage change, and recent news.
        """
        try:
            # Fetch history for the last 2 days to calculate change
            hist = self.stock.history(period="5d")
            
            if hist.empty:
                print(f"Error: No data found for ticker {self.ticker}")
                return None

            # Get the latest close and the one before it
            if len(hist) >= 2:
                last_close = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                percent_change = ((last_close - prev_close) / prev_close) * 100
            else:
                # Fallback if not enough data (e.g., new listing)
                last_close = hist['Close'].iloc[-1]
                percent_change = 0.0

            # Fetch news
            news_items = self.stock.news
            headlines = []
            if news_items:
                # Get top 3 headlines
                for item in news_items[:3]:
                    headlines.append(item.get('title', 'No Title'))
            
            return {
                "ticker": self.ticker,
                "last_close": round(last_close, 2),
                "change_percent": round(percent_change, 2),
                "headlines": headlines
            }

        except Exception as e:
            print(f"Error fetching data for {self.ticker}: {e}")
            return None
