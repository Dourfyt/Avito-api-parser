import asyncio
import logging
import ticket
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import configparser
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_path = os.path.join(parent_dir, 'config.ini')
logging.basicConfig(level=logging.INFO)
config = configparser.ConfigParser()
config.read(config_path)
bot = Bot(token=config['BOT']["token"])
dp = Dispatcher(storage=MemoryStorage())
file = ticket.File('tickets')

class Tickets(StatesGroup):
    add_ticket = State()

@dp.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Здравствуйте, я бот для работы с заявка WB! Введите номер заявки.")
    await state.set_state(Tickets.add_ticket)
    file.delete("29356574")

@dp.message(Tickets.add_ticket, F.text)
async def add_ticket(message: types.Message, state: FSMContext):
    file.add(message)
    await message.answer(file.get_first())

@dp.message(Tickets.add_ticket)
async def wrong_ticket(message: types.Message, state: FSMContext):
    await message.answer("Неправильный формат заявки, попробуйте еще раз")
    

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())