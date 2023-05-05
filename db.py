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

    def add_data(self, dict):
        columns = ', '.join(dict.keys())
        if dict['msg_type']==1:
            columns += ", date_rec"
            replacement_dict = {"turn": repr(dict["turn"]),"status": repr(dict["status"]),
                                "maneuver": repr(dict["maneuver"]),
                                "spare_1": 0, }
            dict.update(replacement_dict)
            result = ', '.join([repr(val) for val in dict.values()]) + ', ' +repr(str(date.today()))
            query = f'INSERT INTO {"ais_ships"} ({columns}) VALUES ({result})'
        elif dict['msg_type']==5:
            replacement_dict = {"ship_type": repr(dict["ship_type"]),
                                "epfd": repr(dict["epfd"]),
                                "spare_1": 0, }
            dict.update(replacement_dict)
            result = ', '.join([repr(val) for val in dict.values()])
            query = f'INSERT INTO {"ais_destinations"} ({columns}) VALUES ({result})'
        self.cursor.execute(query, dict)
        self.connection.commit()