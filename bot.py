import asyncio
import logging, messeges, search_state, buy_state, comment_state, catalog_state, aioschedule

import aiogram.utils.exceptions
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import mail
from messeges import MESSEGES
from aiogram.types import ParseMode

import keyboards, database

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
schedule_logger = logging.getLogger('schedule')
schedule_logger.setLevel(level=logging.ERROR)

bot = Bot (
    #1753605795:AAE_zCdn82CKMqNwk5N4oGthFt7h3FBqYO4 test
    #1752058019:AAGzucvWZN6SDSd-i_1Xa-dxggYA_TFEpWw realese
    token = '1752058019:AAGzucvWZN6SDSd-i_1Xa-dxggYA_TFEpWw', parse_mode = ParseMode.HTML
)
dp = Dispatcher(
    bot=bot, storage=MemoryStorage()
)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    database.createTemp(message.from_user.id)
    await message.answer(MESSEGES["Hello"], reply_markup=keyboards.getMainKeyboard(),
                               disable_notification=True)
    database.setHello(message.from_user.id, True)

@dp.callback_query_handler()
async def process_callback_kb(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data[:10] == "addComment":
        database.tempSetOrder(callback_query.from_user.id, data[10:])
        await bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Add_comment"],
                               reply_markup=keyboards.getNothingKeyboard(),
                               disable_notification=True)
        await comment_state.AddComment.first()
    if data[:11] == "cancelOrder":
        await bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Confirm_delete"],
                               reply_markup=keyboards.getConfirmDeleteKeyboard(data[11:]),
                               disable_notification=True)
    if data[:13] == "confirmDelete":
        for job in buy_state.scheduler.get_jobs():
            if job.id == data[13:]:
                buy_state.scheduler.remove_job(job_id=data[13:])

        await bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Deleted"],
                               reply_markup=keyboards.getMainKeyboard(),
                               disable_notification=True)

        o = database.dataGetAll(data[13:])
        parfume = database.getParfume(o[1])
        mail.sendEmail(messeges.createEmailDeleteMessage(o[9], parfume[0], parfume[1], parfume[3], o[5], o[2], o[3],
                                                         o[4], o[6], o[7], o[8]))
        database.plusCount(parfume[1])
        database.dataDelete(data[13:])
    if data[:2] == "no":
        await bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Not deleted"],
                               reply_markup=keyboards.getMainKeyboard(),
                               disable_notification=True)
    if (data[:6] == "delete"):
        buy_state.scheduler.remove_job(job_id="delete" + data[6:])
        await buy_state.deleteOrder(callback_query.from_user.id, data[6:], callback_query.bot)
    elif (data[:2] == "ok"):
        await bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Ok"],
                               disable_notification=True)
        buy_state.scheduler.remove_job(job_id="delete" + data[2:])
        dataBase = database.dataGetAll(data[2:])
        parfume = database.getParfume(dataBase[1])
        email = messeges.createEmailMessage(dataBase[9], parfume[0], parfume[1], parfume[3], dataBase[5], dataBase[2], dataBase[3],
                                            dataBase[4], dataBase[6], dataBase[7], callback_query.from_user.id)
        mail.sendEmail(email)

@dp.message_handler(content_types=types.ContentType.TEXT)
async def do_echo(message:types.Message):
    database.dataClear(message.from_user.id)
    if message.text == 'Каталог 📙':
        await message.answer(MESSEGES["Сhoose_sex"], reply_markup=keyboards.getSexKeyboard(),
                               disable_notification=True)
        await catalog_state.CatalogState.first()
        database.setHello(message.from_user.id, False)
    elif message.text == "Заказы 📖":
        orders = database.dataGetOrders(message.from_user.id)
        if orders == []:
            await message.answer(MESSEGES["No_orders"])
        for o in reversed(orders):
            parfume = database.getParfume(o[1])
            await message.answer(messeges.createOrderMessage(o[9], parfume[0], parfume[1], parfume[3], o[5], o[2], o[3],
                                                             o[4], o[6], o[7], o[8], parfume[9], parfume[8]),
                                 reply_markup=keyboards.getOrderKeyboard(o[9]),
                               disable_notification=True)
            database.setHello(message.from_user.id, False)
    elif message.text == "Поиск 🔎":
        await message.answer(MESSEGES["Start_search"], reply_markup=keyboards.getMenuKeyboard(),
                               disable_notification=True)
        await search_state.Search.first()
        database.setHello(message.from_user.id, False)
    elif message.text == "Наши гарантии ⭐️":
        await message.answer(MESSEGES["Warranties"], reply_markup=keyboards.getMainKeyboard(),
                               disable_notification=True)
    elif message.text == "Контакты 📱":
        await message.answer(MESSEGES["Contacts"], reply_markup=keyboards.getMainKeyboard(),
                               disable_notification=True)
    elif message.text == "Инструкции 📋️":
        await message.answer(MESSEGES["Guide"], reply_markup=keyboards.getMainKeyboard(), disable_notification=True)

async def checkTrack():
    orders = database.dataGetOrders()
    for o in orders:
        if o[10] == 0 and o[8] != None:
            await bot.send_message(chat_id=o[0], text=messeges.createTrackMessage(o[9], o[8]))
            database.dataSetNotificationSent(o[9])

async def scheduler():
    aioschedule.every(1).minutes.do(checkTrack)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())
    ids = database.tempGetChatIDs()

    for id in ids:
        if database.getHello(id[0]) == False:
            try:
              await bot.send_message(chat_id=id[0], text=MESSEGES["Hello"], reply_markup=keyboards.getMainKeyboard(),
                                 disable_notification=True)
              database.setHello(id[0], True)
            except aiogram.utils.exceptions.BotBlocked:
              None

def main():
    buy_state.scheduler.start()
    catalog_state.register_handlers_food(dp)
    search_state.register_handlers_food(dp)
    buy_state.register_handlers_food(dp)
    comment_state.register_handlers_food(dp)
    executor.start_polling(
        dispatcher=dp, skip_updates=False, on_startup=on_startup
    )

if __name__ == '__main__':
    main()
