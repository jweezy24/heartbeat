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
            'value': bytes(get_service_using_id(id)),
        })

        messenger.write_message(req)
        return messenger
    else:
        print("The id has to be a int")
        return None

def update_services():
    out = sp.check_output(["systemctl", "-a"])
    for i in str(out.decode()).split("\n"):
        temp = i.split("   ")
        #TODO: do a regex
        temp_str = str(temp).replace("'',", "").replace("''", "").replace("[", "").replace("]", "").replace('"', "").replace("  ", "")
        new_temp = temp_str.split(",")
        if len(new_temp) > 3:
            val = {new_temp[0].replace("'", "") : (new_temp[1].strip().replace("'", "").replace(" ", "") +
            '-' + new_temp[2].strip().replace("'", "").replace(" ", "") + '-' + new_temp[3].replace("'", "").replace(" ", ""))}
            if '●' not in new_temp[0]:
                services_name.update(val)
    return services_name

def get_service_using_name(name):
    return services_name.get(name)

def get_service_using_id(id):
    return services_id.get(id)

def list_service_names():
    return list(services_name.keys())

def fill_services_by_ids():
    count = 0
    f = open('./mapping.txt', 'w')
    for i in list_service_names():
        f.write( str(i) + " -> " + str(count) + "\n")
        services_id.update({count: services_name.get(i)})
        count+=1
    f.close()

if __name__ == "__main__":
    update_services()
    fill_services_by_ids()
    #list_service_names()
    pack_heartbeat("Cx1")
    #print(services_id)
