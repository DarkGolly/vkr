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

    def execute_query(self):
        sqlite_select_query = "select version();"
        self.cursor.execute(sqlite_select_query)
        record = self.cursor.fetchall()
        print("Версия базы данных Psql: ", record)
        return record

    def execute_query_all(self):
        sqlite_select_query = "select * from ais_ships;"
        self.cursor.execute(sqlite_select_query)
        record = self.cursor.fetchall()
        print(record)
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
            self.cursor.execute(f"SELECT mmsi, date_rec FROM ais_ships WHERE mmsi = {dict['mmsi']}")
            existing_object = self.cursor.fetchone()
            #'msg_type, repeat, mmsi, status, turn, speed, accuracy, lon, lat, course, heading, second, maneuver, spare_1, raim, radio, date_rec'
            if existing_object:
                # Объект найден, выполняем обновление
                self.cursor.execute("UPDATE ais_ships SET msg_type = %s, repeat = %s, status = %s, turn = %s, speed"
                                    " = %s, accuracy = %s, lon = %s, lat = %s, course = %s, heading = %s, second = %s,"
                                    " maneuver = %s, spare_1 = %s, raim = %s, radio = %s, date_rec = %s WHERE mmsi ="
                                    " %s RETURNING mmsi", (dict['msg_type'], dict['repeat'], dict['status'], dict['turn'], dict['speed'],
                                    dict['accuracy'], dict['lon'], dict['lat'], dict['course'], dict['heading'], dict['second'], dict['maneuver'],
                                    dict['spare_1'], dict['raim'], dict['radio'], existing_object[1], dict['mmsi']))

            else:
                query = f'INSERT INTO {"ais_ships"} ({columns}) VALUES ({result})'
                self.cursor.execute(query, dict)

        elif dict['msg_type'] >= 5:
            replacement_dict = {"ship_type": repr(dict["ship_type"]),
                                "epfd": repr(dict["epfd"]),
                                "spare_1": 0, }
            dict.update(replacement_dict)
            result = ', '.join([repr(val) for val in dict.values()])
            query = f'INSERT INTO {"ais_destinations"} ({columns}) VALUES ({result})'
            self.cursor.execute(query, dict)
        self.connection.commit()
