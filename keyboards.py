from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_start_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("💰 Live Price", callback_data="price"),
            InlineKeyboardButton("📊 24H Chart", callback_data="chart_1d"),
        ],
        [
            InlineKeyboardButton("📈 5D Chart", callback_data="chart_5d"),
            InlineKeyboardButton("🗓️ 1M Chart", callback_data="chart_1mo"),
        ],
        [
            InlineKeyboardButton("🐣 My Stats", callback_data="stats"),
            InlineKeyboardButton("ℹ️ About Yumy", callback_data="about"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_chart_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("⚡ 24 Hours", callback_data="chart_1d"),
            InlineKeyboardButton("📅 5 Days", callback_data="chart_5d"),
        ],
        [
            InlineKeyboardButton("🗓️ 1 Month", callback_data="chart_1mo"),
        ],
        [
            InlineKeyboardButton("🏠 Back to Menu", callback_data="start"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    keyboard = [
        [InlineKeyboardButton("🏠 Back to Menu", callback_data="start")]
    ]
    return InlineKeyboardMarkup(keyboard)
