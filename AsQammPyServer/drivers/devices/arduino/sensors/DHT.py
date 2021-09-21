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
            kwargs['isEnabled'], kwargs['instanceName'], kwargs['instanceDescription'])

        print(kwargs)
        self.attrl.extend(['probeFrequency'])
        self.type = ArduinoSensor.Digital

        self.canRetrieve = True
        self.retrieves = [
            AqHardwareValueType(self, 'TEMPC', float, 'celsius', self.temperature, 
                (kwargs['probeFrequency'][0] if 'probeFrequency' in kwargs.keys() else 60.0),
                typeDisplayName = 'Температура, oC'),
            
            AqHardwareValueType(self, 'HUMIP', float, 'percent', self.humidity,
                (kwargs['probeFrequency'][1] if 'probeFrequency' in kwargs.keys() else 60.0),
                typeDisplayName = 'Относительная влажность, %')]
        

    def temperature(self) -> float:
        '''
        Получить температуру с датчика.

        :returns: float
        '''
        self.parent.sendString(f'DHTt({self.deviceAddress[-1]})')

        try:
            return float(self.parent.getLastMessage().receivedInfo[0])
        except AttributeError:
            while not hasattr(self.parent.getLastMessage(), 'receivedInfo'): sleep(1)
            return float(self.parent.getLastMessage().receivedInfo[0])



    def humidity(self) -> float:
        '''
        Получить влажность с датчика.

        :returns: float
        '''
        self.parent.sendString(f'DHTt({self.deviceAddress[-1]})')
        
        try:
            return float(self.parent.getLastMessage().receivedInfo[1])
        except AttributeError:
            while not hasattr(self.parent.getLastMessage(), 'receivedInfo'): sleep(1)
            return float(self.parent.getLastMessage().receivedInfo[1])
