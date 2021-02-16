import logging
from asyncio import get_event_loop

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.utils.exceptions import Throttled

import messages as msg
from api import get_data, prepare_data, get_post_id_from_json, get_final_message
from config import TOKEN


logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO)
loop = get_event_loop()
bot = Bot(token=TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)
dp.middleware.setup(LoggingMiddleware())


button = ReplyKeyboardMarkup(resize_keyboard=True)
button.add(KeyboardButton('🎲🎲'))
button.add(KeyboardButton('Как добавить свою запись?'))


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
	await message.reply(msg.start_message, reply_markup=button)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
	await message.reply(msg.help_message, reply_markup=button)


@dp.callback_query_handler(lambda call_back: call_back.data == 'get_photo_button')
async def process_callback_button1(callback_query: types.CallbackQuery):
	try:
		await dp.throttle('text', rate=0.5)
	except Throttled:
		# Если пользователь продолжит флудить, то просто игнорируем его
		try:
			await dp.throttle('text_', rate=1.5)
		except Throttled:
			pass
		else:
			await bot.send_message(
				callback_query.from_user.id, msg.rate_limit
			)
	else:
		await bot.answer_callback_query(callback_query.id)
		await bot.send_chat_action(callback_query.from_user.id, 'upload_photo')
		photo_data = await get_post_id_from_json(callback_query.message.reply_markup)
		me = await bot.get_me()
		await bot.send_photo(
			chat_id=callback_query.from_user.id,
			photo=photo_data,
			caption='@'+me.username,
			reply_to_message_id=callback_query.message.message_id,
		)


@dp.message_handler(content_types=['text'])
async def handle_message_received(message_telegram):
	# Если пользователь пишет чаще чем раз в 0.3 секунды, то отправляем ему сообщение с прозьбой не флудить
	try: await dp.throttle('text', rate=0.3)
	except Throttled:
		# Если пользователь продолжит флудить, то просто игнорируем его
		try: await dp.throttle('text_', rate=0.5)
		except Throttled: pass
		else: await message_telegram.reply(msg.rate_limit)
	else:
		if message_telegram.text == '🎲🎲':
			await bot.send_chat_action(message_telegram.chat.id, "typing")
			message, link = await get_final_message()
			try:
				await message_telegram.reply(message, reply_markup=link)
			except:
				# Повторна спроба
				message, link = await get_final_message()
				await message_telegram.reply(message, reply_markup=link)

		elif message_telegram.text == 'Как добавить свою запись?':
			await message_telegram.reply(msg.info_text, reply_markup=msg.website_link)
		else:
			await message_telegram.reply(msg.error_command, reply_markup=button)


async def shutdown(dispatcher: Dispatcher):
	await dispatcher.storage.close()
	await dispatcher.storage.wait_closed()


if __name__ == '__main__':
	executor.start_polling(dp, loop=loop, skip_updates=False, on_shutdown=shutdown)
