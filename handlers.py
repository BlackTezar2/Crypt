from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from price_service import PriceService
from chart_service import ChartService
from config import YUMY_EMOJIS
import os
import random

price_service = PriceService()
chart_service = ChartService()

# ... (YUMY_PHRASES و get_random_phrase مثل قبل)
YUMY_PHRASES = {
    "greeting": [
        "Cheep cheep! I'm so happy to see you! {}",
        "Oh! A human friend! Hello hello! {}",
        "Yay! Someone woke me up! {}",
        "Peep peep! I was just dreaming about Bitcoin! {}",
        "Welcome welcome! My little chicken heart is excited! {}",
    ],
    "fetching": [
        "Let me check my magic crystal ball... {}",
        "Asking the Bitcoin gods... {}",
        "Running to check the charts! Wait here! {}",
        "My chicken brain is calculating... {}",
        "Peeking at the market for you... {}",
    ],
    "chart_ready": [
        "Ta-da! Here's your beautiful chart! {}",
        "I drew this with my tiny wings! {}",
        "A masterpiece from your favorite chick! {}",
        "Chart fresh from the nest! {}",
        "Look at those golden lines! So pretty! {}",
    ],
    "error": [
        "Oopsies! My chicken brain froze! {}",
        "Oh no! The internet worms are slow today! {}",
        "Peep... something went wrong... {}",
        "I'm just a baby chick! Don't be mad! {}",
        "The market is so crazy, even I got confused! {}",
    ],
    "stats": [
        "Look how much we've grown together! {}",
        "Your adventure with me so far! {}",
        "We make a great team, human! {}",
    ],
    "about": [
        "I'm Yumy, a baby chick who loves Bitcoin! I was born to make crypto fun and cute! No scary charts, no complicated words. Just a friendly chick helping you understand the crypto world! I might not always be right, but I'll always be honest and adorable! {}",
    ]
}

def get_random_phrase(category):
    phrases = YUMY_PHRASES.get(category, ["Cheep! {}"])
    return random.choice(phrases).format(random.choice(["🐣", "💛", "✨", "🍯", "🐤"]))

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

# 🔘 هندلر دکمه‌ها - فیکس شده!
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "start":
        greeting = get_random_phrase("greeting")
        message = f"""
{greeting}

Welcome back to CryptYumy!

What would you like to do today?

💰 Check live Bitcoin price
📊 View beautiful char

ts
🐣 See your stats

Choose an option below! {YUMY_EMOJIS['wink']}
"""
        await query.edit_message_text(
            message,
            reply_markup=get_start_keyboard(),
            parse_mode='Markdown'
        )

    elif query.data == "price":
        fetching_msg = get_random_phrase("fetching")
        await query.edit_message_text(
            f"{fetching_msg}\n\n_Fetching the latest price..._",
            parse_mode='Markdown'
        )

        data = price_service.get_btc_price()

        if not data:
            error_msg = get_random_phrase("error")
            await query.edit_message_text(
                f"{error_msg}\n\n_Sorry! Try again in a bit!_",
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

{YUMY_EMOJIS['love']} CryptYumy - Stay cute, trade smart!
"""
        await query.edit_message_text(
            message,
            reply_markup=get_back_keyboard(),
            parse_mode='Markdown'
        )

    elif query.data == "about":
        about_text = get_random_phrase("about")
        message = f"""
{YUMY_EMOJIS['baby']} About Yumy

{about_text}

My Promise to You:
✨ I'll always be honest
📊 I'll make pretty charts
💛 I'll keep learning
🆓 I'll stay FREE forever!

Coming Soon:
🧠 AI Predictions
🎙️ Voice Messages
🏆 XP & Achievements
👥 Friend System

Let's grow together! {YUMY_EMOJIS['love']}
"""
        await query.edit_message_text(
            message,
            reply_markup=get_back_keyboard(),
            parse_mode='Markdown'
        )

    elif query.data == "stats":
        message = f"""
{YUMY_EMOJIS['star']} Your Adventure!

🐣 Friendship Stats:

📊 Charts: {random.randint(5, 50)}
💰 Prices: {random.randint(10, 100)}
🔥 Days: {random.randint(1, 30)}
💛 Bond: Growing!

{YUMY_EMOJIS['magic']} Coming Soon:
✨ XP System
🎯 Daily Quests
🏅 Achievements

You're my favorite human! {YUMY_EMOJIS['love']}
"""
        await query.edit_message_text(
            message,
            reply_markup=get_back_keyboard(),
            parse_mode='Markdown'
        )

    elif query.data.startswith("chart_"):
        period = query.data.replace("chart_", "")
        period_names = {"1d": "24 Hours", "5d": "5 Days", "1mo": "1 Month"}
        period_name = period_names.get(period, period)

        fetching_msg = get_random_phrase("fetching")
        await query.edit_message_text(
            f"{fetching_msg}\n\n_Drawing your {period_name} chart..._",
            parse_mode='Markdown'
        )

        chart_path = chart_service.generate_chart(period)

        if chart_path and os.path.exists(chart_path):
            chart_msg = get_random_phrase("chart_ready")

            # 🎯 فیکس: ارسال عکس با دکمه‌های اینلاین روی caption
            with open(chart_path, 'rb') as photo:
                await query.message.reply_photo(
                    photo=photo,
                    caption=f"{chart_msg}\n\n📊 CryptYumy Chart - {period_name}\n\n_Hand-drawn with love by your favorite chick!_ {YUMY_EMOJIS['love']}",
                    reply_markup=get_chart_keyboard(),  # ✅ دکمه‌ها روی عکس!
                    parse_mode='Markdown'
                )

            # پاک کردن پیام "در حال ساخت..."
            await query.delete_message()

            # پاک کردن فایل
            if os.path.exists(chart_path):
                os.remove(chart_path)
        else:
            error_msg = get_random_phrase("error")
            await query.edit_message_text(
                f"{error_msg}\n\n_My wings got tired drawing! Try again!_",
                reply_markup=get_back_keyboard(),
                parse_mode='Markdown'
            )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")

    error_message = f"""
{YUMY_EMOJIS['sad']} Oopsies!

My little chicken brain encountered an error!
But don't worry, I'll be okay!

Try again or come back later! {YUMY_EMOJIS['love']}
"""
    if update and update.message:
        await update.message.reply_text(
            error_message,
            reply_markup=get_back_keyboard(),
            parse_mode='Markdown'
        )
