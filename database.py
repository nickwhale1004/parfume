import sqlite3

conn = sqlite3.connect("pafumes.db")
cursor = conn.cursor()


def createTables():
    cursor.execute("""CREATE TABLE parfumes
                         (header text, name text, description text,
                          price int, media_link1 text, media_link2 text, media_link3 text, count int, number int, sex text)
                      """)
    cursor.execute("""CREATE TABLE headers (header text) """)
    cursor.execute("""CREATE TABLE data
                        (chat_id int, name text, city text, adress text, 'index' int, man text, contacts text, comment text,
                        track text, orders int, notification int)
                      """)
    cursor.execute("""CREATE TABLE temp (chat_id int, number int, number2 int, sex text, header text, orders int)""")

def createTemp(chat_id):
    cursor.execute("SELECT * FROM temp WHERE chat_id = (?)", (chat_id,))
    data = cursor.fetchall()
    if(data == []):
        cursor.execute("INSERT INTO temp (chat_id) VALUES (?)", (chat_id,))
        conn.commit()

def getParfumeNumber():
    cursor.execute("SELECT * FROM temp WHERE chat_id = -1")
    data = cursor.fetchall()
    cursor.execute(f"UPDATE temp SET number2 = (?) WHERE chat_id = -1", (data[0][2] + 1,))
    conn.commit()
    if data == None:
        return []
    return data[0][2]

def getNewOrderNumber():
    cursor.execute("SELECT * FROM temp WHERE chat_id = -1")
    data = cursor.fetchall()
    cursor.execute(f"UPDATE temp SET number = (?) WHERE chat_id = -1", (data[0][1] + 1,))
    conn.commit()
    if data == None:
        return []
    return data[0][1]

def setOrderNumber(chat_id):
    cursor.execute("UPDATE temp SET number = (?) WHERE chat_id = (?)", (getNewOrderNumber(), chat_id,))
    conn.commit()

def getOrderNumber(chat_id):
    cursor.execute(f"SELECT * FROM temp WHERE chat_id = '{chat_id}'")
    data = cursor.fetchall()
    if data == None:
        return []
    return data[0][1]

def dataSetName(name, chat_id):
    cursor.execute("INSERT INTO data (chat_id, name, orders, notification) VALUES (?, ?, ?, ?)", (chat_id, name, getOrderNumber(chat_id), 0))
    conn.commit()

def dataSetCity(city, chat_id):
    cursor.execute(f"UPDATE data SET city = (?) WHERE orders = '{getOrderNumber(chat_id)}'", (city,))
    conn.commit()

def dataSetAdress(adress, chat_id):
    cursor.execute(f"UPDATE data SET adress = (?) WHERE orders = '{getOrderNumber(chat_id)}'", (adress,))
    conn.commit()

def dataSetIndex(index, chat_id):
    cursor.execute(f"UPDATE data SET 'index' = (?) WHERE orders = '{getOrderNumber(chat_id)}'", (index,))
    conn.commit()

def dataSetMan(man, chat_id):
    cursor.execute(f"UPDATE data SET man = (?) WHERE orders = '{getOrderNumber(chat_id)}'", (man,))
    conn.commit()

def dataSetContacts(contacts, chat_id):
    cursor.execute(f"UPDATE data SET contacts = (?) WHERE orders = '{getOrderNumber(chat_id)}'", (contacts,))
    conn.commit()

def dataSetComment(comment, chat_id):
    cursor.execute(f"UPDATE data SET comment = (?) WHERE orders = '{getOrderNumber(chat_id)}'", (comment,))
    conn.commit()

def dataChangeComment(comment, order):
    old = dataGetAll(order)[7]
    cursor.execute(f"UPDATE data SET comment = (?) WHERE orders = '{order}'", (old+'\n'+comment,))
    conn.commit()

def dataSetTrack(track, order):
    cursor.execute(f"UPDATE data SET track = (?) WHERE orders = '{order}'", (track,))
    conn.commit()

def dataSetNotificationSent(order):
    cursor.execute(f"UPDATE data SET notification = '1' WHERE orders = '{order}'")
    conn.commit()

def dataGetOrdersNames():
    cursor.execute("SELECT orders, track FROM data")
    orders = cursor.fetchall()
    return orders

def dataGetOrderByNumber(number):
    cursor.execute(f"SELECT * FROM data WHERE orders = {number}")
    orders = cursor.fetchall()
    return orders

def dataGetOrders(chat_id = ""):
    if(chat_id != ""):
        cursor.execute(f"SELECT * FROM data WHERE chat_id = {chat_id}")
    else:
        cursor.execute("SELECT * FROM data")
    orders = cursor.fetchall()
    return orders

def dataGetTracks(order):
    cursor.execute("SELECT track FROM data WHERE orders = (?)", (order,))
    tracks = cursor.fetchall()
    return tracks

def dataGetAll(order):
    cursor.execute("SELECT * FROM data WHERE orders = (?)", (order,))
    data = cursor.fetchall()
    if data == None:
        return []
    return data[0]

def dataGet(chat_id):
    cursor.execute("SELECT * FROM data WHERE orders = (?)", (getOrderNumber(chat_id),))
    data = cursor.fetchall()
    if data == None:
        return []
    return data[0]

