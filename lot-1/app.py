#required libraries
import sys
import ssl
import paho.mqtt.client as mqtt
import os
import json

#called while client tries to establish connection with the server
def on_connect(mqttc, obj, flags, rc):
    print "hola"
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")

#called when a topic is successfully subscribed to
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos)+"data"+str(obj))

#called when a message is received by a topic
def on_message(mqttc, obj, msg):
    print("Received message from topic: "+msg.topic+" | QoS: "+str(msg.qos)+" | Data Received: "+str(msg.payload))

#creating a client with client-id=mqtt-test
mqttc = mqtt.Client(client_id="mqtt-test")

mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
root_cert_path  = os.path.join(os.path.dirname(__file__), '../certs/root-CA.crt')
cert_path  = os.path.join(os.path.dirname(__file__), '../certs/868fde4221-certificate.pem.crt')
private_key_path  = os.path.join(os.path.dirname(__file__), '../certs/868fde4221-private.pem.key')

#mqttc.tls_set("./certs/root-CA.crt",
#                certfile="./certs/868fde4221-certificate.pem.key",
#                keyfile="./certs/868fde4221-privete.pem.key",
#              tls_version=ssl.PROTOCOL_TLSv1_2,
#              ciphers=None)


mqttc.tls_set(root_cert_path,certfile=cert_path, keyfile=private_key_path,tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)


#connecting to aws-account-specific-iot-endpoint
print mqttc.connect("a1io4zpp14aci0.iot.us-west-2.amazonaws.com", port=8883) #AWS IoT service hostname and portno

#the topic to publish to
mqttc.subscribe("$aws/things/parking-lot-1/shadow/update", qos=1) #The names of these topics start with $aws/things/thingName/shadow."

thing = "parking-lot-1"
payload = json.dumps({
    "state": {
        "reported": {
            "this_thing_is_alive": True
        }
    }
})

print mqttc.publish("$aws/things/" + thing +"/shadow/update", payload)



#automatically handles reconnecting
mqttc.loop_forever()
