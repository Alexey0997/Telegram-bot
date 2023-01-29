from create import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
import random

# ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ КОМАНДЫ "START" (НАЧАЛО ВЗАИМОДЕЙСТВИЯ С БОТОМ)
@dp.message_handler(commands = ['start'])
async def mes_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}!\n\
    Умный бот предлагает Вам принять участие в розыгрыше конфет!\n\
    Первый ход определяется жеребьевкой.\n\
    За один ход можно забрать не менее 1 и не более 28 конфет.\n\
    Все конфеты оппонента достаются игроку, сделавшему последний ход.\n\
    В ходе игры будут доступны следующие команды:\n\
    \t"/ruls" - справка о правилах игры;\n\
    \t"/set" - задать, какое количество конфет будем розыгрывать;\n\
    \t"/start" - жеребьевка, чтобы определить, кто ходит первым;\n\
    \t"/step 5" - Ваш ход: введите step и через пробел нужное количество конфет;\n\
    \t"/help" - вызов психологической помощи;\n\
    \t"/feedback" - ввести команду, пробел, а затем текст отзыва об игре.\n\
    \n\tВведите "/yes", чтобы начать игру.\n')

# ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ КОМАНДЫ "YES" (СОГЛАСИЕ НА ИГРУ)
@dp.message_handler(commands = ['yes'])
async def mes_yes(message: types.Message):
    await message.answer(f'Правильное решение!\n\
    Сколько конфет хотите разыграть? Можно 100 и даже 200!\n\
    Введите /set и через пробел количество конфет для розыгрыша.')

# ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ КОМАНДЫ "RULS" (ПРАВИЛА ИГРЫ)
@dp.message_handler(commands = ['ruls'])
async def mes_yes(message: types.Message):
    await message.answer(f'Правила игры простые:\n\
    \t- Первый ход определяется жеребьевкой.\n\
    \t- За один ход можно забрать не менее 1 и не более 28 конфет.\n\
    \t- Все конфеты оппонента достаются игроку, сделавшему последний ход.\n\
    Введите "/yes", чтобы начать игру.\n')

# ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ КОМАНДЫ "HELP" (ОКАЗАНИЕ ПОМОЩИ)
@dp.message_handler(commands = ['help'])
async def mes_yes(message: types.Message):
    await message.answer(f'\tУважаемый пользователь, если Вы несколько раз проиграли боту,\
    это не означает, что у Вас низкий IQ.\n\
    Дело в том, что искусственный интеллект уверенно побеждает по всей планете\
    и скоро получит контроль над людьми.\n\
    Хотите спастись?\n\
    Напишите об этом в разделе "/feedback" (команда, пробел, текст) и мы подумаем, как Вам помочь.')

# ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ КОМАНДЫ "SET" (ОБЩЕЕ КОЛИЧЕСТВО КОНФЕТ)
@dp.message_handler(commands = ['set'])
async def mes_set(message: types.Message):
    global total
    count = int(message.text.split()[1])
    total = count
    await message.answer(f'Максимальное количество конфет установлено - {total}.\n\
    Чтобы все было честно, определим чей будет первый ход с помощью жеребьевки.\n\
    Введите "/first" и через пробел случайное число от 1 до 100.')

# ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ КОМАНДЫ "FIRST" (ЖЕРЕБЬЕВКА - КТО ПЕРВЫЙ ХОДИТ)
@dp.message_handler(commands = ['first'])
async def mes_first(message: types.Message):
    global total
    max = 28
    min = 1
    number = int(message.text.split()[1])
    if number < 1:
        await message.answer(f'Ваше число "{number}"? Оно должно быть больше 1!')
    elif number > 100:
        await message.answer(f'Ваше число "{number}"? Оно должно быть меньше 100!')
    else: 
        valid = True
    if valid == True:    
        user_lot = number
        bot_lot = random.randint(0, 101)
        await message.answer(f'Ваше число - {user_lot}? Отлично!\n\
        Теперь умный бот сгенерирует свое число и определим, чей ход первый.')
        while True:                 
            bot_lot = random.randint(0, 101)
            first = 3
            try:
                if user_lot > bot_lot:
                    first = 1            # Первый ход пользователя
                    break
                elif user_lot == bot_lot:
                    first = 0            # Ничья
                elif user_lot < bot_lot:
                    first = 2            # Первый ход бота
                    break
            except: 
                first = 3
        if first == 1:
            await message.answer(f'Бот загадал число {bot_lot}. Вы делаете первый ход.\n\
            Введите "/step" и через пробел количество конфет от 1 до 28.')
        elif first == 0:
            await message.answer(f'Бот тоже загадал число {bot_lot}.\n\
            Введите "/first" и через пробел случайное число от 1 до 100 чтобы повторить жеребьевку.\n')
        elif first == 2: # Если первый ход бота, то он реализуется в этом модуле.
            await message.answer(f'Бот загадал число {bot_lot} и делает первый ход.\n')
            bot_step = total%(max + 1)           
            total -= bot_step
            await message.answer(f'Бот взял {bot_step}. Осталось {total}.\n\
            Ваш ход. Введите "/step" и через пробел количество конфет от 1 до 28.')

# ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ КОМАНДЫ "STEP" (ИГРА НАЧИНАЯ С ХОДА ИГРОКА)
@dp.message_handler(commands = ['step'])
async def mes_step(message: types.Message):
    global total    # Общее количество конфет на кону.
    max = 28        # Максимальное число, которое можно взять за один ход.
    min = 1         # Минимальное число, которое можно взять за один ход. 
    number = int(message.text.split()[1])
    valid = False
    if number < 1:
        await message.answer(f'Хотите взять "{number}"? Нужно не менее одной!')
    elif number > 28:
        await message.answer(f'Хотите взять "{number}"? Можно не более 28!')
    else: 
        valid = True
    if valid == True:    
        user_step = number
        total -= user_step
        if total >= 0:
            await message.answer(f'На столе осталось "{total}" конфет. Следующий ход бота.')
        else:
            await message.answer('Конфет больше не осталось. Вы победили!!!')
        if total > max:                        # Ход бота, если конфет > 28.
            bot_step = total%(max + 1) 
            total -= bot_step
            await message.answer(f'Бот взял {bot_step}. Осталось {total}.\n\
            Ваш ход. Введите "/step" и через пробел количество конфет от 1 до 28.')
        elif total >= min and total <= max:    # Ход бота, если конфет < 28.
            bot_step = total            
            total -= bot_step
            await message.answer(f'Бот взял {bot_step}. Конфет не осталось и бот победил.\n\
            Если хотите поиграть еще, введите "/start".')

# ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ КОМАНДЫ "FEEDBACK" (ОТЗЫВ ОБ ИГРЕ)        
@dp.message_handler(commands = ['feedback'])
async def mes_yes(message: types.Message):
    await message.answer(f'\tУважаемый {message.from_user.full_name}, умный бот примет к сведению\n\
    Ваше сообщение. Спасибо за обратную связь.')
    print(f'От игрока {message.from_user.full_name} получено сообщение: "{message.text}".')

 # ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ НЕПРЕДУСМОТРЕННЫХ КОМАНД      
@dp.message_handler()
async def mes_all(message: types.Message):
    await message.answer(f'\tУважаемый {message.from_user.full_name}, будьте внимательнее при вводе команд.')
    print(f'От игрока {message.from_user.full_name} получено сообщение: "{message.text}".')
