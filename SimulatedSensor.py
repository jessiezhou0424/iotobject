# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.
import random
import time
import sys

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id {DeviceID} --output table
# For checking connection using following command:
# iothub-explorer monitor-events {DeviceID} --login {your hub service connection string}

CONNECTION_STRING_Sensor_1 = "HostName=sensor-simulator.azure-devices.net;DeviceId=sensor_1;SharedAccessKey=v2kJa8b71LZDLHm/woG1oZcChaa+9bAmuICTQdfRtjU="
CONNECTION_STRING_Sensor_2 = "HostName=sensor-simulator.azure-devices.net;DeviceId=sensor_2;SharedAccessKey=+1LQG0/wB8GwshtkoE7WirBjI6CBTswGSPBjwGGFEr0="
CONNECTION_STRING_Sensor_3 = "HostName=sensor-simulator.azure-devices.net;DeviceId=sensor_3;SharedAccessKey=eL0lWAiMX0FelfqvVUb7K2ziAhhmF16V03n4OSBNO6Y="

# ID, coordination, number of bike, the state of every bike (True or False)

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.
# Define the Bike number base
BIKE_NUM = 10

# MSG_TXT = "{\"Sensor ID\": {}, " + \
#     "\"Latitude\": {},\"Longitude\": {}, " + \
#     "\"the number of bike: {}\", " + \
#     "\" Bike State: {} \"" + \
#     "}"

# MSG_TXT = \
# """
#     "Sensor ID": "{}",
#     "Latitude": {},
#     "Longitude": {},
#     "the number of bike": {},
#     "Bike State": {},
#     "Bike Empty" : {}
# """
MSG_TXT = \
"""
    "Sensor ID": "{}",
    "Latitude": {},
    "Longitude": {},
    "Bike State": {}
"""

# simulation GPS data:
s1_position_list = [(-33.916359, 151.225834), (-33.915901, 151.225775),
                    (-33.915694, 151.225729), (-33.915500, 151.225697),
                    (-33.915317, 151.225665), (-33.915088, 151.225606),
                    (-33.914857, 151.225566), (-33.914663, 151.225515)]

s2_position_list = [(-33.915213, 151.228229), (-33.915184, 151.228049),
                    (-33.915151, 151.227910), (-33.915122, 151.227779),
                    (-33.915075, 151.227519), (-33.915048, 151.227283),
                    (-33.914999, 151.226914), (-33.914948, 151.226540)]

s3_position_list = [(-33.918767, 151.226246), (-33.919004, 151.226308),
                    (-33.919089, 151.226319), (-33.919249, 151.226351),
                    (-33.919404, 151.226372), (-33.919422, 151.226061),
                    (-33.919444, 151.225857), (-33.919477, 151.225562)]


def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client_sensor_1 = IoTHubClient(CONNECTION_STRING_Sensor_1, PROTOCOL)
    client_sensor_2 = IoTHubClient(CONNECTION_STRING_Sensor_2, PROTOCOL)
    client_sensor_3 = IoTHubClient(CONNECTION_STRING_Sensor_3, PROTOCOL)

    return client_sensor_1, client_sensor_2, client_sensor_3

def iothub_client_telemetry_sample_run():

    try:
        client_sensor_1, client_sensor_2, client_sensor_3 = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        MsgNum = 0
        while True:
            
            if MsgNum == 8:
                MsgNum = 0
            # Build the message with simulated telemetry values.
            # for sensor 1
            # bike_num_1 = BIKE_NUM + int(random.random() * 5)
            # bike_state_1 = [random.random() > 0.5 for _ in range(bike_num_1)]
            # msg_txt_formatted_S1 = MSG_TXT.format('sensor_1', '-33.9245', '151.228561', bike_num_1, bike_state_1, all(bike_state_1))
            msg_txt_formatted_S1 = MSG_TXT.format('sensor_1', str(s1_position_list[MsgNum][0]), str(s1_position_list[MsgNum][1]), bool(random.random() > 0.5))

            # for sensor 2
            # bike_num_2 = BIKE_NUM + int(random.random() * 5)
            # bike_state_2 = [random.random() > 0.5 for _ in range(bike_num_2)]
            # msg_txt_formatted_S2 = MSG_TXT.format('sensor_2', '-33.915473', '151.229261', bike_num_2, bike_state_2, all(bike_state_2))
            msg_txt_formatted_S2 = MSG_TXT.format('sensor_2', str(s2_position_list[MsgNum][0]), str(s2_position_list[MsgNum][1]), bool(random.random() > 0.5))

            # for sensor 3
            # bike_num_3 = BIKE_NUM + int(random.random() * 5)
            # bike_state_3 = [random.random() > 0.5 for _ in range(bike_num_3)]
            # msg_txt_formatted_S3 = MSG_TXT.format('sensor_3', '-33.918322', '151.226236', bike_num_3, bike_state_3, all(bike_state_3))
            msg_txt_formatted_S3 = MSG_TXT.format('sensor_3', str(s3_position_list[MsgNum][0]), str(s3_position_list[MsgNum][1]), bool(random.random() > 0.5))

            # message_1 = IoTHubMessage(bytearray('{' + msg_txt_formatted_S1 + '}', 'utf-8'))
            # message_2 = IoTHubMessage(bytearray('{' + msg_txt_formatted_S2 + '}', 'utf-8'))
            # message_3 = IoTHubMessage(bytearray('{' + msg_txt_formatted_S3 + '}', 'utf-8'))
            msg_txt_formatted_S1 = '{' + msg_txt_formatted_S1.strip() + '}'
            msg_txt_formatted_S2 = '{' + msg_txt_formatted_S2.strip() + '}'
            msg_txt_formatted_S3 = '{' + msg_txt_formatted_S3.strip() + '}'

            message_1 = IoTHubMessage(msg_txt_formatted_S1)
            message_2 = IoTHubMessage(msg_txt_formatted_S2)
            message_3 = IoTHubMessage(msg_txt_formatted_S3)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.

            prop_map_1 = message_1.properties()
            prop_map_2 = message_2.properties()
            prop_map_3 = message_3.properties()

            prop_map_1.add("level", 'critical')
            prop_map_2.add("level", 'critical')
            prop_map_3.add("level", 'critical')

            # Send the message.
            print(f"sensor_1 Sending message: {message_1.get_string()}")
            print(f"sensor_2 Sending message: {message_2.get_string()}")
            print(f"sensor_3 Sending message: {message_3.get_string()}")

            client_sensor_1.send_event_async(message_1, send_confirmation_callback, None)
            client_sensor_2.send_event_async(message_2, send_confirmation_callback, None)
            client_sensor_3.send_event_async(message_3, send_confirmation_callback, None)

            MsgNum += 1
            time.sleep(30)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()

