import unittest
from smpValue import SmpValue, SmpType
from smpMessage import SmpMessage


class TestSmpMessage(unittest.TestCase):
    def setUp(self):
        self.message = SmpMessage()
        self.values = [
            SmpValue(SmpType.SMP_TYPE_UINT8, 42),
            SmpValue(SmpType.SMP_TYPE_UINT16, 4242),
            SmpValue(SmpType.SMP_TYPE_INT8, -42),
            SmpValue(SmpType.SMP_TYPE_STRING, "Caribou"),
        ]

    def test_setMsgid(self):
        self.assertEqual(self.message.msgid, 0)
        self.message.msgid = 42
        self.assertEqual(self.message.msgid, 42)
        self.message.msgid = -1
        self.assertEqual(self.message.msgid, 42)
        self.message.msgid = 0
        self.assertEqual(self.message.msgid, 0)
        self.message.msgid = 0xffffffff
        self.assertEqual(self.message.msgid, 0xffffffff)
        self.message.msgid = 0xffffffff + 1
        self.assertEqual(self.message.msgid, 0xffffffff)

    def test_addValue(self):
        self.assertEqual(self.message.getNumberOfValues(), 0)
        for i in range(len(self.values)):
            self.assertEqual(
                        self.message,
                        self.message.addValue(self.values[i])
                    )
            self.assertEqual(self.message.getNumberOfValues(), i + 1)
            for j in range(self.message.getNumberOfValues() - 1):
                self.assertEqual(self.message.getValue(j), self.values[j])

    def test_removeValue(self):
        for i in range(len(self.values)):
            self.assertEqual(
                        self.message,
                        self.message.addValue(self.values[i])
                    )

        self.assertEqual(self.message, self.message.removeValue(3))
        self.assertEqual(self.message.getNumberOfValues(), 3)
        self.assertEqual(self.message, self.message.removeValue(1))
        self.assertEqual(self.message.getNumberOfValues(), 2)
        self.assertEqual(self.message.getValue(0), self.values[0])
        self.assertEqual(self.message.getValue(1), self.values[2])
        self.assertEqual(self.message, self.message.removeValue(3))
        self.assertEqual(self.message.getValue(0), self.values[0])
        self.assertEqual(self.message.getValue(1), self.values[2])

    def test_resetValue(self):
        for i in range(len(self.values)):
            self.assertEqual(
                        self.message,
                        self.message.addValue(self.values[i])
                    )
        self.assertEqual(self.message.getNumberOfValues(), 4)

        self.assertEqual(self.message, self.message.resetValue())
        self.assertEqual(self.message.getNumberOfValues(), 0)

    def test_string(self):
        self.message.msgid = 25
        self.message.addValue(self.values[0]).addValue(self.values[3])
        self.assertEqual(
                    "<id:25,values:[<0x01,42>,<0x09,Caribou>,]>",
                    str(self.message)
                )

    def test_dump(self):
        self.message.msgid = 0x25
        self.message.addValue(self.values[0]).addValue(self.values[1])
        exported = [
                    0x25, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x01, 42,
                    0x03, 0x92, 0x10
                ]
        self.assertEqual(exported, self.message.dump())

        # With string
        self.message.resetValue()
        self.message.msgid = 0x45623187
        for value in self.values:
            self.message.addValue(value)
        exported = [
                    0x87, 0x31, 0x62, 0x45, 0x12, 0x00, 0x00, 0x00, 0x01, 42,
                    0x03, 0x92, 0x10, 0x02, 0xd6, 0x09, 0x08, 0x00, 0x43, 0x61,
                    0x72, 0x69, 0x62, 0x6F, 0x75, 0x00
                ]
        self.assertEqual(exported, self.message.dump())

    def test_load(self):
        uselessValue = 0x42
        message = SmpMessage(0x25)
        message.addValue(self.values[0]).addValue(self.values[1])
        imported = [
                    0x25, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x01, 42,
                    0x03, 0x92, 0x10, uselessValue
                ]
        self.assertEqual(13, self.message.load(imported))
        self.assertEqual(message, self.message)

        message = SmpMessage(0x45623187)
        self.message.resetValue()
        for value in self.values:
            message.addValue(value)
        imported = [
                    0x87, 0x31, 0x62, 0x45, 0x12, 0x00, 0x00, 0x00, 0x01, 42,
                    0x03, 0x92, 0x10, 0x02, 0xd6, 0x09, 0x08, 0x00, 0x43, 0x61,
                    0x72, 0x69, 0x62, 0x6F, 0x75, 0x00, uselessValue
                ]
        self.assertEqual(26, self.message.load(imported))
        self.assertEqual(message, self.message)
