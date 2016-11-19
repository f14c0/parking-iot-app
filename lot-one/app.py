import paho.mqtt.client as mqtt
import json
import os
import ssl

def on_connect(mqttc, obj, flags, rc):
    if rc == 0:
        print ("Subscriber Connection status code: " + str(rc) + " | Connection status: successful")
    elif rc == 1:
        print ("Subscriber Connection status code: " + str(rc) + " | Connection status: Connection refused")


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos) + "data" + str(obj))
    first_message()


def on_message(mqttc, obj, msg):
    print(
    "Received message from topic: " + msg.topic + " | QoS: " + str(msg.qos) + " | Data Received: " + str(msg.payload))


def on_publish(client, userdata, mid):
    print("Message is published")


def first_message():
    payload = json.dumps({
        "state":{
            "reported":{
                "this_thing_is_alive":True,
                "color":{
                    "r":255,
                    "g":1,
                    "b":255
                }
            }
        }
    })
    mqttc.publish("$aws/things/parking-lot-one/shadow/update", payload)


root_cert_path = os.path.join(os.path.dirname(__file__), '../certs/root-CA.crt')
cert_path = os.path.join(os.path.dirname(__file__), '../certs/one/69ecbfbb92-certificate.pem.crt')
private_key_path = os.path.join(os.path.dirname(__file__), '../certs/one//69ecbfbb92-private.pem.key')


mqttc = mqtt.Client(client_id="parking-lot-one")
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
mqttc.on_publish = on_publish

mqttc.tls_set(root_cert_path, certfile=cert_path, keyfile=private_key_path, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
mqttc.connect("a1io4zpp14aci0.iot.us-west-2.amazonaws.com", port=8883)  # AWS IoT service hostname and port
mqttc.subscribe("$aws/things/parking-lot-one/shadow/update/#",  qos=1)  # The names of these topics start with $aws/things/thingName/shadow."

mqttc.loop_forever()