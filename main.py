# -*- coding: utf-8 -*-

from wox import Wox
import requests
import json
import time
import threading
from datetime import datetime

class USDtoUAH(Wox):

    def query(self, param):
        q = param
        qs = q.split(' ')
        results = []
        r = self.req()
        if not q:
            time.sleep(1)
            for i in r[:-1]:
                results.append({
                        "Title": f"{i['ccy']} to {i['base_ccy']}",
                        "SubTitle": f"buy - {round(float(i['buy']),2)} sell - {round(float(i['sale']),2)}",
                        "IcoPath":"Images/app.png"
                })
                
            results.append({
                "Title": f"Last refresh - {datetime.fromtimestamp(int(r[4]['unix'])).strftime('%H:%M:%S %d-%m-%Y')}",
                "IcoPath":"Images/app.png"
            })
            return results

        elif qs[0] == 'usd':
            sm = qs[1]
            results.append({
                "Title": f"{r[0]['ccy']} to {r[0]['base_ccy']}",
                "SubTitle": f"buy - {round(float(r[0]['buy'])*float(sm),2)} sell - {round(float(r[0]['sale'])*float(sm),2)}",
                "IcoPath":"Images/app.png"
            })
            return results
        
        elif qs[0] == 'uah':
            sm = qs[1]
            for i in r[:-2]:
                results.append({
                        "Title": f"{i['base_ccy']} to {i['ccy']}",
                        "SubTitle": f"buy - {round(float(sm)/float(i['buy']),2)} sell - {round(float(sm)/float(i['sale']),2)}",
                        "IcoPath":"Images/app.png"
                })
            return results
     
        else:
            results.append({
                "Title": "!c (uah or usd)",
                "IcoPath":"Images/app.png"
            })
            return results
        


    def req(self):
        with open('cur.json') as json_file:
            r = json.load(json_file)
            
        unix = str(time.time()).split('.')[0]

        if int(unix) > int(r[4]['unix'])+3600:
            r = requests.get("https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11").json()
            r.append({'unix': str(unix)})
            with open('cur.json', 'w') as outfile:
                json.dump(r, outfile)
            return r
        else:
            return r

if __name__ == "__main__":
    USDtoUAH()



'''        elif q[0] == 'u':
            sm = q.split(' ')[1]
            results = []
            r = self.req()
            if isinstance(i, float):
                results.append({
                    "Title": f"e"
                })
            else:
                results.append({
                    "Title": f"uuuuuu"
                })
            return results'''