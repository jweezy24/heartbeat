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

            sensor_packet(messenger, 0)

            sensor_packet(messenger, 1)

            for resp in messenger.read_messages():
                print('response')
                dict = unpack_sensorgram(resp)
        time.sleep(1)

def sensor_packet(messenger, id):
    if type(num) == type(0):
        req = pack_sensorgram({
            'sensor_id': id,
            'parameter_id': 0,
            'value': b'hello',
        })

        messenger.write_message(req)
    else:
        print("The id has to be a int")
        return None



if __name__ == "__main__":
    do_heartbeat("Cx1")
