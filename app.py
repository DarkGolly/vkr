from flask import Flask, render_template, request, url_for,redirect
from flask_sock import Sock
from pyais import decode, NMEAMessage

from Ship import Ship
from db import DataBase
from marker_maker import MarkersMaker

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# app.config['SECRET_KEY'] = 'secret!'

sock = Sock(app)


@app.route("/", methods=["POST", "GET"])
def index():
    map = MarkersMaker()
    #decoded = decode("!AIVDM,1,1,,A,144fk`1Oh5R:NvrRBCAlhE;V2000,0*47")
    #as_dict = decoded.asdict()
    #db = DataBase()
    #db.add_data(as_dict)
    map.plotMarkers(None, 'off')
    return render_template('index.html')#map.plotMarkers()

@app.route("/ship/<int:mmsi>")
def ship(mmsi):
    db = DataBase()
    dir = db.execute_query_one(mmsi)
    ship = Ship(dir[0])
    return render_template('ship.html', data=ship)

@app.route("/search", methods=["POST", "GET"])
def search():
    db = DataBase()
    records = db.execute_query_status()
    return render_template('search.html', recs=records)  # map.plotMarkers()@app.route("/search", methods=["POST", "GET"])

@app.route("/fast_mmsi", methods=["POST", "GET"])
def fast_mmsi():
    map = MarkersMaker()
    try:
        if request.method == 'POST' and request.form['mmsi'].isdigit():
            mmsi = request.form['mmsi']
        elif request.args.get('mmsi').isdigit():
            mmsi = request.args.get('mmsi')
    except:
        mmsi = 0
    if mmsi==0:
        map.plotMarkers(None, "off")
    else:
        map.plotMarker(mmsi)
    return render_template("index.html")
@app.route("/process_data", methods=['POST'])
def process_data():
    map = MarkersMaker()
    mmsi, callsign, shipname, IMO, status = None, None, None, None, None
    for key, value in request.form.items():
        if key == 'mmsi':
            if value == '':
                mmsi = ''
            else:
                mmsi = request.form['mmsi']
            continue
        elif key == 'status':
            if value == '':
                status = ''
            else:
                status = request.form['status']
            continue
    try:
        full = request.form['full']
    except:
        full = 'off'
        imo = ''
        callsign = ''
        shipname = ''

    if full == 'on':
        for key, value in request.form.items():
            if key == 'IMO':
                if value == '':
                    imo = ''
                else:
                    imo = request.form['IMO']
                continue
            elif key == 'callsign':
                if value == '':
                    callsign = ''
                else:
                    callsign = f"\'{request.form['callsign']}\'"
                continue
            elif key == 'name':
                if value == '':
                    shipname = ''
                else:
                    shipname = f"\'{request.form['name']}\'"
                continue
    map.plotMarkers({'ais_ships.mmsi': mmsi, 'ais_meta.shipname': f'{shipname}', 'ais_ships.status': f'{status}',
                     'ais_meta.callsign': f'{callsign}', 'ais_meta.imo': imo}, full)
    return render_template('index.html')


@sock.route('/ais')
def ais(ws):
    while True:
        text = ws.receive()
        ws.send("Данные пришли!")
        #print(text)
        encoding_data(text)



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
