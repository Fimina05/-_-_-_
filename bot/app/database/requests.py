from app.database.models import async_session
from app.database.models import User, Category, Item
from sqlalchemy import select    # ещё есть функции  updete, delete, desc


async def set_user(tg_id: int) -> None:                  # будет передаваться айди пользователя и добавляться в таблицу
    async with async_session() as session:  
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:    # если ничего не нашли
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_categories():               #достаём все категории
    async with async_session() as session:
        return await session.scalars(select(Category))
    

async def get_category_item(category_id):     # передаём айди категории
     async with async_session() as session:
         return await session.scalars(select(Item).where(Item.category == category_id))


async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))

