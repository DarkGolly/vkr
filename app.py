from flask import Flask, request
from pyais import decode
app = Flask(__name__)

@app.route('/post-handler', methods=['POST'])
def handle_post_request():
    if request.content_type == 'text/plain':
        data = request.get_data(as_text=True)
        # process the data
        print(data)
        print("--------------------")
        decoded = decode(data)
        as_dict = decoded.asdict()
        print(as_dict)
        return f'The data you sent was: {data}'
    else:
        return 'Unsupported Media Type', 415

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
