import asyncio
import logging
import ticket
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import configparser
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from kb import kb


logging.basicConfig(level=logging.INFO)
config = configparser.ConfigParser()
config.read('config.ini')
bot = Bot(token=config['BOT']["token"])
dp = Dispatcher(storage=MemoryStorage())
file = ticket.File('tg/tickets')

users = config["BOT"]["PERSON"].split(",")

class IsAllowedUser(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return str(message.from_user.id) in users

class States(StatesGroup):
    add_ticket = State()
    del_ticket = State()

@dp.message(Command("start"), IsAllowedUser())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Здравствуйте, я бот для работы с заявками WB!", reply_markup=kb.tickets_kb())
    await state.clear()

@dp.callback_query(F.data=="add", IsAllowedUser())
async def add_ticket(call : types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите номер заявки")
    await state.set_state(States.add_ticket)

@dp.callback_query(States.add_ticket, IsAllowedUser())
async def add(message : types.Message, state : FSMContext):
    file.add(message.text)
    await message.answer(f"Поставка №{message.text} успешно добавлена")
    await state.clear()

@dp.callback_query(F.data=="del", IsAllowedUser())
async def add_ticket(call : types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите номер заявки для удаления")
    await state.set_state(States.del_ticket)

@dp.callback_query(States.del_ticket, IsAllowedUser(), F.text)
async def delete(message : types.Message, state : FSMContext):
    file.delete(message.text)
    await message.answer(f"Поставка №{message.text} успешно удалена")
    await state.clear()

@dp.callback_query(F.data=="show", IsAllowedUser())
async def show(call : types.CallbackQuery):
    await call.message.answer(file.show())

@dp.callback_query(F.data=="reset", IsAllowedUser())
async def reset(call : types.CallbackQuery):
    await call.message.answer(file.rewrite())

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())