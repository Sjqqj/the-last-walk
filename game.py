# منطق بازی THE LAST WALK
# Game logic for THE LAST WALK

import random
from datetime import datetime, timedelta
from config import GAME_CONFIG, RESOURCES, MAP_CONFIG, NPCS
from database import get_player, update_player, update_leaderboard, get_db, Player

class GameLogic:
    """منطق بازی"""
    
    def __init__(self):
        self.config = GAME_CONFIG
        self.resources = RESOURCES
        self.map_config = MAP_CONFIG
    
    # ============ مدیریت سلامتی و وضعیت ============
    
    def damage_player(self, user_id: int, damage: int):
        """آسیب به بازیکن"""
        player = get_player(user_id)
        if player:
            player.health = max(0, player.health - damage)
            if player.health == 0:
                player.is_alive = False
            update_player(user_id, health=player.health, is_alive=player.is_alive)
            return player.health
        return 0
    
    def heal_player(self, user_id: int, heal: int):
        """شفا دادن به بازیکن"""
        player = get_player(user_id)
        if player:
            player.health = min(self.config["max_health"], player.health + heal)
            update_player(user_id, health=player.health)
            return player.health
        return 0
    
    def consume_resource(self, user_id: int, resource: str, amount: int) -> bool:
        """مصرف منبع"""
        player = get_player(user_id)
        if player and resource in player.inventory:
            if player.inventory[resource] >= amount:
                player.inventory[resource] -= amount
                update_player(user_id, inventory=player.inventory)
                return True
        return False
    
    def add_resource(self, user_id: int, resource: str, amount: int):
        """اضافه کردن منبع"""
        player = get_player(user_id)
        if player and resource in player.inventory:
            player.inventory[resource] += amount
            update_player(user_id, inventory=player.inventory)
    
    # ============ مبارزه با زامبی ============
    
    def battle_zombie(self, user_id: int) -> dict:
        """مبارزه با زامبی"""
        player = get_player(user_id)
        if not player:
            return {"success": False, "message": "بازیکن پیدا نشد"}
        
        # بررسی مهمات
        if player.inventory.get("ammo", 0) < 1:
            return {"success": False, "message": "مهمات ندارید! 🔫"}
        
        # احتمال برد
        accuracy = 0.7 + (player.level * 0.02)
        if random.random() < accuracy:
            # برد
            self.consume_resource(user_id, "ammo", 1)
            xp_gain = 10 + (player.level * 2)
            self.add_xp(user_id, xp_gain)
            
            # امتیاز
            score_gain = 50
            player = get_player(user_id)
            update_player(user_id, 
                         score=player.score + score_gain,
                         kills=player.kills + 1)
            
            return {
                "success": True,
                "message": "🎯 زامبی کشته شد!",
                "xp_gain": xp_gain,
                "score_gain": score_gain,
                "kills": player.kills + 1
            }
        else:
            # باخت
            self.consume_resource(user_id, "ammo", 1)
            damage = random.randint(10, 30)
            self.damage_player(user_id, damage)
            
            return {
                "success": False,
                "message": f"😱 زامبی حمله کرد! {damage} آسیب دریافت کردید",
                "damage": damage
            }
    
    # ============ سیستم XP و Level ============
    
    def add_xp(self, user_id: int, amount: int):
        """افزودن تجربه"""
        player = get_player(user_id)
        if player:
            player.experience += amount
            
            # بررسی Level Up
            xp_needed = player.level * 100
            if player.experience >= xp_needed:
                player.level += 1
                player.experience = 0
                player.health = self.config["max_health"]
                update_player(user_id,
                            experience=player.experience,
                            level=player.level,
                            health=player.health)
                return True, player.level
            else:
                update_player(user_id, experience=player.experience)
                return False, player.level
        return False, 0
    
    # ============ مدیریت منطقه ============
    
    def move(self, user_id: int, direction: str) -> dict:
        """حرکت به منطقه دیگر"""
        player = get_player(user_id)
        if not player:
            return {"success": False, "message": "بازیکن پیدا نشد"}
        
        # جهت‌های حرکت
        directions = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        
        if direction not in directions:
            return {"success": False, "message": "جهت نامعتبر"}
        
        dx, dy = directions[direction]
        new_x = player.location_x + dx
        new_y = player.location_y + dy
        
        # بررسی مرزهای نقشه
        if (new_x < 0 or new_x >= self.map_config["width"] or
            new_y < 0 or new_y >= self.map_config["height"]):
            return {"success": False, "message": "نمی‌تونید از حدود نقشه خارج بشید"}
        
        update_player(user_id, location_x=new_x, location_y=new_y)
        
        # خطر منطقه
        danger = random.randint(1, 5)
        if danger >= 3:
            # زامبی!
            return {
                "success": True,
                "message": "⚠️ زامبی دیده شد!",
                "location": (new_x, new_y),
                "zombie_encounter": True
            }
        
        return {
            "success": True,
            "message": f"✅ به موقعیت ({new_x}, {new_y}) رفتید",
            "location": (new_x, new_y),
            "zombie_encounter": False
        }
    
    # ============ جستجو در منطقه ============
    
    def search_area(self, user_id: int) -> dict:
        """جستجو در منطقه فعلی"""
        player = get_player(user_id)
        if not player:
            return {"success": False, "message": "بازیکن پیدا نشد"}
        
        # منابع ممکن
        possible_resources = [
            ("food", random.randint(1, 5)),
            ("water", random.randint(1, 3)),
            ("medicine", random.randint(0, 2)),
            ("ammo", random.randint(2, 8)),
            ("wood", random.randint(0, 10)),
            ("metal", random.randint(0, 3)),
        ]
        
        # انتخاب تصادفی
        resource, amount = random.choice(possible_resources)
        self.add_resource(user_id, resource, amount)
        
        return {
            "success": True,
            "message": f"🔍 {amount} عدد {RESOURCES[resource]['name']} پیدا شد!",
            "resource": resource,
            "amount": amount
        }
    
    # ============ مدیریت پناهگاه ============
    
    def upgrade_shelter(self, user_id: int) -> dict:
        """ارتقای پناهگاه"""
        player = get_player(user_id)
        if not player:
            return {"success": False, "message": "بازیکن پیدا نشد"}
        
        # هزینه ارتقا
        wood_cost = player.shelter_level * 20
        metal_cost = player.shelter_level * 10
        
        if (player.inventory.get("wood", 0) < wood_cost or
            player.inventory.get("metal", 0) < metal_cost):
            return {
                "success": False,
                "message": f"منابع کافی ندارید! نیاز: {wood_cost} چوب، {metal_cost} فلز"
            }
        
        self.consume_resource(user_id, "wood", wood_cost)
        self.consume_resource(user_id, "metal", metal_cost)
        
        new_level = player.shelter_level + 1
        update_player(user_id, shelter_level=new_level)
        
        return {
            "success": True,
            "message": f"🏗️ پناهگاه به سطح {new_level} ارتقا یافت!",
            "new_level": new_level
        }
    
    # ============ مدیریت روز و شب ============
    
    def next_day(self, user_id: int) -> dict:
        """رفتن به روز بعد"""
        player = get_player(user_id)
        if not player:
            return {"success": False, "message": "بازیکن پیدا نشد"}
        
        # کاهش منابع (گرسنگی و تشنگی)
        hunger_loss = 15
        thirst_loss = 10
        
        player.hunger = max(0, player.hunger - hunger_loss)
        player.thirst = max(0, player.thirst - thirst_loss)
        player.survived_days += 1
        
        # بررسی مرگ
        if player.hunger <= 0 or player.thirst <= 0:
            player.is_alive = False
            update_player(user_id,
                         hunger=player.hunger,
                         thirst=player.thirst,
                         survived_days=player.survived_days,
                         is_alive=False)
            return {
                "success": False,
                "message": "💀 شما تلف شدید! گرسنگی یا تشنگی سبب مرگتان شد",
                "days_survived": player.survived_days
            }
        
        update_player(user_id,
                     hunger=player.hunger,
                     thirst=player.thirst,
                     survived_days=player.survived_days)
        
        # بروزرسانی لیدربرد
        update_leaderboard(user_id, player.username, player.score,
                         player.level, player.survived_days, player.kills)
        
        return {
            "success": True,
            "message": f"📅 روز {player.survived_days} شروع شد!",
            "day": player.survived_days,
            "hunger": player.hunger,
            "thirst": player.thirst
        }
    
    # ============ اطلاعات بازیکن ============
    
    def get_player_status(self, user_id: int) -> str:
        """دریافت وضعیت بازیکن"""
        player = get_player(user_id)
        if not player:
            return "بازیکن پیدا نشد"
        
        status = f"""
📊 وضعیت بازی
━━━━━━━━━━━━━━━━━
👤 بازیکن: {player.username}
💪 سلامتی: {player.health}/{self.config['max_health']}
🍖 گرسنگی: {player.hunger}/100
💧 تشنگی: {player.thirst}/100
⭐ Level: {player.level}
🎯 امتیاز: {player.score}
📈 تجربه: {player.experience}
🔫 کشته‌های زامبی: {player.kills}
📅 روزهای زنده‌ماندن: {player.survived_days}
🏠 سطح پناهگاه: {player.shelter_level}
📍 موقعیت: ({player.location_x}, {player.location_y})

📦 Inventory:
"""
        for resource, amount in player.inventory.items():
            status += f"  {RESOURCES[resource]['icon']} {RESOURCES[resource]['name']}: {amount}\n"
        
        return status

# Instance
game = GameLogic()
