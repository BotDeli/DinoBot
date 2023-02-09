from aiogram.utils.exceptions import MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted, MessageToDeleteNotFound
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram import Bot, executor, types
from contextlib import suppress
from random import randint
import sqlite3 as sq
import math
import logging
import asyncio
from config import ID_BOT, ADMIN

from keysR import Menu, AMenu, Click, Dino_buy, Buy, DINO
from keysI import KB, apanel, DONATE, Buy_menu, Buy_menup1, Buy_menup2, Buy_menup3, Buy_menud1, Buy_menud2, Buy_menud3, Buy_menud4, Buy_menud5, Buy_menud6, Buy_menud7, Buy_menud8, Buy_menud9, Buy_menud10
storage=MemoryStorage()
bot = Bot(token=ID_BOT)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
db = sq.connect('Dino.db')
cur = db.cursor()
admin=int(ADMIN)
#'...'.isdigit() вернет true если в строке только цифры (123)


# ПРОВЕРКА НА РЕГИСТРАЦИЮ ПОЛЬЗОВАТЕЛЯ--------------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands='start')
async def start(message: Message):
	us_id = message.from_user.id
	us_name = message.from_user.first_name
	cur.execute("SELECT user_id FROM users WHERE user_id = ?", (us_id,))
	if cur.fetchone() is None:
		cur.execute("INSERT INTO users ('user_id', 'name') VALUES (?, ?)", (us_id, us_name,))
		db.commit()
		await message.answer("Добро пожаловать в IDLE DinoBot,\nваша цель кликать и зарабатывать игровую валюту,\nвы можете их использовать для преобретения динозавров,\nчтобы зарабатывать еще больше денег.\nС некоторым шансом выпадают алмазы за которые можно преобрести более сильных динозавров.")
	else:
		cur.execute("SELECT gold FROM users WHERE user_id = ?", (us_id,))
		money = cur.fetchone()
		cur.execute("SELECT diamonds FROM users WHERE user_id = ?", (us_id,))
		diamonds = cur.fetchone() 
		await message.answer(f"Ваш баланс:\n{str(money)[1:-2]} баксов 💰\n{str(diamonds)[1:-2]} алмазов 💎", reply_markup=Menu)
		await message.delete()

# УДАЛЕНИЕ СООБЩЕНИЯ------------------------------------------------------------------------------------------------------------------------------------------
async def del_mes(message: Message, sleep_time: int = 0):
	await asyncio.sleep(sleep_time)
	with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
		await message.delete()
# БАЛАНС-------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands=['баланс', 'balance', 'деньги', 'money'])
@dp.message_handler(Text(equals=['баланс', 'деньги', 'balance', 'money'], ignore_case=True))
async def money(message: Message):
	us_id = message.from_user.id
	cur.execute("SELECT gold FROM users WHERE user_id = ?", (us_id,))
	money = str(cur.fetchone())[1:-2]
	cur.execute("SELECT diamonds FROM users WHERE user_id = ?", (us_id,))
	diamonds = str(cur.fetchone())[1:-2]
	msg = await message.answer(f"Ваш баланс:\n{money} баксов 💰\n{diamonds} алмазов 💎")
	await message.delete()
	asyncio.create_task(del_mes(msg, 60))

# МЕНЮ-------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands=['menu', 'меню'])
@dp.message_handler(Text(equals=['menu', 'меню', 'В меню'], ignore_case=True))
async def menu(message:Message):
	us_id = message.from_user.id
	if(us_id==admin):
		msg = await message.answer("Добро пожаловать в меню!", reply_markup=AMenu)
	else:
		msg = await message.answer("Добро пожаловать в меню!", reply_markup=Menu)
	asyncio.create_task(del_mes(msg, 60))

# ДОНАТ МЕНЮ-------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.message_handler(commands=['donate', 'донат'])
@dp.message_handler(Text(equals=['donate', 'донат'], ignore_case=True))
async def donate_menu(message:Message):
	us_id = message.from_user.id
	cur.execute("SELECT BALANCE FROM users WHERE user_id = ?", (us_id,))
	donate_balance = str(cur.fetchone())[1:-2]
	msg = await message.answer(f"Ваш баланс {donate_balance} руб.\n- click_multi это количество засчитанных кликов сделанных за один клик = 50 руб.\n- gold_multi это множитель получаемых баксов 💰 = 20 руб.\n- diamond_multi это множитель получаемых алмазов 💎 = 30 руб.", reply_markup=DONATE)
	asyncio.create_task(del_mes(msg, 60))

