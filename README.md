# 🧟 THE LAST WALK - بازی بقا در دنیای آخرالزمانی

![Game Banner](https://img.shields.io/badge/THE%20LAST%20WALK-Survival%20Game-red)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 درباره بازی

**THE LAST WALK** یک بازی بقا متنی است که در تلگرام بازی می‌شود. شما باید در دنیای نابود شده زنده بمانید، منابع جمع کنید، با زامبی‌ها مبارزه کنید و پناهگاه خود را ارتقا دهید!

## 🎮 ویژگی‌های بازی

- 🗺️ **نقشه جهان**: 10×10 موقعیت برای اکتشاف
- 🧟 **مبارزه**: مبارزه با زامبی‌ها و کسب تجربه
- 📦 **منابع**: غذا، آب، دارو، مهمات، چوب، فلز
- 🏠 **پناهگاه**: ارتقای پناهگاه برای بهتر شدن دفاع
- ⭐ **سیستم Level**: تا Level 100
- 🏆 **جدول امتیازات**: رقابت با بازیکنان دیگر
- 📅 **روز و شب**: شب‌ها خطرناک‌تر!
- 💪 **منابع اندام**: سلامتی، گرسنگی، تشنگی

## 🚀 شروع سریع

### الف) نیازمندی‌ها

```bash
Python 3.8+
pip (مدیر بسته Python)
```

### ب) نصب محلی

1. **Repository رو Clone کن:**
```bash
git clone https://github.com/Sjqqj/the-last-walk.git
cd the-last-walk
```

2. **محیط مجازی ایجاد کن:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Dependencies نصب کن:**
```bash
pip install -r requirements.txt
```

4. **فایل `.env` ایجاد کن:**
```bash
cp .env.example .env
```

5. **Token بات رو اضافه کن:**

   - به [@BotFather](https://t.me/BotFather) در تلگرام برو
   - دستور `/start` بزن
   - دستور `/newbot` بزن
   - نام و نام‌کاربری بات رو وارد کن
   - Token رو کپی کن
   - توی فایل `.env` جای `your_token_here` رو جایگزین کن:

   ```
   BOT_TOKEN=your_actual_token_here
   DATABASE_URL=sqlite:///game.db
   ```

6. **بات رو شروع کن:**
```bash
python main.py
```

## 🌐 Hosting رایگان (Render.com)

### مراحل:

1. **Repository رو به GitHub Push کن:**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **به [render.com](https://render.com) برو و ثبت‌نام کن**

3. **New Web Service ایجاد کن:**
   - GitHub repository رو انتخاب کن
   - Name: `the-last-walk`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

4. **Environment Variables اضافه کن:**
   - KEY: `BOT_TOKEN`
   - VALUE: (token بات تو)

5. **Deploy کن!** ✅

> **نکته**: Render رایگان هر ۱۵ دقیقه بیکار بودن رو متوقف می‌کند. برای Always-On:
> - Uptime Robot استفاده کن یا
> - پلن Paid رو انتخاب کن

## 📱 نحوه بازی

### شروع:
```
/start - شروع بازی
/play - منوی بازی
```

### حرکت:
```
/move_up - حرکت به بالا ⬆️
/move_down - حرکت به پایین ⬇️
/move_left - حرکت به چپ ⬅️
/move_right - حرکت به راست ➡️
```

### جستجو و مبارزه:
```
/search - جستجو در منطقه فعلی 🔍
/battle - مبارزه با زامبی ⚔️
```

### مدیریت منابع:
```
/eat - خوردن غذا 🍖
/drink - نوشیدن آب 💧
/heal - استفاده از دارو 💊
```

### پناهگاه و پیشرفت:
```
/upgrade_shelter - ارتقای پناهگاه 🏗️
/next_day - رفتن به روز بعد 📅
```

### اطلاعات:
```
/status - نمایش وضعیت کامل 📊
/leaderboard - جدول امتیازات 🏆
/help - راهنمای کامل 📖
```

## 🎯 استراتژی پیروزی

1. **جستجو**: در شروع بازی، منابع جمع‌آوری کن
2. **ارتقای پناهگاه**: یک پناهگاه قوی بساز
3. **مبارزه**: زامبی‌ها را کشته و تجربه بگیر
4. **Level Up**: هرچقدر Level بالاتر، احتمال برد بیشتر
5. **جدول امتیازات**: بهترین باشی! 🏆

## 📊 سیستم‌های بازی

### منابع:
| منبع | نماد | استفاده |
|------|------|--------|
| غذا | 🍖 | کاهش گرسنگی |
| آب | 💧 | کاهش تشنگی |
| دارو | 💊 | افزایش سلامتی |
| مهمات | 🔫 | برای مبارزه |
| چوب | 🪵 | ارتقای پناهگاه |
| فلز | ⚙️ | ارتقای پناهگاه |

### سطح Level:
- هر **100 XP** = 1 Level
- هر Level Up: سلامتی تکمیل می‌شود
- دقت در مبارزه: 70% + (Level × 2%)

### منطقه‌ها:
- 🏠 محل ایمن - خطر: ۰
- 🌲 جنگل - خطر: ۲
- 🏚️ شهر - خطر: ۳
- 🏥 بیمارستان - خطر: ۳
- 🏪 فروشگاه - خطر: ۳
- 💀 خرابه - خطر: ۵

## 🛠️ فناوری‌های استفاده‌شده

- **aiogram** - کتابخانه Telegram Bot
- **SQLAlchemy** - ORM برای دیتابیس
- **SQLite/PostgreSQL** - پایگاه داده
- **Python asyncio** - برنامه‌نویسی ناهمزمان

## 📁 ساختار پروژه

```
the-last-walk/
├── main.py           # برنامه اصلی
├── config.py         # تنظیمات بازی
├── database.py       # مدل‌های دیتابیس
├── game.py           # منطق بازی
├── handlers.py       # دستورات تلگرام
├── requirements.txt  # وابستگی‌ها
├── .env.example      # نمونه متغیرهای محیط
├── .gitignore        # فایل‌های نادیده‌گرفتنی
├── Procfile          # برای Hosting
└── README.md         # این فایل
```

## 🐛 رفع مشکلات

### مشکل: "BOT_TOKEN is None"
**حل:** فایل `.env` رو چک کن و Token رو صحیح‌تر وارد کن

### مشکل: "Database locked"
**حل:** SQLite می‌تونه مشکل‌های Concurrent داشته باشه - PostgreSQL استفاده کن

### مشکل: Buat timeout شد
**حل:** روی Render، Worker Dynos رو استفاده کن (نه Web Dynos)

## 🤝 مشارکت

Pull Request‌ها خوش‌آمد!

## 📝 لایسنس

MIT License - برای جزئیات [LICENSE](LICENSE) رو ببین

## 👤 نویسنده

- **GitHub**: [@Sjqqj](https://github.com/Sjqqj)

## 💬 پشتیبانی

مشکل پیدا کردی؟
- Issue ایجاد کن: [GitHub Issues](https://github.com/Sjqqj/the-last-walk/issues)
- Email: hashemiandanial74@gmail.com

---

**هیچ دنیا نابود نشده است، تنها انسان‌ها هستند که نسیان می‌روند** 🌍

🚀 **حالا شروع کن و زنده بمان!**
