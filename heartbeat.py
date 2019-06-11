import os
import time
import serial as ser
from waggle.messaging import Messenger
from waggle.protocol import pack_sensorgram
from waggle.protocol import unpack_sensorgram

time_low = 0
time_high = 1


def do_heartbeat(model):
    if "Cx" in model:
        serial = ser.Serial('/dev/ttyS1', 9600, timeout=2)
        messenger = Messenger(ser)

        while True:
            req = pack_sensorgram({
                'sensor_id': 1,
                'parameter_id': 0,
                'value': b'hello',
                })
            messenger.write_message(req)

            req = pack_sensorgram({
                'sensor_id': 2,
                'parameter_id': 0,
                'value': b'hello',
            })

            messenger.write_message(req)

            for resp in messenger.read_messages():
                print('response')
                print(unpack_sensorgram(resp))

    time.sleep(1)


if __name__ == "__main__":
    do_heartbeat("Cx1")
