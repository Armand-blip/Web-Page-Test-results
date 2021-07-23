import requests
import wget
import urllib.request
import datetime
import time
import json
#import csv
from urllib.request import urlopen
import os
import pandas as pd
from datetime import date

today = date.today()
today_str=today.strftime('%m.%d.%Y')
today_str.replace('/','_')
# specify the columns of the dataframe
df = pd.DataFrame(columns = ['url','LCP','CLS','FCP','TBT','Doc. Comp. Time','summary','LCP_origin','CLS_origin','FCP_origin','TBT_origin','Doc. Comp. Time_origin','summary_origin'])

# read all the url's thatwant to test
with open('url.txt','r') as f:
    count=0
    for url in f:
        if url != "\n":  # control if the row is not empty from the text file
            url=url.strip("\n")
            apikey = "c7cb0683-6f4d-4fa2-9b42-f65550a34bac" #the key for making the test from wpt
            # specifying all the parameteres of the test and make the request for two different url's(iSF and Origin)
            param="ec2-eu-south-1:Chrome.4G" #Milano
            fvonly="1" # only first view
            akatop="akatop"

            finalurl = "http://www.webpagetest.org/runtest.php?url="+url+"&k="+apikey+"&fvonly="+fvonly+"&location="+param+"&f=json"
            res = requests.get(finalurl)
            json1 = res.json()

            finalurl_origin = "http://www.webpagetest.org/runtest.php?url="+url+"&k="+apikey+"&fvonly="+fvonly+"&location="+param+"&appendua="+akatop+"&f=json"
            res_origin = requests.get(finalurl_origin)
            json_origin = res_origin.json()

            # save the response in a json file
            with open("testresponse.json","a") as file:
                 file.write("\n\n--new entry {}-- \n\n".format(datetime.datetime.now()))
                 file.write(str(json1))
            print("response json1 saved in file testresponse.json")
        
            with open("testresponse.json","a") as file:
                 file.write("\n\n--new entry {}-- \n\n".format(datetime.datetime.now()))
                 file.write(str(json_origin))
            print("response json_origin saved in file testresponse.json")

            #control if the dict data exist in the response of the test
            if "data" in json1 and "data" in json_origin:
                data=json1['data']
                data_origin=json_origin['data']
                testId=data['testId']
                testId_origin=data_origin['testId']
                while True: # open a cycle in order to test and verify it the result is ready
                    response_json="https://www.webpagetest.org/testStatus.php?"+"test="+testId
                    res = requests.get(response_json)
                    json2 = res.json()
                    print(json2)

                    response_json="https://www.webpagetest.org/testStatus.php?"+"test="+testId_origin
                    res_origin = requests.get(response_json)
                    json2_origin = res_origin.json()
                    print(json2_origin)

                    # control if the result is succesfully taken
                    statusCode=json2['statusCode']
                    statusCode_origin=json2_origin['statusCode']
                    if statusCode==200 and statusCode_origin == 200:

                        jsonurl="https://www.webpagetest.org/jsonResult.php?"+"test="+testId
                        res_2 = requests.get(jsonurl)
                        json3 = res_2.json()
                        print(json3)

                        jsonurl_origin="https://www.webpagetest.org/jsonResult.php?"+"test="+testId_origin
                        res_2_origin = requests.get(jsonurl_origin)
                        json3_origin = res_2_origin.json()
                        print(json3_origin)
                        if "data" in json3 and "data" in json3_origin:
                            data_1=json3['data']
                            data_1_origin=json3_origin['data']
                            if "average" in data_1 and "average" in data_1_origin:
                                summary=data_1['summary']
                                url=data_1['url']
                                fcp=data_1['average']['firstView']['firstContentfulPaint']
                                si=data_1['average']['firstView']['SpeedIndex']
                                tbt=data_1['average']['firstView']['TotalBlockingTime']
                                lcp=data_1['average']['firstView']['chromeUserTiming.LargestContentfulPaint']
                                cls_1=data_1['average']['firstView']['chromeUserTiming.CumulativeLayoutShift']
                                cls=round(cls_1,3)
                                doc_time=data_1['average']['firstView']['docTime']
                            
                                summary_origin=data_1_origin['summary']
                                url_origin=data_1_origin['url']
                                fcp_origin=data_1_origin['average']['firstView']['firstContentfulPaint']
                                si_origin=data_1_origin['average']['firstView']['SpeedIndex']
                                tbt_origin=data_1_origin['average']['firstView']['TotalBlockingTime']
                                lcp_origin=data_1_origin['average']['firstView']['chromeUserTiming.LargestContentfulPaint']
                                cls_1_origin=data_1_origin['average']['firstView']['chromeUserTiming.CumulativeLayoutShift']
                                cls_origin=round(cls_1_origin,3)
                                doc_time_origin=data_1_origin['average']['firstView']['docTime']

                                # print all the desired values in console
                                print("The values for the page " +url+ " are:")
                                print("the value of lcp is:", lcp)
                                print("the value of cls is:", cls*1000)
                                print("the value of tbt is:", tbt)
                                print("the value of fcp is:", fcp)
                                print("the value of Doc. Comp. Time is:", doc_time)
                                #print("the value of si is:", si)
                                print("The origin values for the page " +url_origin+ " are:")
                                print("the value of lcp_origin is:", lcp_origin)
                                print("the value of cls_origin is:", cls_origin*1000)
                                print("the value of tbt_origin is:", tbt_origin)
                                print("the value of fcp_origin is:", fcp_origin)

                                print("the value of Doc. Comp. Time origin is:", doc_time_origin)
                                #print("the value of si_origin is:", si)

                                data = [url,lcp,cls*1000,fcp,tbt,doc_time,summary,lcp_origin,cls_origin*1000,fcp_origin,tbt_origin,doc_time_origin,summary_origin]
                                df.loc[count] = data
                                count=count+1
                                break
                            else:
                                print("Average does not exist in data dictionary")
                        else:
                            print("Data does not exist in json2 or json2_origin dictionary")
                    else:
                        time.sleep(30) #control every 30 seconds if the result is ready or not
        
    f.close()
    print("We have finished reading all the URL's, we need to close the file")




try:
    writer=pd.ExcelWriter('datafile_'+today_str+'.xlsx',engine="xlsxwriter")
    df.to_excel(writer,sheet_name='WPT_'+today_str)
    writer.save()

except IOError:
    print("Could not open file! Please close Excel file and rerun the test") # The file is open


    # when we let the file open (error)
#try:
#    datafile=open('datafile.xlsx','w')
#except IOError:
#    input("Could not open file! Please close Excel.Press Enter to continue") #The file is open
             
#with data_file:
#    writer=pd.ExcelWriter('datafile.xlsx',engine="xlsxwriter")
#    # Convert the dataframe to an XlsxWriter Excel object.           
#    df.to_excel(writer,sheet_name='WPT')
#    writer.save()
    
    
  

             
                      
        

        

