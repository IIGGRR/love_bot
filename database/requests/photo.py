from love_bot.database.models import async_session, User, Photo
from sqlalchemy import select


async def set_photo(file_path, user_id, name, public_id):
    async with async_session() as session:
        session.add(Photo(file_path=file_path, user_id=int(user_id), name=name, public_id=public_id))
        await session.commit()


async def get_photo(photo_id):
    async with async_session() as session:
        photo = await session.scalar((select(Photo).where(int(photo_id) == Photo.id)))
        return photo


async def get_all_photos_partner(user_fr_id):
    async with async_session() as session:
        photos = await session.scalars((select(Photo).where(Photo.user_id == int(user_fr_id))))
        return photos


async def delete_all_photo():
    async with async_session() as session:
        session.delete(select(Photo))
        await session.commit()


async def get_my_photo(user_id):
    async with async_session() as session:
        photos = await session.scalars((select(Photo).where(int(user_id) == Photo.user_id)))
        return photos


async def delete_my_photo(photo_id):
    async with async_session() as session:
        photo = await session.scalar(select(Photo).where(int(photo_id) == Photo.id))
        await session.delete(photo)
        await session.commit()


async def rename_my_photo(photo_id, new_name):
    async with async_session() as session:
        photo = await session.scalar(select(Photo).where(int(photo_id) == Photo.id))
        photo.name = new_name
        await session.commit()