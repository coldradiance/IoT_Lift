import sqlite3
import os
from db_init import ConnectDB

temp1 = ConnectDB()
conn = temp1.connect_db()
cursor = conn.cursor()

sql = "SELECT * from User"

cursor.execute(sql)