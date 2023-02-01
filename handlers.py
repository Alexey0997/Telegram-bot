from create import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
import random
from datetime import datetime
from keyboard import kb_main_menu


# ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ КОМАНДЫ "START" (НАЧАЛО ВЗАИМОДЕЙСТВИЯ С БОТОМ)
@dp.message_handler(commands = ['start'])
async def mes_start(message: types.Message):
    await message.answer(f'\
    \tПривет, {message.from_user.first_name}!👋\n\
    Умный бот предлагает Вам принять участие в розыгрыше конфет!🦉\n\
    Первый ход определяется жеребьевкой.🎲\n\
    За один ход можно забрать не менее 1 и не более 28 конфет.🍬🍬\n\
    Все конфеты оппонента достаются игроку, сделавшему последний ход.🔥\n\
    В ходе игры будут доступны следующие команды:\n\
    \t"/login" - ввести имя игрока;\n\
    \t"/set" - задать, какое количество конфет будем розыгрывать;\n\
    \t"/first" - провести жеребьевку;\n\
    \t"/step 5" - сделать ход;\n\
    \t"/rules" - вызвать справку о правилах игры;\n\
    \t"/help" - обратиться за психологической помощью;\n\
    \t"/feedback" - ввести команду, пробел, а затем текст отзыва об игре.\n\
    \n\tДЛЯ НАЧАЛА ИГРЫ введите ❗"/login"❗ и через пробел укажите свое ❗имя❗.\n')

# ФУНКЦИЯ ЛОГИРОВАНИЯ (ЗНАКОМСТВО С ИГРОКОМ)
@dp.message_handler(commands = ['login'])
async def mes_login(message: types.Message):
    global login
    login = message.text.split()[1]
    await message.answer(f'\tПриятно познакомиться, {login}👋!\n\
    Сколько конфет хотите разыграть❓\n\
    Можно 100 и даже 200!\n\
    Введите /set и через пробел количество конфет для розыгрыша.')
    user = []
    user.append(datetime.now())
    user.append(message.from_user.id)
    user.append(message.from_user.full_name)
    # user.append(message.from_user.user_name)
    user.append(login)
    user = list(map(str, user))
    with open('user_data.txt', 'a', encoding = 'UTF-8') as data:
        data.write(' | '.join(user) + '\n')



# ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ КОМАНДЫ "SET" (ОБЩЕЕ КОЛИЧЕСТВО КОНФЕТ)
@dp.message_handler(commands = ['set'])
async def mes_set(message: types.Message):
    global total
    count = int(message.text.split()[1])
    valid = False
    if count < 56:
        await message.answer(f'\tХотите разыграть "{count}"? Это мало. Игра быстро закончится. Задайте больше 60.')
    elif count > 200:
        await message.answer(f'\tВаше число "{count}"? Игра будет слишком долгой. Введите значение меньше 200.')
    else: 
        valid = True
    if valid == True:    
        total = count
        await message.answer(f'\
    \tМаксимальное количество конфет установлено - {total}.\n\
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
        await message.answer(f'\tВаше число "{number}"? Оно должно быть больше 1!')
    elif number > 100:
        await message.answer(f'\tВаше число "{number}"? Оно должно быть меньше 100!')
    else: 
        valid = True
    if valid == True:    
        user_lot = number
        bot_lot = random.randint(0, 101)
        await message.answer(f'\
    \tВаше число - {user_lot}? Отлично!\n\
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
            await message.answer(f'\
        \tБот загадал число {bot_lot}. Вы делаете первый ход.\n\
        Введите "/step" и через пробел количество конфет от 1 до 28.')
        elif first == 0:
            await message.answer(f'\
        \tБот тоже загадал число {bot_lot}.\n\
        Введите "/first" и через пробел случайное число от 1 до 100 чтобы повторить жеребьевку.\n')
        elif first == 2: # Если первый ход бота, то он реализуется в этом модуле.
            await message.answer(f'\tБот загадал число {bot_lot} и делает первый ход.\n')
            bot_step = total%(max + 1)           
            total -= bot_step
            await message.answer(f'\
        \tБот взял {bot_step}. Осталось {total}.\n\
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
        await message.answer(f'\tХотите взять "{number}"? Нужно не менее одной!')
    elif number > 28:
        await message.answer(f'\tХотите взять "{number}"? Можно не более 28!')
    else: 
        valid = True
    if valid == True:    
        user_step = number
        total -= user_step
        if total > 0:
            await message.answer(f'\tНа столе осталось "{total}" конфет. Следующий ход бота.')
        else:
            await message.answer('\
    \tКонфет больше не осталось. Вы победили!!!🏆 Если хотите поиграть еще, введите "/start".')
        if total > max:                        # Ход бота, если конфет > 28.
            if total%(max + 1) != 0:
                bot_step = total%(max + 1) 
                total -= bot_step
                await message.answer(f'\
    \tБот взял {bot_step}. Осталось {total}.\n\
    Ваш ход. Введите "/step" и через пробел количество конфет от 1 до 28.')
            else:
                bot_step = random.randint(1, 29)
                total -= bot_step
                await message.answer(f'\
    \tБот взял {bot_step}. Осталось {total}.\n\
    Ваш ход. Введите "/step" и через пробел количество конфет от 1 до 28.')

        elif total >= min and total <= max:    # Ход бота, если конфет < 28.
            bot_step = total            
            total -= bot_step
            await message.answer(f'\
    \tБот взял {bot_step}. Конфет не осталось и бот победил.✌\n\
    Если хотите поиграть еще, введите "/start".')


# ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ КОМАНДЫ "RULES" (ПРАВИЛА ИГРЫ)
@dp.message_handler(commands = ['rules'])
async def mes_rules(message: types.Message):
    await message.answer(f'\
    \tПравила игры простые:\n\
    \t- Первый ход определяется жеребьевкой.\n\
    \t- За один ход можно забрать не менее 1 и не более 28 конфет.\n\
    \t- Все конфеты оппонента достаются игроку, сделавшему последний ход.\n\
    Введите "/set" и через пробел укажите количество конфет для розыгрыша.\n',\
    reply_markup = kb_main_menu)

# ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ КОМАНДЫ "FEEDBACK" (ОТЗЫВ ОБ ИГРЕ)        
@dp.message_handler(commands = ['feedback'])
async def mes_yes(message: types.Message):
    await message.answer(f'\tУважаемый {message.from_user.full_name},\n\
    умный бот примет к сведению Ваше сообщение. Спасибо за обратную связь.🤝')
    print(f'От игрока {message.from_user.full_name} получено сообщение: "{message.text}".')    


# ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ КОМАНДЫ "HELP" (ОКАЗАНИЕ ПОМОЩИ)
@dp.message_handler(commands = ['help'])
async def mes_yes(message: types.Message):
    global login
    await message.answer(f'\
    \tУважаемый {login},\n\
    если Вы несколько раз проиграли боту, это не означает, что у Вас низкий IQ.\n\
    Дело в том, что искусственный интеллект уверенно побеждает по всей планете.\
    Cкоро он установит контроль над людьми.\n\
    Хотите спастись?😎\n\
    Напишите об этом в разделе "/feedback" (команда, пробел, текст) и мы подумаем, как Вам помочь.',\
    reply_markup = kb_main_menu)


# ФУНКЦИЯ ВЫВОДА СООБЩЕНИЯ ПРИ ПОСТУПЛЕНИИ НЕПРЕДУСМОТРЕННЫХ КОМАНД      
@dp.message_handler()
async def mes_all(message: types.Message):
    global login
    await message.answer(f'\
    \tУважаемый {login}, будьте внимательнее при вводе команд.')
    print(f'От игрока {message.from_user.full_name} получено сообщение: "{message.text}".')
