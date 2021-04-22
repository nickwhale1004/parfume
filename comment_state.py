from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher

import buy_state
import database, mail, messeges, keyboards
from messeges import MESSEGES

class AddComment(StatesGroup):
    addComment = State()

async def add_comment(message: types.Message, state: FSMContext):
    database.dataChangeComment(message.text, database.tempGetOrder(message.from_user.id))
    await message.answer(text=MESSEGES["Added_comment"],
                               disable_notification=True)
    o = database.dataGetAll(database.tempGetOrder(message.from_user.id))
    parfume = database.getParfume(o[1])
    mail.sendEmail(
        messeges.createEmailEditMessage(o[9], parfume[0], parfume[1], parfume[3], o[5], o[2], o[3], o[4], o[6],
                                          o[7], o[8]))
    await state.finish()

async def inline(callback_query: types.CallbackQuery, state :FSMContext):
    data = callback_query.data
    if(data == "nothing"):
        await state.finish()
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Not_added"],
                               disable_notification=True)
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
    dp.register_callback_query_handler(inline, state=AddComment)
    dp.register_message_handler(add_comment, state=AddComment)