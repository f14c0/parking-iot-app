# Import SDK packages
import os
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("parking-lot-1")
# For Websocket connection
# myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)
# Configurations
# For TLS mutual authentication
myMQTTClient.configureEndpoint("a1io4zpp14aci0.iot.us-west-2.amazonaws.com", 8883)
# For Websocket

# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
root_cert_path  = os.path.join(os.path.dirname(__file__), '../certs/root-CA.crt')
cert_path  = os.path.join(os.path.dirname(__file__), '../certs/61bed7fc7e-certificate.pem.crt')
private_key_path  = os.path.join(os.path.dirname(__file__), '../certs/61bed7fc7e-private.pem.key')

myMQTTClient.configureCredentials(root_cert_path,private_key_path,cert_path)
# For Websocket, we only need to configure the root CA
# myMQTTClient.configureCredentials("YOUR/ROOT/CA/PATH")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec


#Callback functions
def on_message(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)


myMQTTClient.connect()
myMQTTClient.subscribe("parking-lots", 1, on_message)


# Publish to the same topic in a loop forever
loopCount = 0

while True:
    myMQTTClient.publish("parking-lots", "New Message " + str(loopCount), 1)
    loopCount += 1
    time.sleep(5)


#myMQTTClient.publish("myTopic", "myPayload", 0)
#myMQTTClient.unsubscribe("myTopic")
#myMQTTClient.disconnect()
