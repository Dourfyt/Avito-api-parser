import asyncio
import logging
import configparser
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from multiprocessing import Process
import signal
import os
from core import main as run_sel  # Импорт функции main из core.py

logging.basicConfig(level=logging.INFO)
config = configparser.ConfigParser()
config.read('config.ini')
bot = Bot(token=config['BOT']["TOKEN"])
dp = Dispatcher(storage=MemoryStorage())

# Глобальная переменная для хранения процесса
proc = None

@dp.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Здравствуйте, я бот для работы с заявками WB! Введите /help, для ознакомления с командами")
    await state.clear()

@dp.message(Command('help'))
async def cmd_help(message: types.Message, state: FSMContext):
    await message.answer("Добавить поставку - /add номер поставки\nУдалить поставку - /del номер поставки\nПросмотреть файл - /show\nЗапустить процесс - /run\nОстановить процесс - /stop")

@dp.message(Command('run'))
async def run(message: types.Message, state: FSMContext):
    global proc
    if proc and proc.is_alive():
        await message.answer("Процесс уже запущен.")
    else:
        proc = Process(target=run_sel)
        proc.start()
        await message.answer("Процесс запущен.")

@dp.message(Command('stop'))
async def stop(message: types.Message, state: FSMContext):
    global proc
    if proc and proc.is_alive():
        proc.terminate()
        proc.join()
        await message.answer("Процесс остановлен.")
    else:
        await message.answer("Процесс не запущен.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
