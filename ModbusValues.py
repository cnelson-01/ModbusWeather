from struct import unpack


class ModbusBase:
    def __init__(self, name, addr, rr):
        self.rr = rr
        self.name = name
        self.addr = addr

    def __str__(self):
        return self.name + ":" + str(self.value)

    def readAsInt(self, addr):
        # msb = self.rr.read(self.addr) << 8
        # lsb = self.rr.read(self.addr + 1)
        # return msb + lsb
        return self.rr.read(self.addr)

    def intToBytes(self, val):
        # 16bit only
        msb = (val >> 8) & 0xff
        lsb = (val & 0xFF)
        return bytes([msb]) + bytes([lsb])

    def readAsFloat(self):
        # floats are 32 bit by default try to find the next reg
        msb = bytes(self.intToBytes(self.rr.read(self.addr)))
        lsb = bytes(self.intToBytes(self.rr.read(self.addr + 1)))
        binStr = lsb + msb
        if len(binStr) == 4:
            n = unpack(b'>f', binStr)
            return n[0]
        return 0

    @property
    def value(self):
        raise NotImplementedError


class ModbusFloat(ModbusBase):
    def __init__(self, name, addr, rr, fixedPoint=1, offset=0):
        self.fixedPoint = fixedPoint
        self.offset = offset
        super().__init__(name, addr, rr)

    @property
    def modified(self):
        return self.rr.isModified(self.addr)

    @modified.setter
    def modified(self, val):
        self.rr.setModified(val)
    @property
    def value(self):
        if self.fixedPoint == 1:
            return self.readAsFloat()
        return ((0.0 + self.readAsInt(self.addr)) / self.fixedPoint) + self.offset


class ModbusInt(ModbusBase):
    @property
    def value(self):
        return self.readAsInt(self.addr)
