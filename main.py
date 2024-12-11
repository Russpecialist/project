import config
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.types import PreCheckoutQuery, Message, ContentType, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup


# log
logging.basicConfig(level=logging.INFO)
# init
bot = Bot(token=config.TOKEN)
dp = Dispatcher()



    
# dp.pre_checkout_query.register(process_pre_checkout_query)
# dp.message.register(success_payment,F.successful_payment)

#prices
PRICE_1_MONTH = types.LabeledPrice(label = 'Подписка на 1 месяц', amount=500*100) #в копейках(руб)
PRICE_3_MONTHS = types.LabeledPrice(label = 'Подписка на 3 месяца', amount=1000*100) #в копейках(руб)
PRICE_6_MONTHS = types.LabeledPrice(label = 'Подписка на 6 месяцев', amount=3000*100) #в копейках(руб)
PRICE_12_MONTHS = types.LabeledPrice(label = 'Подписка на 12 месяцев', amount=5000*100) #в копейках(руб)



@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nЯ бот помощник отправь команду /buy для выбора тарифа')

#buy
@dp.message(Command(commands=["buy"]))
async def buy(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 месяц - 500₽", callback_data="buy_1_month")],
        [InlineKeyboardButton(text="3 месяца - 1300₽", callback_data="buy_3_months")],
        [InlineKeyboardButton(text="6 месяцев - 2400₽", callback_data="buy_6_months")]  
    ])
    await message.answer("Выберите срок подписки:", reply_markup=keyboard)



@dp.callback_query(lambda c: c.data and c.data.startswith('buy'))
async def process_subscription_selection(callback_query: types.CallbackQuery):
    duration = callback_query.data.split('_')[1]  # Extract duration (e.g., "1", "3", "6, )
    prices = {
        "1": PRICE_1_MONTH,
        "3": PRICE_3_MONTHS,
        "6": PRICE_6_MONTHS,
        
    }
    selected_price = prices.get(duration)
    
    if not selected_price:
        await callback_query.answer("Неверный выбор.")
        return

    if config.PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(callback_query.message.chat.id, 'Тестовый платеж')

    await bot.send_invoice(
        callback_query.message.chat.id,
        title=f"Подписка на {selected_price.label}",
        description=f"Активируйте подписку на {selected_price.label.lower()}",
        provider_token=config.PAYMENTS_TOKEN,
        currency="rub",
        photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
        photo_width=416,
        photo_height=234,
        is_flexible=False,
        prices=[selected_price],
        start_parameter=f"subscription-{duration}-months",
        payload=f"subscription-{duration}-months-payload")

# @dp.message(Command(commands = ['buy']))
# async def buy(message:Message):
#     if config.PAYMENTS_TOKEN.split(':')[1]=='TEST':
#         await bot.send_message(message.chat.id, 'Тестовый платеж')

# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query:PreCheckoutQuery, bot:Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# successful payment
@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def success_payment(message:Message, bot:Bot):
    await message.answer('Платеж прошел успешно держи ссылку на канал  https://t.me/Rus_chatbot27')


# Создаем асинхронную функцию
async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Запуск бота'),
        BotCommand(command='/buy',
                   description='Выбор тарифа и покупка'),
    ]

    await bot.set_my_commands(main_menu_commands)


dp.startup.register(set_main_menu)






#run long.polling

if __name__ == '__main__':
    dp.run_polling(bot)