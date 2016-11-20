import paho.mqtt.client as mqtt
import os
import ssl


def on_connect(mqttc, obj, flags, rc):
    if rc == 0:
        print ("Subscriber Connection status code: " + str(rc) + " | Connection status: successful")
        mqttc.subscribe("parkings", qos=1)
    elif rc == 1:
        print ("Subscriber Connection status code: " + str(rc) + " | Connection status: Connection refused")


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos) + "data" + str(obj))


def on_message(mqttc, obj, msg):
    print("Received message from topic: " + msg.topic + " | QoS: " + str(msg.qos))
    #msg= msg.payload



#mqtt settings

root_cert_path = os.path.join(os.path.dirname(__file__), 'certs/root-CA.crt')
cert_path = os.path.join(os.path.dirname(__file__), 'certs/one/69ecbfbb92-certificate.pem.crt')
private_key_path = os.path.join(os.path.dirname(__file__), 'certs/one//69ecbfbb92-private.pem.key')


mqttc = mqtt.Client(client_id="parking-manager")
# setup callback functions
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

mqttc.tls_set(root_cert_path, certfile=cert_path, keyfile=private_key_path, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
mqttc.connect("a1io4zpp14aci0.iot.us-west-2.amazonaws.com", port=8883)  # AWS IoT service hostname and port

mqttc.loop_forever()

