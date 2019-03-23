# 1f3e 0000 000b ff 10 0055 0002 0457 c742 8d
# A    B    C    D  E  F    G    H    I    k
# A  transaction id
# B  protocol id
# C  bytes to follow
# D  slave id
# E  function code 10h = write multiple registers
# F  slave register start
# G  number of coils to write (16 bit)
# H  register 1
# I  register 2
# k  crc checksum


class ModbusServerSocketHandler:
    def __init__(self, s):
        self.headerLength = 6
        self.body = ''
        self.header = s[:self.headerLength]
        self.body = s[self.headerLength:]

        if len(self.body) != self.bodyLength:
            print("error body length mismatch, actual:" + str(len(self.body)) + " expected:" + str(self.bodyLength))

    def getByte(self, binStr, index):
        body = list(self.body)
        if (index < len(binStr)):
            val = binStr[index]
            # return int(binStr[index].encode('hex'), 16)
            return val
        return 0

    @property
    def bodyLength(self):
        if len(self.header) == self.headerLength:
            return self.getByte(self.header, self.headerLength - 1)
        return 0

    @property
    def modbusCommand(self):
        if len(self.body):
            return self.getByte(self.body, 1)
        return -1

    @property
    def modbusTargetID(self):
        if len(self.body):
            return elf.getByte(self.body, 0)
        return -1

    @property
    def modbusTargetAddress(self):
        if (len(self.body)):
            msb = self.getByte(self.body, 2) << 8
            lsb = self.getByte(self.body, 3)
            return msb + lsb
        return -1
