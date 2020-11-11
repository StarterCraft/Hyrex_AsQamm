from drivers.dependencies import *


class AqSeeeduinoV4WithBaseShield(AqAbstractHardwareUnit.ArduinoUnit, pyfirmata.Arduino):
    driverId = 1072
    digitalPins = ['d:2', 'd:3', 'd:4', 'd:5', 'd:6', 'd:7', 'd:8']
    analogPins = ['a:0', 'a:1', 'a:2', 'a:3']

    def __init__(self, comPort: str, dr, **kwargs):
        pyfirmata.Arduino.__init__(self, comPort)
        AqAbstractHardwareUnit.ArduinoUnit.__init__(self, comPort, kwargs['isEnabled'], kwargs['description'])
        self.iterator.setName(f'Iterator:SeeeduinoV4:{self.motherPort}')
        if self.isEnabled:
            self.iterator.start()

        self.setPinMap(kwargs['pinMap'], dr)
