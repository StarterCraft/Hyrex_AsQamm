import drivers
from drivers.dependencies import *
ArduinoDevice = drivers.getDeviceClass('arduino', 'ArduinoDevice')
ArduinoSensor = drivers.getDeviceClass('arduino', 'ArduinoSensor')


class GroveTemperatureSensor(ArduinoSensor):
    driverId = 'TS01'
    typeDescription = 'Аналоговый датчик темпepaтуры Grove версии 1.2'


    def __init__(self, atBoard: ArduinoDevice, atPin, **kwargs):
        super().__init__(atBoard, atPin,
            kwargs['isEnabled'], kwargs['instanceName'], kwargs['instanceDescription'])

        self.attrl.extend(['calibrationValue', 'probeFrequency'])
        self.type = ArduinoSensor.Analog
        
        self.canRetrieve = True
        self.retrieves = [
            AqHardwareValueType(self, 'TEMPC', float, 'celsius', self.temperature,
                (kwargs['probeFrequency'][0] if 'probeFrequency' in kwargs.keys() else 60.0),
                calm = self.calibrate, calv = kwargs['calibrationValue'],
                typeDisplayName = 'Температура, oC')]

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
                        (4275) + 1 / 298.15) - self.retrieves[0].calibrationValue), 1)
        except TypeError:
            sleep(2)
            return self.temperature()


    def calibrate(self, calibrationValue: float):
        self.retrieves[0].calibrationValue = calibrationValue
