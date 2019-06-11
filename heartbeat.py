import os
import time
import serial as ser
from waggle.messaging import Messenger
from waggle.protocol import pack_sensorgram
from waggle.protocol import unpack_sensorgram
import json
import subprocess as sp

services_name = {}
services_id = {}

def pack_heartbeat(model):
    if "Cx" in model:
        serial = ser.Serial('/dev/ttyS2', 9600, timeout=2)
        messenger = Messenger(serial)

        while True:
            val = ''
            temp = sensor_packet(messenger, 0)
            if  temp:
                for resp in temp.read_messages():
                    print('response')
                    dict = unpack_sensorgram(dict)
                    try:
                        val = json.loads(json.loads(str(dict).replace("b'", ''))["value"])
                        print(val)
                    except Exception as e:
                        print("Error: \t" + str(e))
            else:
                print("Sensor 0 aint up chief.")

            temp = sensor_packet(messenger, 1)

            if  temp:
                for resp in temp.read_messages():
                    print('response')
                    dict = unpack_sensorgram(resp)
                    try:
                        print(dict)
                        val = json.loads(json.loads(str(dict).replace("b'", ''))["value"])
                        print(val)
                    except Exception as e:
                        print("Error: \t" + str(e))
                    print(val)
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

def update_services():
    out = sp.check_output(['systemctl', '-a'])
    for i in out.decode().split("\n"):
        temp = i.split("   ")
        temp_str = str(temp).replace("'',", "").replace("''", "").replace("[", "").replace("]", "").replace('"', "").replace("  ", "")
        new_temp = temp_str.split(",")
        if len(new_temp) > 3:
            val = {new_temp[0].replace("'", "") : (new_temp[1].strip().replace("'", "").replace(" ", "") +
            '-' + new_temp[2].strip().replace("'", "").replace(" ", "") + '-' + new_temp[3].replace("'", "").replace(" ", ""))}
            services_name.update(val)
            fill_services_by_ids(val)
    return services_name

def get_service_using_name(name):
    if name in services_name.keys():
        return services_name[name]
    else:
        return None

def list_service_names():
    for i in services_name.keys():
        print(i)

def fill_services_by_ids(val):
    name = list(val.keys())[0]
    if name == '1':
        services_id.update({1:val[name]})
    if name == '2':
        services_id.update({2:val[name]})
    if name == '3':
        services_id.update({3:val[name]})
    if name == 'bolt.service':
        services_id.update({4:val[name]})

if __name__ == "__main__":
    update_services()
    print(get_service_using_name("bolt.service"))
    print(services_id)
