from enum import Enum
try:
    from .smpMessage import SmpMessage
    from .smpValue import SmpValue, SmpType
except (ImportError, SystemError):
    from smpMessage import SmpMessage
    from smpValue import SmpValue, SmpType


class MagicChar(Enum):
    START_BYTE = 0x10
    END_BYTE = 0xFF
    ESC_BYTE = 0x1B

    @staticmethod
    def isMagic(value):
        enum_list = [e.value for e in MagicChar]
        return value in enum_list


class FrameState(Enum):
    WAIT_HEADER = 0
    IN_FRAME = 1
    IN_FRAME_ESC = 2
    END = 3


class Frame(object):
    def __init__(self, message=None):
        self._payload = []
        self._state = FrameState.WAIT_HEADER
        if message is not None and isinstance(message, SmpMessage):
            self.setMessage(message)

    def __str__(self):
        data = ""
        for i in range(len(self._payload)):
            data += "0x{:02X} ".format(self._payload[i])
        return "<state:{}, payload:{}>".format(self._state, data)

    def __eq__(self, other):
        if len(self._payload) != len(other._payload):
            return False

        for i in range(len(self._payload)):
            if self._payload[i] != other._payload[i]:
                return False

        return True

    def isFinish(self):
        return self._state == FrameState.END

    def isValid(self):
        if not self.isFinish():
            return False

        if self._payload[len(self._payload)-1] != self._computeChecksum():
            return False

        return True

    def _computeChecksum(self):
        checksum = 0

        for i in range(len(self._payload)-1):
            checksum ^= self._payload[i]

        return checksum

    def _addBytes(self, data):
        if isinstance(data, int):
            if data >= 0 and data <= 255:
                self._payload.append(data)
        elif isinstance(data, MagicChar):
            self._payload.append(data.value)
        return self

    def getEncodedFrame(self):
        encoded = [MagicChar.START_BYTE.value]
        for i in range(len(self._payload)):
            if (MagicChar.isMagic(self._payload[i])):
                encoded.append(MagicChar.ESC_BYTE.value)
            encoded.append(self._payload[i])

        encoded += [MagicChar.END_BYTE.value]
        return encoded

    def processByte(self, data):
        if self._state == FrameState.WAIT_HEADER:
            if data == MagicChar.START_BYTE.value:
                self.reset()
                self._state = FrameState.IN_FRAME
        elif self._state == FrameState.IN_FRAME:
            self.processByteInFrame(data)
        elif self._state == FrameState.IN_FRAME_ESC:
            self._addBytes(data)
            self._state = FrameState.IN_FRAME
        elif self._state == FrameState.END:
            self._state = FrameState.END
        return self

    def processByteInFrame(self, data):
        if isinstance(data, int):
            if data >= 0 and data <= 255:
                if data == MagicChar.START_BYTE.value:
                    self.reset()
                    self._state = FrameState.IN_FRAME
                elif data == MagicChar.ESC_BYTE.value:
                    self._state = FrameState.IN_FRAME_ESC
                elif data == MagicChar.END_BYTE.value:
                    self._state = FrameState.END
                else:
                    self._addBytes(data)
        return self

    def setMessage(self, message):
        self._payload = message.dump()
        self._payload.append(0x00)
        self._payload[len(self._payload)-1] = self._computeChecksum()
        self._state = FrameState.END
        return self

    def getMessage(self):
        if self._state != FrameState.END:
            return
        if not self.isValid():
            return
        message = SmpMessage()
        message.load(self._payload)
        return message

    def reset(self):
        del self._payload[:]
        self._state = FrameState.WAIT_HEADER
        return self
