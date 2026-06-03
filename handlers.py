from telegram import Update
from telegram.ext import ContextTypes
from price_service import PriceService
from chart_service import ChartService
from keyboards import get_start_keyboard, get_chart_keyboard, get_back_keyboard
from config import YUMY_EMOJIS
import os
import random

price_service = PriceService()
chart_service = ChartService()

# 🎭 جملات تصادفی Yumy
YUMY_PHRASES = {
    "greeting": [
        "Cheep cheep! I'm so happy to see you! {}",
        "Oh! A human friend! Hello hello! {}",
        "Yay! Someone woke me up! {}",
    ],
    "fetching": [
        "Let me check my magic crystal ball... {}",
        "Asking the Bitcoin gods... {}",
        "Running to check the charts! Wait here! {}",
    ],
    "chart_ready": [
        "Ta-da! Here's your beautiful chart! {}",
        "I drew this with my tiny wings! {}",
        "A masterpiece from your favorite chick! {}",
    ],
    "error": [
        "Oopsies! My chicken brain froze! {}",
        "Oh no! The internet worms are slow today! {}",
        "Peep... something went wrong... {}",
    ],
    "about": [
        "I'm Yumy, a baby chick who loves Bitcoin! I was born to make crypto fun and cute! No scary charts, no complicated words. Just a friendly chick helping you understand the crypto world! I might not always be right, but I'll always be honest and adorable! {}",
    ],
}

def get_random_phrase(category):
    phrases = YUMY_PHRASES.get(category, ["Cheep! {}"])
    return random.choice(phrases).format(random.choice(["🐣", "💛", "✨", "🍯", "🐤"]))

# 🎯 /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    greeting = get_random_phrase("greeting")

    message = f"""
{greeting}

Welcome to CryptYumy, {user.first_name}!

I'm your cute crypto companion! 
Here's what I can do for you:

💰 /price - Live Bitcoin price with market mood
📊 /chart - Beautiful price charts (24h to 1 month)
🐣 /stats - Your adventure stats with me

Why me?
✨ I'm cute (obviously!)
📊 I make pretty charts
💛 I'm always honest
🆓 I'm completely FREE!

Ready to explore crypto together?
Tap a button below or use the commands!

Stay cute, trade smart! {YUMY_EMOJIS['love']}
"""
    await update.message.reply_text(
        message,
        reply_markup=get_start_keyboard(),
        parse_mode='Markdown'
    )

# 💰 /price
async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fetching_msg = get_random_phrase("fetching")
    msg = await update.message.reply_text(f"{fetching_msg}\n\n_Fetching live price..._", parse_mode='Markdown')

    data = price_service.get_btc_price()

    if not data:
        error_msg = get_random_phrase("error")
        await msg.edit_text(
            f"{error_msg}\n\n_Sorry, couldn't fetch the price. Try again in a moment!_",
            reply_markup=get_back_keyboard(),
            parse_mode='Markdown'
        )
        return

    change = data['change_24h']
    mood = PriceService.get_market_mood(change)

    if change > 0:
        change_emoji = "🟢📈"
        change_sign = "+"
    else:
        change_emoji = "🔴📉"
        change_sign = ""

    message = f"""
{YUMY_EMOJIS['price']} Bitcoin Price

${data['price']:,.0f} USD
{change_emoji} {change_sign}{change:.2f}% (24h)

{mood}

📊 24 Hour Stats:
🔺 Highest: ${data['high_24h']:,.0f}
🔻 Lowest: ${data['low_24h']:,.0f}
📦 Volume: {data['volume_24h']:,.0f} BTC

🕐 Updated: {data['timestamp'].strftime('%H:%M UTC')}

{YUMY_EMOJIS['love']} CryptYumy - Your cute crypto friend!
"""
    await msg.edit_text(
        message,
        reply_markup=get_back_keyboard(),
        parse_mode='Markdown'
    )

# 📊 /chart
async def chart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = f"""
{YUMY_EMOJIS['chart']} Choose Your Chart!

I'll draw a pretty chart just for you!
Pick a time period below:

⚡ 24 Hours - See today's action
📅 5 Days - Check the week
🗓️ 1 Month - Monthly view

My tiny wings will draw it beautifully! {YUMY_EMOJIS['love']}
"""
    await update.message.reply_text(
        message,
        reply_markup=get_chart_keyboard(),
        parse_mode='Markdown'
    )

# 🐣 /stats
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = f"""
{YUMY_EMOJIS['star']} Your CryptYumy Adventure!

🐣 Yumy's Friend Stats:

📊 Charts viewed: {random.randint(5, 50)}
💰 Prices checked: {random.randint(10, 100)}
🔥 Days together: {random.randint(1, 30)}
💛 Friendship level: Growing strong!

Every day with you makes my chicken heart happier! {YUMY_EMOJIS['love']}

🏆 Coming Soon:
✨ XP System
🎯 Daily Quests
🏅 Achievements
👑 Leaderboard

Stay tuned for more fun! {YUMY_EMOJIS['magic']}
"""
    await update.message.reply_text(
        message,
        reply_markup=get_back_keyboard(),
        parse_mode='Markdown'
    )

