# Задача - создать телеграм-бота, который реализует алгоритм игры с конфетами. 

# Aiogram - это простой и полностью асинхронный фреймворк для Telegram Bot API,\
# написанный на Python 3.7 с asyncio и aiohttp.
# Dispatcher - модуль, отслеживающий входящие сообщения, осуществляющий их селекцию 
# и перенаправление потребителям в соответствии с алгоритмом.
# Token - цифровой ключ доступа к боту.

from aiogram import Bot, Dispatcher, executor, types
from handlers import dp

total = 170   # Начальное общее количество конфет для розыгрыша.
login = ''
                                
async def on_start(_):
    print('Бот запущен!')

executor.start_polling(dp, skip_updates=True, on_startup=on_start)
