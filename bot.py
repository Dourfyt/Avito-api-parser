import asyncio
import logging
import tg.ticket
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import configparser
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State



logging.basicConfig(level=logging.INFO)
config = configparser.ConfigParser()
config.read('config.ini')
bot = Bot(token=config['BOT']["token"])
dp = Dispatcher(storage=MemoryStorage())
file = tg.ticket.File('tg/tickets')

users = config["BOT"]["PERSON"].split(",")

class IsAllowedUser(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return str(message.from_user.id) in users

class Tickets(StatesGroup):
    add_ticket = State()

@dp.message(Command("start"), IsAllowedUser())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Здравствуйте, я бот для работы с заявками WB! Введите /help, для ознакомления с командами")
    await state.clear()

@dp.message(Command("help"), IsAllowedUser())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Добавить поставку - /add номер поставки\nУдалить поставку - /del номер поставки\nПросмотреть файл - /show\nСбросить файл - /reset")

@dp.message(Command("add"), IsAllowedUser())
async def add_ticket(message: types.Message, state: FSMContext):
    file.add(message.text.split(' ')[-1])
    await message.answer("Успешно!")

@dp.message(Command("del"), IsAllowedUser())
async def del_ticket(message: types.Message, state: FSMContext):
    file.delete(message.text.split(' ')[-1])
    await message.answer("Успешно")

@dp.message(Command('show'), IsAllowedUser())
async def show(message: types.Message, state: FSMContext):
    await message.answer(file.show())

@dp.message(Command('reset'), IsAllowedUser())
async def show(message: types.Message, state: FSMContext):
    await message.answer(file.rewrite())

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())