import datetime

from sqlalchemy import String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
import os
from sqlalchemy.sql import func
from dotenv import load_dotenv
load_dotenv()

engine = create_async_engine(os.getenv('DATABASE_URL'))
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class User(Base):
    tg_id: Mapped[str] = mapped_column(String(32))
    tg_fr_id: Mapped[str] = mapped_column(String(32), nullable=True)
    name: Mapped[str] = mapped_column(String(64))
    reg_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Photo(Base):
    name: Mapped[str] = mapped_column(String(32), default='Фото')
    file_path: Mapped[str] = mapped_column(String(256))
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    public_id: Mapped[str] = mapped_column(String(256), nullable=True)
    pub_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Visit(Base):
    text: Mapped[str] = mapped_column(String(512))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

