import aiogram
import sqlalchemy
import asyncio 

from aiogram import Bot, Dispatcher

import handlers, keyboards
    

async def main():
    bot = Bot(token='7533292756:AAEO4pJJTqHkftyHrIUCzm5GTeife79a5kI')
    dp = Dispatcher()
    dp.include_router(handlers.handler)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is off')