from enum import Enum
import struct
try:
    from .smpValue import SmpType, SmpValue
except (ImportError, SystemError):
    from smpValue import SmpType, SmpValue


class SmpMessage(object):
    def __init__(self, id=0):
        self.msgid = id
        self._values = []
        pass

    def __str__(self):
        value = '<id:{},values:['.format(self._msgid)
        for id in range(len(self._values)):
            value += str(self._values[id])
            value += ','
        value += ']>'
        return value

    def __eq__(self, other):
        if self._msgid != other._msgid:
            return False
        return (self._values == other._values)

    @property
    def msgid(self):
        return self._msgid

    @msgid.setter
    def msgid(self, id):
        if isinstance(id, int):
            if id >= 0 and id <= 0xffffffff:
                self._msgid = id

    def addValue(self, value):
        if isinstance(value, SmpValue):
            self._values.append(value)
        return self

    def getNumberOfValues(self):
        return len(self._values)

    def removeValue(self, id):
        if isinstance(id, int) and id < len(self._values):
            del self._values[id]
        return self

    def getValue(self, id):
        if isinstance(id, int) and id < len(self._values):
            return self._values[id]

    def resetValue(self):
        del self._values[:]
        return self

    def dump(self):
        data = []
        data += struct.pack("<I", self._msgid)
        values = []
        for value in self._values:
            values += value.dump()
        data += struct.pack("<I", len(values))
        data += values
        return data

    def load(self, bytesArray):
        if len(bytesArray) < 8:
            return 0
        self.msgid = struct.unpack("<I", bytes(bytesArray[:4]))[0]
        length = struct.unpack("<I", bytes(bytesArray[4:8]))[0]
        if len(bytesArray) < 8 + length:
            return 0

        datas = bytesArray[8:8+length]
        while len(datas) > 0:
            value = SmpValue()
            size = value.load(datas)
            self.addValue(value)
            datas = datas[size:]

        return 8 + length
