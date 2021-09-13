import drivers
from drivers.dependencies import *
ArduinoDevice = drivers.getDeviceClass('arduino', 'ArduinoDevice')


class AqSeeeduinoV4WithBaseShield(ArduinoDevice):
    driverId = 'ASV4'

    typeDisplayName = 'Seeduino V4 (Grove Base Shield)'
    typeDescription = 'Seeeduino V4 от Seeed c установленным Grove Base Shield'
    digitalPins = ['d:2', 'd:3', 'd:4', 'd:5', 'd:6', 'd:7', 'd:8']
    analogPins = ['a:0', 'a:1', 'a:2', 'a:3']

    def __init__(self, comPort: str, dr, **kwargs):
        ArduinoDevice.__init__(self, comPort, 
            kwargs['isEnabled'], kwargs['instanceName'], kwargs['instanceDescription'])
        try:
           self.iterator.setName(f'Iterator:ArduinoUno:{self.motherPort}')
           self.iterator.start()
        except AttributeError: pass

        self.setChildren(kwargs['pinMap'], dr)
