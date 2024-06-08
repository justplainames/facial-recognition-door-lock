import paho.mqtt.client as mqtt
def onConnect(client, userInput, flags, rc):
    if rc == 0:
        print("Lock connected")
    #subscribe to lock @ client to listen if grant/deny access
    client.subscribe("CSC1010/Lock")

def onMessage(client, userdata, msg):
    #print("\nmessage topic :" + msg.topic + "\tmessage payload :" + msg.payload.decode("utf-8"))

    #if message from client ==True, grant access
    if msg.payload.decode("utf-8") == "True":
        print("\n\nAccess granted: Door Open")
        print("green light\n\n")
    else:
        # if message from client !=True, grant access
        print("\n\nAccess Denied: Door Close")
        print("Red light\n\n")

client = mqtt.Client()
client.on_connect = onConnect
client.on_message = onMessage
client.connect("test.mosquitto.org", 1883, 60)
client.loop_forever()