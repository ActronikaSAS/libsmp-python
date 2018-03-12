# Python LibSMP

[![Build Status](http://jenkins.actronika.com:8080/buildStatus/icon?job=libsmp-python)](https://jenkins.actronika.com:8080/job/libsmp-python/)

## Reference

libsmp stands for Simple Message Protocol library. It aims to provide a simple
protocol to exchange message between two peers over a serial lane. Messages are
identified by an ID, choosen by user application, and contains 0 or more
arguments which are typed.

For more informations, go to [https://github.com/ActronikaSAS/libsmp](https://github.com/ActronikaSAS/libsmp)

## Dependencies

* unittest (for unit test only)
* pycodestyle (for unit test)
* serial

```
sudo -h pip3 install pyserial unittest pycodestyle
```

## How to use

In a folder, clone repo and create test file with next example.
Execute the example.

```bash
mkdir libsmp-example
cd libsmp-example
git clone git@github.com:ActronikaSAS/libsmp-python.git
touch example.py
# Edit example.py to set example
python3 example.py
```

```python
"""
    To execute this test, connect the TX of serial port to RX
"""
from libsmp import SerialFrame, Frame, SmpMessage, SmpType, SmpValue

# Define callback when received valid serial data
def callback(message):
    print("Received message :")
    print(str(message))

# Create object serial
serial = SerialFrame('/dev/ttyUSB1')

# Set callback for Serial
serial.callback = callback

# Open serial port
serial.open()

# Define some SmpValue
values = [
    SmpValue(SmpType.SMP_TYPE_INT8, -42),
    SmpValue(SmpType.SMP_TYPE_UINT8, 0x42),
    SmpValue(SmpType.SMP_TYPE_INT64, -563214795),
    SmpValue(SmpType.SMP_TYPE_STRING, "Hello World !"),
]

# Create message object with id 0x42424242
message = SmpMessage(0x42424242)

# Add value in message
for value in values:
    message.addValue(value)

# Create Frame
frame = Frame()

# Add message in frame
frame.setMessage(message)

# Write frame on serial
serial.write(frame)

"""
    Normally, you print received message:
        > Received message :
        > <id:1111638594,values:[<0x02,-42>,<0x01,66>,<0x08,-563214795>,<0x09,Hello World !>,]>
"""
```

## How to test

In the module folder, you can execute unit test with script test.py

```bash
git clone git@github.com:ActronikaSAS/libsmp-python.git
cd libsmp-python
python3 test.py
```
