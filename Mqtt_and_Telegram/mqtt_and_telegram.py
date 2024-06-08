# Write your code here :-)
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import csv
from datetime import datetime
import requests

def onConnect(client, userInput, flags, rc):
    if rc==0:
        print("Server connected\n")


    #Subscribe/listen to message topic "Door" @ the inputDevice
    client.subscribe("CSC1010/Door")

    #can subscribe to other message topic if needed, and process different request based on message topic
    #client.subscribe("CSC1010/Camera")


def onMessage(client, userdata, msg):
    #print("\nmessage topic :" + msg.topic + "\tmessage payload :" + msg.payload.decode("utf-8"))
    
    #time and date
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    
    #authorized users and password
    users= {'raymond':'password','michelle':'password','obama':'password','moses':'password','eisen':'raspberry','daiyu':'raspberry2','aneesha':'password','yuanlin':'password','pokka':'test','bachman':'test2'}
    
    
    userID = msg.payload.decode("utf-8")
    userID = userID.lower()
    
    
    print(userID) 
    #if userID in users.keys() and (users.get(userID)==userPassword):
    if userID in users.keys():
        print("Client side grant entry \t dateTime: "+dt_string)
        print("\n"+userID+" entered room @"+dt_string)
        
        
        #telegram bot to notify owner of authorized entry
        base_url = 'ADDBASEURL{}'.format("Authorized user:"+userID+" entered room @ "+dt_string)
        requests.get(base_url)
        
        #append to csv for transaction log
        with open("/home/pi/Desktop/webServer/CSV/user.csv", "a") as f:
            fields=[userID,dt_string]
            writer= csv.writer(f)
            writer.writerow(fields)
        
        #send True to output device lock to unlock door
        publish.single("CSC1010/Lock",True,hostname="test.mosquitto.org")
    #if facial data no match
    else:
        print("Client side deny entry")
        
        #telegram bot to notify owner of un-authorized entry
        base_url = 'https://api.telegram.org/bot1683250188:AAGwAK34XwAfBacNQ8M2OwzgGyrqg9CdJqM/sendMessage?chat_id=576078261&text={}'.format("Unknown user tried to enter room @"+dt_string)
        requests.get(base_url)
        print("Un-authorized user ID :"+userID+" tried to enter room @ "+dt_string)
        #print("User Entered \nID : "+userID+"\nPassword : :"+userPassword)
        
        
        #send False to output device lock to deny entry
        publish.single("CSC1010/Lock", False, hostname="test.mosquitto.org")




client = mqtt.Client()#intiantiate client
client.on_connect = onConnect#if client connect, subscribe to message topic, in this case Door
client.on_message = onMessage#if client receive message, execute onMessage routine

client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()#loop client forever
