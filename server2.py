from http.server import HTTPServer, BaseHTTPRequestHandler
import json

import bot
import database


#create
#add:*header:*name:*description:*price:*media_link1:*media_link2:*media_link3:*count
#getheaders
#get:*header
#delete:*name
#new:*header
#getorders
#gettracks:*order
#track:*number:*order
#getpricecount:*name

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def addParfume(self, header, name, description, price, media_link1, media_link2, media_link3, count, sex):
        database.addParfume(header, name, description, price, media_link1, media_link2, media_link3, count, sex)
        self.send_response(200)
        self.wfile.write("Added!".encode())
        self.end_headers()
        headers = database.getHeaders()
        for h in headers:
            if h[0] == header:
                return
        database.addHeader(header)

    def sendHeaders(self):
        headers = database.getHeaders()
        jsonObj = json.dumps(headers, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
        if headers == []:
            self.send_response(200)
            self.end_headers()
        else:
            self.wfile.write(jsonObj.encode())

    def sendOrders(self):
        orders = database.dataGetOrdersNames()
        jsonObj = json.dumps(orders, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
        if orders == []:
            self.send_response(200)
            self.end_headers()
        else:
            self.wfile.write(jsonObj.encode())

    def getParfumesNames(self, header):
        names = database.getNames(header)
        jsonObj = json.dumps(names, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
        self.wfile.write(jsonObj.encode())

    def getParfumesPriceAndCount(self, name):
        parfume = database.getParfume(name)
        jsonObj = json.dumps([(parfume[3],), (parfume[7],)], sort_keys=False, indent=4, separators=(',', ': '),
                             ensure_ascii=False)
        self.wfile.write(jsonObj.encode())

    def deleteByName(self, name):
        database.deleteParfume(name)
        self.send_response(200)
        self.wfile.write("Deleted!".encode())
        self.end_headers()

    def addHeader(self, header):
        database.addHeader(header)
        self.send_response(200)
        self.wfile.write("added!".encode())
        self.end_headers()

    def addTrack(self, track, order):
        database.dataSetTrack(track, order)
        self.send_response(200)
        self.wfile.write("added!".encode())
        self.end_headers()

    def getTracks(self, order):
        names = database.dataGetTracks(order)
        jsonObj = json.dumps(names, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
        self.wfile.write(jsonObj.encode())

    def changePriceAndCount(self, name, price, count):
        database.changePriceAndCount(name, price, count)
        self.send_response(200)
        self.wfile.write("added!".encode())
        self.end_headers()

    # определяем метод `do_GET`
    def do_GET(self):
        print(self.path)
        request = self.path[1:]
        if (request == "create"):
            database.createTables()
        if (request == "getheaders"):
            self.sendHeaders()
        if(request == "getorders"):
            self.sendOrders()
        if (request[:3] == "new"):
            print(request[5:])
            self.addHeader(request[5:])

    def do_POST(self):
        print(self.path)
        request = self.path[1:]
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        if (request[:6] == "delete"):
            jsonObj = json.loads(body.decode("utf-8"))
            self.deleteByName(jsonObj["name"])
        if (request[:4] == "get:"):
            jsonObj = json.loads(body.decode("utf-8"))
            self.getParfumesNames(jsonObj["header"])
            return
        if (request[:3] == "new"):
            jsonObj = json.loads(body.decode("utf-8"))
            print(jsonObj["header"])
            self.addHeader(jsonObj["header"])
        if (request[:3] == "add"):
            jsonObj = json.loads(body.decode("utf-8"))
            self.addParfume(jsonObj["header"], jsonObj["name"], jsonObj["description"], jsonObj["price"],
                            jsonObj["media_link1"], jsonObj["media_link2"], jsonObj["media_link3"], jsonObj["count"],
                            jsonObj["sex"])
            print(jsonObj["header"], jsonObj["name"], jsonObj["description"], jsonObj["price"],
                            jsonObj["media_link1"], jsonObj["media_link2"], jsonObj["media_link3"], jsonObj["count"])
        if (request[:5] == "track"):
            jsonObj = json.loads(body.decode("utf-8"))
            self.addTrack(jsonObj["number"], jsonObj["order"])
        if (request[:9] == "gettracks"):
            jsonObj = json.loads(body.decode("utf-8"))
            self.getTracks(jsonObj["order"])
        if (request[:13] == "getpricecount"):
            jsonObj = json.loads(body.decode("utf-8"))
            self.getParfumesPriceAndCount(jsonObj["name"])
        if (request[:16] == "changepricecount"):
            jsonObj = json.loads(body.decode("utf-8"))
            self.changePriceAndCount(jsonObj["name"], jsonObj["price"], jsonObj["count"])
        self.send_header('Content-type', 'text/html')


#194.67.105.184
httpd = HTTPServer(('194.67.105.184', 2000), SimpleHTTPRequestHandler)
httpd.serve_forever()