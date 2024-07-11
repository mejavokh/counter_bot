from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from database import *
from config import *


bot = Bot(token=token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.reply('Привет! Я бот для учета ваших трат. Отправьте сумму'
                        'вашей траты, чтобы я мог их записать,'
                        'команда "\stats" для того чтобы посмотреть траты')


@dp.message_handler(commands='stats')
async def send_stats(message: Message):
    user_id = message.from_user.id
    day_expenses = get_expenses(user_id, 'day')
    week_expenses = get_expenses(user_id, 'week')
    month_expenses = get_expenses(user_id, 'month')
    year_expenses = get_expenses(user_id, 'year')

    response = (f"Траты за день: {day_expenses: .2f}\n"
                f"Траты за неделью: {week_expenses: .2f}\n"
                f"Траты за месяц: {month_expenses: .2f}\n"
                f"Траты за год: {year_expenses: .2f}\n")

    await message.reply(response)


@dp.message_handler()
async def add_new_expense(message: Message):
    user_id = message.from_user.id
    try:
        amount = float(message.text)
        add_expense(user_id, amount)
        await message.reply('Трата добавлена!')
    except ValueError:
        await message.reply('Пожалуйста отправьте число для записи траты.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)





