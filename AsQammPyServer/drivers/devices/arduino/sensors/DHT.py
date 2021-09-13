import drivers
from drivers.dependencies import *
ArduinoDevice = drivers.getDeviceClass('arduino', 'ArduinoDevice')
ArduinoSensor = drivers.getDeviceClass('arduino', 'ArduinoSensor')


class DHT22Sensor(ArduinoSensor):
    driverId = 'TS02'
    typeDisplayName = 'Датчик температуры DHT22'
    typeDescription = 'Цифровой датчик температуры DHT22'

    
    def __init__(self, atBoard: ArduinoDevice, atPin, **kwargs):
        ArduinoSensor.__init__(self, atBoard, atPin,
            kwargs['isEnabled'], False, kwargs['instanceName'], kwargs['instanceDescription'],
            self.temperature)

        self.attrl.extend(['probeFrequency'])
        self.type = ArduinoSensor.Digital
        if 'probeFrequency' in kwargs.keys(): self.probeFrequency = float(kwargs['probeFrequency'])
        else: self.probeFrequency = 60.0
        

    def temperature(self) -> float:
        '''
        Получить температуру с датчика.

        :returns: float
        '''
        self.parent.sendString(f'DHTt({self.deviceAddress[-1]})')
        sleep(2)

        return float(self.parent.getLastMessage().receivedInfo[0])
