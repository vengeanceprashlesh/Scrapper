import os
from openai import OpenAI
from typing import Dict, Optional

class AIAnalyst:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        self.client = OpenAI(api_key=api_key)

    def analyze_stock(self, market_data: Dict) -> str:
        """
        Generates a brief analysis based on market data and news.
        """
        ticker = market_data.get('ticker')
        price = market_data.get('last_close')
        change = market_data.get('change_percent')
        headlines = market_data.get('headlines', [])

        prompt = (
            f"You are a financial analyst. Analyze the following data for {ticker}:\n"
            f"- Price: ${price}\n"
            f"- Change: {change}%\n"
            f"- Recent News Headlines: {', '.join(headlines)}\n\n"
            "Provide a concise summary (max 3 sentences) of the stock's performance and sentiment based on the news. "
            "Do not give financial advice, just analysis."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful financial assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating analysis: {e}"
