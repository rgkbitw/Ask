#Data Extractor 
# Takes a String ==> Gives Out Results. 

# Json --> 1. "RelatedTopics" --> List -> Dict['Text']
#          2.                             Dict["Topics"]-> Dict ->['Text']
#          3.                             Dict['Name'] 
#          4. ["Type"]='D'
import json
import requests

def Out(data):
    s=requests.get("https://api.duckduckgo.com/?q="+data+"&format=json&pretty=1&skip_disambg=1").text
    data=json.loads(s)
    out=""
    if data['Type']=="D":
        out+="Sorry! But I Got You These :"+"\n"
        y=data['RelatedTopics']
        for i in y:
            if "Topics" not in i.keys():
                out+=i['Text']+"\n"
            elif "Topics" in i.keys():
                out+="\n"+i['Name'].upper()+"\n"
                out+=i['Topics'][0]['Text']
    elif data['Type']=="A":
        out+="Here It is :"+"\n"
        out+=data['Abstract']
    else:
        out+="Sorry Try Again"
    return out
	
print(Out(input()))
            
        
