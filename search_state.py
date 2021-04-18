from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher

import catalog_state
import database, mail, messeges, keyboards
from messeges import MESSEGES

class Search(StatesGroup):
    getNumber = State()

async def get_number(message: types.Message, state: FSMContext):
    parfume = database.getParfumeByNumber(message.text)
    if parfume == []:
        await message.answer(MESSEGES["Error_search"], reply_markup=keyboards.getMainKeyboard(),
                               disable_notification=True)
    else:
        await state.finish()
        await catalog_state.CatalogState.last()
        await message.answer_photo(parfume[4], caption=messeges.createParfumeMessage(parfume),
                                reply_markup=keyboards.getBuyKeyboard(parfume[1]),
                               disable_notification=True)
        return
    await state.finish()

async def inline(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "cancel":
        await state.finish()
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Hello"],
                               reply_markup=keyboards.getMainKeyboard(),
                               disable_notification=True)

def register_handlers_food(dp: Dispatcher):
    dp.register_callback_query_handler(inline, state=Search)
    dp.register_message_handler(get_number, state=Search)


