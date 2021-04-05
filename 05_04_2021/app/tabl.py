
import sqlite3
import os


def log():
    conn = sqlite3.connect("DB/elevator")
    cursor = conn.cursor().execute("select * from log")
    result = cursor.fetchall()
    print(result)
    return result
    #cursor.close()
