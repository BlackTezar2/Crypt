import requests
from datetime import datetime
import time

class PriceService:
    BASE_URL = "https://api.coingecko.com/api/v3"

    @staticmethod
    def get_btc_price():
        """دریافت قیمت بیتکوین از CoinGecko"""
        try:
            # قیمت اصلی
            url = f"{PriceService.BASE_URL}/simple/price"
            params = {
                "ids": "bitcoin",
                "vs_currencies": "usd",
                "include_24hr_change": "true",
                "include_24hr_vol": "true",
                "include_24hr_high": "true",
                "include_24hr_low": "true",
            }

            headers = {
                'Accept': 'application/json',
                'User-Agent': 'CryptYumy/1.0'
            }

            resp = requests.get(url, headers=headers, params=params, timeout=15)

            # اگه Rate Limit خورد، ۳۰ ثانیه صبر کن
            if resp.status_code == 429:
                print("⏳ Rate limit, waiting 30s...")
                time.sleep(30)
                resp = requests.get(url, headers=headers, params=params, timeout=15)

            if resp.status_code != 200:
                print(f"❌ API Error: {resp.status_code}")
                return None

            data = resp.json()

            if 'bitcoin' not in data:
                return None

            btc = data['bitcoin']

            return {
                'price': btc.get('usd', 0),
                'change_24h': btc.get('usd_24h_change', 0),
                'high_24h': btc.get('usd_24h_high', btc.get('usd', 0)),
                'low_24h': btc.get('usd_24h_low', btc.get('usd', 0)),
                'volume_24h': btc.get('usd_24h_vol', 0),
                'timestamp': datetime.now()
            }

        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
            time.sleep(5)
            # یه بار دیگه تلاش کن
            try:
                return PriceService.get_btc_price()
            except:
                return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None

    @staticmethod
    def get_market_mood(change):
        if change > 5:
            return "🚀🌕 TO THE MOON! Party time!"
        elif change > 2:
            return "🌈✨ Bulls are dancing! Happy vibes!"
        elif change > 0:
            return "🙂💛 Gentle smile. Slow and steady!"
        elif change > -2:
            return "🥺👀 A bit shy today. Market's quiet."
        elif change > -5:
            return "😰📉 Bears are growling! Ouchie!"
        else:
            return "😱💔 PANIC! But hey, discounts! Sale sale!"
