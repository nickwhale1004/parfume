from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
import database, messeges, keyboards, buy_state
from messeges import MESSEGES

class CatalogState(StatesGroup):
    choose_sex = State()
    choose_header = State()
    choose_parfume = State()
    see_parfume = State()

async def choose_sex(message: types.Message, state: FSMContext):
    if message.text == "⬆️ Назад":
        await message.answer(MESSEGES["Hello"], reply_markup=keyboards.getMainKeyboard(),
                               disable_notification=True)
        database.setHello(message.from_user.id, True)
        await state.finish()
        return
    elif message.text == "👩🏻 ‍Женский":
        database.tempSetSex(message.from_user.id, "w")
    elif message.text == "️🧔🏻 Мужской":
        database.tempSetSex(message.from_user.id, "m")
    else:
        database.tempSetSex(message.from_user.id, "u")

    await message.answer(MESSEGES["Catalog"], reply_markup=keyboards.getCatalogKeyboard(database.tempGetSex(message.from_user.id)),
                               disable_notification=True)
    await CatalogState.next()

async def choose_header(message: types.Message, state: FSMContext):
    if message.text == "⬆️ Назад ⬆️":
        await message.answer(MESSEGES["Сhoose_sex"], reply_markup=keyboards.getSexKeyboard(),
                               disable_notification=True)
        await CatalogState.previous()
        return
    header = message.text[2:message.text.rfind('🌟') - 1]
    database.tempSetHeader(message.from_user.id, header)
    await message.answer(MESSEGES["Names"], reply_markup=keyboards.getParfumesKeyboard(header, database.tempGetSex(message.from_user.id)),
                               disable_notification=True)
    await CatalogState.next()

async def choose_parfume(message: types.Message, state: FSMContext):
    if message.text == "⬆️ Назад ⬆️":
        await message.answer(MESSEGES["Catalog"], reply_markup=keyboards.getCatalogKeyboard(database.tempGetSex(message.from_user.id)),
                               disable_notification=True)
        await CatalogState.previous()
        return
    name = message.text[2:message.text.rfind('🩸') - 1]
    parfume = database.getParfume(name)
    await message.answer_photo(parfume[4], caption=messeges.createParfumeMessage(parfume),
                               reply_markup=keyboards.getBuyKeyboard(name),
                               disable_notification=True)
    await CatalogState.next()

async def inline(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    if data[:3] == "see":
        parfume = database.getParfume(data[3:])
        mediaGroup = types.MediaGroup()
        mediaGroup.attach_photo(parfume[5])
        mediaGroup.attach_photo(parfume[6])
        await callback_query.bot.send_media_group(chat_id=callback_query.from_user.id, media=mediaGroup,
                               disable_notification=True)
    if data[:3] == "buy":
        database.setOrderNumber(callback_query.from_user.id)
        database.dataSetName(data[3:], callback_query.from_user.id)
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Choose_man"],
                               reply_markup=keyboards.getCancelKeyboard(),
                               disable_notification=True)
        await buy_state.OrderParfume.first()
    if data[:4] == "back":
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Names"],
                               reply_markup=keyboards.getParfumesKeyboard(database.tempGetHeader(callback_query.from_user.id),
                                                                          database.tempGetSex(callback_query.from_user.id)),
                               disable_notification=True)
        await CatalogState.previous()
    if data == "cancel":
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Hello"],
                                              reply_markup=keyboards.getMainKeyboard(),
                               disable_notification=True)
        database.setHello(callback_query.from_user.id, True)
        await state.finish()

def register_handlers_food(dp: Dispatcher):
    dp.register_callback_query_handler(inline, state=CatalogState)
    dp.register_message_handler(choose_sex, state=CatalogState.choose_sex)
    dp.register_message_handler(choose_header, state=CatalogState.choose_header)
    dp.register_message_handler(choose_parfume, state=CatalogState.choose_parfume)