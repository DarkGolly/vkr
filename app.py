import socketserver

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/main')
def main():  # put application's code here
    return 'Workplace!'


if __name__ == '__main__':
    #MyServer.server_program()
    app.run()



