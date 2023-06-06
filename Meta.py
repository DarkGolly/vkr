from Ship import Ship


class Meta(Ship):
    msg_type, repeat = None, None
    ais_version, draught = None, None
    imo, callsign = None, None
    shipname, ship_type = None, None
    to_bow, to_stern = None, None
    to_port, to_starboard = None, None
    epfd, month = None, None
    day, hour = None, None
    minute, destination = None, None
    dte, spare_1 = None, None

    def __init__(self, list):
        super().__init__(list)
        self.msg_type = list[17]
        self.repeat = list[18]
        self.mmsi = list[19]
        self.ais_version = list[20]
        self.imo = list[21]
        self.callsign = list[22]
        self.shipname = list[23]
        self.ship_type = list[24]
        self.to_bow = list[25]
        self.to_stern = list[26]
        self.to_port = list[27]
        self.to_starboard = list[28]
        self.epfd = list[29]
        self.month = list[30]
        self.day = list[31]
        self.hour = list[32]
        self.minute = list[33]
        self.draught = list[34]
        self.destination = list[35]
        self.dte = list[36]
        self.spare_1 = list[37]

