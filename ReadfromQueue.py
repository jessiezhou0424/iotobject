from azure.servicebus import ServiceBusService, Message, Queue
from main_app.models.bike import Bike
import sqlalchemy
import time
import json

# SERVICE_BUS_NAME = {serviceBusName}
# SHARED_ACCESS_POLICY_NAME = {sharedAccessPolicyName}
# SHARED_ACCESS_POLICY_KEY_VALUE = {sharedAccessPolicyKeyValue}
# QUEUE_NAME = {queueName}
engine = sqlalchemy.create_engine('mysql+mysqldb://root:dev@localhost/iot', pool_recycle=3600)
conn = engine.connect()
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
            print(msg.body)
            msg_dict = eval(str(msg.body, 'utf-8'))
            st=0
            if msg_dict["Bike State"]:
                st=1
            # bike=Bike(id=int(msg_dict["Sensor ID"].split(" ")[1]),lon=msg_dict["Longitude"],lat=msg_dict["Latitude"],status= st)
            device_id = int(msg_dict["Sensor ID"].split("_")[1])
            bike = Bike.query.get(device_id)
            # if bike is None:
            bike_new = Bike(device_id=device_id,lon=msg_dict["Longitude"],lat=msg_dict["Latitude"], status=st)
            # else:
            #     bike.lon = msg_dict["Longitude"]
            #     bike.lat = msg_dict["Latitude"]
            print(bike.to_dict())
            bike_new=conn.session.merge(bike_new)
            #conn.session.add(bike)
            conn.session.commit()
            print("___", conn)
        # else:
        #     print("There is no data in the queue.")
        time.sleep(30)

conn.close()
if __name__ == '__main__':
    setup_client()
