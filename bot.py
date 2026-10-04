import os
import json
import requests
import ccxt

def get_smart_money():
    url = "https://fapi.binance.com/futures/data/topLongShortAccountRatio?symbol=BTCUSDT&period=5m&limit=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    data = response.json()[0]
    
    long_pct = float(data['longAccount']) * 100
    
    if long_pct >= 60:
        return "STRONG_BULLISH"
    elif long_pct <= 40:
        return "STRONG_BEARISH"
    return "NEUTRAL"

if __name__ == "__main__":
    # 1. Read the signal sent from TradingView (injected by GitHub Actions)
    tv_action = os.environ.get('TV_ACTION', 'NONE').upper()
    print(f"🚨 TradingView Signal: {tv_action}")
    
    # 2. Get unblocked sentiment from Binance
    sentiment = get_smart_money()
    print(f"🕵️ Smart Money Sentiment: {sentiment}")
    
    # 3. Connect to Phemex
    exchange = ccxt.phemex({
        'apiKey': os.environ.get('PHEMEX_API_ID'),
        'secret': os.environ.get('PHEMEX_SECRET'),
        'enableRateLimit': True,
    })
    exchange.set_sandbox_mode(True)
    
    # 4. Execute Logic
    if tv_action == "BUY" and sentiment == "STRONG_BULLISH":
        print("✅ Consensus Reached! Executing HIGH RISK BUY.")
        exchange.create_market_buy_order("BTC/USDT", 0.05)
    elif tv_action == "SELL" and sentiment == "STRONG_BEARISH":
        print("✅ Consensus Reached! Executing HIGH RISK SELL.")
        exchange.create_market_sell_order("BTC/USDT", 0.05)
    else:
        print("🛑 Sentiment Conflict or Neutral. Trade Ignored.")