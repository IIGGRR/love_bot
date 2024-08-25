from love_bot.database.models import async_session, Visit


async def set_visit(text):
    async with async_session() as session:
        session.add(Visit(text=text))
        await session.commit()
