#!/usr/bin/env python3
"""
🐣 CryptYumy Bot - Your Cute Bitcoin Companion
"""

from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from crypt.config import BOT_TOKEN
from crypt.handlers import *
import sys

def main():
    print("""
    ╔══════════════════════════════════╗
    ║                                  ║
    ║     ╭━━━━━━━━━━━━━━━━━━╮       ║
    ║     ┃  CryptYumy Bot  ┃       ║
    ║     ╰━━━━━━━━━━━━━━━━━━╯       ║
    ║                                  ║
    ║   Your Cute Crypto Friend!      ║
    ║                                  ║
    ╚══════════════════════════════════╝
    """)
    
    if not BOT_TOKEN or BOT_TOKEN == "your_token_here":
        print("❌ Please set your BOT_TOKEN in .env file!")
        sys.exit(1)
    
    print("🐣 Hatching CryptYumy...")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # 🎯 هندلرها
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(CommandHandler("chart", chart_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)
    
    print("✨ CryptYumy is ready to make friends!")
    print("🐣 Bot is running... Press Ctrl+C to stop")
    print("💛 Go make some human friends, Yumy!")
    
    app.run_polling(poll_interval=1)

if __name__ == "__main__":
    main()
