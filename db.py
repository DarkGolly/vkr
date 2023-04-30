import sqlite3

class DataBase:
    connection = None
    cursor = None
    def __init__(self):
        try:
            self.connection = sqlite3.connect('navigacions_data.db')
            self.cursor = self.connection.cursor()
            print("База данных успешно подключена к SQLite")
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)

    def execute_query(self):
        sqlite_select_query = "select sqlite_version();"
        self.cursor.execute(sqlite_select_query)
        record = self.cursor.fetchall()
        print("Версия базы данных SQLite: ", record)

    def add_data(self, dict):
        columns = ', '.join(dict.keys())
        placeholders = ':' + ', :'.join(dict.keys())
        query = f'INSERT INTO {"ais_data"} ({columns}) VALUES ({placeholders})'
        self.cursor.execute(query, dict)
        self.connection.commit()