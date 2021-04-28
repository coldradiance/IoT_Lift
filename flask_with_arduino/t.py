
import sqlite3
import os


conn = sqlite3.connect("DB/elevator.db")

floor = 'floor'
controlmode = 'controlmode'
timeStamp = '13:56:12'
dayStamp = '2021-04-26'

cursor = conn.cursor()
sql = "INSERT INTO log (floor, controlmode, timeStamp, dayStamp) VALUES (?,?,?,?)"
val = (floor, controlmode, timeStamp, dayStamp)
cursor.execute(sql, val)

conn.commit()


