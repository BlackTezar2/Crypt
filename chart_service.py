import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
import os

class ChartService:
    def __init__(self):
        self.zard = '#FFD700'
        self.zard_light = '#FFF4B8'
        self.zard_glow = '#FFE566'
        self.abi_sky = '#87CEEB'
        self.abi_pastel = '#B3E5FC'
        self.bg_color = '#FFFDF5'
        self.card_color = '#FFFFFF'
        self.text_dark = '#2C3E50'

    def generate_chart(self, period="1d"):
        try:
            btc = yf.Ticker("BTC-USD")
            interval = "1h" if period in ["1d", "5d"] else "1d"
            df = btc.history(period=period, interval=interval)

            if df.empty:
                return None

            plt.style.use('default')
            plt.rcParams['font.family'] = 'DejaVu Sans'
            plt.rcParams['font.size'] = 10

            fig, ax = plt.subplots(figsize=(12, 7), facecolor=self.bg_color)
            ax.set_facecolor(self.card_color)

            dates = df.index
            prices = df['Close'].values

            # 🌟 سایه زیر منحنی
            ax.fill_between(dates, prices, min(prices)*0.995,
                          color=self.zard_light, alpha=0.4, zorder=1)

            # 💛 خط اصلی
            ax.plot(dates, prices, color=self.zard, linewidth=2.5, zorder=3)

            # ⭐ نقاط مهم
            max_idx = np.argmax(prices)
            min_idx = np.argmin(prices)

            ax.scatter(dates[max_idx], prices[max_idx],
                      color=self.zard, s=100, edgecolors=self.text_dark,
                      linewidth=1.5, zorder=5, marker='D')
            ax.scatter(dates[min_idx], prices[min_idx],
                      color=self.abi_sky, s=100, edgecolors=self.text_dark,
                      linewidth=1.5, zorder=5, marker='D')

            # 🎯 آخرین قیمت
            ax.scatter(dates[-1], prices[-1],
                      color=self.zard_glow, s=200, edgecolors=self.text_dark,
                      linewidth=2, zorder=6)

            # 🎨 استایل
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color(self.text_dark)
            ax.spines['bottom'].set_color(self.text_dark)
            ax.spines['left'].set_alpha(0.2)
            ax.spines['bottom'].set_alpha(0.2)

            ax.tick_params(colors=self.text_dark, labelsize=8)

            if period == "1d":
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            elif period == "5d":
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))
            else:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

            ax.grid(True, alpha=0.08, color=self.text_dark, linestyle='-')

            # 📛 عنوان‌ها
            period_names = {"1d": "24 Hours", "5d": "5 Days", "1mo": "1 Month"}
            period_name = period_names.get(period, period)

            ax.set_title(f'CryptYumy Chart - {period_name}',
                        fontsize=18, color=self.text_dark, fontweight='bold', pad=15)

            ax.set_xlabel('~ CryptYumy ~', fontsize=11, color=self.zard,
                        fontweight='bold', alpha=0.8, labelpad=8)
            ax.set_ylabel('Price (USD)', fontsize=10, color=self.text_dark, alpha=0.7)

            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

            # ✨ واترمارک
            ax.text(0.98, 0.02, 'CryptYumy Bot - Your Cute Crypto Friend',
                   transform=ax.transAxes, fontsize=8,
                   color=self.zard, alpha=0.6, ha='right', style='italic')

            plt.tight_layout(pad=2)

            if not os.path.exists('charts'):
                os.makedirs('charts')
                filename = f"charts/btc_{period}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor=self.bg_color)
            plt.close()

            return filename

        except Exception as e:
            print(f"Error generating chart: {e}")
            return None
