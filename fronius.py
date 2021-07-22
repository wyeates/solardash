import requests
import json
import datetime
import sqlite3
import csv
def initSQL():
    cn = sqlite3.connect("solardata")
    return cn


date = datetime.date.today()
dt = datetime.datetime.combine(date, datetime.datetime.min.time())
t1 =  date + datetime.timedelta(days=1)
today = date.strftime("%d.%m.%Y")
tomorrow = t1.strftime("%d.%m.%Y")
# datedate.strftime("%d.%m.%y")
getstring = f"http://192.168.50.5/solar_api/v1/GetArchiveData.cgi?Scope=System&StartDate={today}&EndDate={tomorrow}&Channel=TimeSpanInSec&Channel=EnergyReal_WAC_Sum_Produced"
response = requests.get(getstring, timeout=40)
j_resp = json.loads(response.text)

data = j_resp['Body']['Data']['inverter/1']['Data']['EnergyReal_WAC_Sum_Produced']['Values']
cn = initSQL()
cur = cn.cursor()
for k in data:
    timecapture = str(dt+datetime.timedelta(seconds=int(k)))
    inserttime = str(datetime.datetime.now())
    genval = float(data[k])*12
    print(timecapture,float(data[k])*12)
    query = f"""INSERT INTO generation VALUES ('{timecapture}',{genval},'{inserttime}')
            ON CONFLICT (dt)
            DO UPDATE set (kw, lastupdated)
                = (EXCLUDED.kw,
                EXCLUDED.lastupdated)"""
    cur.execute(query)
cn.commit()


data = cur.execute("select dt, kw from generation where DATE(dt) =  DATE('now','+10 Hour' ) order by dt  ;")

with open('generation.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['dt', 'dw'])
    writer.writerows(data)


cur.close()


