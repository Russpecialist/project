import config
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, PreCheckoutQuery
from aiogram import types

# log
logging.basicConfig(level=logging.INFO)
 
# init
bot = Bot(token=config.TOKEN)
dp = Dispatcher()

#prices
PRICE = types.LabeledPrice(label = 'Подписка на 1 месяц', amount=500*100) #в копейках(руб)

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')

#buy
@dp.message(Command(commands = ['buy']))
async def buy(message:Message):
    if config.PAYMENTS_TOKEN.split(':')[1]=='TEST':
        await bot.send_message(message.chat.id, 'Тестовый платеж')


    await bot.send_invoice(message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")

# pre checkout  (must be answered in 10 seconds)
@dp.message()
async def pre_checkout_query(pre_checkout_query:PreCheckoutQuery, bot:Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
# successful payment
@dp.message()
async def successful_payment(message:Message):
   msg = f"Платёж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!! держите ссылку на канал"



#run long.polling

if __name__ == '__main__':
    dp.run_polling(bot)