import os
import time
import serial as ser
from waggle.messaging import Messenger
from waggle.protocol import pack_sensorgram
from waggle.protocol import unpack_sensorgram

time_low = 0
time_high = 1


def pack_heartbeat(model):
    if "Cx" in model:
        serial = ser.Serial('/dev/ttyS2', 9600, timeout=2)
        messenger = Messenger(serial)

        while True:
            temp = sensor_packet(messenger, 0)
            if  temp:
                for resp in temp.read_messages():
                    print('response')
                    dict = unpack_sensorgram(resp)
                    print(dict)
            else:
                print("Sensor 0 aint up chief.")

            temp = sensor_packet(messenger, 1)

            if  temp:
                for resp in temp.read_messages():
                    print('response')
                    dict = unpack_sensorgram(resp)
                    print(dict)
            else:
                print("Sensor 1 aint up chief.")

        time.sleep(1)

def sensor_packet(messenger, id):
    if type(id) == type(0):
        req = pack_sensorgram({
            'sensor_id': id,
            'parameter_id': 0,
            'value': b'hello',
        })

        messenger.write_message(req)
        return messenger
    else:
        print("The id has to be a int")
        return None



if __name__ == "__main__":
    pack_heartbeat("Cx1")
