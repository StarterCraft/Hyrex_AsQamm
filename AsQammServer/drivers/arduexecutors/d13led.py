from drivers.dependencies import *

class D13LED(AqAbstractHardwareModule.ArduinoExecutor):
    driverId = 1000

    def __init__(self, atBoard: AqAbstractHardwareUnit.ArduinoUnit, atPin: str, **kwargs):
        super().__init__(atBoard, atPin, kwargs['isEnabled'], kwargs['name'], kwargs['description'], '')
        self.type = AqAbstractHardwareModule.ArduinoExecutor.Digital


    def checkState(self):
        if self.motherPin.mode == AqArduinoHardwareModes.Input:
            return bool(self.motherPin.read())
        else:
            self.motherPin.mode = AqArduinoHardwareModes.Input
            return bool(self.motherPin.read())


    def setState(self, state: bool):
        if self.motherPin.mode == AqArduinoHardwareModes.Output:
            self.motherPin.write(state)
        else:
            self.motherPin.mode = AqArduinoHardwareModes.Output
            self.motherPin.write(state)

