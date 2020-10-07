from pandas import    (read_csv    as csv)
from pyfirmata import (Arduino     as ArduinoUno,
                       ArduinoMega as ArduinoMega,
                       util        as ArduinoUtil)

from PyQt5.QtCore import (QThread    as QThread,
                          pyqtSignal as QSignal)


class AqArduinoHardwareUnit:
    def __init__(self, arduType: (ArduinoUno or ArduinoMega), COM: str, pinMap):
        self.board = arduType(COM)
        self.iterator = ArduinoUtil.Iterator(self.board)


    def registerPinValue(self, PIN: str):
        pin = self.board.get_pin(PIN + ':i')
        pin.read()
