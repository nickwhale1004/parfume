from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from bot import bot

import catalog_state
import database, mail, messeges, keyboards
from messeges import MESSEGES

scheduler = AsyncIOScheduler()

class OrderParfume(StatesGroup):
    chooseMan = State()
    chooseCity = State()
    chooseAdress = State()
    chooseIndex = State()
    chooseContacts = State()
    chooseComment = State()
    confirmOrder = State()

async def choose_man(message: types.Message, state: FSMContext):
    database.dataSetMan(message.text, message.from_user.id)
    await message.answer(text=MESSEGES["Choose_city"], reply_markup=keyboards.getCancelKeyboard())
    await OrderParfume.next()

async def choose_city(message: types.Message, state: FSMContext):
    database.dataSetCity(message.text, message.from_user.id)
    await message.answer(MESSEGES["Choose_adress"], reply_markup=keyboards.getCancelKeyboard())
    await OrderParfume.next()

async def choose_adress(message: types.Message, state: FSMContext):
    database.dataSetAdress(message.text, message.from_user.id)
    await message.answer(MESSEGES["Choose_index"], reply_markup=keyboards.getCancelKeyboard())
    await OrderParfume.next()

async def choose_index(message: types.Message, state: FSMContext):
    database.dataSetIndex(int(message.text), message.from_user.id)
    await message.answer(MESSEGES["Choose_contacts"], reply_markup=keyboards.getCancelKeyboard())
    await OrderParfume.next()

async def choose_contacts(message: types.Message, state: FSMContext):
    database.dataSetContacts(message.text, message.from_user.id)
    await message.answer(MESSEGES["Choose_comment"], reply_markup=keyboards.getCommentKeyboard())
    await OrderParfume.next()

async def choose_comment(message: types.Message, state: FSMContext):
    database.dataSetComment(message.text, message.from_user.id)
    await message.answer(MESSEGES["Confirm_order"])
    data = database.dataGet(message.from_user.id)
    parfume = database.getParfume(data[1])
    await message.answer(messeges.createConfrimMessage(data[9], parfume[0], parfume[1], parfume[3], data[5], data[2], data[3], data[4],
                                          data[6], data[7], parfume[9]), reply_markup=keyboards.getConfirmKeyboard())

async def deleteOrder(chat_id, order):
    await bot.send_message(chat_id=chat_id, text=MESSEGES["Deleted"],
                           reply_markup=keyboards.getMainKeyboard())
    database.dataDelete(order)

async def checkAgain(chat_id, order, header, name):
    my_date = datetime.now() + timedelta(hours=24)
    scheduler.add_job(deleteOrder, "date", run_date=my_date, args=(chat_id, order), id="delete"+str(order))
    await bot.send_message(chat_id=chat_id, text=messeges.createCheckAgainMessage(order, header, name),
                           reply_markup=keyboards.getCheckAgainKeyboard(order))

async def inline(callback_query: types.CallbackQuery, state: FSMContext):
    if (callback_query.data == "no"):
        database.dataSetComment("Нет", callback_query.from_user.id)
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id, text=(MESSEGES["Confirm_order"]))
        data = database.dataGet(callback_query.from_user.id)
        parfume = database.getParfume(data[1])
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id, text=
            messeges.createConfrimMessage(data[9], parfume[0], parfume[1], parfume[3], data[5], data[2], data[3], data[4],
                                          data[6], data[7], parfume[9]), reply_markup=keyboards.getConfirmKeyboard())
    elif (callback_query.data == "confirm"):
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Confirmed"],
                                              reply_markup=keyboards.getMainKeyboard())
        data = database.dataGet(callback_query.from_user.id)
        my_date = datetime.now() + timedelta(hours=1)
        scheduler.add_job(checkAgain, "date", run_date=my_date, args=(callback_query.from_user.id, data[9],
                                                                      database.getParfume(data[1])[0],
                                                                      data[1]), id=str(data[9]))

        await state.finish()
    elif (callback_query.data == "repeat"):
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Choose_man"],
                               reply_markup=keyboards.getCancelKeyboard())
        database.dataClear(callback_query.from_user.id)
        await OrderParfume.first()
    elif (callback_query.data == "back"):
        if (await state.get_state() == OrderParfume.chooseMan.state) :
            parfume = database.getParfume(database.dataGet(callback_query.from_user.id)[1])
            await callback_query.bot.send_photo(chat_id=callback_query.from_user.id, photo=parfume[4],
                                                caption=messeges.createParfumeMessage(parfume),
                                    reply_markup=keyboards.getBuyKeyboard(database.dataGet(callback_query.from_user.id)[1]))
            await state.finish()
            await catalog_state.CatalogState.last()
            return
        elif (await state.get_state() == OrderParfume.chooseCity.state) :
            await callback_query.bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Choose_man"],
                                   reply_markup=keyboards.getCancelKeyboard())
        elif (await state.get_state() == OrderParfume.chooseAdress.state):
            await callback_query.bot.send_message(chat_id=callback_query.from_user.id,text=MESSEGES["Choose_city"],
                                                  reply_markup=keyboards.getCancelKeyboard())
        elif (await state.get_state() == OrderParfume.chooseIndex.state):
            await callback_query.bot.send_message(chat_id=callback_query.from_user.id,text=MESSEGES["Choose_adress"],
                                                  reply_markup=keyboards.getCancelKeyboard())
        elif (await state.get_state() == OrderParfume.chooseContacts.state):
            await callback_query.bot.send_message(chat_id=callback_query.from_user.id,text=MESSEGES["Choose_index"],
                                                  reply_markup=keyboards.getCancelKeyboard())
        elif (await state.get_state() == OrderParfume.chooseComment.state):
            await callback_query.bot.send_message(chat_id=callback_query.from_user.id,text=MESSEGES["Choose_contacts"],
                                                  reply_markup=keyboards.getCancelKeyboard())
        await OrderParfume.previous()
    elif(callback_query.data == "cancel"):
        database.dataDelete(database.dataGet(callback_query.from_user.id)[9])
        await state.finish()
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Hello"],
                                          reply_markup=keyboards.getMainKeyboard())

def register_handlers_food(dp: Dispatcher):
    dp.register_callback_query_handler(inline, state=OrderParfume)
    dp.register_message_handler(choose_man, state=OrderParfume.chooseMan)
    dp.register_message_handler(choose_city, state=OrderParfume.chooseCity)
    dp.register_message_handler(choose_adress, state=OrderParfume.chooseAdress)
    dp.register_message_handler(choose_index, state=OrderParfume.chooseIndex)
    dp.register_message_handler(choose_contacts, state=OrderParfume.chooseContacts)
    dp.register_message_handler(choose_comment, state=OrderParfume.chooseComment)