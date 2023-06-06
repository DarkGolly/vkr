from datetime import date
import os
import psycopg2


class DataBase:
    connection = None
    cursor = None

    def __init__(self):
        try:
            self.connection = psycopg2.connect(host='localhost',
                                               database='ais_db',
                                               user=os.environ['DB_USERNAME'],
                                               password=os.environ['DB_PASSWORD'])
            self.cursor = self.connection.cursor()
            print("База данных успешно подключена к Psql")
        except psycopg2.Error as error:
            print("Ошибка при подключении к Psql", error)

    def execute_query_status(self):
        query = "SELECT DISTINCT status FROM ais_ships;"
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        new = []
        for i in record:
            i = str(i).replace('(', '')
            i = str(i).replace(')', '')
            i = str(i).replace(',', '')
            new.append(i)
        return new

    def execute_query_twise(self, params):
        print(params)
        new = {}
        query = "SELECT * FROM ais_ships JOIN ais_meta ON ais_ships.mmsi = ais_meta.mmsi WHERE "
        for param in params:
            if params[param] != '':
                new.update({param:params[param]})
        query += ' AND '.join([f'{condition} = {params[condition]}' for condition in new])
        if len(new)==0:
            return {}
        try:
            self.cursor.execute(query)
            record = self.cursor.fetchall()
            print("Запрос успешен!")
            return record
        except EnvironmentError:
            print('Ошибка запроса!')



    def execute_query_all(self):
        sqlite_select_query = "select * from ais_ships;"
        self.cursor.execute(sqlite_select_query)
        record = self.cursor.fetchall()
        #print(record)
        print("Запрос успешен!")
        return record

    def add_data(self, dict):
        columns = ', '.join(dict.keys())
        query = None
        if dict['msg_type'] < 5:
            columns += ", date_rec"
            replacement_dict = {"turn": repr(dict["turn"]), "status": repr(dict["status"]),
                                "maneuver": repr(dict["maneuver"]),
                                "spare_1": 0, }
            dict.update(replacement_dict)
            result = ', '.join([repr(val) for val in dict.values()]) + ', ' + repr(str(date.today()))
            self.cursor.execute(f"SELECT mmsi FROM ais_ships WHERE mmsi = {dict['mmsi']}")
            existing_object = self.cursor.fetchone()
            #'msg_type, repeat, mmsi, status, turn, speed, accuracy, lon, lat, course, heading, second, maneuver, spare_1, raim, radio, date_rec'
            if existing_object:
                # Объект найден, выполняем обновление
                self.cursor.execute("UPDATE ais_ships SET msg_type = %s, repeat = %s, status = %s, turn = %s, speed"
                                    " = %s, accuracy = %s, lon = %s, lat = %s, course = %s, heading = %s, second = %s,"
                                    " maneuver = %s, spare_1 = %s, raim = %s, radio = %s, date_rec = %s WHERE mmsi ="
                                    " %s RETURNING mmsi", (dict['msg_type'], dict['repeat'], dict['status'], dict['turn'], dict['speed'],
                                    dict['accuracy'], dict['lon'], dict['lat'], dict['course'], dict['heading'], dict['second'], dict['maneuver'],
                                    dict['spare_1'], dict['raim'], dict['radio'], str(date.today()), dict['mmsi']))
            else:
                query = f'INSERT INTO {"ais_ships"} ({columns}) VALUES ({result})'
                self.cursor.execute(query, dict)

        elif dict['msg_type'] >= 5:
            replacement_dict = {"ship_type": repr(dict["ship_type"]),
                                "epfd": repr(dict["epfd"]),
                                "spare_1": 0, }
            dict.update(replacement_dict)
            result = ', '.join([repr(val) for val in dict.values()])
            self.cursor.execute(f"SELECT mmsi FROM ais_meta WHERE mmsi = {dict['mmsi']}")
            existing_object = self.cursor.fetchone()
            if existing_object:
                self.cursor.execute("UPDATE ais_meta SET msg_type = %s, repeat = %s, ais_version = %s, imo = %s, callsign"
                                    " = %s, shipname = %s, ship_type = %s, to_bow = %s, to_stern = %s, to_port = %s, to_starboard = %s,"
                                    " epfd = %s, month = %s, day = %s, hour = %s, minute = %s, draught= %s, destination"
                                    "= %s, dte= %s, spare_1= %s  WHERE mmsi = %s RETURNING mmsi",
                                    (dict['msg_type'], dict['repeat'], dict['ais_version'], dict['imo'], dict['callsign'],
                                     dict['shipname'], dict['ship_type'], dict['to_bow'], dict['to_stern'], dict['to_port'],
                                     dict['to_starboard'], dict['epfd'], dict['month'], dict['day'], dict['hour'],
                                     dict['minute'], dict['draught'], dict['destination'], dict['dte'], dict['spare_1'], dict['mmsi']))
            else:
                query = f'INSERT INTO {"ais_meta"} ({columns}) VALUES ({result})'
                self.cursor.execute(query, dict)
        self.connection.commit()

    def execute_query_one(self, param):
        query = f"select * from ais_ships where mmsi = {param};"
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        print("Запрос успешен!")
        return record

    def execute_query_on(self, params):
        print(params)
        new = {}
        query = "SELECT * FROM ais_ships WHERE "
        for param in params:
            if params[param] != '':
                new.update({param: params[param]})
        query += ' AND '.join([f'{condition} = {params[condition]}' for condition in new])
        if len(new)==0:
            return {}
        try:
            self.cursor.execute(query)
            record = self.cursor.fetchall()
            print("Запрос успешен!")
            return record
        except EnvironmentError:
            print('Ошибка запроса!')