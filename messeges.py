MESSEGES = {
    "Hello": """<b>Привет!</b>
Я бот, с помощью которого, Вы сможете выбрать себе парфюм высшего качества!
Заходите в меню и выбирайте что Вам интересно.""",

    "Catalog": "Можете ознакомиться с нашим ассортиментом товаров!",

    "Names": "Вот что у нас сейчас есть.",

    "Choose_last": "Хотите использовать данные доставки из предыдущего заказа?",

    "Choosed_last" : "Хорошо, Вам осталось только добавить комментарий или нажать 'нет'",

    "Сhoose_sex": "Уточните, какой именно парфюм Вам нужен?",

    "Choose_man": """---<b>ОФОРМЛЕНИЕ ЗАКАЗА</b>---\n
<b>1. Укажите Ваши ФИО:</b>
Пример: <i>Петренко Иван Иванович</i>""",

    "Choose_city": """<b>2. Укажите Ваш город:</b>
Пример: <i>Москва</i>""",

    "Choose_adress": """<b>3. Укажите адрес доставки:</b>
Пример: <i>ул. Московская 134а, 23 кв.</i>""",

    "Choose_index": """<b>4. Укажите индекс:</b>
Пример: <i>101000</i>""",

    "Choose_contacts": """<b>5. Укажите Ваш номер телефона или Email для связи:</b>
Пример: <i>88005555800</i>""",

    "Choose_comment": """<b>6. Укажите комментарий или нажмите "нет":</b>
Пример: <i>Нужно в кол-ве 2-х штук</i>""",

    "Confirm_order": "Подтвердите, пожалуйста, Ваш заказ!",

    "Confirmed": """<b>Подтверждено!</b>
Спасибо за заказ! После отправки мы вышлем Вам номер отслеживания. Его можно будет найти в меню <i>"заказы"</i>.""",

    "Deleted": "<b>Ваш заказ отменён!</b> Нам жаль, что Вы отказались от покупки. "
"Можете отправить Ваши пожелания нам в Телеграм по номеру, указанному в контактах. Будем рады видеть Вас снова!",

    "Confirm_delete": "Вы уверены, что хотите отменить Ваш заказ?",

    "Not deleted": "Мы сохранили Ваш заказ в целости и сохранности.",

    "Add_comment": "Напишите, чтобы Вы хотели добавить:",

    "Added_comment": "<b>Комментарий успешно сохранён!</b>",

    "Not_added": "Новый комментарий <b>не был добавлен</b>",

    "No_orders": "Вы пока не совершали покупок. Вы можете оформить заказ с помощью каталога или поиска в главном меню!",

    "Start_search": """<b>Напишите номер товара, который хотите посмотреть.</b>
<i>Номера товаров можно найти в нашем <b>телеграм-канале,</b> где мы публикуем актуальную информацию об ассортименте товаров.</i>""",

    "Error_search": "К сожалению, мы не нашли товара с таким номером.",

    "Warranties": "<b>Мы - опытная команда,</b> занимающаяся продажей парфюмерии уже <b>больше 10 лет.</b>"
                  " За долгое время работы мы отобрали<b> лучших поставщиков</b> <i>Luxe-копий</i> брендов и оригинальных <i>tester'ов</i>"
                  "\n🌟️ Каждый товар поставляется в <b>оригинальной коробе</b>, на которую нанесены <b>подлинные UPC-коды</b>, а это значит, что Вы можете подарить брендовый парфюм и он будет отображаться на сайте компании как подлинный."
                  "\n🌟️️ Мы отправляем товары <b>наложенным платежом</b>, так что Вы оплатите свой заказ <b>только</b> после фактического получения."
                  "\n🌟️️ К каждому товару в течение нескольких дней мы прикрепляем <b>track-номер</b> для отслеживания, чтобы Вы не беспокоились о сроках доставки."
                  "\n🌟️️ В магазине представлены <b>настоящие фотографии товаров.</b>",
    "Contacts": "В случае возникновения технических неполадок или дополнительных вопросов, напишите нам:"
                "\n<b>Помощь:</b> <a href='https://t.me/parfumemanager'>написать</a>"
                "\n<b>Telegram-канал:</b> <a href='https://t.me/parfumediscount'>посмотреть</a>",
    "Ok": "Отлично, тогда мы готовим его к отправке!",
    "Guide": "<b>Имейте в виду, что:</b>"
             "\n🔎<b>1.</b> Вы можете воспользоваться <b>поиском,</b> введя <b>номер товара,</b> его можно посмотреть в <i>карточке товара</i> или <i>нашем канале.</i>"
             "\n📝<b>2.</b> Если Вы хотите заказать товар в кол-ве <b>нескольких штук,</b> можете указать это <b>в комментарии,</b> оформляя заказ."
             "\n🪄<b>3.</b> Чтобы не вводить <i>одни и те же данные</i> доставки каждый раз, можете нажать на кнопку <b>'использовать информацию предыдущего заказа'.</b>"
             "\n📦<b>4.</b> Если Вы закажите <i>несколько разных</i> товаров мы вышлем их <b>одной</b> посылкой."
             "\n🎬<b>5.</b> Снимайте распаковку товара <b>на видео,</b> это поможет Вам в спорных ситуациях, если Вы столкнетесь с браком."
             "\n💰️<b>6.</b> Мы отправляем <b>наложенным платежом,</b> так что Вы оплатите товар <b>на почте.</b>"
}
def createCheckAgainMessage(order, header, name):
    return f"Во избежание случайных заказов, мы выслали Вам это сообщение. Вы действительно ждёте свой заказ №{order} ({header} {name})?"

