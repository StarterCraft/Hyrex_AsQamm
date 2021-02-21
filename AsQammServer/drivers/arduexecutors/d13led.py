from drivers.dependencies import *

class D13LED(AqAbstractHardwareModule.ArduinoExecutor):
    driverId = 1000

    def __init__(self, atBoard: AqAbstractHardwareUnit.ArduinoUnit, atPin: str, **kwargs):
        super().__init__(atBoard, atPin, kwargs['isEnabled'], kwargs['name'], kwargs['description'], '')
        self.type = AqAbstractHardwareModule.ArduinoExecutor.Digital
        self.motherBoard.sendString('LEDo()') #Включить моргание светодиода

