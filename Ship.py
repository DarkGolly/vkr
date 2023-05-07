
class Ship:
    msg_type, repeat = None, None
    mmsi, status = None, None
    turn, speed = None, None
    accuracy, lon = None, None
    lat, course = None, None
    heading, second = None, None
    maneuver, spare_1 = None, None
    raim, radio = None, None
    date_rec = None, None
    list_db = None, None
    def __init__(self, list):
        self.msg_type = list[0]
        self.repeat = list[1]
        self.mmsi = list[2]
        self.status = list[3]
        self.turn = list[4]
        self.speed = list[5]
        self.accuracy = list[6]
        self.lon = list[7]
        self.lat = list[8]
        self.course = list[9]
        self.heading = list[10]
        self.second = list[11]
        self.maneuver = list[12]
        self.spare_1 = list[13]
        self.raim = list[14]
        self.radio = list[15]
        self.date_rec = list[16]
