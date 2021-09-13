import drivers
from drivers.dependencies import *
ArduinoDevice = drivers.getDeviceClass('arduino', 'ArduinoDevice')
ArduinoSensor = drivers.getDeviceClass('arduino', 'ArduinoSensor')


class GroveTemperatureSensor(ArduinoSensor):
    driverId = 'TS01'
    typeDescription = 'Аналоговый датчик темпepaтуры Grove версии 1.2'


    def __init__(self, atBoard: ArduinoDevice, atPin, **kwargs):
        super().__init__(atBoard, atPin,
            kwargs['isEnabled'], True, kwargs['instanceName'], kwargs['instanceDescription'],
            self.temperature, clmeth = self.calibrate)

        self.attrl.extend(['calibrationValue', 'probeFrequency'])
        self.type = ArduinoSensor.Analog
        self.bValue = 4275
        self.calibrationValue = int(kwargs['calibrationValue'])
        self.outputAccuracy = int(kwargs['outputAccuracy'])
        if 'probeFrequency' in kwargs.keys(): self.probeFrequency = float(kwargs['probeFrequency'])
        else: self.probeFrequency = 60.0

        try:
            while not self.motherPin.read():
                self.motherPin.read()
                sleep(0.5)
        except AttributeError: pass

                     
    def value(self):
        if self.motherPin.read():
            return self.motherPin.read()


    def temperature(self):
        try:
            return round((1.0 / (log(1023.0 / self.value() - 1.0) / 
                        (self.bValue) + 1 / 298.15) - self.calibrationValue), self.outputAccuracy)
        except TypeError:
            sleep(2)
            return self.temperature()


    def calibrate(self, calibrationValue: int):
        self.calibrationValue = calibrationValue
