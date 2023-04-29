import sqlite3

class DataBase:
    connection = None
    def __init__(self):
        try:
            self.connection = sqlite3.connect('navigacions_data.db')
            print("База данных успешно подключена к SQLite")
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)

    def execute_query(self):
        cursor = self.connection.cursor()
        sqlite_select_query = "select sqlite_version();"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print("Версия базы данных SQLite: ", record)

    def add_data(self, dict):
        cursor = self.connection.cursor()
        columns = ', '.join(dict.keys())
        placeholders = ':' + ', :'.join(dict.keys())
        query = f'INSERT INTO {"ais_data"} ({columns}) VALUES ({placeholders})'
        cursor.execute(query, dict)
        self.connection.commit()