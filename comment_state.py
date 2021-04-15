from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
import database, mail, messeges, keyboards
from messeges import MESSEGES

class AddComment(StatesGroup):
    addComment = State()

async def add_comment(message: types.Message, state: FSMContext):
    database.dataChangeComment(message.text, database.tempGetOrder(message.from_user.id))
    await message.answer(text=MESSEGES["Added_comment"])
    o = database.dataGetAll(database.tempGetOrder(message.from_user.id))
    parfume = database.getParfume(o[1])
    mail.sendEmail(
        messeges.createEmailEditMessage(o[9], parfume[0], parfume[1], parfume[3], o[5], o[2], o[3], o[4], o[6],
                                          o[7], o[8]))
    await state.finish()

async def inline(callback_query: types.CallbackQuery, state :FSMContext):
    if(callback_query.data == "nothing"):
        await state.finish()
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id, text=MESSEGES["Not_added"])

def register_handlers_food(dp: Dispatcher):
    dp.register_callback_query_handler(inline, state=AddComment)
    dp.register_message_handler(add_comment, state=AddComment)