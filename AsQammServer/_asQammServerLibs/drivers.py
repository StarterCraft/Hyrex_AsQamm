from _asQammServerLibs.hardware import (AqAbstractHardwareUnit,
                                        AqAbstractHardwareModule)

from pyfirmata import (Arduino     as ArduinoUno,
                       ArduinoMega as ArduinoMega,
                       util        as ArduinoUtil,
                       PinAlreadyTakenError,
                       )
from math import       (log        as log,
                        ceil       as ceil)

#####################################################
#            #         Платы           #            #
#####################################################

class AqArduinoUnoR3(AqAbstractHardwareUnit.ArduinoUnit, ArduinoUno):
    driverId = 1071

    def __init__(self, comPort: str, pinMap: dict, desc: str):
        ArduinoUno.__init__(self, comPort)
        AqAbstractHardwareUnit.ArduinoUnit.__init__(self, comPort)
        self.iterator.setName(f'Iterator:ArduinoUno:{self.motherPort}')
        self.setPinMap(pinMap)
        self.description = desc


    def startIterator(self):
        self.iterator.start()

    def setPinMap(self, _map):
        self.pinMap = {'a:0': None, 'd:0':  None,
                       'a:1': None, 'd:1':  None,
                       'a:2': None, 'd:2':  None,
                       'a:3': None, 'd:3':  None,
                       'a:4': None, 'd:4':  None,
                       'a:5': None, 'd:5':  None,
                                    'd:6':  None,
                                    'd:7':  None,
                                    'd:8':  None,
                                    'd:9':  None,
                                    'd:10': None,
                                    'd:11': None,
                                    'd:12': None}

        for key, value in _map.items():
            if value[0] == 1101:
                self.pinMap.update({key: GroveTemperatureSensor(self, key, ((value[1])['enabled']),
                                                               ((value[1])['description']),
                                                               ((value[1])['calibrationValue']),
                                                               ((value[1])['probeFrequency'])
                                                               )})
            elif value[0] == 1102:
                self.pinMap.update({key: CapativeSoilMoistureSensor(self, key, value[1])})
            else:
                continue


class AqSeeeduinoV4WithBaseShield(AqAbstractHardwareUnit.ArduinoUnit, ArduinoUno):
    driverId = 1072

    def __init__(self, comPort: str, pinMap: dict, desc: str):
        ArduinoUno.__init__(self, comPort)
        AqAbstractHardwareUnit.ArduinoUnit.__init__(self, comPort, desc)
        self.iterator.setName(f'Iterator:SeeeduinoV4:{self.motherPort}')
        self.iterator.start()
        self.setPinMap(pinMap)
        self.description = desc


    def setPinMap(self, _map):
        self.pinMap = {'a:0': None, 'd:2': None,
                       'a:1': None, 'd:3': None,
                       'a:2': None, 'd:4': None,
                       'a:3': None, 'd:5': None,
                                    'd:6': None,
                                    'd:7': None,
                                    'd:8': None}

        for key, value in _map.items():
            if value[0] == 1101:
                self.pinMap.update({key: GroveTemperatureSensor(self, key, (value[1])['enabled'],
                                                                (value[1])['description'],
                                                                (value[1])['calibrationValue'], 
                                                                (value[1])['probeFrequency'])})
            elif value[0] == 1102:
                self.pinMap.update({key: CapativeSoilMoistureSensor(self, key, value[1])})
            else:
                continue

#####################################################
#            #         Модули          #            #
#####################################################

class GroveTemperatureSensor(AqAbstractHardwareModule.ArduinoSensor):
    driverId = 1101

    def __init__(self, atBoard: AqAbstractHardwareUnit.ArduinoUnit, atPin: str, isEnabled: bool, 
                 description: str, calibrationValue: int, probeFrequency):
        super().__init__(atBoard, atPin, isEnabled, True, description, self.temperature,
                         'Аналоговый датчик темпepaтуры Grove версии 1.2')
        self.bV = 4275
        self.cV = int(calibrationValue)
        if probeFrequency is not None:
            self.pF = float(probeFrequency)
        else:
            self.pF = 60.0

        while self.motherPin.read() != None:
            self.motherPin.read()
        
                     
    def value(self):
        if self.motherPin.read():
            return self.motherPin.read()


    def temperature(self):
        return (1.0 / (log(1023.0 / self.value() - 1.0) / (self.bV) + 1 / 298.15) - self.cV)


    def calibrate(calibrationValue: int):
        self.cV = calibrationValue


class CapativeSoilMoistureSensor(AqAbstractHardwareModule.ArduinoSensor):
    driverId = 1102

    def __init__(self, atBoard: AqAbstractHardwareUnit.ArduinoUnit, atPin: str, isEnabled: bool, 
                 description: str, calibrationValue: int, probeFrequency):
        super().__init__(atBoard, atPin, False, '', description, self.moisture,
                        'Аналоговый ёмкостный датчик влажности почвы версии 1.0')
        self.pF = float(probeFrequency)



    def value(self):
        if self.motherPin.read():
            return self.motherPin.read()
        else:
            pass


    def moisture(self):
        if self.value():
            m = self.motherPin.read() * 100
            return ceil(m)