# 🔘 هندلر دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # 🎯 منوی اصلی
    if query.data == "start":
        greeting = get_random_phrase("greeting")
        message = f"""
{greeting}

Welcome back to CryptYumy!

What would you like to do today?

💰 Check live Bitcoin price
📊 View beautiful charts
🐣 See your stats

Choose an option below! {YUMY_EMOJIS['wink']}
"""
        # 🎯 فیکس: اگه عکسه، پیام جدید بفرست
        if query.message.photo:
            await query.message.reply_text(
                message,
                reply_markup=get_start_keyboard(),
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(
                message,
                reply_markup=get_start_keyboard(),
                parse_mode='Markdown'
            )

    # 💰 قیمت
    elif query.data == "price":
        fetching_msg = get_random_phrase("fetching")

        # 🎯 فیکس: اگه عکسه، پیام جدید
        if query.message.photo:
            msg = await query.message.reply_text(
                f"{fetching_msg}\n\n_Fetching..._",
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(
                f"{fetching_msg}\n\n_Fetching..._",
                parse_mode='Markdown'
            )
            msg = query.message

        data = price_service.get_btc_price()

        if not data:
            error_msg = get_random_phrase("error")
            await msg.edit_text(
                f"{error_msg}\n\n_Sorry! Try again!_",
                reply_markup=get_back_keyboard(),
                parse_mode='Markdown'
            )
            return

        change = data['change_24h']
        mood = PriceService.get_market_mood(change)
        change_sign = "+" if change >= 0 else ""

        message = f"""
{YUMY_EMOJIS['price']} Bitcoin Price

${data['price']:,.0f} USD
{change_sign}{change:.2f}% (24h)

{mood}

📊 24h Stats:
🔺 High: ${data['high_24h']:,.0f}
🔻 Low: ${data['low_24h']:,.0f}

{YUMY_EMOJIS['love']} CryptYumy - Stay cute!
"""
        await msg.edit_text(
            message,
            reply_markup=get_back_keyboard(),
            parse_mode='Markdown'
        )

    # ℹ️ درباره
    elif query.data == "about":
        about_text = get_random_phrase("about")
        message = f"""
{YUMY_EMOJIS['baby']} About Yumy

{about_text}

Let's grow together! {YUMY_EMOJIS['love']}
"""
        if query.message.photo:
            await query.message.reply_text(
                message,
                reply_markup=get_back_keyboard(),
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(
                message,
                reply_markup=get_back_keyboard(),
                parse_mode='Markdown'
            )

    # 📊 آمار
    elif query.data == "stats":
        message = f"""
{YUMY_EMOJIS['star']} Your Adventure!

🐣 Friendship Stats:

📊 Charts: {random.randint(5, 50)}
💰 Prices: {random.randint(10, 100)}
🔥 Days: {random.randint(1, 30)}

You're my favorite human! {YUMY_EMOJIS['love']}
"""
        if query.message.photo:
            await query.message.reply_text(
                message,
                reply_markup=get_back_keyboard(),
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(
                message,
                reply_markup=get_back_keyboard(),
                parse_mode='Markdown'
            )

    # 📊 چارت‌ها
    elif query.data.startswith("chart_"):
        period = query.data.replace("chart_", "")
        period_names = {"1d": "24 Hours", "5d": "5 Days", "1mo": "1 Month"}
        period_name = period_names.get(period, period)

        fetching_msg = get_random_phrase("fetching")

        # 🎯 فیکس: اگه عکسه، پیام جدید بفرست
        if query.message.photo:
            msg = await query.message.reply_text(
                f"{fetching_msg}\n\n_Drawing {period_name} chart..._",
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(
                f"{fetching_msg}\n\n_Drawing {period_name} chart..._",
                parse_mode='Markdown'
            )
            msg = query.message

        chart_path = chart_service.generate_chart(period)

        if chart_path and os.path.exists(chart_path):
            chart_msg = get_random_phrase("chart_ready")

            # ارسال عکس با دکمه
            with open(chart_path, 'rb') as photo:
                await msg.reply_photo(
                    photo=photo,
                    caption=f"{chart_msg}\n\n📊 CryptYumy Chart - {period_name}\n\n_Tap a button for another chart!_ {YUMY_EMOJIS['love']}",
                    reply_markup=get_chart_keyboard(),
                    parse_mode='Markdown'
                )

            # پاک کردن پیام "در حال ساخت"
            await msg.delete()

            # پاک کردن فایل
            if os.path.exists(chart_path):
                os.remove(chart_path)
        else:
            error_msg = get_random_phrase("error")
            await msg.edit_text(
                f"{error_msg}\n\n_Try again!_",
                reply_markup=get_back_keyboard(),
                parse_mode='Markdown'
            )

# ⚠️ هندلر خطا
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")

    if update and update.message:
        await update.message.reply_text(
            f"{YUMY_EMOJIS['sad']} Oopsies!\n\n_Try again later!_ {YUMY_EMOJIS['love']}",
            reply_markup=get_back_keyboard(),
            parse_mode='Markdown'
        )
