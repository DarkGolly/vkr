from flask import Flask, request
from pyais import decode, NMEAMessage
from pyais.stream import ByteStream

from db import DataBase

app = Flask(__name__)

@app.route("/")
def hello_world():
    db = DataBase()
    db.execute_query()
    return "This is VKR."
@app.route('/post-handler', methods=['POST'])
def handle_post_request():
    if request.content_type == 'text/plain':
        data = request.get_data(as_text=True)
        splitData = data.split()
        if len(splitData) > 1:
            res = NMEAMessage.assemble_from_iterable(
                messages=[
                    NMEAMessage(str.encode(splitData[0])),
                    NMEAMessage(str.encode(splitData[1]))
                ]
            ).decode().asdict()
            print(splitData)
            print("------")
            print(res)
        else:
            decoded = decode(splitData[0])
            as_dict = decoded.asdict()
            print(splitData)
            print("-------")
            print(as_dict)
        db = DataBase()
        db.add_data(as_dict)
        return f'The data you sent was: {data}'
    else:
        return 'Unsupported Media Type', 415

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
