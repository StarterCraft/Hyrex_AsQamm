from drivers.dependencies import *


class AqArduinoUnoR3(AqHardwareDevice.ArduinoDevice, pyfirmata.Arduino):
    driverId = 1071
    typeDescription = 'Стандартная Arduino UNO R3'
    digitalPins = ['d:0', 'd:1', 'd:2', 'd:3', 'd:4', 'd:5', 'd:6', 'd:7', 'd:8', 'd:9', 'd:10', 'd:11', 'd:12']
    analogPins = ['a:0', 'a:1', 'a:2', 'a:3', 'a:4', 'a:5']

    def __init__(self, comPort: str, dr, **kwargs):
        AqHardwareDevice.ArduinoDevice.__init__(self, comPort, kwargs['isEnabled'],
                                                    kwargs['instanceName'],
                                                    kwargs['instanceDescription'])
        try:
           self.iterator.setName(f'Iterator:ArduinoUno:{self.motherPort}')
           self.iterator.start()
        except AttributeError: pass


        self.setPinMap(kwargs['pinMap'], dr)
