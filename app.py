from flask import Flask, request
from pyais import decode, NMEAMessage

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
        #print(as_dict)

        msg_2_part_0 = b'!AIVDM,2,1,9,A,538CQ>02A;h?D9QC800pu8@T>0P4l9E8L0000017Ah:;;5r50Ahm5;C0,0*0F'
        msg_2_part_1 = b'!AIVDM,2,2,9,A,F@V@00000000000,2*3D'

        msg = NMEAMessage.assemble_from_iterable(
            messages=[
                NMEAMessage(msg_2_part_0),
                NMEAMessage(msg_2_part_1)
            ]
        ).decode().to_json()
        print(msg)
        return f'The data you sent was: {data}'
    else:
        return 'Unsupported Media Type', 415

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
