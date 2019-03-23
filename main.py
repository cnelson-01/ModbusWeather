# create an INET, STREAMing socket
import socket
import threading
import time
from ModbusServer import ModbusServer
from RegisterRepo import RegisterRepo
from ModbusValues import *

rr = RegisterRepo()
ms = ModbusServer(rr)
# ih = InputHandler()

solarValsStart = 256
scale = 1

values = [
    ModbusFloat("TempSensor(f)", 85, rr),
    ModbusFloat("Pannel(V)", solarValsStart, rr, fixedPoint=100),
    ModbusFloat("Pannel(A)", solarValsStart + 1 * scale, rr, fixedPoint=100),
    ModbusFloat("Pannel(PL)", solarValsStart + 2 * scale, rr, fixedPoint=100),
    ModbusFloat("Pannel(PH)", solarValsStart + 3 * scale, rr, fixedPoint=100),
    ModbusFloat("Battery(PL)", solarValsStart + 6 * scale, rr, fixedPoint=100),
    ModbusFloat("Battery(PH)", solarValsStart + 7 * scale, rr, fixedPoint=100),
    ModbusFloat("Load(C)", solarValsStart + 13 * scale, rr, fixedPoint=100),
    ModbusFloat("Load(v)", solarValsStart + 12 * scale, rr, fixedPoint=100),

    ModbusFloat("TempCase(f)", solarValsStart + 17 * scale, rr, fixedPoint=100 * 5/9, offset=32),

]

while threading.active_count() > 0:
    # rr.printAll()
    for v in values:
        print(str(v))
    print('\n')
    time.sleep(2)
