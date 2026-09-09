# Handlers برای دستورات تلگرام
# Telegram Bot Handlers for THE LAST WALK

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import create_player, get_player, update_player, get_leaderboard
from game import game
from config import RESOURCES, MAP_CONFIG
import logging

router = Router()
logger = logging.getLogger(__name__)

# ============ States ============

class GameStates(StatesGroup):
    in_game = State()
    in_battle = State()
    in_menu = State()

# ============ دستورات شروع ============

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """شروع بازی"""
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    player = get_player(user_id)
    
    if player:
        await message.answer(f"""
🎮 خوش آمدید به THE LAST WALK!

شما قبلاً بازی می‌کنید!
برای ادامه از دستورات زیر استفاده کنید:

/play - بازی کردن
/status - وضعیت بازی
/leaderboard - جدول امتیازات
/help - راهنما
        """)
    else:
        # بازیکن جدید
        create_player(user_id, username)
        await message.answer(f"""
🌍 THE LAST WALK - خوش آمدید!

دنیا نابود شده است...
بعد از یک فاجعه ناشناخته، شما یکی از بازمانده‌هایید.

🎯 هدف شما: زنده ماندن، جستجو، مبارزه و ارتقای پناهگاه!

حالا بازی رو شروع کن!
        """)
        await message.answer("/play برای شروع بازی")
    
    await state.set_state(GameStates.in_menu)

# ============ منوی اصلی ============

@router.message(Command("play"))
async def cmd_play(message: Message, state: FSMContext):
    """منوی بازی"""
    user_id = message.from_user.id
    player = get_player(user_id)
    
    if not player:
        await message.answer("❌ ابتدا /start را بزنید")
        return
    
    menu = """
🎮 منوی بازی:

/move_up - حرکت به بالا
/move_down - حرکت به پایین
/move_left - حرکت به چپ
/move_right - حرکت به راست

/search - جستجو در منطقه
/battle - مبارزه با زامبی
/status - نمایش وضعیت
/eat - خوردن غذا
/drink - نوشیدن آب
/heal - استفاده از دارو
/upgrade_shelter - ارتقای پناهگاه
/next_day - رفتن به روز بعد

/leaderboard - جدول امتیازات
/help - راهنما کامل
    """
    await message.answer(menu)
    await state.set_state(GameStates.in_game)

# ============ حرکت ============

@router.message(Command("move_up"))
async def cmd_move_up(message: Message):
    result = game.move(message.from_user.id, "up")
    await message.answer(result["message"])
    
    if result.get("zombie_encounter"):
        await message.answer("⚔️ یک زامبی پیدا شد! برای مبارزه /battle را بزن")

@router.message(Command("move_down"))
async def cmd_move_down(message: Message):
    result = game.move(message.from_user.id, "down")
    await message.answer(result["message"])
    
    if result.get("zombie_encounter"):
        await message.answer("⚔️ یک زامبی پیدا شد! برای مبارزه /battle را بزن")

@router.message(Command("move_left"))
async def cmd_move_left(message: Message):
    result = game.move(message.from_user.id, "left")
    await message.answer(result["message"])
    
    if result.get("zombie_encounter"):
        await message.answer("⚔️ یک زامبی پیدا شد! برای مبارزه /battle را بزن")

@router.message(Command("move_right"))
async def cmd_move_right(message: Message):
    result = game.move(message.from_user.id, "right")
    await message.answer(result["message"])
    
    if result.get("zombie_encounter"):
        await message.answer("⚔️ یک زامبی پیدا شد! برای مبارزه /battle را بزن")

# ============ اقدامات ============

@router.message(Command("search"))
async def cmd_search(message: Message):
    """جستجو"""
    result = game.search_area(message.from_user.id)
    await message.answer(result["message"])

@router.message(Command("battle"))
async def cmd_battle(message: Message):
    """مبارزه"""
    result = game.battle_zombie(message.from_user.id)
    
    if result["success"]:
        msg = f"""
{result['message']}
⭐ +{result['xp_gain']} تجربه
🎯 +{result['score_gain']} امتیاز
🔫 کشته‌های کل: {result['kills']}
        """
    else:
        msg = result["message"]
        if "damage" in result:
            msg += f"\n❤️ سلامتی باقی‌مانده: "
            player = get_player(message.from_user.id)
            msg += f"{player.health}/{100}"
    
    await message.answer(msg)

