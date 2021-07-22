
import requests
import json
import datetime
import sqlite3
import csv

def initSQL():
    cn = sqlite3.connect("solardata")
    return cn


cn = initSQL()
cur = cn.cursor()
data = cur.execute("select dt, kw from generation where DATE(dt) =  DATE('now','+10 Hour' )  ;")

with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['dt', 'dw'])
    writer.writerows(data)

