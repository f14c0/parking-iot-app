# Import SDK packages
import os, time, json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient


# For certificate based connection
myShadowClient = AWSIoTMQTTShadowClient("parking-lot-1")
# For Websocket connection
# myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)
# Configurations
# For TLS mutual authentication
myShadowClient.configureEndpoint("a1io4zpp14aci0.iot.us-west-2.amazonaws.com", 8883)

# For Websocket
# myShadowClient.configureEndpoint("YOUR.ENDPOINT", 443)
root_cert_path = os.path.join(os.path.dirname(__file__), '../certs/root-CA.crt')
cert_path = os.path.join(os.path.dirname(__file__), '../certs/61bed7fc7e-certificate.pem.crt')
private_key_path = os.path.join(os.path.dirname(__file__), '../certs/61bed7fc7e-private.pem.key')

myShadowClient.configureCredentials(root_cert_path,private_key_path,cert_path)
# For Websocket, we only need to configure the root CA
# myShadowClient.configureCredentials("YOUR/ROOT/CA/PATH")
myShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
myShadowClient.configureMQTTOperationTimeout(5)  # 5 sec


#Callback functions

def on_update(payload, response_status, token):
	if response_status == "timeout":
		print("Update request " + token + " time out!")
	if response_status == "accepted":
		payloadDict = json.loads(payload)
		print("Update request with token: " + token + " accepted!")
		print("property: " + str(payloadDict["state"]["desired"]["property"]))
	if response_status == "rejected":
		print("Update request " + token + " rejected!")


def on_delete(payload, response_status, token):
	if response_status == "timeout":
		print("Delete request " + token + " time out!")
	if response_status == "accepted":
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		print("Delete request with token: " + token + " accepted!")
		print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	if response_status == "rejected":
		print("Delete request " + token + " rejected!")


# Connect to AWS IoT
myShadowClient.connect()
# Create a device shadow instance using persistent subscription
myDeviceShadow = myShadowClient.createShadowHandlerWithName("Bot", True)
# Shadow operations
# myDeviceShadow.shadowGet(customCallback, 5)
# myDeviceShadow.shadowDelete(customCallback, 5)
# myDeviceShadow.shadowRegisterDeltaCallback(customCallback)
# myDeviceShadow.shadowUnregisterDeltaCallback()

loopCount = 0
while True:
	JSONPayload = '{"state":{"desired":{"property":'+'"parking ' + str(loopCount) + '"}}}'
	print JSONPayload
	myDeviceShadow.shadowUpdate(JSONPayload, on_update, 5)
	loopCount += 1
	time.sleep(5)





