def createParfumeMessage(parfume):
    sexText = ""
    if parfume[9] == "u":
        sexText = "Унисекс"
    elif parfume[9] == "m":
        sexText = "Мужской"
    elif parfume[9] == "w":
        sexText = "Женский"
    return ("<b>"+parfume[0] + " " + parfume[1] + '</b><i>\n'
            + parfume[2] + "</i>" +
            "\n<b>Тип: </b>" + sexText +
            "\n<b>В наличии: </b> " + str(parfume[7]) + " шт. (код: " + str(parfume[8]) + ')')

def createConfrimMessage(order, header, name, price, man, city, adress, index, contacts, comments, sex):
    sexText = ""
    if sex == "u":
        sexText = "Унисекс"
    elif sex == "m":
        sexText = "Мужской"
    elif sex == "w":
        sexText = "Женский"
    return f"""---<b>Заказ № {order}--- </b>
<b>Товар: </b><i>{header} {name}</i>
<b>Тип: </b><i>{sexText}</i>
<b>К оплате: </b><i>{price}</i> руб.
<b>ФИО: </b><i>{man}</i>
<b>Город: </b><i>{city}</i>
<b>Адрес: </b><i>{adress}</i>
<b>Индекс: </b><i>{index}</i>
<b>Номер телефона (email): </b><i>{contacts}</i>
<b>Комментарий: </b><i>{comments}</i>
    """

def createEmailMessage(order, header, name, price, man, city, adress, index, contacts, comments, chat_id):
    return f"""-------------Заказ № {order} -------------
Товар: {header} {name}
К оплате: {price} руб.
ФИО: {man}
Город: {city}
Адрес: {adress}
Индекс: {index}
Номер телефона (email): {contacts}
Комментарий: {comments}
ID: {chat_id}
    """

def createEmailDeleteMessage(order, header, name, price, man, city, adress, index, contacts, comments, track):
    xtrack = track
    if track == None:
        xtrack = "Ожидается"
    return f"""-------------Заказ № {order} -------------
    -------------    ОТМЕНЁН    -------------
    Товар: {header} {name}
    К оплате: {price} руб.
    ФИО: {man}
    Город: {city}
    Адрес: {adress}
    Индекс: {index}
    Номер телефона (email): {contacts}
    Комментарий: {comments}
    Трек-номер: {xtrack}
        """

def createEmailEditMessage(order, header, name, price, man, city, adress, index, contacts, comments, track):
    xtrack = track
    if track == None:
        xtrack = "Ожидается"
    return f"""-------------Заказ № {order} -------------
    -------------    ИЗМЕНЁН    -------------
    Товар: {header} {name}
    К оплате: {price} руб.
    ФИО: {man}
    Город: {city}
    Адрес: {adress}
    Индекс: {index}
    Номер телефона (email): {contacts}
    Комментарий: {comments}
    Трек-номер: {xtrack}
        """

def createOrderMessage(order, header, name, price, man, city, adress, index, contacts, comments, track, sex, code):
    sexText = ""
    if sex == "u":
        sexText = "Унисекс"
    elif sex == "m":
        sexText = "Мужской"
    elif sex == "w":
        sexText = "Женский"
    xtrack = track
    if track == None :
        xtrack = "Ожидается"
    return f"""<b>---Заказ № {order} ---</b>
<b>Товар:</b> {header} {name}
<b>Код товара: </b>{code}
<b>Тип: </b>{sexText}
<b>К оплате:</b> {price} руб.
<b>ФИО: </b>{man}
<b>Город:</b> {city}
<b>Адрес: </b>{adress}
<b>Индекс:</b> {index}
<b>Номер телефона (email):</b> {contacts}
<b>Комментарий:</b> {comments}
<b>Трек-номер:</b> {xtrack}
    """

def createTrackMessage(order, track):
    return f"К Вашему заказу №{order} был подключен track-номер {track}"