from love_bot.databasa.models import async_session, User
from sqlalchemy import select


async def set_user(tg_id, tg_fr_id):
    async with async_session() as session:
        session.add(User(tg_id=tg_id, tg_fr_id=tg_fr_id))
        session.add(User(tg_id=tg_fr_id, tg_fr_id=tg_id))
        await session.commit()


async def check_registration(tg_id):
    async with async_session() as session:
        if session.scalar(select(User).where(User.tg_id == tg_id)):
            return True
        return False

