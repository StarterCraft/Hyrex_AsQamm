from drivers.dependencies import *

class D13LED(AqHardwareModule.ArduinoExecutor):
    typeDescription = 'Светодиод на пине 13'
    driverId = 1000

    def __init__(self, atBoard: AqHardwareDevice.ArduinoDevice, atPin: str, **kwargs):
        super().__init__(atBoard, atPin, kwargs['isEnabled'], 
                         kwargs['instanceName'], 
                         kwargs['instanceDescription'])
        self.type = AqHardwareModule.ArduinoExecutor.Digital
        self.motherBoard.sendString('LEDo()') #Включить моргание светодиода
