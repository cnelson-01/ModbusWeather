# create an INET, STREAMing socket
import socket
import threading
import time
from ModbusServer import ModbusServer
from RegisterRepo import RegisterRepo
from ModbusValues import *

import requests

rr = RegisterRepo()
ms = ModbusServer(rr)
# ih = InputHandler()

solarValsStart = 256
scale = 1

values = [
    ModbusFloat("TempSensor(f)", 85, rr),
    ModbusFloat("Pannel(V)", solarValsStart, rr, fixedPoint=100),
    ModbusFloat("Pannel(A)", solarValsStart + 1 * scale, rr, fixedPoint=100),
    ModbusFloat("Pannel(WL)", solarValsStart + 2 * scale, rr, fixedPoint=100),
    ModbusFloat("Pannel(WH)", solarValsStart + 3 * scale, rr, fixedPoint=100),
    ModbusFloat("Battery(V)", solarValsStart + 4 * scale, rr, fixedPoint=100),
    ModbusFloat("Battery(A)", solarValsStart + 5 * scale, rr, fixedPoint=100),
    ModbusFloat("Battery(WL)", solarValsStart + 6 * scale, rr, fixedPoint=100),
    ModbusFloat("Battery(WH)", solarValsStart + 7 * scale, rr, fixedPoint=100),
    ModbusFloat("Load(V)", solarValsStart + 12 * scale, rr, fixedPoint=100),
    ModbusFloat("Load(I)", solarValsStart + 13 * scale, rr, fixedPoint=100),

    ModbusFloat("TempCase(f)", solarValsStart + 17 * scale, rr, fixedPoint=100 * 5 / 9, offset=32),

]

while threading.active_count() > 0:
    try:
        if values[0].modified:
            values[0].modified = False
            for v in values:
                print(str(v))
            print('\n')
            r = requests.post("http://127.0.0.1:8000/logTempData/", data={'tempInF': values[0].value, })
            print(r.status_code, r.reason)
        if values[1].modified:
            values[1].modified = False
            r = requests.post("http://127.0.0.1:8000/logSystemStatus/", data=
            {
                'panelVoltage': values[1].value,
                'panelCurrent': values[2].value,
                'batteryVoltage': values[5].value,
                'loadVoltage': values[9].value,
                'loadCurrent': values[10].value,
                'caseTemp': values[11].value
            })
            print(r.status_code, r.reason)
    except Exception as e:
        print("error posting data " + str(e))
