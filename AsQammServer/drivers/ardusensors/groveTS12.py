from drivers.dependencies import *


class GroveTemperatureSensor(AqAbstractHardwareModule.ArduinoSensor):
    driverId = 1101
    typeDescription = 'Аналоговый датчик темпepaтуры Grove версии 1.2'

    def __init__(self, atBoard, atPin, **kwargs):
        super().__init__(atBoard, atPin, kwargs['isEnabled'], True, 
                         kwargs['instanceName'],
                         kwargs['instanceDescription'], 
                         self.temperature)
        self.attrl.extend(['calibrationValue', 'probeFrequency'])
        self.type = AqAbstractHardwareModule.ArduinoSensor.Analog
        self.bValue = 4275
        self.calibrationValue = int(kwargs['calibrationValue'])
        self.outputAccuracy = int(kwargs['outputAccuracy'])
        if kwargs['probeFrequency']: self.probeFrequency = float(kwargs['probeFrequency'])
        else: self.probeFrequency = 60.0

        try:
            while not self.motherPin.read():
                self.motherPin.read()
                slp(0.5)
        except AttributeError: pass

                     
    def value(self):
        if self.motherPin.read():
            return self.motherPin.read()


    def temperature(self):
        try:
            return round((1.0 / (log(1023.0 / self.value() - 1.0) / 
                        (self.bValue) + 1 / 298.15) - self.calibrationValue), self.outputAccuracy)
        except TypeError:
            slp(2)
            self.temperature()


    def calibrate(self, calibrationValue: int):
        self.calibrationValue = calibrationValue
