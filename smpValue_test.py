import unittest
from smpValue import SmpValue, SmpType


class TestSmpValue(unittest.TestCase):
    def setUp(self):
        self.value = SmpValue()

    def test_setType(self):
        self.assertEqual(self.value.type, SmpType.SMP_TYPE_NONE)
        self.value.type = SmpType.SMP_TYPE_INT32
        self.assertEqual(self.value.type, SmpType.SMP_TYPE_INT32)
        self.value.type = 42
        self.assertEqual(self.value.type, SmpType.SMP_TYPE_INT32)

    def test_setValue(self):
        self.assertEqual(self.value.value, None)
        self.setTypeAndValue(SmpType.SMP_TYPE_NONE, -42, False)
        self.setTypeAndValue(SmpType.SMP_TYPE_NONE, 0, False)

        # Test uint8
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT8, -1, False)
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT8, 0, True)
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT8, 255, True)
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT8, 256, False)
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT8, 42.51, False)

        # Test int8
        self.setTypeAndValue(SmpType.SMP_TYPE_INT8, -129, False)
        self.setTypeAndValue(SmpType.SMP_TYPE_INT8, -128, True)
        self.setTypeAndValue(SmpType.SMP_TYPE_INT8, 127, True)
        self.setTypeAndValue(SmpType.SMP_TYPE_INT8, 128, False)
        self.setTypeAndValue(SmpType.SMP_TYPE_INT8, 42.51, False)

        # Test uint16
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT16, -1, False)
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT16, 0, True)
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT16, 65535, True)
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT16, 65536, False)
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT16, 42.51, False)

        # Test int16
        self.setTypeAndValue(SmpType.SMP_TYPE_INT16, -32769, False)
        self.setTypeAndValue(SmpType.SMP_TYPE_INT16, -32768, True)
        self.setTypeAndValue(SmpType.SMP_TYPE_INT16, 32767, True)
        self.setTypeAndValue(SmpType.SMP_TYPE_INT16, 32768, False)
        self.setTypeAndValue(SmpType.SMP_TYPE_INT16, 42.51, False)

        # Test uint32
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT32, -1, False)
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT32, 0, True)
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT32, 4294967295, True)
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT32, 4294967296, False)
        self.setTypeAndValue(SmpType.SMP_TYPE_UINT32, 42.51, False)

        # Test int32
        self.setTypeAndValue(SmpType.SMP_TYPE_INT32, -2147483649, False)
        self.setTypeAndValue(SmpType.SMP_TYPE_INT32, -2147483648, True)
        self.setTypeAndValue(SmpType.SMP_TYPE_INT32, 2147483647, True)
        self.setTypeAndValue(SmpType.SMP_TYPE_INT32, 2147483648, False)
        self.setTypeAndValue(SmpType.SMP_TYPE_INT32, 42.51, False)

        # Test uint64
        self.setTypeAndValue(
                    SmpType.SMP_TYPE_UINT64,
                    -1,
                    False
                )
        self.setTypeAndValue(
                    SmpType.SMP_TYPE_UINT64,
                    0,
                    True
                )
        self.setTypeAndValue(
                    SmpType.SMP_TYPE_UINT64,
                    18446744073709551615,
                    True
                )
        self.setTypeAndValue(
                    SmpType.SMP_TYPE_UINT64,
                    18446744073709551616,
                    False
                )
        self.setTypeAndValue(
                    SmpType.SMP_TYPE_UINT64,
                    42.51,
                    False
                )

        # Test int64
        self.setTypeAndValue(
                    SmpType.SMP_TYPE_INT64,
                    -9223372036854775809,
                    False
                )
        self.setTypeAndValue(
                    SmpType.SMP_TYPE_INT64,
                    -9223372036854775808,
                    True
                )
        self.setTypeAndValue(
                    SmpType.SMP_TYPE_INT64,
                    9223372036854775807,
                    True
                )
        self.setTypeAndValue(
                    SmpType.SMP_TYPE_INT64,
                    9223372036854775808,
                    False
                )
        self.setTypeAndValue(
                    SmpType.SMP_TYPE_INT64,
                    42.51,
                    False
                )

        # Test string
        self.setTypeAndValue(SmpType.SMP_TYPE_STRING, -42, False)
        self.setTypeAndValue(SmpType.SMP_TYPE_STRING, "-42", True)

    def setTypeAndValue(self, type, value, result):
        self.value.type = type
        self.value.value = value
        if result:
            self.assertEqual(self.value.value, value)
        else:
            self.assertNotEqual(self.value.value, value)

    def test_export(self):
        self.export(
                    SmpType.SMP_TYPE_UINT8,
                    0x42,
                    [0x01, 0x42]
                )
        self.export(
                    SmpType.SMP_TYPE_UINT16,
                    0x42,
                    [0x03, 0x42, 0x00]
                )
        self.export(
                    SmpType.SMP_TYPE_UINT32,
                    0x42,
                    [0x05, 0x42, 0x00, 0x00, 0x00]
                )
        self.export(
                    SmpType.SMP_TYPE_UINT64,
                    0x42,
                    [0x07, 0x42, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
                )
        self.export(
                    SmpType.SMP_TYPE_INT8,
                    0x42,
                    [0x02, 0x42]
                )
        self.export(
                    SmpType.SMP_TYPE_INT16,
                    0x42,
                    [0x04, 0x42, 0x00]
                )
        self.export(
                    SmpType.SMP_TYPE_INT32,
                    0x42,
                    [0x06, 0x42, 0x00, 0x00, 0x00]
                )
        self.export(
                    SmpType.SMP_TYPE_INT64,
                    0x42,
                    [0x08, 0x42, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
                )
        self.export(
                    SmpType.SMP_TYPE_INT8,
                    -4,
                    [0x02, 0xfc]
                )
        self.export(
                    SmpType.SMP_TYPE_INT16,
                    -256,
                    [0x04, 0x00, 0xff]
                )
        self.export(
                    SmpType.SMP_TYPE_INT32,
                    -65536,
                    [0x06, 0x00, 0x00, 0xff, 0xff]
                )
        self.export(
                    SmpType.SMP_TYPE_STRING,
                    "1337",
                    [0x09, 0x05, 0x00, 0x31, 0x33, 0x33, 0x37, 0x00]
                )

    def export(self, type, value, data):
        self.value.type = type
        self.value.value = value
        self.assertEqual(data, self.value.dump())

    def test_import(self):
        uselessValue = 0xff
        self.loadTest(
                    [0x01, 0x42, uselessValue],
                    SmpValue(SmpType.SMP_TYPE_UINT8, 0x42),
                    2
                )
        self.loadTest(
                    [0x03, 0x42, 0x00, uselessValue],
                    SmpValue(SmpType.SMP_TYPE_UINT16, 0x42),
                    3
                )
        self.loadTest(
                    [0x05, 0x42, 0x00, 0x00, 0x00, uselessValue],
                    SmpValue(SmpType.SMP_TYPE_UINT32, 0x42),
                    5
                )
        self.loadTest(
                    [
                        0x07, 0x42, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00, uselessValue
                    ],
                    SmpValue(SmpType.SMP_TYPE_UINT64, 0x42),
                    9
                )
        self.loadTest(
                    [0x02, 0x42, uselessValue],
                    SmpValue(SmpType.SMP_TYPE_INT8, 0x42),
                    2
                )
        self.loadTest(
                    [0x04, 0x42, 0x00, uselessValue],
                    SmpValue(SmpType.SMP_TYPE_INT16, 0x42),
                    3
                )
        self.loadTest(
                    [0x06, 0x42, 0x00, 0x00, 0x00, uselessValue],
                    SmpValue(SmpType.SMP_TYPE_INT32, 0x42),
                    5
                )
        self.loadTest(
                    [
                        0x08, 0x42, 0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, uselessValue
                    ],
                    SmpValue(SmpType.SMP_TYPE_INT64, 0x42),
                    9
                )
        self.loadTest(
                    [0x02, 0xfc, uselessValue],
                    SmpValue(SmpType.SMP_TYPE_INT8, -4),
                    2
                )
        self.loadTest(
                    [0x04, 0x00, 0xff, uselessValue],
                    SmpValue(SmpType.SMP_TYPE_INT16, -256),
                    3
                )
        self.loadTest(
                    [0x06, 0x00, 0x00, 0xff, 0xff, uselessValue],
                    SmpValue(SmpType.SMP_TYPE_INT32, -65536),
                    5
                )
        self.loadTest(
                    [
                        0x09, 0x05, 0x00, 0x31, 0x33,
                        0x33, 0x37, 0x0, uselessValue
                    ],
                    SmpValue(SmpType.SMP_TYPE_STRING, "1337"),
                    8
                )

        # Bad string
        self.loadTest(
                    [
                        0x09, 0x05, 0x00, 0x31, 0x33,
                        0x33, 0x37, 0xff, uselessValue
                    ],
                    SmpValue(),
                    0
                )

    def loadTest(self, bytesArray, value, size):
        smpValue = SmpValue()
        self.assertEqual(size, smpValue.load(bytesArray))
        self.assertEqual(smpValue, value)


if __name__ == '__main__':
    unittest.main()
