from flask import Flask, request
app = Flask(__name__)


@app.route('/', methods=['POST'])
def process_post_request():
    if request.method == 'POST':
        data = request.form['data']
        # обрабатываем полученные данные
        return f'Received data: {data}'

@app.route('/main')
def main():  # put application's code here
    return 'Workplace!'


if __name__ == '__main__':
    #MyServer.server_program()
    app.run(host="0.0.0.0")



