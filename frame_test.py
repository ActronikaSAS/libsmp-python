import unittest
from frame import Frame, MagicChar, FrameState
from smpValue import SmpValue, SmpType
from smpMessage import SmpMessage


class TestFrame(unittest.TestCase):
    def setUp(self):
        self.frame = Frame()

    def test_str(self):
        self.assertEqual(
                    self.frame,
                    self.frame._addBytes(MagicChar.START_BYTE)
                )
        self.assertEqual(self.frame, self.frame._addBytes(0x42))
        self.assertEqual(self.frame, self.frame._addBytes(0x12))
        self.assertEqual(self.frame, self.frame._addBytes(0x25))
        self.assertEqual(self.frame, self.frame._addBytes(MagicChar.END_BYTE))
        self.assertEqual(str(self.frame), "<state:FrameState.WAIT_HEADER,\
 payload:0x10 0x42 0x12 0x25 0xFF >")

    def test_constructor(self):
        value1 = SmpValue(SmpType.SMP_TYPE_UINT8, 42)
        value2 = SmpValue(SmpType.SMP_TYPE_INT32, -1337)
        message = SmpMessage(0x25)
        message.addValue(value1).addValue(value2)
        frame = Frame(message)
        self.assertEqual(
            frame._payload,
            [
                0x25, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00,
                0x01, 42, 0x06, 0xC7, 0xFA, 0xFF, 0xFF, 0x32
            ]
        )

    def test_computeChecksum(self):
        # Add some bytes
        self.frame._addBytes(0x21)._addBytes(0x42)._addBytes(0xff)
        # Add checksum
        self.frame._addBytes(0x9c)
        self.assertEqual(0x9c, self.frame._computeChecksum())

        self.frame.reset()
        self.assertEqual(0x00, self.frame._computeChecksum())

        self.frame.reset()
        self.frame._payload = [
                    0x25, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x01, 42,
                    0x06, 0xC7, 0xFA, 0xFF, 0xFF, 0x32
                ]
        self.assertEqual(0x32, self.frame._computeChecksum())

    def test_isValid(self):
        # Test simple frame

        # Add some bytes
        self.frame._addBytes(0x21)._addBytes(0x42)._addBytes(0xff)
        # Add checksum
        self.frame._addBytes(0x9c)
        self.frame._state = FrameState.END
        self.assertTrue(self.frame.isValid())
        # Test bad checksum
        self.frame.reset()
        self.frame._state = FrameState.END
        # Add some bytes
        self.frame._addBytes(0x21)._addBytes(0x42)._addBytes(0xff)
        # Add checksum
        self.frame._addBytes(0x9d)
        self.assertFalse(self.frame.isValid())

    def test_getEncodedFrame(self):
        encoded = [
                    MagicChar.START_BYTE.value,
                    MagicChar.ESC_BYTE.value, 16, 0x21, 0x42,
                    MagicChar.ESC_BYTE.value, 0xff,
                    MagicChar.ESC_BYTE.value, 16, 0x9c,
                    MagicChar.END_BYTE.value
                ]
        self.frame._state = FrameState.END
        # Add some bytes
        self.frame._addBytes(16)._addBytes(0x21)._addBytes(0x42)
        self.frame._addBytes(0xff)._addBytes(16)
        # Add checksum
        self.frame._addBytes(0x9c)
        self.assertTrue(self.frame.isValid())
        self.assertEqual(encoded, self.frame.getEncodedFrame())

    def test_setMessage(self):
        value1 = SmpValue(SmpType.SMP_TYPE_UINT8, 42)
        value2 = SmpValue(SmpType.SMP_TYPE_INT32, -1337)
        message = SmpMessage(0x25)
        message.addValue(value1).addValue(value2)
        self.assertEqual(self.frame._state, FrameState.WAIT_HEADER)
        self.assertEqual(self.frame, self.frame.setMessage(message))
        self.assertEqual(self.frame._state, FrameState.END)
        self.assertEqual(self.frame._payload, [
                    0x25, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x01, 42,
                    0x06, 0xC7, 0xFA, 0xFF, 0xFF, 0x32
                ])

    def test_getMessage(self):
        value1 = SmpValue(SmpType.SMP_TYPE_UINT8, 42)
        value2 = SmpValue(SmpType.SMP_TYPE_INT32, -1337)
        message = SmpMessage(0x25)
        message.addValue(value1).addValue(value2)
        self.frame._payload = [
                    0x25, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x01,
                    42, 0x06, 0xC7, 0xFA, 0xFF, 0xFF, 0x5A
                ]
        self.frame._state = FrameState.END
        self.assertEqual(None, self.frame.getMessage())
        self.frame._payload = [
                    0x25, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x01, 42,
                    0x06, 0xC7, 0xFA, 0xFF, 0xFF, 0x32
                ]
        self.frame._state = FrameState.END
        self.assertEqual(message, self.frame.getMessage())

    def test_processByte(self):
        payload = [
                    MagicChar.START_BYTE.value, 0x25,
                    0x42, MagicChar.ESC_BYTE.value, MagicChar.END_BYTE.value,
                    MagicChar.ESC_BYTE.value, MagicChar.START_BYTE.value,
                    MagicChar.ESC_BYTE.value, MagicChar.ESC_BYTE.value, 0x93,
                    MagicChar.END_BYTE.value
                ]
        self.assertEqual(self.frame._state, FrameState.WAIT_HEADER)
        self.assertEqual(self.frame, self.frame.processByte(payload[0]))
        self.assertEqual(self.frame._state, FrameState.IN_FRAME)
        for i in range(1, len(payload) - 1):
            self.assertEqual(self.frame, self.frame.processByte(payload[i]))
        self.assertEqual(self.frame._state, FrameState.IN_FRAME)
        self.assertEqual(self.frame,
                         self.frame.processByte(payload[len(payload)-1]))
        self.assertEqual(self.frame._state, FrameState.END)
        self.assertEqual(self.frame._payload, [
                    0x25, 0x42, MagicChar.END_BYTE.value,
                    MagicChar.START_BYTE.value, MagicChar.ESC_BYTE.value, 0x93
                ])
