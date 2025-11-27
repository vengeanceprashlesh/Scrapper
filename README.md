# AI Stock Analyst

A Python-based automated tool that fetches daily stock market data, performs AI-driven analysis using OpenRouter (GPT-4o-mini), and delivers a consolidated HTML report via email.

## Features

- **Real-time Data**: Fetches latest stock prices, percentage changes, and news headlines using `yfinance`.
- **AI Analysis**: Uses OpenRouter (GPT-4o-mini) to generate concise financial insights based on market data and news.
- **Automated Reporting**: Compiles a professional HTML report and emails it to a specified recipient.
- **Multi-Asset Support**: Capable of tracking both Stocks (e.g., AAPL, TSLA) and Crypto (e.g., BTC-USD).

## Prerequisites

- Python 3.8 or higher
- An [OpenRouter](https://openrouter.ai/) API Key
- A Gmail account (for SMTP) with an App Password generated

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the root directory.
2. Add the following environment variables:

   ```env
   # AI Configuration
   OPENROUTER_API_KEY=your_openrouter_api_key_here

   # Email Configuration
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_gmail_app_password
   RECIPIENT_EMAIL=recipient_email@example.com
   ```

   > **Note**: For Gmail, you must use an **App Password**, not your regular login password. Go to Google Account > Security > 2-Step Verification > App passwords to generate one.

## Usage

Run the main script to generate and send the daily report:

```bash
python main.py
```

The script will:
1. Fetch data for configured targets (default: AAPL, TSLA, NVDA, BTC-USD, ETH-USD).
2. Generate AI analysis for each.
3. Compile an HTML report.
4. Send the report to `RECIPIENT_EMAIL`.

## Project Structure

- `main.py`: Entry point. Orchestrates the workflow.
- `src/data_fetcher.py`: Handles fetching stock data and news via `yfinance`.
- `src/analyst.py`: Interfaces with OpenRouter API for text analysis.
- `src/notifier.py`: Manages SMTP connection and email sending.
