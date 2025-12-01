import os
import asyncio
from collections import Counter
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ChatMemberUpdated
from dotenv import load_dotenv
from sqlalchemy import select

from .db import init_db, SessionLocal
from .models import User
from .report import send_daily_report
from datetime import datetime, timedelta  # timedelta shu yerga import qilindi

# --- LOCAL OFFSET --- 
LOCAL_OFFSET = timedelta(hours=5)  # O‘zbekiston vaqti UTC+5

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = Bot(TOKEN)
dp = Dispatcher()


# --- Foydalanuvchini bazaga qo'shish ---
async def add_user_to_db(user):
    async with SessionLocal() as session:
        db_user = User(
            telegram_id=str(user.id),
            full_name=user.full_name,
            joined_at=datetime.utcnow()
        )
        session.add(db_user)
        await session.commit()


# --- Foydalanuvchi chiqqanda bazani yangilash ---
async def remove_user_from_db(user):
    async with SessionLocal() as session:
        # Oxirgi qo‘shilgan yozuvni olamiz
        result = await session.execute(
            select(User).where(User.telegram_id == str(user.id)).order_by(User.joined_at.desc())
        )
        db_user = result.scalars().first()
        if db_user and db_user.left_at is None:
            db_user.left_at = datetime.utcnow()
            db_user.duration_in_group = int((db_user.left_at - db_user.joined_at).total_seconds())
            await session.commit()


# --- /start komanda ---
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Monitoring bot ishga tushdi!")


@dp.message(Command("stats"))
async def stats_cmd(message: Message):
    async with SessionLocal() as session:
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        tomorrow_start = today_start + timedelta(days=1)

        # Bugun qo'shilganlar
        result = await session.execute(
            select(User).where(User.joined_at >= today_start, User.joined_at < tomorrow_start)
        )
        users_today = result.scalars().all()
        joined_count = len(users_today)

        # Bugun chiqqanlar
        result = await session.execute(
            select(User).where(User.left_at >= today_start, User.left_at < tomorrow_start)
        )
        left_users = result.scalars().all()
        left_count = len(left_users)

        # Hozir guruhda bo‘lganlar
        result = await session.execute(
            select(User).where(User.left_at == None)
        )
        in_group_users = result.scalars().all()
        in_group_count = len(in_group_users)

        # Soatlik statistikani hisoblash (lokal vaqt)
        hours_counter = Counter()
        for user in users_today:
            local_joined = user.joined_at + LOCAL_OFFSET
            hours_counter[local_joined.hour] += 1

        if hours_counter:
            max_hour = max(hours_counter, key=hours_counter.get)
            min_hour = min(hours_counter, key=hours_counter.get)
            max_count = hours_counter[max_hour]
            min_count = hours_counter[min_hour]
        else:
            max_hour = min_hour = max_count = min_count = None

        text = f"📊 Bugungi statistika:\n\n" \
               f"✅ Bugun qo‘shilganlar: {joined_count}\n" \
               f"❌ Chiqqanlar: {left_count}\n" \
               f"👥 Hozir guruhda: {in_group_count}\n\n"

        if max_hour is not None:
            text += f"📈 Eng ko‘p qo‘shilgan soat: {max_hour}:00 — {max_count} ta\n" \
                    f"📉 Eng kam qo‘shilgan soat: {min_hour}:00 — {min_count} ta"

        await message.answer(text)

# --- ChatMember event handler ---
@dp.chat_member()
async def member_update_handler(event: ChatMemberUpdated):
    if event.new_chat_member.status == "member":
        await add_user_to_db(event.new_chat_member.user)
    elif event.new_chat_member.status in ["left", "kicked"]:
        await remove_user_from_db(event.new_chat_member.user)


# --- Kunlik hisobot uchun scheduler ---
async def scheduler():
    while True:
        now = datetime.utcnow()
        if now.hour == 23 and now.minute == 59:
            await send_daily_report(bot, OWNER_ID)
            await asyncio.sleep(60)  # keyingi minutgacha kutadi
        await asyncio.sleep(30)  # 30 soniyada bir tekshiradi


# --- Bot ishga tushirish ---
async def main():
    await init_db()
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)
