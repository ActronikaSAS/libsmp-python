import serial
import threading
import time
try:
    from .frame import Frame
except (ImportError, SystemError):
    from frame import Frame


class SerialFrame(object):
    def __init__(self, port, callback=None, baudrate=115200):
        self._serial = serial.Serial()
        self._serial.port = port
        self._serial.baudrate = baudrate
        self._serial_open = False
        self._listener_thread = threading.Thread(target=self.listen)
        self.callback = callback
        self._frame = Frame()

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, callback):
        if callable(callback):
            self._callback = callback
        else:
            self._callback = None

    def open(self):
        self._serial.timeout = None
        self._serial.open()
        self._serial_open = True
        self._listener_thread.start()

    def close(self):
        if self._serial_open:
            self._serial_open = False
            self._serial.close()
            self._listener_thread.join()

    def listen(self):
        while self._serial_open:
            try:
                incoming_bytes = self._serial.read(self._serial.in_waiting)
            except OSError:
                print("error: serial disconnected")
                self._serial_open = False
                return
            for incoming_byte in incoming_bytes:
                self._frame.processByte(int(incoming_byte))
                if self._frame.isValid():
                    if self._callback is not None:
                        self._callback(self._frame.getMessage())
                    self._frame.reset()
            time.sleep(0.1)

    def write(self, frame):
        if isinstance(frame, Frame):
            self._serial.write(frame.getEncodedFrame())
        elif isinstance(frame, list):
            for value in frame:
                self.write(value)
