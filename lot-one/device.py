import paho.mqtt.client as mqtt
import json
import os
import ssl
import datetime
import time
import random


DEVICE_ID = 3043791462


def on_connect(mqttc, obj, flags, rc):
    if rc == 0:
        print ("Subscriber Connection status code: " + str(rc) + " | Connection status: successful")
    elif rc == 1:
        print ("Subscriber Connection status code: " + str(rc) + " | Connection status: Connection refused")


def on_publish(client, userdata, mid):
    print("Message published ")


def get_current_state():
    states = [True, False]
    return random.choice(states)


def update_state():
    payload = json.dumps({
        "parking":{
            "device_id":DEVICE_ID,
            "device_location":{
                "lat":74.5968521,
                "long":-77.596474
            },
            "state":{
                "alive":True,
                "parking_state":{
                    "available":get_current_state(),
                    "reserved":get_current_state(),
                    "reservation_due" : str(datetime.datetime.now())
                }
            }
        }
    })
    mqttc.publish("parkings", payload)


#mqtt settings

root_cert_path = os.path.join(os.path.dirname(__file__), '../certs/root-CA.crt')
cert_path = os.path.join(os.path.dirname(__file__), '../certs/one/69ecbfbb92-certificate.pem.crt')
private_key_path = os.path.join(os.path.dirname(__file__), '../certs/one//69ecbfbb92-private.pem.key')

client_id = "parking_lot_%s" % str(DEVICE_ID)

mqttc = mqtt.Client(client_id=client_id)

# setup callback functions
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

mqttc.tls_set(root_cert_path, certfile=cert_path, keyfile=private_key_path, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
mqttc.connect("a1io4zpp14aci0.iot.us-west-2.amazonaws.com", port=8883)  # AWS IoT service hostname and port
mqttc.subscribe("parkings",  qos=1)  # The names of these topics start with $aws/things/thingName/shadow."

mqttc.loop_start()


while True:
    update_state()
    time.sleep(3)
