from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher

import buy_state
import catalog_state
import database, mail, messeges, keyboards
from messeges import MESSEGES

class Search(StatesGroup):
    getNumber = State()

async def get_number(message: types.Message, state: FSMContext):
    if(not message.text.isdigit()) :
        await message.answer(MESSEGES["Error_search"], reply_markup=types.ReplyKeyboardRemove(),
                             disable_notification=True)
        await message.answer(MESSEGES["Start_search"], reply_markup=keyboards.getMenuKeyboard(),
                             disable_notification=True)
        return
    parfume = database.getParfumeByNumber(message.text)
    if parfume == []:
        await message.answer(MESSEGES["Error_search"], reply_markup=types.ReplyKeyboardRemove(),
                               disable_notification=True)
        await message.answer(MESSEGES["Start_search"], reply_markup=keyboards.getMenuKeyboard(),
                             disable_notification=True)
    else:
        await state.finish()
        await catalog_state.CatalogState.last()
        await message.answer_photo(parfume[4], caption=messeges.createParfumeMessage(parfume),
                                reply_markup=keyboards.getBuyKeyboard(parfume[1]),
                               disable_notification=True)

async def inline(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data == "cancel":
        await state.finish()
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Hello"],
                               reply_markup=keyboards.getMainKeyboard(),
                               disable_notification=True)
        database.setHello(callback_query.from_user.id, True)
    if (data[:6] == "delete"):
        buy_state.scheduler.remove_job(job_id="delete" + data[6:])
        await buy_state.deleteOrder(callback_query.from_user.id, data[6:], callback_query.bot)
    elif (data[:2] == "ok"):
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Ok"],
                               disable_notification=True)
        buy_state.scheduler.remove_job(job_id="delete" + data[2:])
        dataBase = database.dataGetAll(data[2:])
        parfume = database.getParfume(dataBase[1])
        email = messeges.createEmailMessage(dataBase[9], parfume[0], parfume[1], parfume[3], dataBase[5], dataBase[2], dataBase[3],
                                            dataBase[4], dataBase[6], dataBase[7], callback_query.from_user.id)
        mail.sendEmail(email)

def register_handlers_food(dp: Dispatcher):
    dp.register_callback_query_handler(inline, state=Search)
    dp.register_message_handler(get_number, state=Search)


