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
        jsonS = json.loads(serv)
        print(jsonS[0])
        ulid= jsonS[0].get("server_ulid")
        lastIoTDataInput = requests.get(url+f"{ulid}").text
        print(lastIoTDataInput)
        lastIoTDataInputJson = json.loads(lastIoTDataInput)
        currentTime = time.time()
        currentDate= datetime.datetime.now()
        print(currentDate)
        LastDateInput = lastIoTDataInputJson.get("timestamp")
        data_format = "%Y-%m-%dT%H:%M:%SZ"
        converted_LastDateInput = datetime.datetime.strptime(LastDateInput, data_format)
        if currentDate > converted_LastDateInput:
            requests.put(urlUpdate+f"{ulid}/offline")
        else:
            LastTimeInput = converted_LastDateInput.time()
            print(LastTimeInput)
            converted_LastDateInput = datetime.strptime(LastTimeInput, "%H:%M:%S")
            LastsecondInput = converted_LastDateInput.hour * 3600 + converted_LastDateInput.minute * 60 + converted_LastDateInput.second
            WaitingFor = currentTime - converted_LastDateInput.time()
            if WaitingFor > 10:
                requests.put(urlUpdate+f"{ulid}/offline")
            requests.put(urlUpdate+f"{ulid}/online")
        time.sleep(10)