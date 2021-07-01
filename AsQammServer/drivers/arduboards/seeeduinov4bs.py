from drivers.dependencies import *


class AqSeeeduinoV4WithBaseShield(AqHardwareDevice.ArduinoDevice, pyfirmata.Arduino):
    driverId = 1072
    typeDescription = 'Seeeduino V4 от Seeed c установленным Grove Base Shield'
    digitalPins = ['d:2', 'd:3', 'd:4', 'd:5', 'd:6', 'd:7', 'd:8']
    analogPins = ['a:0', 'a:1', 'a:2', 'a:3']

    def __init__(self, comPort: str, dr, **kwargs):
        AqHardwareDevice.ArduinoDevice.__init__(self, comPort, kwargs['isEnabled'],
                                                    kwargs['instanceName'],
                                                    kwargs['instanceDescription'])
        try:
           self.iterator.setName(f'Iterator:ArduinoUno:{self.motherPort}')
           self.iterator.start()
        except AttributeError: pass

        self.setPinMap(kwargs['pinMap'], dr)