def dataClear(chat_id):
    cursor.execute(f"SELECT * FROM data WHERE chat_id = {chat_id}")
    data = cursor.fetchall()
    for i in data:
        if (i[1] == None or i[2] == None or i[3] == None or i[4] == None or i[5] == None or i[6] == None or i[7] == None):
            cursor.execute(f"DELETE FROM data WHERE orders = {i[9]}")
            conn.commit()

def dataDelete(order):
    cursor.execute("DELETE FROM data WHERE orders = (?)", (order,))
    conn.commit()

def addParfume(header, name, description, price, media_link1, media_link2, media_link3, count, sex):
    cursor.execute(
        "INSERT INTO parfumes (header, name, description, price, media_link1, media_link2, media_link3, count, number, sex)"
        " VALUES (?,?,?,?,?,?,?,?,?, ?)",
        (header, name, description, price, media_link1, media_link2, media_link3, count, getParfumeNumber(), sex))
    conn.commit()

def addHeader(header):
    cursor.execute("INSERT INTO headers (header) VALUES (?)", (header,))
    conn.commit()

def getParfume(name):
    cursor.execute("SELECT * FROM parfumes WHERE name = (?)", (name,))
    parfume = cursor.fetchall()
    if parfume == None:
        return []
    return parfume[0]

def getParfumeByNumber(number):
    cursor.execute("SELECT * FROM parfumes WHERE number = (?)", (number,))
    parfume = cursor.fetchall()
    if parfume == []:
        return []
    return parfume[0]

def getHeaders(sex = "u"):
    cursor.execute("SELECT header FROM headers")
    headers = cursor.fetchall()
    if headers == None:
        return []
    if sex != "u":
        filtredHeaders = []
        for h in headers:
            cursor.execute("SELECT name FROM parfumes WHERE header = (?) AND (sex = (?) OR sex = 'u') AND count <> 0", (h[0], sex,))
            names = cursor.fetchall()
            if names != []:
               filtredHeaders.append(h)
        return filtredHeaders
    return headers


def getNames(header, sex = "u"):
    if (sex == "u"):
        cursor.execute("SELECT name FROM parfumes WHERE header = (?) AND count <> 0", (header,))
    else:
        cursor.execute("SELECT name FROM parfumes WHERE header = (?) AND (sex = (?) OR sex = 'u') AND count <> 0",
                       (header, sex))
    names = cursor.fetchall()
    if names == None:
        return []
    return names

def deleteParfume(name):
    cursor.execute("DELETE FROM parfumes WHERE name = (?)", (name,))
    conn.commit()
    headers = getHeaders()
    for h in headers:
        names = getNames(h[0])
        if names == []:
            cursor.execute("DELETE FROM headers WHERE header = (?)", (h[0],))
            conn.commit()

def tempSetSex(chat_id, sex):
    cursor.execute(f"UPDATE temp SET sex = (?) WHERE chat_id = (?)", (sex, chat_id))
    conn.commit()

def tempGetSex(chat_id):
    cursor.execute(f"SELECT sex FROM temp  WHERE chat_id = (?)", (chat_id,))
    sex = cursor.fetchall()
    if sex == None:
        return []
    return sex[0][0]

def tempSetHeader(chat_id, header):
    cursor.execute(f"UPDATE temp SET header = (?) WHERE chat_id = (?)", (header, chat_id))
    conn.commit()

def tempGetHeader(chat_id):
    cursor.execute(f"SELECT header FROM temp  WHERE chat_id = (?)", (chat_id,))
    header = cursor.fetchall()
    if header == None:
        return []
    return header[0][0]

def tempSetOrder(chat_id, order):
    cursor.execute(f"UPDATE temp SET orders = (?) WHERE chat_id = (?)", (order, chat_id))
    conn.commit()

def tempGetOrder(chat_id):
    cursor.execute(f"SELECT orders FROM temp WHERE chat_id = (?)", (chat_id,))
    order = cursor.fetchall()
    if order == None:
        return []
    return order[0][0]

def tempGetChatIDs():
    cursor.execute(f"SELECT chat_id FROM temp WHERE chat_id <> '-1'")
    ids = cursor.fetchall()
    if ids == None:
        return []
    return ids

def setHello(chat_id, value: bool):
    res = 0
    if value:
        res = 1
    cursor.execute(f"UPDATE temp SET hello = (?) WHERE chat_id = (?)", (res, chat_id))
    conn.commit()

def getHello(chat_id):
    cursor.execute(f"SELECT hello FROM temp WHERE chat_id = (?)", (chat_id,))
    hello = cursor.fetchall()
    if (hello[0][0] == None): return False
    if (hello[0][0] == 0): return False
    return True

def changePriceAndCount(name, price, count):
    cursor.execute(f"UPDATE parfumes SET price = (?), count = (?) WHERE name = (?)", (price, count, name))
    conn.commit()

def minusCount(name):
    cursor.execute(f"SELECT count FROM parfumes WHERE name = (?)", (name,))
    count = cursor.fetchall()[0][0]
    cursor.execute(f"UPDATE parfumes SET count = (?) WHERE name = (?)", (count - 1, name))
    conn.commit()

def plusCount(name):
    cursor.execute(f"SELECT count FROM parfumes WHERE name = (?)", (name,))
    count = cursor.fetchall()[0][0]
    cursor.execute(f"UPDATE parfumes SET count = (?) WHERE name = (?)", (count + 1, name))
    conn.commit()