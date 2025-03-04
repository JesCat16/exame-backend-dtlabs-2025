import requests
import json
import time
import datetime
#This worker is used to see if server is online and alters it's status
url = "http://127.0.0.1:8000/dataIntern/"
urlUpdate = "http://127.0.0.1:8000/updateServerStatus/"
urlServers = "http://127.0.0.1:8000/health"

while True:
    #Get server list
    servers = requests.get(urlServers).text
    listjsons = servers.split()
    listServers = []
    for serv in listjsons:
        currentDate= datetime.datetime.now()
        jsonS = json.loads(serv)
        for item in jsonS:
            #get the server's ulid
            ulid= item.get("server_ulid")
            #See last data placed in DataBase with same ulid
            lastIoTDataInput = requests.get(url+f"{ulid}").text
            lastIoTDataInputJson = json.loads(lastIoTDataInput)
            #if there are none
            if lastIoTDataInputJson == None:
                #Set server as offline
                requests.put(urlUpdate+f"{ulid}/offline")
            else:
                #Continue to see if server is online
                LastDateInput = lastIoTDataInputJson.get("timestamp")
                data_format = "%Y-%m-%dT%H:%M:%SZ"
                #Get last timestamp
                converted_LastDateInput = datetime.datetime.strptime(LastDateInput, data_format)
                #See if timestamp is olders than current day
                if currentDate.date() != converted_LastDateInput.date():
                    #If it is the status is offline
                    requests.put(urlUpdate+f"{ulid}/offline")
                else:
                    #Now worker will see if the last data input was 10 second ago
                    DateInFormat = currentDate.strftime("%Y-%m-%dT%H:%M:%SZ")
                    converted_DateInFormat = datetime.datetime.strptime(DateInFormat, data_format)
                    WaitingFor = currentDate - converted_LastDateInput 
                    #if it is the server is now offline 
                    if WaitingFor.total_seconds() > 10:
                        requests.put(urlUpdate+f"{ulid}/offline")
                    else:
                        #if not the server is now online 
                        requests.put(urlUpdate+f"{ulid}/online")
        #Worker will pass through this process every 10 seconds 
        time.sleep(10)