@router.message(Command("eat"))
async def cmd_eat(message: Message):
    """خوردن"""
    player = get_player(message.from_user.id)
    
    if player.inventory.get("food", 0) < 1:
        await message.answer("❌ غذای کافی ندارید!")
        return
    
    game.consume_resource(message.from_user.id, "food", 1)
    player = get_player(message.from_user.id)
    player.hunger = min(100, player.hunger + 30)
    update_player(message.from_user.id, hunger=player.hunger)
    
    await message.answer(f"🍖 خوردید!\n گرسنگی: {player.hunger}/100")

@router.message(Command("drink"))
async def cmd_drink(message: Message):
    """نوشیدن"""
    player = get_player(message.from_user.id)
    
    if player.inventory.get("water", 0) < 1:
        await message.answer("❌ آب کافی ندارید!")
        return
    
    game.consume_resource(message.from_user.id, "water", 1)
    player = get_player(message.from_user.id)
    player.thirst = min(100, player.thirst + 30)
    update_player(message.from_user.id, thirst=player.thirst)
    
    await message.answer(f"💧 آب خوردید!\n تشنگی: {player.thirst}/100")

@router.message(Command("heal"))
async def cmd_heal(message: Message):
    """شفا"""
    player = get_player(message.from_user.id)
    
    if player.inventory.get("medicine", 0) < 1:
        await message.answer("❌ دارو کافی ندارید!")
        return
    
    game.consume_resource(message.from_user.id, "medicine", 1)
    game.heal_player(message.from_user.id, 40)
    player = get_player(message.from_user.id)
    
    await message.answer(f"💊 درمان شدید!\n سلامتی: {player.health}/{100}")

@router.message(Command("upgrade_shelter"))
async def cmd_upgrade_shelter(message: Message):
    """ارتقای پناهگاه"""
    result = game.upgrade_shelter(message.from_user.id)
    await message.answer(result["message"])

@router.message(Command("next_day"))
async def cmd_next_day(message: Message):
    """روز بعد"""
    result = game.next_day(message.from_user.id)
    
    if not result["success"]:
        await message.answer(f"{result['message']}\n\n📅 روزهای زنده‌ماندن: {result['days_survived']}")
    else:
        await message.answer(f"""
{result['message']}
🍖 گرسنگی: {result['hunger']}/100
💧 تشنگی: {result['thirst']}/100
        """)

# ============ اطلاعات ============

@router.message(Command("status"))
async def cmd_status(message: Message):
    """وضعیت"""
    player = get_player(message.from_user.id)
    
    if not player:
        await message.answer("❌ بازیکن پیدا نشد")
        return
    
    status = game.get_player_status(message.from_user.id)
    await message.answer(status)

@router.message(Command("leaderboard"))
async def cmd_leaderboard(message: Message):
    """جدول امتیازات"""
    leaderboard = get_leaderboard(10)
    
    msg = "🏆 جدول امتیازات جهانی\n━━━━━━━━━━━━━━━━━\n"
    
    if not leaderboard:
        msg += "هنوز کسی در لیدربرد نیست"
    else:
        for i, entry in enumerate(leaderboard, 1):
            msg += f"\n{i}. {entry.username}\n"
            msg += f"   🎯 امتیاز: {entry.score}\n"
            msg += f"   ⭐ Level: {entry.level}\n"
            msg += f"   📅 روز: {entry.survived_days}\n"
            msg += f"   🔫 کشته: {entry.kills}\n"
    
    await message.answer(msg)

@router.message(Command("help"))
async def cmd_help(message: Message):
    """راهنما"""
    help_text = """
📖 راهنمای THE LAST WALK

🎯 هدف:
زنده ماندن در دنیای آخرالزمانی!

🎮 سیستم‌های بازی:

1️⃣ حرکت:
   - /move_up, /move_down, /move_left, /move_right

2️⃣ جستجو:
   - /search - در منطقه فعلی جستجو کن

3️⃣ مبارزه:
   - /battle - با زامبی مبارزه کن

4️⃣ مدیریت منابع:
   - /eat - غذا بخور
   - /drink - آب بنوش
   - /heal - از دارو استفاده کن

5️⃣ پناهگاه:
   - /upgrade_shelter - پناهگاه رو بهتر کن

6️⃣ اطلاعات:
   - /status - وضعیت کاملت رو ببین
   - /leaderboard - بهترین‌ها رو ببین

💡 نکات:
- هر روز منابع کمتر می‌شه
- شب‌ها خطرناک‌تره
- Level Up می‌دی ستاره بگیری
- امتیاز برای هر کشت زامبی می‌گیری

🚀 شروع کن: /play
    """
    await message.answer(help_text)
