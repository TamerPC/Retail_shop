from aiogram import Bot, Dispatcher, executor, types
import test_script

API_TOKEN = '6131907632:AAE3M2O7Tr7a21mPg5of0Yv97535kHZgiTg'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
   await message.reply("Привет!\nЯ ShopDetBot!, я буду оповещать если на полках закончатся товары")

@dp.message_handler()
async def echo(message: types.Message):
   await message.answer(message.text)

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)