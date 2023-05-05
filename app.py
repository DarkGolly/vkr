from flask import Flask
from flask_sock import Sock
from pyais import decode, NMEAMessage

from db import DataBase

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
sock = Sock(app)
@app.route("/")
def index():
    db = DataBase()
    return db.execute_query()


@sock.route('/ais')
def ais(ws):
    while True:
        text = ws.receive()
        encoding_data(text)
        ws.send("Данные пришли!")

def encoding_data(data):
    splitData = data.split()
    if len(splitData) > 1:
        as_dict = NMEAMessage.assemble_from_iterable(
            messages=[
                NMEAMessage(str.encode(splitData[0])),
                NMEAMessage(str.encode(splitData[1]))
            ]
        ).decode().asdict()
        print(splitData)
        print("------")
        print(as_dict)
    else:
        decoded = decode(splitData[0])
        as_dict = decoded.asdict()
        print(splitData)
        print("-------")
        print(as_dict)
    db = DataBase()
    db.add_data(as_dict)

