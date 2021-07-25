import requests
import json
import datetime
import sqlite3
import csv
from datetime import  timedelta
def initSQL():
    cn = sqlite3.connect("solardata")
    return cn

# date = datetime.date.today()
# date = datetime.date(2020,4,1)


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = datetime.date(2020, 4, 1)
end_date = datetime.date(2021, 7, 24)

for single_date in daterange(start_date, end_date):
    print(single_date.strftime("%Y-%m-%d"))
    dt = datetime.datetime.combine(single_date, datetime.datetime.min.time())
    t1 =  single_date + datetime.timedelta(days=1)
    today = single_date.strftime("%d.%m.%Y")
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


    # data = cur.execute("select dt, kw from generation where DATE(dt) =  DATE('now','+10 Hour' ) order by dt  ;")

    # with open('generation.csv', 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(['dt', 'kw'])
    #     writer.writerows(data)


    cur.close()


