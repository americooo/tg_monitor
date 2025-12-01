from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from .models import Base, User
from datetime import datetime

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# --- User qo'shish ---
async def add_user_to_db(user):
    async with SessionLocal() as session:
        db_user = User(
            telegram_id=str(user.id),
            full_name=user.full_name,
            joined_at=datetime.utcnow()
        )
        session.add(db_user)
        await session.commit()

# --- User chiqsa yozuvni yangilash ---
async def remove_user_from_db(user):
    async with SessionLocal() as session:
        # oxirgi qo‘shilgan yozuvni olamiz
        result = await session.execute(
            User.__table__.select().where(
                User.telegram_id == str(user.id)
            ).order_by(User.joined_at.desc())
        )
        db_user = result.scalar_one_or_none()
        if db_user and db_user.left_at is None:  # faqat hali chiqmagan yozuvni yangilaymiz
            db_user.left_at = datetime.utcnow()
            db_user.duration_in_group = int((db_user.left_at - db_user.joined_at).total_seconds())
            await session.commit()
