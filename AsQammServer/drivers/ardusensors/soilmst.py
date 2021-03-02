from drivers.dependencies import *


class CapacitiveSoilMoistureSensor(AqHardwareModule.ArduinoSensor):
    driverId = 1102

    def __init__(self, atBoard: AqHardwareUnit.ArduinoUnit, atPin: str, **kwargs):
        super().__init__(atBoard, atPin, kwargs['isEnabled'], True, kwargs['name'], kwargs['description'],
                        'Аналоговый ёмкостный датчик влажности почвы версии 1.0', self.moisture)
        self.attrl.extend(['calibrationValue', 'probeFrequency'])
        self.type = AqHardwareModule.ArduinoSensor.Analog

        self.topCalibrationValue = int(kwargs['topCalibrationValue'])
        self.lowCalibrationValue = int(kwargs['lowCalibrationValue'])
        self.outputAccuracy = int(kwargs['outputAccuracy'])
        self.probeFrequency = float(kwargs['probeFrequency'])
        

    def value(self):
        if self.motherPin.read():
            return self.motherPin.read() * 1000
        else:
            pass
        

    def mathMap(self, x, inMin, inMax, outMin, outMax):
        return (x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin


    def moisture(self):
        if self.value():
            return round(self.mathMap(self.value(), self.lowCalibrationValue, self.topCalibrationValue, 0, 100), self.outputAccuracy)
        else:
            return
