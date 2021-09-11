import drivers
from drivers.dependencies import *
ArduinoDevice = drivers.getDeviceClass('arduino', 'ArduinoDevice')


class AqArduinoUnoR3(ArduinoDevice):
    driverId = 'AUR3'

    typeDisplayName = 'Arduino UNO R3'
    typeDescription = 'Стандартная Arduino UNO R3'
    digitalPins = ['d:0', 'd:1', 'd:2', 'd:3', 'd:4', 'd:5', 'd:6', 'd:7', 'd:8', 'd:9', 'd:10', 'd:11', 'd:12']
    analogPins = ['a:0', 'a:1', 'a:2', 'a:3', 'a:4', 'a:5']

    def __init__(self, comPort: str, dr, **kwargs):
        ArduinoDevice.__init__(self, comPort, kwargs['isEnabled'], kwargs['instanceName'], kwargs['instanceDescription'])
        try:
           self.iterator.setName(f'Iterator:ArduinoUno:{self.motherPort}')
           self.iterator.start()
        except AttributeError: pass


        self.setChildren(kwargs['children'], dr)
