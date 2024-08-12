import asyncio
import sys
import os
from aiogram import Bot, Dispatcher, F

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.handlers import router
from app.database.models import async_main


async def main():
    await async_main() # при запуске бота, чтобы содавались таблицы
    bot = Bot(token='7274770099:AAGUVNYnKipQbzsESZFfkLccI6-kru3Ct7o')
    dp = Dispatcher() 
    dp.include_router(router)
    await dp.start_polling(bot)
   

if __name__ == '__main__':   
    try: 
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')

