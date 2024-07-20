from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
import os
from dotenv import load_dotenv
load_dotenv()

engine = create_async_engine(os.getenv('DATABASE_URL'))
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[str] = mapped_column(String(32))
    tg_fr_id: Mapped[str] = mapped_column(String(32))


class Photo(Base):
    __tablename__ = 'photos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=True)
    file_path: Mapped[str] = mapped_column(String(256))
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))


class Visit(Base):
    __tablename__ = 'visits'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(512))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

