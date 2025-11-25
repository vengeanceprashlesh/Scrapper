import os
from openai import OpenAI
from typing import Dict, Optional

class AIAnalyst:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = None
        self.model = "gpt-4o-mini"

        # Check for OpenRouter override
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            self.api_key = openrouter_key
            self.base_url = "https://openrouter.ai/api/v1"
            self.model = "openai/gpt-4o-mini"

        if not self.api_key:
            raise ValueError("Neither OPENAI_API_KEY nor OPENROUTER_API_KEY is set.")
            
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

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
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful financial assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating analysis: {e}"
