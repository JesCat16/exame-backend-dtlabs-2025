import requests
import json
import time
import datetime

url = "http://127.0.0.1:8000/dataIntern/"
urlUpdate = "http://127.0.0.1:8000/updateServerStatus/"
urlServers = "http://127.0.0.1:8000/health"

while True:
    servers = requests.get(urlServers).text
    listjsons = servers.split()
    listServers = []
    for serv in listjsons:
        currentDate= datetime.datetime.now()
        jsonS = json.loads(serv)
        for item in jsonS:
            ulid= item.get("server_ulid")
            lastIoTDataInput = requests.get(url+f"{ulid}").text
            lastIoTDataInputJson = json.loads(lastIoTDataInput)
            if lastIoTDataInputJson == None:
                requests.put(urlUpdate+f"{ulid}/offline")
            else:
                LastDateInput = lastIoTDataInputJson.get("timestamp")
                data_format = "%Y-%m-%dT%H:%M:%SZ"
                converted_LastDateInput = datetime.datetime.strptime(LastDateInput, data_format)
                if currentDate.date() != converted_LastDateInput.date():
                    requests.put(urlUpdate+f"{ulid}/offline")
                else:
                    DateInFormat = currentDate.strftime("%Y-%m-%dT%H:%M:%SZ")
                    converted_DateInFormat = datetime.datetime.strptime(DateInFormat, data_format)
                    WaitingFor = currentDate - converted_LastDateInput 
                    if WaitingFor.total_seconds() > 10:
                        requests.put(urlUpdate+f"{ulid}/offline")
                    else:
                        requests.put(urlUpdate+f"{ulid}/online")
        time.sleep(10)