# پایگاه داده بازی THE LAST WALK
# Database setup for THE LAST WALK Game

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==================== Models ====================

class Player(Base):
    """مدل بازیکن"""
    __tablename__ = "players"
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    health = Column(Integer, default=100)
    hunger = Column(Integer, default=50)
    thirst = Column(Integer, default=50)
    experience = Column(Integer, default=0)
    level = Column(Integer, default=1)
    score = Column(Integer, default=0)
    location_x = Column(Integer, default=5)
    location_y = Column(Integer, default=5)
    inventory = Column(JSON, default={})
    shelter_level = Column(Integer, default=1)
    survived_days = Column(Integer, default=0)
    kills = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_alive = Column(Boolean, default=True)
    
class GameSession(Base):
    """جلسه بازی"""
    __tablename__ = "game_sessions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    current_day = Column(Integer, default=1)
    is_day = Column(Boolean, default=True)
    session_start = Column(DateTime, default=datetime.utcnow)
    session_end = Column(DateTime, nullable=True)
    
class Leaderboard(Base):
    """جدول امتیازات"""
    __tablename__ = "leaderboard"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    score = Column(Integer)
    level = Column(Integer)
    survived_days = Column(Integer)
    kills = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class NPC(Base):
    """شخصیت‌های غیرقابل کنترل"""
    __tablename__ = "npcs"
    
    id = Column(Integer, primary_key=True)
    npc_type = Column(String)  # trader, doctor, scout, elder
    location_x = Column(Integer)
    location_y = Column(Integer)
    dialogue = Column(JSON, default={})
    available = Column(Boolean, default=True)

class Event(Base):
    """رویدادهای داستانی"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    event_type = Column(String)
    description = Column(String)
    choices = Column(JSON)  # گزینه‌های ممکن
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# ==================== Initialize Database ====================

def init_db():
    """ایجاد تمام جداول"""
    Base.metadata.create_all(bind=engine)
    print("✅ پایگاه داده مقدماتی شد!")

def get_db():
    """دریافت نشست دیتابیس"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# توابع کمکی برای Database

def create_player(user_id: int, username: str) -> Player:
    """ایجاد بازیکن جدید"""
    db = SessionLocal()
    try:
        player = Player(
            user_id=user_id,
            username=username,
            inventory={
                "food": 5,
                "water": 3,
                "medicine": 2,
                "ammo": 10,
                "wood": 0,
                "metal": 0
            }
        )
        db.add(player)
        db.commit()
        return player
    finally:
        db.close()

def get_player(user_id: int) -> Player:
    """دریافت بازیکن"""
    db = SessionLocal()
    try:
        return db.query(Player).filter(Player.user_id == user_id).first()
    finally:
        db.close()

def update_player(user_id: int, **kwargs):
    """بروزرسانی بازیکن"""
    db = SessionLocal()
    try:
        player = db.query(Player).filter(Player.user_id == user_id).first()
        if player:
            for key, value in kwargs.items():
                if hasattr(player, key):
                    setattr(player, key, value)
            db.commit()
    finally:
        db.close()

def get_leaderboard(limit: int = 10) -> list:
    """دریافت جدول امتیازات"""
    db = SessionLocal()
    try:
        return db.query(Leaderboard).order_by(Leaderboard.score.desc()).limit(limit).all()
    finally:
        db.close()

def update_leaderboard(user_id: int, username: str, score: int, level: int, survived_days: int, kills: int):
    """بروزرسانی جدول امتیازات"""
    db = SessionLocal()
    try:
        entry = db.query(Leaderboard).filter(Leaderboard.user_id == user_id).first()
        if entry:
            entry.score = score
            entry.level = level
            entry.survived_days = survived_days
            entry.kills = kills
            entry.updated_at = datetime.utcnow()
        else:
            entry = Leaderboard(
                user_id=user_id,
                username=username,
                score=score,
                level=level,
                survived_days=survived_days,
                kills=kills
            )
            db.add(entry)
        db.commit()
    finally:
        db.close()
