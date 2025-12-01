from datetime import datetime, timedelta
from collections import Counter
from .db import SessionLocal
from .models import User
from aiogram import Bot

async def send_daily_report(bot: Bot, owner_id: int):
    async with SessionLocal() as session:
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        tomorrow_start = today_start + timedelta(days=1)

        # Bugun qo'shilganlar
        result = await session.execute(
            User.__table__.select().where(User.joined_at >= today_start, User.joined_at < tomorrow_start)
        )
        users_today = result.fetchall()
        joined_count = len(users_today)

        # Bugun chiqqanlar
        result = await session.execute(
            User.__table__.select().where(User.left_at >= today_start, User.left_at < tomorrow_start)
        )
        left_users = result.fetchall()
        left_count = len(left_users)

        # Hozir guruhda bo‘lganlar
        result = await session.execute(
            User.__table__.select().where(User.left_at == None)
        )
        in_group_users = result.fetchall()
        in_group_count = len(in_group_users)

        # Soatlik statistikani hisoblash
        hours_counter = Counter()
        for row in users_today:
            joined_at = row.joined_at
            hours_counter[joined_at.hour] += 1

        if hours_counter:
            max_hour = max(hours_counter, key=hours_counter.get)
            min_hour = min(hours_counter, key=hours_counter.get)
            max_count = hours_counter[max_hour]
            min_count = hours_counter[min_hour]
        else:
            max_hour = min_hour = max_count = min_count = None

        # Hisobot matni
        text = f"📊 Bugungi kunlik hisobot:\n\n" \
               f"✅ Bugun qo‘shilganlar: {joined_count}\n" \
               f"❌ Chiqqanlar: {left_count}\n" \
               f"👥 Hozir guruhda: {in_group_count}\n\n"

        if max_hour is not None:
            text += f"📈 Eng ko‘p qo‘shilgan soat: {max_hour}:00 — {max_count} ta\n" \
                    f"📉 Eng kam qo‘shilgan soat: {min_hour}:00 — {min_count} ta"

        # Telegram’ga yuborish
        await bot.send_message(chat_id=owner_id, text=text)
