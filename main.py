# برنامه اصلی بات تلگرام
# Main Bot Application for THE LAST WALK

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import BOT_TOKEN
from database import init_db
from handlers import router

# تنظیمات Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============ تابع اصلی ============

async def set_commands(bot: Bot):
    """تنظیم دستورات بات"""
    commands = [
        BotCommand(command="start", description="شروع بازی"),
        BotCommand(command="play", description="منوی بازی"),
        BotCommand(command="status", description="وضعیت فعلی"),
        BotCommand(command="move_up", description="حرکت به بالا"),
        BotCommand(command="move_down", description="حرکت به پایین"),
        BotCommand(command="move_left", description="حرکت به چپ"),
        BotCommand(command="move_right", description="حرکت به راست"),
        BotCommand(command="search", description="جستجو در منطقه"),
        BotCommand(command="battle", description="مبارزه با زامبی"),
        BotCommand(command="eat", description="خوردن غذا"),
        BotCommand(command="drink", description="نوشیدن آب"),
        BotCommand(command="heal", description="استفاده از دارو"),
        BotCommand(command="upgrade_shelter", description="ارتقای پناهگاه"),
        BotCommand(command="next_day", description="رفتن به روز بعد"),
        BotCommand(command="leaderboard", description="جدول امتیازات"),
        BotCommand(command="help", description="راهنمای کامل"),
    ]
    await bot.set_my_commands(commands)

async def main():
    """تابع اصلی"""
    # مقدماتی‌سازی دیتابیس
    init_db()
    logger.info("✅ پایگاه داده مقدماتی شد")
    
    # ایجاد Bot و Dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # اضافه کردن router
    dp.include_router(router)
    
    # تنظیم دستورات
    await set_commands(bot)
    logger.info("✅ دستورات تنظیم شد")
    
    # شروع Polling
    logger.info("🚀 بات شروع شد!")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
