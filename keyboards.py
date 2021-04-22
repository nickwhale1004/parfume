from aiogram.types import ReplyKeyboardRemove,\
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import database

def getMainKeyboard():
    button_katalog = KeyboardButton('Каталог 📙')
    button_search = KeyboardButton('Поиск 🔎')
    button_orders = KeyboardButton('Заказы 📖')
    button_about = KeyboardButton('Контакты 📱')
    button_ask = KeyboardButton('Инструкции 📋️')
    button_garanties = KeyboardButton('Наши гарантии ⭐️')
    return ReplyKeyboardMarkup(resize_keyboard=True).row(button_katalog, button_orders,button_search).add(button_ask, button_garanties).add(button_about)

def getSexKeyboard():
    buttonBack = KeyboardButton("⬆️ Назад")
    button_man = KeyboardButton("️🧔🏻 Мужской")
    button_woman = KeyboardButton("👩🏻 ‍Женский")
    button_unisex = KeyboardButton("🐰 Не важно")
    return ReplyKeyboardMarkup(resize_keyboard=True).add(buttonBack).add(button_man).add(button_woman).add(button_unisex)

def getCatalogKeyboard(sex = "u"):
    headers = database.getHeaders(sex)
    catalogKeyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    buttonBack = KeyboardButton("⬆️ Назад ⬆️")
    catalogKeyboard.add(buttonBack)
    for i in headers:
        catalogKeyboard.add(KeyboardButton(f"🌟 {i[0]} 🌟"))
    return catalogKeyboard

def getParfumesKeyboard(header, sex = "u"):
    names = database.getNames(header, sex)
    namesKeyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    buttonBack = KeyboardButton("⬆️ Назад ⬆️")
    namesKeyboard.add(buttonBack)
    for i in names:
        namesKeyboard.add(KeyboardButton(f"🩸 {i[0]} 🩸"))
    return namesKeyboard

def getBuyKeyboard(name):
    parfume = database.getParfume(name)
    inlineKeyboard = InlineKeyboardMarkup()
    buyButton = InlineKeyboardButton("Оформить заказ: " + str(parfume[3]) + " руб", callback_data="buy" + parfume[1])
    seePhotoButton = InlineKeyboardButton("Посмотреть все фото", callback_data="see"+parfume[1])
    backButton = InlineKeyboardButton("Назад", callback_data="back")
    buttonCancel = InlineKeyboardButton("Меню", callback_data="cancel")
    inlineKeyboard.add(buyButton).add(seePhotoButton).add(buttonCancel, backButton)
    return inlineKeyboard

def getCancelKeyboard():
    buttonCancel = InlineKeyboardButton("Меню", callback_data="cancel")
    buttonBack = InlineKeyboardButton("Назад", callback_data="back")
    return InlineKeyboardMarkup().add(buttonCancel, buttonBack)

def getCommentKeyboard():
    buttonNo = InlineKeyboardButton("Не нужен", callback_data="no")
    buttonBack = InlineKeyboardButton("Назад", callback_data="back")
    buttonCancel = InlineKeyboardButton("Меню", callback_data="cancel")
    return InlineKeyboardMarkup().add(buttonNo).add(buttonCancel, buttonBack)

def getConfirmKeyboard():
    buttonYes = InlineKeyboardButton("Подтверждаю", callback_data="confirm")
    buttonNo = InlineKeyboardButton("Заново", callback_data="repeat")
    buttonCancel = InlineKeyboardButton("Меню", callback_data="cancel")
    return InlineKeyboardMarkup().add(buttonYes).add(buttonCancel, buttonNo)

def getOrderKeyboard(order):
    buttonAdd = InlineKeyboardButton("Добавить комментарий", callback_data="addComment"+str(order))
    buttonCancel = InlineKeyboardButton("Отменить заказ", callback_data="cancelOrder"+str(order))
    return InlineKeyboardMarkup().add(buttonAdd).add(buttonCancel)

def getNothingKeyboard():
    buttonNothing = InlineKeyboardButton("Ничего", callback_data="nothing")
    return InlineKeyboardMarkup().add(buttonNothing)

def getMenuKeyboard():
    buttonPupblic = InlineKeyboardButton("Канал", url="https://t.me/parfumediscount")
    buttonCancel = InlineKeyboardButton("Меню", callback_data="cancel")
    return InlineKeyboardMarkup().add(buttonPupblic, buttonCancel)

def getConfirmDeleteKeyboard(order):
    buttonYes = InlineKeyboardButton("Да", callback_data="confirmDelete"+str(order))
    buttonNo = InlineKeyboardButton("Нет", callback_data="no")
    return InlineKeyboardMarkup().add(buttonYes, buttonNo)

def getCheckAgainKeyboard(order):
    buttonYes = InlineKeyboardButton("Да", callback_data="ok" + str(order))
    buttonNo = InlineKeyboardButton("Нет", callback_data="delete" + str(order))
    return InlineKeyboardMarkup().add(buttonYes, buttonNo)

def getLastKeyboard():
    buttonYes = InlineKeyboardButton("Использовать", callback_data="yes" )
    buttonNo = InlineKeyboardButton("Нет", callback_data="no")
    return InlineKeyboardMarkup().add(buttonYes, buttonNo)