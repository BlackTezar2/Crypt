import yfinance as yf
from datetime import datetime

class PriceService:
    @staticmethod
    def get_btc_price():
        try:
            btc = yf.Ticker("BTC-USD")
            data = btc.history(period="1d", interval="1h")
            
            if data.empty:
                return None
            
            current_price = data['Close'].iloc[-1]
            open_price = data['Open'].iloc[0]
            high_24h = data['High'].max()
            low_24h = data['Low'].min()
            change_24h = ((current_price - open_price) / open_price) * 100
            volume_24h = data['Volume'].sum()
            
            return {
                'price': current_price,
                'change_24h': change_24h,
                'high_24h': high_24h,
                'low_24h': low_24h,
                'volume_24h': volume_24h,
                'timestamp': datetime.now()
            }
        except Exception as e:
            print(f"Error fetching price: {e}")
            return None
    
    @staticmethod
    def get_market_mood(change):
        if change > 5:
            return "PARTY TIME! 🚀🌕 Everyone is celebrating!"
        elif change > 2:
            return "Happy vibes! 🌈✨ Bulls are dancing!"
        elif change > 0:
            return "Gentle smile 🙂💛 Slow and steady!"
        elif change > -2:
            return "A bit shy today 🥺👀 Markets are quiet"
        elif change > -5:
            return "Ouchie! 😰📉 Bears are growling!"
        else:
            return "PANIC MODE! 😱💔 But hey, discounts!"
