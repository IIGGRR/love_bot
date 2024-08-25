
from love_bot.database.models import async_session, User, Photo, Visit
from sqlalchemy import select


async def set_user(tg_id, name, tg_fr_id=None):
    async with async_session() as session:
        if tg_fr_id is None:
            session.add(User(tg_id=str(tg_id), name=str(name)))
        else:
            session.add(User(tg_id=str(tg_id), name=str(name), tg_fr_id=str(tg_fr_id)))
            user = await session.scalar(select(User).where(User.tg_id == str(tg_fr_id)))
            user.tg_fr_id = str(tg_id)
        await session.commit()


async def add_tg_fr_id(tg_id, tg_fr_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == str(tg_id)))
        user.tg_fr_id = tg_fr_id
        await session.commit()
        return user


async def add_sync_tg_fr_id(tg_id, tg_fr_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == str(tg_id)))
        partner = await session.scalar(select(User).where(User.tg_id == str(tg_fr_id)))
        partner.tg_fr_id = str(tg_id)
        user.tg_fr_id = str(tg_fr_id)
        await session.commit()


async def get_id(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == str(tg_id)))
        return user.id


async def get_user_by_tg_id(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == str(tg_id)))
        if user is None:
            return None
        return user


async def get_id_partner(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_fr_id == str(tg_id)))
        return user.id


async def get_tg_id_partner(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_fr_id == str(tg_id)))
        return user.tg_id


async def get_partner(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_fr_id == str(tg_id)))
        if user is None:
            return None
        return user


async def delete_partner(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == str(tg_id)))
        partner = await session.scalar(select(User).where(User.tg_id == str(user.tg_fr_id)))
        user.tg_fr_id = None
        partner.tg_fr_id = None
        await session.commit()