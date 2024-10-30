import asyncio 

from aiogram import Bot, Dispatcher

import handlers
from requests import create_tables


async def main():
    await create_tables()
    bot = Bot(token='7533292756:AAEO4pJJTqHkftyHrIUCzm5GTeife79a5kI')
    dp = Dispatcher()
    dp.include_router(handlers.handler)
  # Создаем таблицы при запуске бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is off')