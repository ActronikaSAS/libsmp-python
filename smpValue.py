from enum import Enum
import struct
import array


UINT8_MAX = 2**8 - 1
UINT16_MAX = 2**16 - 1
UINT32_MAX = 2**32 - 1
UINT64_MAX = 2**64 - 1
INT8_MIN = -1 * 2**7
INT8_MAX = 2**7 - 1
INT16_MIN = -1 * 2**15
INT16_MAX = 2**15 - 1
INT32_MIN = -1 * 2**31
INT32_MAX = 2**31 - 1
INT64_MIN = -1 * 2**63
INT64_MAX = 2**63 - 1


class SmpType(Enum):
    SMP_TYPE_NONE = 0x00
    SMP_TYPE_UINT8 = 0x01
    SMP_TYPE_INT8 = 0x02
    SMP_TYPE_UINT16 = 0x03
    SMP_TYPE_INT16 = 0x04
    SMP_TYPE_UINT32 = 0x05
    SMP_TYPE_INT32 = 0x06
    SMP_TYPE_UINT64 = 0x07
    SMP_TYPE_INT64 = 0x08
    SMP_TYPE_STRING = 0x09
    SMP_TYPE_MAX = 0x7f

    def __str__(self):
        return str(self.value[0])


class SmpValue(object):
    def __init__(self, type=SmpType.SMP_TYPE_NONE, value=None):
        self.type = type
        self._value = None
        self.value = value

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{}'.format(self._value)

    def __eq__(self, other):
        return ((self._type == other._type) and (self._value == other._value))

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @type.setter
    def type(self, type):
        if isinstance(type, SmpType):
            self._type = type

    @value.setter
    def value(self, value):
        if self._type == SmpType.SMP_TYPE_UINT8:
            if isinstance(value, int):
                if 0 <= value <= UINT8_MAX:
                    self._value = value
        if self._type == SmpType.SMP_TYPE_INT8:
            if isinstance(value, int):
                if INT8_MIN <= value <= INT8_MAX:
                    self._value = value
        if self._type == SmpType.SMP_TYPE_UINT16:
            if isinstance(value, int):
                if 0 <= value <= UINT16_MAX:
                    self._value = value
        if self._type == SmpType.SMP_TYPE_INT16:
            if isinstance(value, int):
                if INT16_MIN <= value <= INT16_MAX:
                    self._value = value
        if self._type == SmpType.SMP_TYPE_UINT32:
            if isinstance(value, int):
                if 0 <= value <= UINT32_MAX:
                    self._value = value
        if self._type == SmpType.SMP_TYPE_INT32:
            if isinstance(value, int):
                if INT32_MIN <= value <= INT32_MAX:
                    self._value = value
        if self._type == SmpType.SMP_TYPE_UINT64:
            if isinstance(value, int):
                if 0 <= value <= UINT64_MAX:
                    self._value = value
        if self._type == SmpType.SMP_TYPE_INT64:
            if isinstance(value, int):
                if INT64_MIN <= value <= INT64_MAX:
                    self._value = value
        if self._type == SmpType.SMP_TYPE_STRING:
            if isinstance(value, str):
                self._value = value

    def set(self, type, value):
        self.type = type
        self.value = value

    def dump(self):
        data = []
        if self._type == SmpType.SMP_TYPE_UINT8:
            data += struct.pack("<B", self.value)
        elif self._type == SmpType.SMP_TYPE_INT8:
            data += struct.pack('<b', self.value)
        elif self._type == SmpType.SMP_TYPE_UINT16:
            data += struct.pack('<H', self.value)
        elif self._type == SmpType.SMP_TYPE_INT16:
            data += struct.pack('<h', self.value)
        elif self._type == SmpType.SMP_TYPE_UINT32:
            data += struct.pack('<I', self.value)
        elif self._type == SmpType.SMP_TYPE_INT32:
            data += struct.pack('<i', self.value)
        elif self._type == SmpType.SMP_TYPE_UINT64:
            data += struct.pack('<Q', self.value)
        elif self._type == SmpType.SMP_TYPE_INT64:
            data += struct.pack('<q', self.value)
        elif self._type == SmpType.SMP_TYPE_STRING:
            data += struct.pack('<H', len(self.value)+1)
            data += self.value.encode()
            data += [0]
        return [self._type.value] + data

    def load(self, bytesArray):
        if len(bytesArray) < 1:
            return 0
        if bytesArray[0] == SmpType.SMP_TYPE_UINT8.value:
            if len(bytesArray) < 2:
                return 0
            self._type = SmpType.SMP_TYPE_UINT8
            self.value = struct.unpack('<B', bytes(bytesArray[1:2]))[0]
            return 2
        elif bytesArray[0] == SmpType.SMP_TYPE_INT8.value:
            if len(bytesArray) < 2:
                return 0
            self._type = SmpType.SMP_TYPE_INT8
            self.value = struct.unpack('<b', bytes(bytesArray[1:2]))[0]
            return 2
        elif bytesArray[0] == SmpType.SMP_TYPE_UINT16.value:
            if len(bytesArray) < 3:
                return 0
            self._type = SmpType.SMP_TYPE_UINT16
            self.value = struct.unpack('<H', bytes(bytesArray[1:3]))[0]
            return 3
        elif bytesArray[0] == SmpType.SMP_TYPE_INT16.value:
            if len(bytesArray) < 3:
                return 0
            self._type = SmpType.SMP_TYPE_INT16
            self.value = struct.unpack('<h', bytes(bytesArray[1:3]))[0]
            return 3
        elif bytesArray[0] == SmpType.SMP_TYPE_UINT32.value:
            if len(bytesArray) < 5:
                return 0
            self._type = SmpType.SMP_TYPE_UINT32
            self.value = struct.unpack('<I', bytes(bytesArray[1:5]))[0]
            return 5
        elif bytesArray[0] == SmpType.SMP_TYPE_INT32.value:
            if len(bytesArray) < 5:
                return 0
            self._type = SmpType.SMP_TYPE_INT32
            self.value = struct.unpack('<i', bytes(bytesArray[1:5]))[0]
            return 5
        elif bytesArray[0] == SmpType.SMP_TYPE_UINT64.value:
            if len(bytesArray) < 9:
                return 0
            self._type = SmpType.SMP_TYPE_UINT64
            self.value = struct.unpack('<Q', bytes(bytesArray[1:9]))[0]
            return 9
        elif bytesArray[0] == SmpType.SMP_TYPE_INT64.value:
            if len(bytesArray) < 9:
                return 0
            self._type = SmpType.SMP_TYPE_INT64
            self.value = struct.unpack('<q', bytes(bytesArray[1:9]))[0]
            return 9
        elif bytesArray[0] == SmpType.SMP_TYPE_STRING.value:
            if len(bytesArray) < 3:
                return 0
            length = struct.unpack('<H', bytes(bytesArray[1:3]))[0]
            if len(bytesArray) < 3 + length:
                return 0
            if bytesArray[3+length - 1] != 0x00:
                return 0
            self._type = SmpType.SMP_TYPE_STRING
            self.value = bytes(bytesArray[3:2+length]).decode()
            return 3 + length
