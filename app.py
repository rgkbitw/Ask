import os,sys,json,pprint,requests
from flask import Flask,request
from pymessenger import Bot



def Out(data):
    s=requests.get("https://api.duckduckgo.com/?q="+data+"&format=json&pretty=1&skip_disambg=1").text
    try:
        data=json.loads(s)
    except:
        data={}
    out=""
    if data!={}:
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



Page="EAAZA6CYgqIGwBAABuIpJY1sHQDU9dM8wYLujIZAQ3xRbutJEf5CYzrqPaQJ4vGG0aBNAW2AlXLtLj7pvdMZBd7uCoj0pMZCTlwWIsxD1Kr93dkqdRBvi45KPMroxN7UpreXYrzb8HM5xVh8BEkwINbfBY6A83vfkygZCbDXc91ymP0A4Of6ZAX"

bot=Bot(Page)    
app=Flask(__name__)

@app.route('/',methods=['GET'])
def verify():
    #webhook verification
    if request.args.get("hub.mode")=="subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token")=="hello":
            return "Verification token mismatch",403
        return request.args["hub.challenge"],200
    return '<img src="http://img10.deviantart.net/83f6/i/2012/129/8/8/marc_ecko_graffiti_piece_by_taijohnnguyen-d4z14qg.jpg"><h1>@rgkbitw</h1>',200


@app.route('/',methods=['POST'])
def webhook():
    data=request.get_json()
    log(data)
    if data['object']=='page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                #ID's:
                sender_id=messaging_event['sender']['id']
                recipient_id=messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text=messaging_event['message']['text']
                    else:
                        messaging_text="None"
                    response=messaging_text
                    z=Out(response)
                    bot.send_text_message(sender_id,z)
    return "ok",200

def log(message):
    pprint.pprint(message)
    print("."*100)
    sys.stdout.flush()

if __name__=="__main__":
   app.run(debug=True,port=80)
   print("Success") 
