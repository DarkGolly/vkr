from flask import Flask, request
from pyais import decode, NMEAMessage
from pyais.stream import ByteStream

app = Flask(__name__)

@app.route("/")
def hello_world():
    data = ["!AIVDM,2,1,2,A,53Kt>r02BF18ta0>220eDm1Dh622222222222216D8T:F79V0ATUH31A8888,0*51",
            "!AIVDM,2,2,2,A,88888888880,2*26"]
    res = NMEAMessage.assemble_from_iterable(
        messages=[
            NMEAMessage(str.encode(data[0])),
            NMEAMessage(str.encode(data[1]))
        ]
    ).decode().to_json()
    return res
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
            print(res)
        else:
            decoded = decode(splitData[0])
            as_dict = decoded.asdict()
            print(as_dict)
        return f'The data you sent was: {data}'
    else:
        return 'Unsupported Media Type', 415

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
