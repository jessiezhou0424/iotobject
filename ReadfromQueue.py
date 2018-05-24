from azure.servicebus import ServiceBusService, Message, Queue
from main_app.models.bike import Bike
from main_app import db

# SERVICE_BUS_NAME = {serviceBusName}
# SHARED_ACCESS_POLICY_NAME = {sharedAccessPolicyName}
# SHARED_ACCESS_POLICY_KEY_VALUE = {sharedAccessPolicyKeyValue}
# QUEUE_NAME = {queueName}

SERVICE_BUS_NAME = "IoTdataQueue"
SHARED_ACCESS_POLICY_NAME = "RootManageSharedAccessKey"
SHARED_ACCESS_POLICY_KEY_VALUE = "sctQlqNz7BW0pxmpnUYA3apz0LId6UBs24WgygP3vWs="
# "Endpoint=sb://iotdataqueue.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=sctQlqNz7BW0pxmpnUYA3apz0LId6UBs24WgygP3vWs="
QUEUE_NAME = "iotqueue"

def setup_client():
    bus_service = ServiceBusService(
        service_namespace=SERVICE_BUS_NAME,
        shared_access_key_name=SHARED_ACCESS_POLICY_NAME,
        shared_access_key_value=SHARED_ACCESS_POLICY_KEY_VALUE)

    while True:
        msg = bus_service.receive_queue_message(QUEUE_NAME, peek_lock=False)
        if msg.body != None:
            msg_dict = eval(str(msg.body, 'utf-8'))
            bike=Bike(id=msg_dict["Sensor ID"].split(" ")[1],lon=msg_dict["Longitude"],lat=msg_dict["Latitude"],status= msg_dict["Bike State"])
            db.session.add(bike)
            db.session.commit()
        else:
            print("There is no data in the queue.")


if __name__ == '__main__':
    setup_client()
