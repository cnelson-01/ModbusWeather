class ModbusWriteMultipleReg:
    def __init__(self, modbusServerSocketHandler, registerRepo):
        self.mss = modbusServerSocketHandler
        self.rr = registerRepo

        for a in range(self.numberOfRegistersToWrite):
            reg = self.getReg(a)
            self.rr.write(self.mss.modbusTargetAddress + a, reg)

    @property
    def numberOfRegistersToWrite(self):
        if len(self.mss.body):
            msb = self.mss.getByte(self.mss.body, 4) << 8
            lsb = self.mss.getByte(self.mss.body, 5)
            return msb + lsb
        return -1

    def getReg(self, index):
        if self.mss.body:
            msb = self.mss.getByte(self.mss.body, 7 + (index * 2)) << 8
            lsb = self.mss.getByte(self.mss.body, 7 + 1 + (index * 2))
            return msb + lsb
        return -1
