import drivers
from drivers.dependencies import *
ArduinoDevice = drivers.getDeviceClass('arduino', 'ArduinoDevice')
ArduinoExecutor = drivers.getDeviceClass('arduino', 'ArduinoExecutor')


class D13LED(ArduinoExecutor):
    driverId = 'A001'
    typeDescription = 'Светодиод на пине 13'

    def __init__(self, atBoard: ArduinoDevice, atPin: str, **kwargs):
        ArduinoExecutor.__init__(self, atBoard, atPin, kwargs['isEnabled'], 
            kwargs['instanceName'], kwargs['instanceDescription'])
        self.type = ArduinoExecutor.Digital
        self.parent.sendString('LEDo(3,1000)') #Включить моргание светодиода
