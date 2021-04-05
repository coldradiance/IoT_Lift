import sqlite3
import os
from db_init import ConnectDB


temp1 = ConnectDB()
conn = temp1.connect_db()
cursor = conn.cursor()

sqlite_insert_with_param = """INSERT INTO User
                             (id, login, root, hash)
                             VALUES (?, ?, ?, ?);"""

data_tuple = (1, "2ww", 2, 3232)
cursor.execute(sqlite_insert_with_param, data_tuple)



