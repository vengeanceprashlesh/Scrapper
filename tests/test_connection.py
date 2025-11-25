import os
import sys
from dotenv import load_dotenv
import yfinance as yf
from openai import OpenAI

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_connections():
    print("Loading environment variables...")
    load_dotenv()

    # 1. Check Environment Variables
    required_vars = ["OPENAI_API_KEY", "EMAIL_USER", "EMAIL_PASS"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
    else:
        print("✅ All required environment variables are present.")

    # 2. Test yfinance
    print("\nTesting yfinance connection...")
    try:
        ticker = "AAPL"
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if not hist.empty:
            print(f"✅ yfinance connection successful. Fetched data for {ticker}.")
        else:
            print(f"⚠️ yfinance connection successful but no data returned for {ticker}.")
    except Exception as e:
        print(f"❌ yfinance connection failed: {e}")

    # 3. Test OpenAI / OpenRouter
    print("\nTesting AI Client initialization...")
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        
        if openrouter_key:
            print(f"✅ OpenRouter API Key detected.")
            client = OpenAI(api_key=openrouter_key, base_url="https://openrouter.ai/api/v1")
            print("✅ OpenRouter client initialized successfully.")
        elif api_key:
            print(f"✅ OpenAI API Key detected.")
            client = OpenAI(api_key=api_key)
            print("✅ OpenAI client initialized successfully.")
        else:
            print("❌ No AI API Key (OpenAI or OpenRouter) missing, skipping client init.")
    except Exception as e:
        print(f"❌ AI client initialization failed: {e}")

    # 4. Mock Email (Print only)
    print("\nTesting Email Configuration (Mock)...")
    email_user = os.getenv("EMAIL_USER")
    if email_user:
        print(f"✅ Email User configured as: {email_user}")
        print("ℹ️  Real email sending is skipped in this test to avoid spam.")
    else:
        print("❌ Email User not configured.")

if __name__ == "__main__":
    test_connections()
