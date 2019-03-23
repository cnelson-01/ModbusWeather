from struct import unpack


class ModbusRegister:
    def __init__(self, value):
        self.value = value

    def asBytes(self):
        return bytes([(self.value >> 8) & 0xff, self.value & 0xff])

    def asInt(self):
        return self.value

    def asHex(self):
        return hex(self.value)


class RegisterRepo:
    def __init__(self):
        self.registerArray = {}

    def write(self, addr, value):
        self.registerArray[str(addr)] = ModbusRegister(value)

    def read(self, addr):
        if isinstance(addr, int):
            addr = str(addr)
        if addr in self.registerArray:
            return self.registerArray[addr].asInt()
        return 0

    def printAll(self):
        for key, value in self.registerArray.items():
            print("addr: " + key + " value: " + str(value.asHex()))
        if not self.registerArray:
            print("no items to print")
