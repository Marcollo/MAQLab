import platform
import time
import paho.mqtt.client as paho
import threading
import json

from scan_serial import scan_serial_devices

from Extensions.Manson_NTP6531 import NTP6531
from Extensions.BKPrecision_2831E import BK2831E
from Extensions.Keithley_SM2400 import SM2400

# TODO: loading the configurations should be done via mqtt also
with open('config/inventar.json') as json_file:
    inventar = json.load(json_file)
    inventarnumbers = list(inventar.keys())
    # print("Inventarumbers:")
    # print(inventarnumbers)

with open('config/devices.json') as json_file:
    devices = json.load(json_file)
    deviceidentifications = list(devices.keys())
    print("Devices:")
    print(devices)
    print("Deviceidentifications:")
    print(deviceidentifications)
    ld = []
    for d in devices:
        ld.append(devices[d]["cmd_idn"])
        # print(devices[d]["cmd_idn"])
    ld = set(ld)
    # print(ld)

# print(inventarnumbers)
# print(deviceidentifications)

devlist = []
comlist = []
iplist = []
devlock = threading.Lock()
comlock = threading.Lock()



# --------------------------------------------------------
# MQTT Broker callbacks
# --------------------------------------------------------
def mqttloop(_client):
    _client.loop_forever()


def on_connect(_client, userdata, flags, rc):
    # print("CONNACK received with code %d." % (rc))
    _client.subscribe("maqlab/cmd/#", qos=0)


def on_disconnect(_client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
    # server.stop()
    # server.start()
    _client.reconnect()


def on_message(_client, _userdata, _msg):
    global devlist
    global devlock

    with devlock:
        if len(devlist) > 0:
            # distribute message to all devices
            for _dev in devlist:
                try:
                    _dev.mqttmessage(_client, _msg)
                except:
                    pass


if __name__ == "__main__":
    print("Started...")
    client = paho.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.username_pw_set("maqlab", "maqlab")
    client.connect("techfit.at", 1883)

    thread_mqttloop = threading.Thread(target=mqttloop, args=(client,))
    thread_mqttloop.start()

    thread_detect_serial = threading.Thread(target=scan_serial_devices, args=(devices, comlist, comlock,))
    thread_detect_serial.start()

    while True:
        # --------------------------------------------------------------------------
        # Die Comliste durchgehen und die entsprechende Deviceklasse erzeugen
        # --------------------------------------------------------------------------
        with comlock:
            if len(comlist) > 0:
                for com in comlist:
                    # print(com)
                    for d in deviceidentifications:
                        devobject = None
                        # print(d)
                        # print(devices[d]["classname"])
                        dclassname = devices[d]["classname"]
                        if dclassname in com:
                            # generating a deviceclass from classname
                            devobject = globals()[dclassname](com[dclassname])
                        if devobject is not None:
                            # search for inventarnumber of the device with spec serialnumber
                            # there are some devices not declared with a serialnumber
                            # so we have to use the random generated serial for the inventarnumber
                            inventarnumber = '0'
                            for number in inventarnumbers:
                                try:
                                    serialnumber = inventar[str(number)]["serial"]
                                except:
                                    serialnumber = "0"

                                if devobject.serialnumber == serialnumber:
                                    inventarnumber = number
                                    break

                            if inventarnumber == '0':
                                inventarnumber = devobject.serialnumber

                            with devlock:
                                devlist.append(devobject)
                                devobject.on_created(com[dclassname], inventarnumber)

                comlist.clear()
        # --------------------------------------------------------------------------
        time.sleep(0.02)

        # --------------------------------------------------------------------------
        # Die bereits verbundenen Geräte durchgehen und execute aufrufen
        # --------------------------------------------------------------------------

        if len(devlist) > 0:
            for dev in devlist:
                if dev.connected():
                    # print("Connected")
                    dev.execute()
                else:
                    # print("NOT Connected")
                    with devlock:
                        dev.on_destroyed()
                        devlist.remove(dev)
                        del dev

