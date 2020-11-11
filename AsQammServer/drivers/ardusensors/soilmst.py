from drivers.dependencies import *


class CapacitiveSoilMoistureSensor(AqAbstractHardwareModule.ArduinoSensor):
    driverId = 1102

    def __init__(self, atBoard: AqAbstractHardwareUnit.ArduinoUnit, atPin: str, **kwargs):
        super().__init__(atBoard, atPin, kwargs['isEnabled'], False, kwargs['name'], kwargs['description'],
                        'Аналоговый ёмкостный датчик влажности почвы версии 1.0', self.moisture)
        self.attrl.extend(['calibrationValue', 'probeFrequency'])
        self.type = AqAbstractHardwareModule.ArduinoSensor.Analog
        self.probeFrequency = float(probeFrequency)
        

    def value(self):
        if self.motherPin.read():
            return self.motherPin.read()
        else:
            pass


    def moisture(self):
        if self.value():
            m = self.motherPin.read() * 100
            return ceil(m)
        else:
            return
