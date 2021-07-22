
import sqlite3
db = sqlite3.connect('solardata')
cursor = db.cursor()
cursor.execute("create table generation (dt timestamp, kw float,lastupdated timestamp)")

# cursor.execute("drop table generation;")