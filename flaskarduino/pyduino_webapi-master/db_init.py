import sqlite3
import os


class ConnectDB():
    def __init__(self):

        try:
            os.remove("DB\\floorDB.db")
        except:
            print("DB first time create")

        conn = sqlite3.connect("DB\\floorDB.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()


        cursor.execute("create table User (id integer primary key, login varchar unique, root int, hash int)")
        cursor.execute("create table Program (id integer primary key, state varchar, floor int, time varchar)")

        cursor.close()

    # подключаемся к бд
    def connect_db(self):
        try:
            conn = sqlite3.connect("DB\\floorDB.db")
            return conn
        except:
            print("БД не найдена")


create_db = ConnectDB()
