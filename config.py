# تنظیمات بازی THE LAST WALK
# Configuration for THE LAST WALK Game

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///game.db")

# Game Settings
GAME_CONFIG = {
    "max_health": 100,
    "max_hunger": 100,
    "max_thirst": 100,
    "max_inventory_slots": 20,
    "day_length": 300,  # ثانیه (برای تست، در واقع می‌تونه 3600 باشه)
    "night_length": 150,  # شب خطرناک‌تره
    "zombie_spawn_rate_day": 0.3,
    "zombie_spawn_rate_night": 0.8,
}

# Resources
RESOURCES = {
    "food": {"name": "غذا", "icon": "🍖"},
    "water": {"name": "آب", "icon": "💧"},
    "medicine": {"name": "دارو", "icon": "💊"},
    "ammo": {"name": "مهمات", "icon": "🔫"},
    "wood": {"name": "چوب", "icon": "🪵"},
    "metal": {"name": "فلز", "icon": "⚙️"},
}

# Map Tiles
MAP_CONFIG = {
    "width": 10,
    "height": 10,
    "tiles": {
        "safe": {"name": "محل ایمن", "icon": "🏠", "danger": 0},
        "forest": {"name": "جنگل", "icon": "🌲", "danger": 2},
        "city": {"name": "شهر", "icon": "🏚️", "danger": 4},
        "hospital": {"name": "بیمارستان", "icon": "🏥", "danger": 3},
        "store": {"name": "فروشگاه", "icon": "🏪", "danger": 3},
        "wasteland": {"name": "خرابه", "icon": "💀", "danger": 5},
    }
}

# NPCs
NPCS = {
    "trader": {"name": "بازرگان", "icon": "👨‍💼"},
    "doctor": {"name": "پزشک", "icon": "👨‍⚕️"},
    "scout": {"name": "پیشاهنگ", "icon": "🧭"},
    "elder": {"name": "بزرگسال", "icon": "👴"},
}
