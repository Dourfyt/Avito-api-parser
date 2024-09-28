import asyncio
import logging
import tg.ticket
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import configparser
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import os
from multiprocessing import Process
from core import main


logging.basicConfig(level=logging.INFO)
config = configparser.ConfigParser()
config.read('config.ini')
bot = Bot(token=config['BOT']["token"])
dp = Dispatcher(storage=MemoryStorage())
file = tg.ticket.File('tg/tickets')

class Tickets(StatesGroup):
    add_ticket = State()

@dp.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Здравствуйте, я бот для работы с заявка WB! Введите номер заявки.")
    await state.set_state(Tickets.add_ticket)

@dp.message(Tickets.add_ticket, F.text)
async def add_ticket(message: types.Message, state: FSMContext):
    file.add(message)
    await state.clear()
    await message.answer(file.get_first())

@dp.message(Tickets.add_ticket)
async def wrong_ticket(message: types.Message, state: FSMContext):
    await message.answer("Неправильный формат заявки, попробуйте еще раз")

@dp.message(Command('list'))
async def list(message: types.Message, state: FSMContext):
    await message.answer(file.show())

@dp.message(Command('run'))
async def run(message: types.Message, state: FSMContext):
    global p1
    p1 = Process(target=main, daemon=True)
    p1.start()
    p1.join()
    await message.answer("Запущен")

@dp.message(Command('stop'))
async def stop(message: types.Message, state: FSMContext):
    p1.close()
    await message.answer("Отключен")

@dp.message(Command('refresh'))
async def stop(message: types.Message, state: FSMContext):
    p1.close()
    p1.start()
    p1.join()
    await message.answer("Перезагружен")


async def log_tg(text):
    await bot.send_message(chat_id=config["BOT"]["PERSON"], text=text)
    

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())