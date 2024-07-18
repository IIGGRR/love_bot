from databasa.models import async_session, User, Photo
from sqlalchemy import select

from love_bot.databasa.models import Visit


async def set_user(tg_id, tg_fr_id):
    async with async_session() as session:
        session.add(User(tg_id=str(tg_id), tg_fr_id=str(tg_fr_id)))
        session.add(User(tg_id=str(tg_fr_id), tg_fr_id=str(tg_id)))
        await session.commit()


async def get_id(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == str(tg_id)))
        return user.id


async def check_registration(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == str(tg_id)))
        if user:
            return False
        else:
            return True


async def get_id_partner(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_fr_id == str(tg_id)))
        return user.id


async def get_tg_id_partner(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_fr_id == str(tg_id)))
        return user.tg_id


async def set_photo(file_path, user_id):
    async with async_session() as session:
        session.add(Photo(file_path=file_path, user_id=int(user_id)))
        await session.commit()


async def get_photo(photo_id):
    async with async_session() as session:
        photo = await session.scalar((select(Photo).where(int(photo_id) == Photo.id)))
        return photo


async def get_all_photo_partner(user_fr_id):
    async with async_session() as session:
        photos = await session.scalars((select(Photo).where(Photo.user_id == int(user_fr_id))))
        return photos


async def delete_all_photo():
    async with async_session() as session:
        session.delete(select(Photo))
        await session.commit()


async def set_visit(text):
    async with async_session() as session:
        session.add(Visit(text=text))
        await session.commit()
