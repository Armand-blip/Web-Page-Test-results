import requests
import wget
import urllib.request
import datetime
import time

url = "https://www.iberogast.es/"
apiKey = "our api key"

while True:
 finalURL = "http://www.webpagetest.org/runtest.php?url="+url+"&k="+apiKey+"&f=JSON"
 res = requests.get(finalURL)
 json = res.json()
 csvURL = json['data']['summaryCSV']

 with open("testresponse.json","a") as file:
     file.write("\n\n--New entry {}-- \n\n".format(datetime.datetime.now()))
     file.write(str(json))
 print("Response JSON saved in file testresponse.json")
 time.sleep(86400)