@dp.callback_query_handler(text='buy_click_multi')
async def buy_CM(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT BALANCE FROM users WHERE user_id = ?", (us_id,))
	balance = int(str(cur.fetchone())[1:-2])
	if(balance>=50):
		cur.execute("SELECT click_multi FROM users WHERE user_id = ?", (us_id,))
		click_multi = int(str(cur.fetchone())[1:-2])
		balance -= 50
		click_multi += 1
		cur.execute("UPDATE users SET BALANCE = ? WHERE user_id = ?", (balance, us_id,))
		bd.commit()
		cur.execute("UPDATE users SET click_multi = ? WHERE user_id = ?", (click_multi, us_id,))
		bd.commit()
		msg = await bot.send_message(us_id, 'Покупка прошла успешно!')
	else:
		msg = await bot.send_message(us_id, 'Недостаточно средств на балансе. Пополните баланс!')
	asyncio.create_task(del_mes(msg, 10))

@dp.callback_query_handler(text='buy_gold_multi')
async def buy_GM(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT BALANCE FROM users WHERE user_id = ?", (us_id,))
	balance = int(str(cur.fetchone())[1:-2])
	if(balance>=20):
		cur.execute("SELECT gold_multi FROM users WHERE user_id = ?", (us_id,))
		gold_multi = int(str(cur.fetchone())[1:-2])
		balance -= 50
		gold_multi += 1
		cur.execute("UPDATE users SET BALANCE = ? WHERE user_id = ?", (balance, us_id,))
		bd.commit()
		cur.execute("UPDATE users SET gold_multi = ? WHERE user_id = ?", (gold_multi, us_id,))
		bd.commit()
		msg = await bot.send_message(us_id, 'Покупка прошла успешно!')
	else:
		msg = await bot.send_message(us_id, 'Недостаточно средств на балансе. Пополните баланс!')
	asyncio.create_task(del_mes(msg, 10))
@dp.callback_query_handler(text='buy_diamond_multi')
async def buy_GM(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT BALANCE FROM users WHERE user_id = ?", (us_id,))
	balance = int(str(cur.fetchone())[1:-2])
	if(balance>=30):
		cur.execute("SELECT diamonds_multi FROM users WHERE user_id = ?", (us_id,))
		diamonds_multi = int(str(cur.fetchone())[1:-2])
		balance -= 50
		diamonds_multi += 1
		cur.execute("UPDATE users SET BALANCE = ? WHERE user_id = ?", (balance, us_id,))
		bd.commit()
		cur.execute("UPDATE users SET diamonds_multi = ? WHERE user_id = ?", (diamonds_multi, us_id,))
		bd.commit()
		msg = await bot.send_message(us_id, 'Покупка прошла успешно!')
	else:
		msg = await bot.send_message(us_id, 'Недостаточно средств на балансе. Пополните баланс!')
	asyncio.create_task(del_mes(msg, 10))

# КЛИКИ-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#НАЧАТЬ КЛИКАТЬ
@dp.message_handler(commands='начать кликать')
@dp.message_handler(Text(equals='начать кликать', ignore_case=True))
async def start_click(message:Message):
	msg = await message.answer("Заработайте, как можно 📈 💰 💎", reply_markup=Click)
	await message.delete()
	asyncio.create_task(del_mes(msg,60))

#ОБНАРУЖЕНИЕ КЛИКОВ
@dp.message_handler(commands=['click','клик'])
@dp.message_handler(Text(equals=['click','клик'], ignore_case=True))
async def click(message: Message):
	await message.delete()
	us_id = message.from_user.id
	cur.execute("SELECT click_multi FROM users WHERE user_id = ?", (us_id,))
	click_multi = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT gold_multi FROM users WHERE user_id = ?", (us_id,))
	gold_multi = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT diamond_multi FROM users WHERE user_id = ?", (us_id,))
	diamond_multi = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT chance_diamond FROM users WHERE user_id = ?", (us_id,))
	chance_diamond = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
	str_click = int(str(cur.fetchone())[1:-2])
	motions = click_multi
	for i in range(motions):
#золото
		chance = randint(1,100)
		cur.execute("SELECT gold FROM users WHERE user_id = ?", (us_id,))
		gold = int(str(cur.fetchone())[1:-2]) + (str_click * gold_multi)
		cur.execute("UPDATE users SET gold = ? WHERE user_id = ?", (gold, us_id,))
		db.commit()
		gem_chance = 100 - chance_diamond
#алмазы
		if(chance>gem_chance):
			cur.execute("SELECT diamonds FROM users WHERE user_id = ?", (us_id,))
			diamonds = int(str(cur.fetchone())[1:-2]) + (1 * diamond_multi)
			cur.execute("UPDATE users SET diamonds = ? WHERE user_id = ?", (diamonds, us_id,))
			db.commit()
			msg = await message.answer(f'Плюс гем ({diamonds}) ')
			asyncio.create_task(del_mes(msg, 10))

# МАГАЗИН ДИНОЗАВРИКОВ-----------------------------------------------------------------------------------------------------------------------------------------

#ТЕЛО МЕГА ДИНО
@dp.message_handler(Text(equals='Купить МЕГА ДИНО 🦕', ignore_case=True))
async def MEGA(message: Message):
	await message.delete()
	await message.answer('МЕГА ДИНО дают боьшой прирост к клику, но продаются за алмазы 💎\n- ПИВОЗАВРИК +10к\n- ДАВИДОЗАВРИК +5к\n- ТИХОЗАВРИК +1200', reply_markup=DINO)


#ТЕЛО МАГАЗИНА
@dp.message_handler(Text(equals='Купить динозаврика 🦖', ignore_case=True))
async def dino_shop(message: Message):
	await message.delete()
	await message.answer('Добро пожаловать в магазин "дино", здесь вы можете преобрести динозаврика за баксы 💰\nУ нас имеются:\n1. Акилозавр +1,\n2. Эвоплоцефал +3,\n3. Стегозавр +7,\n4. Трицератопс +10,\n5. Кронозавр +25,\n6. Кархародонтозавр +50,\n7. Гиганотозавр +70,\n8. Спинозавр +100,\n9. Тираннозавр Рекс +250,\n10. Аргентинозавр +500.\nОни дают прибавку к силе клика!', reply_markup = Dino_buy)



#ПОКУПКА МЕГАЗАВРА
#Купить ПИВОЗАВРА
@dp.message_handler(Text(equals='Купить ПИВОЗАВРА', ignore_case=True))
async def Dino_prem1(message: Message):
	us_id = message.from_user.id
	cur.execute("SELECT premium1 FROM users WHERE user_id = ?", (us_id,))
	prem1 = int(str(cur.fetchone())[1:-2])
	if(prem1<1):
		cost = 1000
	else:
		cost = 1000 * (1.15*prem1)
	cost = math.floor(cost)
	await message.answer(f'ПИВОЗАВР - ...\n- Дает буст: +10к\n- Стоимость: {cost} 💎\n- У вас в наличии: {prem1}\n\nВы действительно хотите преобрести?', reply_markup=Buy_menup1)


#Купить ДАВИДОЗАВРА
@dp.message_handler(Text(equals='Купить ДАВИДОЗАВРА', ignore_case=True))
async def Dino_prem2(message: Message):
	us_id = message.from_user.id
	cur.execute("SELECT premium2 FROM users WHERE user_id = ?", (us_id,))
	prem2 = int(str(cur.fetchone())[1:-2])
	if(prem2<1):
		cost = 480
	else:
		cost = 480 * (1.2*prem2)
	cost = math.floor(cost)
	await message.answer(f'ДАВИДОЗАВР - ...\n- Дает буст: +5к\n- Стоимость: {cost} 💎\n- У вас в наличии: {prem2}\n\nВы действительно хотите преобрести?', reply_markup=Buy_menup2)

#Купить ТИХОЗАВРА
@dp.message_handler(Text(equals='Купить ТИХОЗАВРА', ignore_case=True))
async def Dino_prem3(message: Message):
	us_id = message.from_user.id
	cur.execute("SELECT premium3 FROM users WHERE user_id = ?", (us_id,))
	prem3 = int(str(cur.fetchone())[1:-2])
	if(prem3<1):
		cost = 120
	else:
		cost = 120 * (1.3*prem3)
	cost = math.floor(cost)
	await message.answer(f'ТИХОЗАВР - ...\n- Дает буст: +1200\n- Стоимость: {cost} 💎\n- У вас в наличии: {prem3}\n\nВы действительно хотите преобрести?', reply_markup=Buy_menup3)
#ПОКУПКА ДИНОЗАВРИКОВ
#Купить Акилозаврика
@dp.message_handler(Text(equals='Купить Акилозаврика', ignore_case=True))
async def ready_dino1(message: Message):
	us_id = message.from_user.id
	cur.execute("SELECT dino1 FROM users WHERE user_id = ?", (us_id,))
	dino1 = int(str(cur.fetchone())[1:-2])
	if(dino1<1):
		cost = 10
	else:
		cost = 10 * (1.3*dino1)
	cost = math.floor(cost)
	await message.answer(f'Акилозаврик - род вымерших растительноядных рептилий из надотряда динозавров, семейства анкилозаврид.(акилозавра нет)\nРост: 1,7 м (почти как у разраба этой игры)\nМасса: 4 800 – 8 000 кг (сильно больше чем у разраба этой игры)\nДлина: 6 – 8 м (как пиписька в жопе разраба этой игры)\n- Дает буст: +1\n- Стоимость: {cost} 💰\n- У вас в наличии: {dino1}\n\nВы действительно хотите преобрести?', reply_markup=Buy_menud1)
#Купить Эвоплоцефалика
@dp.message_handler(Text(equals='Купить Эвоплоцефалика', ignore_case=True))
async def ready_dino2(message: Message):
	us_id = message.from_user.id
	cur.execute("SELECT dino2 FROM users WHERE user_id = ?", (us_id,))
	dino2 = int(str(cur.fetchone())[1:-2])
	if(dino2<1):
		cost = 50
	else:
		cost = 50 * (1.3*dino2)
	cost = math.floor(cost)
	await message.answer(f'Эвоплоцефалик - травоядный панцирный динозаврик, был одними из крупнейших представителей инфраотряда анкилозавров. Тело животного защищено костяными пластинами с крупными колючками, крупнейшие из которых располагались в районе шеи.\nДлина тела около 5—6 м\nМасса: 2 000 – 2 500 кг (весит меньше спинозавра)\nДлина: 5,5 – 7 м (рост почти такой же,как у спинозавтра)\n- Дает буст: +3\n- Стоимость: {cost} 💰\n- У вас в наличии: {dino2}\n\nВы действительно хотите преобрести?', reply_markup=Buy_menud2)
#Купить Стегозаврика 
@dp.message_handler(Text(equals='Купить Стегозаврика', ignore_case=True))
async def ready_dino3(message: Message):
	us_id = message.from_user.id
	cur.execute("SELECT dino3 FROM users WHERE user_id = ?", (us_id,))
	dino3 = int(str(cur.fetchone())[1:-2])
	if(dino3<1):
		cost = 150
	else:
		cost = 150 * (1.25*dino3)
	cost = math.floor(cost)
	await message.answer(f'Стегозаврик - травоядный динозаврик, существовавший 155—145 млн лет назад. Благодаря шипам на хвосте и костяным пластинам на спине являются одними из самых узнаваемых динозавров.\nСкорость: 15 – 18 км/ч (это вся инфа про него)\n- Дает буст: +7\n- Стоимость: {cost} 💰\n- У вас в наличии: {dino3}\n\nВы действительно хотите преобрести?', reply_markup=Buy_menud3)
#Купить Трицератопсика
@dp.message_handler(Text(equals='Купить Трицератопсика', ignore_case=True))
async def ready_dino4(message: Message):
	us_id = message.from_user.id
	cur.execute("SELECT dino4 FROM users WHERE user_id = ?", (us_id,))
	dino4 = int(str(cur.fetchone())[1:-2])
	if(dino4<1):
		cost = 180
	else:
		cost = 180 * (1.5*dino4)
	cost = math.floor(cost)
	await message.answer(f'Трицератопсик - растительноядный динозаврик, существовавший в конце маастрихтского века мелового периода, примерно от 68 до 66 миллионов лет назад на территориях современной Северной Америки.\nМасса: 6 000 – 12 000 кг\nРост: 2,9 – 3 м\n!!! Анекдот:"Наступил трицератопс на колобка и говорит"-"Блин"\n- Дает буст: +10\n- Стоимость: {cost} 💰\n- У вас в наличии: {dino4}\n\nВы действительно хотите преобрести?', reply_markup=Buy_menud4)
#Купить Кронозаврика
@dp.message_handler(Text(equals='Купить Кронозаврика', ignore_case=True))
async def ready_dino5(message: Message):
	us_id = message.from_user.id
	cur.execute("SELECT dino5 FROM users WHERE user_id = ?", (us_id,))
	dino5 = int(str(cur.fetchone())[1:-2])
	if(dino5<1):
		cost = 550
	else:
		cost = 550 * (1.4*dino5)
	cost = math.floor(cost)
	await message.answer(f'Кронозаврик - гигантский плиозавр раннемеловой эпохи. Название дано в честь титана Крона из древнегреческой мифологии. Один из самых крупных и самых известных широкой публике плиозавров, обитавший в раннем меловом периоде.\nДлина: 9 – 11 м (взрослая особь)(посмотрел картинки,супер страшная штука)\n- Дает буст: +25\n- Стоимость: {cost}\n- У вас в наличии: {dino5}\n\nВы действительно хотите преобрести?', reply_markup=Buy_menud5)
#Купить Кархародонтозаврика
@dp.message_handler(Text(equals='Купить Кархародонтозаврика', ignore_case=True))
async def ready_dino6(message: Message):
	us_id = message.from_user.id
	cur.execute("SELECT dino6 FROM users WHERE user_id = ?", (us_id,))
	dino6 = int(str(cur.fetchone())[1:-2])
	if(dino6<1):
		cost = 1000
	else:
		cost = 1000 * (1.3*dino6)
	cost = math.floor(cost)
	await message.answer(f'Кархародонтозаврик - обитал в меловом периоде на территории Африки.\nДлина: 8 – 14 м (хз что тут ещё написать)\nМасса: 6 000 – 15 000 кг (тут тоже хз)\n- Дает буст: +50\n- Стоимость: {cost}\n- У вас в наличии: {dino6}\n\nВы действительно хотите преобрести?', reply_markup=Buy_menud6)
#Купить Гиганотозаврика
@dp.message_handler(Text(equals='Купить Гиганотозаврика', ignore_case=True))
async def ready_dino7(message: Message):
	us_id = message.from_user.id
	cur.execute("SELECT dino7 FROM users WHERE user_id = ?", (us_id,))
	dino7 = int(str(cur.fetchone())[1:-2])
	if(dino7<1):
		cost = 1500
	else:
		cost = 1500 * (1.4*dino7)
	cost = math.floor(cost)
	await message.answer(f'Гиганотозаврик - крупный плотоядный динозавр верхнемеловой эпохи.\nМасса: 4 200 – 14 000 (это как 100 грамовая хинкалина + еще 4 199 900гр)\nСкорость: 50 км/ч (достаточно большая)\nДлина: 12 – 13 м (как пизанская башня, но на 44м меньше)\n- Дает буст: +70\n- Стоимость: {cost} 💰\n- У вас в наличии: {dino7}\n\nВы действительно хотите преобрести?', reply_markup=Buy_menud7)
#Купить Спинозаврика
@dp.message_handler(Text(equals='Купить Спинозаврика', ignore_case=True))
async def ready_dino8(message: Message):
	us_id = message.from_user.id
	cur.execute("SELECT dino8 FROM users WHERE user_id = ?", (us_id,))
	dino8 = int(str(cur.fetchone())[1:-2])
	if(dino8<1):
		cost = 2800
	else:
		cost = 2800 * (1.2*dino8)
	cost = math.floor(cost)
	await message.answer(f'Спинозаврик - обитал на территории современной Северной Африки в меловом периоде.\nРост: 5,4 м (почти как 5 шаурм по метру).\nВес: 5-7,6 т (очень много шаурм)\n- Дает буст: +100\n- Стоимость: {cost} 💰\n- У вас в наличии: {dino8}\n\nВы действительно хотите преобрести?', reply_markup=Buy_menud8)
#Купить Тираннозаврика Рекса
@dp.message_handler(Text(equals='Купить Тираннозаврика Рекса', ignore_case=True))
async def ready_dino9(message: Message):
	us_id = message.from_user.id
	cur.execute("SELECT dino9 FROM users WHERE user_id = ?", (us_id,))
	dino9 = int(str(cur.fetchone())[1:-2])
	if(dino9<1):
		cost = 7000
	else:
		cost = 7000 * (1.4*dino9)
	cost = math.floor(cost)
	await message.answer(f'Тираннозаврик Рекс - обитал в западной части Северной Америки, которая в те времена представляла собой остров Ларамидию.\nРост: 3,7 – 6,1 метровых пицц\nСкорость: 27 км/ч (почти как скорость Давидозавра,когда он видит пару шекелей на земле)\nПродолжительность жизни: 30 лет (меньше чем у ПИВОЗАВРА,ибо он не бухает)\n- Дает буст: +250\n- Стоимость: {cost} 💰\n- У вас в наличии: {dino9}\n\nВы действительно хотите преобрести?', reply_markup=Buy_menud9)
#Купить Аргентинозаврика
@dp.message_handler(Text(equals='Купить Аргентинозаврика', ignore_case=True))
async def ready_dino10(message: Message):
	us_id = message.from_user.id
	cur.execute("SELECT dino10 FROM users WHERE user_id = ?", (us_id,))
	dino10 = int(str(cur.fetchone())[1:-2])
	if(dino10<1):
		cost = 20000
	else:
		cost = 20000 * (1.2*dino10)
	cost = math.floor(cost)
	msg = await message.answer(f'Аргентинозаврик -  один из самых крупных динозавров, когда-либо живших в Южной Америке.\nМасса: 50 000 – 100 000 гаитовых\nДлина: 30 – 40 пиписек Гаитова\n- Дает буст: +500\n- Стоимость: {cost} 💰\n- У вас в наличии: {dino10}\n\nВы действительно хотите преобрести?', reply_markup=Buy_menud10)
#===========================================================================================================================================
#МАШИННОЕ СОСТОЯНИЕ
@dp.callback_query_handler(text='BUYp1')
async def buy_prem1(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT premium1 FROM users WHERE user_id = ?", (us_id,))
	prem1 = int(str(cur.fetchone())[1:-2])
	if(prem1<1):
		cost = 1000
	else:
		cost = 1000 * (1.15*prem1)
	cost = math.floor(cost)
	cur.execute("SELECT diamonds FROM users WHERE user_id = ?", (us_id,))
	gems = int(str(cur.fetchone())[1:-2])
	if(gems>=cost):
		gems -= cost
		cur.execute("UPDATE users SET diamonds = ? WHERE user_id = ?", (gems, us_id,))
		db.commit()
		prem1 += 1
		cur.execute("UPDATE users SET premium1 = ? WHERE user_id = ?", (prem1, us_id,))
		db.commit()
		cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
		click_st = int(str(cur.fetchone())[1:-2])
		click_st += 10000
		cur.execute("UPDATE users SET click_st = ? WHERE user_id = ?", (click_st, us_id,))
		db.commit()
		await bot.send_message(callback.from_user.id, 'Вы преобрели ПИВОЗАВРА',reply_markup=Menu)
	else:
		await bot.send_message(callback.from_user.id, 'У вас недостаточно алмазов 💎', reply_markup=Menu)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='BUYp2')
async def buy_prem2(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT premium2 FROM users WHERE user_id = ?", (us_id,))
	prem2 = int(str(cur.fetchone())[1:-2])
	if(prem2<1):
		cost = 480
	else:
		cost = 480 * (1.2*prem2)
	cost = math.floor(cost)
	cur.execute("SELECT diamonds FROM users WHERE user_id = ?", (us_id,))
	gems = int(str(cur.fetchone())[1:-2])
	if(gems>=cost):
		gems -= cost
		cur.execute("UPDATE users SET diamonds = ? WHERE user_id = ?", (gems, us_id,))
		db.commit()
		prem2 += 1
		cur.execute("UPDATE users SET premium2 = ? WHERE user_id = ?", (prem2, us_id,))
		db.commit()
		cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
		click_st = int(str(cur.fetchone())[1:-2])
		click_st += 5000
		cur.execute("UPDATE users SET click_st = ? WHERE user_id = ?", (click_st, us_id,))
		db.commit()
		await bot.send_message(callback.from_user.id, 'Вы преобрели ДАВИДОЗАВРА',reply_markup=Menu)
	else:
		await bot.send_message(callback.from_user.id, 'У вас недостаточно алмазов 💎', reply_markup=Menu)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='BUYp3')
async def buy_prem3(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT premium3 FROM users WHERE user_id = ?", (us_id,))
	prem3 = int(str(cur.fetchone())[1:-2])
	if(prem3<1):
		cost = 120
	else:
		cost = 120 * (1.3*prem3)
	cost = math.floor(cost)
	cur.execute("SELECT diamonds FROM users WHERE user_id = ?", (us_id,))
	gems = int(str(cur.fetchone())[1:-2])
	if(gems>=cost):
		gems -= cost
		cur.execute("UPDATE users SET diamonds = ? WHERE user_id = ?", (gems, us_id,))
		db.commit()
		prem3 += 1
		cur.execute("UPDATE users SET premium3 = ? WHERE user_id = ?", (prem3, us_id,))
		db.commit()
		cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
		click_st = int(str(cur.fetchone())[1:-2])
		click_st += 1200
		cur.execute("UPDATE users SET click_st = ? WHERE user_id = ?", (click_st, us_id,))
		db.commit()
		await bot.send_message(callback.from_user.id, 'Вы преобрели ТИХОЗАВРА',reply_markup=Menu)
	else:
		await bot.send_message(callback.from_user.id, 'У вас недостаточно алмазов 💎', reply_markup=Menu)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='BUYd1')
async def buy_dino1(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT dino1 FROM users WHERE user_id = ?", (us_id,))
	dino1 = int(str(cur.fetchone())[1:-2])
	if(dino1<1):
		cost = 10
	else:
		cost = 10 * (1.3*dino1)
	cost = math.floor(cost)
	cur.execute("SELECT gold FROM users WHERE user_id = ?", (us_id,))
	money = int(str(cur.fetchone())[1:-2])
	if(money>=cost):
		money -= cost
		cur.execute("UPDATE users SET gold = ? WHERE user_id = ?", (money, us_id,))
		db.commit()
		dino1 += 1
		cur.execute("UPDATE users SET dino1 = ? WHERE user_id = ?", (dino1, us_id,))
		db.commit()
		cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
		click_st = int(str(cur.fetchone())[1:-2])
		click_st += 1
		cur.execute("UPDATE users SET click_st = ? WHERE user_id = ?", (click_st, us_id,))
		db.commit()
		await bot.send_message(callback.from_user.id, 'Вы преобрели Акилозаврика',reply_markup=Menu)
	else:
		await bot.send_message(callback.from_user.id, 'У вас недостаточно баксов 💰', reply_markup=Menu)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='BUYd2')
async def buy_dino2(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT dino2 FROM users WHERE user_id = ?", (us_id,))
	dino2 = int(str(cur.fetchone())[1:-2])
	if(dino2<1):
		cost = 50
	else:
		cost = 50 * (1.3*dino2)
	cost = math.floor(cost)
	cur.execute("SELECT gold FROM users WHERE user_id = ?", (us_id,))
	money = int(str(cur.fetchone())[1:-2])
	if(money>=cost):
		money -= cost
		cur.execute("UPDATE users SET gold = ? WHERE user_id = ?", (money, us_id,))
		db.commit()
		dino2 += 1
		cur.execute("UPDATE users SET dino2 = ? WHERE user_id = ?", (dino2, us_id,))
		db.commit()
		cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
		click_st = int(str(cur.fetchone())[1:-2])
		click_st += 3
		cur.execute("UPDATE users SET click_st = ? WHERE user_id = ?", (click_st, us_id,))
		db.commit()
		await bot.send_message(callback.from_user.id, 'Вы преобрели Эвоплоцефалика', reply_markup=Menu)
	else:
		await bot.send_message(callback.from_user.id, 'У вас недостаточно баксов 💰', reply_markup=Menu)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='BUYd3')
async def buy_dino3(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT dino3 FROM users WHERE user_id = ?", (us_id,))
	dino3 = int(str(cur.fetchone())[1:-2])
	if(dino3<1):
		cost = 150
	else:
		cost = 150 * (1.25*dino3)
	cost = math.floor(cost)
	cur.execute("SELECT gold FROM users WHERE user_id = ?", (us_id,))
	money = int(str(cur.fetchone())[1:-2])
	if(money>=cost):
		money -= cost
		cur.execute("UPDATE users SET gold = ? WHERE user_id = ?", (money, us_id,))
		db.commit()
		dino3 += 1
		cur.execute("UPDATE users SET dino3 = ? WHERE user_id = ?", (dino3, us_id,))
		db.commit()
		cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
		click_st = int(str(cur.fetchone())[1:-2])
		click_st += 7
		cur.execute("UPDATE users SET click_st = ? WHERE user_id = ?", (click_st, us_id,))
		db.commit()
		await bot.send_message(callback.from_user.id, 'Вы преобрели Стегозаврика', reply_markup=Menu)
	else:
		await bot.send_message(callback.from_user.id, 'У вас недостаточно баксов 💰', reply_markup=Menu)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='BUYd4')
async def buy_dino4(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT dino4 FROM users WHERE user_id = ?", (us_id,))
	dino4 = int(str(cur.fetchone())[1:-2])
	if(dino4<1):
		cost = 180
	else:
		cost = 180 * (1.5*dino4)
	cost = math.floor(cost)
	cur.execute("SELECT gold FROM users WHERE user_id = ?", (us_id,))
	money = int(str(cur.fetchone())[1:-2])
	if(money>=cost):
		money -= cost
		cur.execute("UPDATE users SET gold = ? WHERE user_id = ?", (money, us_id,))
		db.commit()
		dino4 += 1
		cur.execute("UPDATE users SET dino4 = ? WHERE user_id = ?", (dino4, us_id,))
		db.commit()
		cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
		click_st = int(str(cur.fetchone())[1:-2])
		click_st += 10
		cur.execute("UPDATE users SET click_st = ? WHERE user_id = ?", (click_st, us_id,))
		db.commit()
		await bot.send_message(callback.from_user.id, 'Вы преобрели Трицератопсика', reply_markup=Menu)
	else:
		await bot.send_message(callback.from_user.id, 'У вас недостаточно баксов 💰')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='BUYd5')
async def buy_dino5(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT dino5 FROM users WHERE user_id = ?", (us_id,))
	dino5 = int(str(cur.fetchone())[1:-2])
	if(dino5<1):
		cost = 550
	else:
		cost = 550 * (1.4*dino5)
	cost = math.floor(cost)
	cur.execute("SELECT gold FROM users WHERE user_id = ?", (us_id,))
	money = int(str(cur.fetchone())[1:-2])
	if(money>=cost):
		money -= cost
		cur.execute("UPDATE users SET gold = ? WHERE user_id = ?", (money, us_id,))
		db.commit()
		dino5 += 1
		cur.execute("UPDATE users SET dino5 = ? WHERE user_id = ?", (dino5, us_id,))
		db.commit()
		cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
		click_st = int(str(cur.fetchone())[1:-2])
		click_st += 25
		cur.execute("UPDATE users SET click_st = ? WHERE user_id = ?", (click_st, us_id,))
		db.commit()
		await bot.send_message(callback.from_user.id, 'Вы преобрели Кронозаврика', reply_markup=Menu)
	else:
		await bot.send_message(callback.from_user.id, 'У вас недостаточно баксов 💰', reply_markup=Menu)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='BUYd6')
async def buy_dino6(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT dino6 FROM users WHERE user_id = ?", (us_id,))
	dino6 = int(str(cur.fetchone())[1:-2])
	if(dino6<1):
		cost = 1000
	else:
		cost = 1000 * (1.3*dino6)
	cost = math.floor(cost)
	cur.execute("SELECT gold FROM users WHERE user_id = ?", (us_id,))
	money = int(str(cur.fetchone())[1:-2])
	if(money>=cost):
		money -= cost
		cur.execute("UPDATE users SET gold = ? WHERE user_id = ?", (money, us_id,))
		db.commit()
		dino6 += 1
		cur.execute("UPDATE users SET dino6 = ? WHERE user_id = ?", (dino6, us_id,))
		db.commit()
		cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
		click_st = int(str(cur.fetchone())[1:-2])
		click_st += 50
		cur.execute("UPDATE users SET click_st = ? WHERE user_id = ?", (click_st, us_id,))
		db.commit()
		await bot.send_message(callback.from_user.id, 'Вы преобрели Кархародонтозаврика', reply_markup=Menu)
	else:
		await bot.send_message(callback.from_user.id, 'У вас недостаточно баксов 💰', reply_markup=Menu)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='BUYd7')
async def buy_dino7(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT dino7 FROM users WHERE user_id = ?", (us_id,))
	dino7 = int(str(cur.fetchone())[1:-2])
	if(dino7<1):
		cost = 1500
	else:
		cost = 1500 * (1.4*dino7)
	cost = math.floor(cost)
	cur.execute("SELECT gold FROM users WHERE user_id = ?", (us_id,))
	money = int(str(cur.fetchone())[1:-2])
	if(money>=cost):
		money -= cost
		cur.execute("UPDATE users SET gold = ? WHERE user_id = ?", (money, us_id,))
		db.commit()
		dino7 += 1
		cur.execute("UPDATE users SET dino7 = ? WHERE user_id = ?", (dino7, us_id,))
		db.commit()
		cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
		click_st = int(str(cur.fetchone())[1:-2])
		click_st += 70
		cur.execute("UPDATE users SET click_st = ? WHERE user_id = ?", (click_st, us_id,))
		db.commit()
		await bot.send_message(callback.from_user.id, 'Вы преобрели Гиганотозаврика', reply_markup=Menu)
	else:
		await bot.send_message(callback.from_user.id, 'У вас недостаточно баксов 💰', reply_markup=Menu)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='BUYd8')
async def buy_dino8(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT dino8 FROM users WHERE user_id = ?", (us_id,))
	dino8 = int(str(cur.fetchone())[1:-2])
	if(dino8<1):
		cost = 2800
	else:
		cost = 2800 * (1.2*dino8)
	cost = math.floor(cost)
	cur.execute("SELECT gold FROM users WHERE user_id = ?", (us_id,))
	money = int(str(cur.fetchone())[1:-2])
	if(money>=cost):
		money -= cost
		cur.execute("UPDATE users SET gold = ? WHERE user_id = ?", (money, us_id,))
		db.commit()
		dino8 += 1
		cur.execute("UPDATE users SET dino8 = ? WHERE user_id = ?", (dino8, us_id,))
		db.commit()
		cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
		click_st = int(str(cur.fetchone())[1:-2])
		click_st += 100
		cur.execute("UPDATE users SET click_st = ? WHERE user_id = ?", (click_st, us_id,))
		db.commit()
		await bot.send_message(callback.from_user.id, 'Вы преобрели Спинозаврика', reply_markup=Menu)
	else:
		await bot.send_message(callback.from_user.id, 'У вас недостаточно баксов 💰', reply_markup=Menu)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='BUYd9')
async def buy_dino9(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT dino9 FROM users WHERE user_id = ?", (us_id,))
	dino9 = int(str(cur.fetchone())[1:-2])
	if(dino9<1):
		cost = 7000
	else:
		cost = 7000 * (1.4*dino9)
	cost = math.floor(cost)
	cur.execute("SELECT gold FROM users WHERE user_id = ?", (us_id,))
	money = int(str(cur.fetchone())[1:-2])
	if(money>=cost):
		money -= cost
		cur.execute("UPDATE users SET gold = ? WHERE user_id = ?", (money, us_id,))
		db.commit()
		dino9 += 1
		cur.execute("UPDATE users SET dino9 = ? WHERE user_id = ?", (dino9, us_id,))
		db.commit()
		cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
		click_st = int(str(cur.fetchone())[1:-2])
		click_st += 250
		cur.execute("UPDATE users SET click_st = ? WHERE user_id = ?", (click_st, us_id,))
		db.commit()
		await bot.send_message(callback.from_user.id, 'Вы преобрели Тираннозаврика Рекса', reply_markup=Menu)
	else:
		await bot.send_message(callback.from_user.id, 'У вас недостаточно баксов 💰', reply_markup=Menu)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='BUYd10')
async def buy_dino10(callback: CallbackQuery):
	us_id = callback.from_user.id
	cur.execute("SELECT dino10 FROM users WHERE user_id = ?", (us_id,))
	dino10 = int(str(cur.fetchone())[1:-2])
	if(dino10<1):
		cost = 20000
	else:
		cost = 20000 * (1.2*dino10)
	cost = math.floor(cost)
	cur.execute("SELECT gold FROM users WHERE user_id = ?", (us_id,))
	money = int(str(cur.fetchone())[1:-2])
	if(money>=cost):
		money -= cost
		cur.execute("UPDATE users SET gold = ? WHERE user_id = ?", (money, us_id,))
		db.commit()
		dino10 += 1
		cur.execute("UPDATE users SET dino10 = ? WHERE user_id = ?", (dino10, us_id,))
		db.commit()
		cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
		click_st = int(str(cur.fetchone())[1:-2])
		click_st += 500
		cur.execute("UPDATE users SET click_st = ? WHERE user_id = ?", (click_st, us_id,))
		db.commit()
		await bot.send_message(callback.from_user.id, 'Вы преобрели Аргентинозаврика', reply_markup=Menu)
	else:
		await bot.send_message(callback.from_user.id, 'У вас недостаточно баксов 💰', reply_markup=Menu)

#=======================================================================================================================================================================
#ОТКАЗ ОТ ПОКУПКИ

@dp.callback_query_handler(text='CANCEL')
async def refusal_to_purchase(callback: CallbackQuery):
	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await bot.send_message(callback.from_user.id, 'Вы отказались от покупки 📉', reply_markup=Menu)


# КОЛЛЕКЦИЯ ДИНО--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.message_handler(Text(equals='Коллекция ДИНО', ignore_case=True))
async def collection(message: Message):
	await message.delete()
	us_id = message.from_user.id
	cur.execute("SELECT dino1 FROM users WHERE user_id = ?", (us_id,))
	dino1 = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT dino2 FROM users WHERE user_id = ?", (us_id,))
	dino2 = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT dino3 FROM users WHERE user_id = ?", (us_id,))
	dino3 = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT dino4 FROM users WHERE user_id = ?", (us_id,))
	dino4 = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT dino5 FROM users WHERE user_id = ?", (us_id,))
	dino5 = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT dino6 FROM users WHERE user_id = ?", (us_id,))
	dino6 = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT dino7 FROM users WHERE user_id = ?", (us_id,))
	dino7 = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT dino8 FROM users WHERE user_id = ?", (us_id,))
	dino8 = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT dino9 FROM users WHERE user_id = ?", (us_id,))
	dino9 = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT dino10 FROM users WHERE user_id = ?", (us_id,))
	dino10 = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT premium1 FROM users WHERE user_id = ?", (us_id,))
	prem1 = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT premium2 FROM users WHERE user_id = ?", (us_id,))
	prem2 = int(str(cur.fetchone())[1:-2])
	cur.execute("SELECT premium3 FROM users WHERE user_id = ?", (us_id,))
	prem3 = int(str(cur.fetchone())[1:-2])
	await message.answer(f'Динозаврики 🦖 :\nАкилозаврики +1 - {dino1}\nЭвоплоцефалики +3 - {dino2}\nСтегозаврики +7 - {dino3}\nТрицератопсики +10 - {dino4}\nКронозаврики +25 - {dino5}\nКархародонтозаврики +50 - {dino6}\nГиганотозаврики +70 - {dino7}\nСпинозаврики +100 - {dino8}\nТираннозаврики Рекс +250 - {dino9}\nАргентинозаврики +500 - {dino10}\n')
	await message.answer(f'МЕГА ДИНО 🦕:\nПИВОЗАВРИКИ +10к - {prem1}\nДАВИДОЗАВРИКИ +5к - {prem2}\nТИХОЗАВРИКИ +1200 - {prem3}')




# ПРОМОКОДИК------------------------------------------------------------------------------------------------------------------------------------

@dp.callback_query_handler(text='DINO')
async def test_dino(callback: types.CallbackQuery):
	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await bot.send_message(callback.from_user.id, 'ДИНО ВЫПУЩЕН!')
	us_id = callback.from_user.id
	cur.execute("SELECT dino10 FROM users WHERE user_id = ?", (us_id,))
	dino10 = int(str(cur.fetchone())[1:-2])
	if(dino10<1):
		dino10=1
		cur.execute("UPDATE users SET dino10 = ? WHERE user_id = ?", (dino10, us_id,))
		db.commit()
		cur.execute("SELECT click_st FROM users WHERE user_id = ?", (us_id,))
		click_st = int(str(cur.fetchone())[1:-2])
		click_st += 500
		cur.execute("UPDATE users SET click_st = ? WHERE user_id = ?", (click_st, us_id,))
		db.commit()

@dp.message_handler(commands='dino')
async def dino(message: Message):
	await message.answer('Привет!', reply_markup=KB)

#АДМИН ПАНЕЛЬ----------------------------------------------------------------------------------------------------------------------------------------------------------
class Amoney_state(StatesGroup):
	money = State()
class Adiamond_state(StatesGroup):
	diamond = State()

@dp.message_handler(Text(equals='Вызвать админ панель', ignore_case=True))
async def start_apanel(message: Message):
	us_id = message.from_user.id
	us_name = message.from_user.first_name
	if(us_id==admin):
		await message.delete()
		msg = await message.answer(f'{us_name}, что вы хотите сделать?', reply_markup=apanel)
		asyncio.create_task(del_mes(msg, 60))
	else:
		await message.delete()
		msg = await message.answer_sticker(r'CAACAgIAAxkBAAEHiHxj2V3iIPI2pwnhUjmHd_M0NkdRcAACzx4AAjY58EupzWdCiBh_zC0E')
		asyncio.create_task(del_mes(msg,10))


@dp.callback_query_handler(text='BASE', state=None)
async def base_date(callback: types.CallbackQuery):
	cur.execute("SELECT user_id, name, gold, diamonds, click_st FROM users")
	basdat = cur.fetchall()
	for row in basdat:
		msg = await bot.send_message(callback.from_user.id, row)
		asyncio.create_task(del_mes(msg, 60))


#MONEY
@dp.callback_query_handler(text='change_money', state=None)
async def Amoney(callback: types.CallbackQuery):
	msg = await bot.send_message(callback.from_user.id,'Введите какое количество баксов вам установить')
	await Amoney_state.next()
	asyncio.create_task(del_mes(msg, 60))
@dp.message_handler(state=Amoney_state.money)
async def sum_Amoney(message: Message, state: FSMContext):
	us_id = message.from_user.id
	message.delete()
	if(message.text.isdigit()):
		sum = int(message.text)
		cur.execute("UPDATE users SET gold = ? WHERE user_id = ?", (sum, us_id))
		db.commit()
		msg = await message.answer('✅')
	else:
		msg = await message.answer('❌')
	asyncio.create_task(del_mes(msg, 10))
	await state.finish()

#DIAMOND
@dp.callback_query_handler(text='change_diamond', state=None)
async def Adiamond(callback: types.CallbackQuery):
	msg = await bot.send_message(callback.from_user.id,'Введите какое количество алмазов вам установить')
	await Adiamond_state.next()
	asyncio.create_task(del_mes(msg, 60))
@dp.message_handler(state=Adiamond_state.diamond)
async def sum_Adiamond(message: Message, state: FSMContext):
	us_id = message.from_user.id
	message.delete()
	if(message.text.isdigit()):
		sum = int(message.text)
		cur.execute("UPDATE users SET diamonds = ? WHERE user_id = ?", (sum, us_id))
		db.commit()
		msg = await message.answer('✅')
	else:
		msg = await message.answer('❌')
	asyncio.create_task(del_mes(msg, 10))
	await state.finish()

# СТИКЕР ------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.message_handler()
async def stickers(message: Message):
	await message.delete()
	msg = await message.answer_sticker(r'CAACAgIAAxkBAAEHiHxj2V3iIPI2pwnhUjmHd_M0NkdRcAACzx4AAjY58EupzWdCiBh_zC0E')
	asyncio.create_task(del_mes(msg,10))

executor.start_polling(dp, skip_updates=True)