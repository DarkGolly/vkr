from flask import Flask, render_template
from flask_sock import Sock
app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
sock = Sock(app)
@app.route('/')
def index():
    return render_template("This is VKR!")
@sock.route('/ais')
def ais(ws):
    while True:
        text = ws.receive()
        ws.send("Данные пришли!")
        print(text)
        print("---------------")


#if __name__ == '__main__':
#    app.run(host='0.0.0.0', debug=True)
