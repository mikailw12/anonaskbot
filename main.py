import asyncio 

from aiogram import Bot, Dispatcher

import handlers


async def main():
    bot = Bot(token='your_token)
    dp = Dispatcher()
    dp.include_router(handlers.handler)
  # Создаем таблицы при запуске бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is off')
