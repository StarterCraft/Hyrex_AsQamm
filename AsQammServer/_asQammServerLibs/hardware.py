from time import      (sleep       as slp)
from pyfirmata import (Arduino     as ArduinoUno,
                       ArduinoMega as ArduinoMega,
                       util        as ArduinoUtil,
                       UNAVAILABLE, INPUT, ANALOG,
                       OUTPUT, PWM, SERVO,
                       PinAlreadyTakenError)

from math import       (log        as log,
                        ceil       as ceil)
from json import       (loads      as loadJson,
                        JSONDecodeError)

from _asQammServerLibs.functions import AqLogger
from serial.serialutil import SerialException


class AqAbstractHardwareComplex:
    pass


class AqAbstractHardwareUnit:
    class ArduinoUnit:
        def __init__(self, comPort, isEnabled: bool, desc: str):
            self.motherPort = comPort
            self.iterator = ArduinoUtil.Iterator(self)
            self.isEnabled = isEnabled
            self.description = desc


        def __repr__(self):
            return f'{self.driverId} Arduboard at {self.motherPort}'
        

        def getId(self):
            return f'{self.motherPort}:{self.driverId}'


        def getPinMap(self, mode = None):
            if mode == None:
                items = []
                moduleDict = {}
                for pin, module in self.pinMap.items():
                    if not module:
                        continue
                    elif module.driverId == 1000:
                        continue
                    else:
                        for attrib in module.attrl:
                            moduleDict.update({attrib: getattr(module, attrib)})
                        items.append(tuple([pin, [module.driverId, moduleDict]]))
                        continue

            if mode == object:
                items = []
                for pin, module in self.pinMap.items():
                    if not module:
                        continue
                    else:
                        items.append(tuple([pin, module]))
                        continue

            return items


class AqAbstractHardwareModule:
    class ArduinoSensor:
        Analog = type('AnalogSensor', (object,), {})
        Digital = type('DigitalSensor', (object,), {})

        def __init__(self, atBoard: AqAbstractHardwareUnit.ArduinoUnit, atPin: str, isEnabled: bool, isCalib: bool,
                     name: str, bkmeth, desc: str):
            self.attrl = ['description', 'isEnabled']
            self.motherBoard = atBoard
            self.motherPinAddress = atPin
            self.motherPin = self.motherBoard.get_pin(f'{self.motherPinAddress}:i')
            self.isEnabled = isEnabled
            self.isCalibrateable = isCalib
            self.name = name
            self.description = desc
            self._bkmeth = bkmeth

        def __repr__(self):
            return f'{self.driverId} device at {self.motherBoard} ({self.motherPinAddress})'

        def getId(self):
            return f'{self.motherBoard.motherPort}:{self.motherPinAddress}:{self.driverId}'

        def baked(self):
            return self._bkmeth()


    class ArduinoExecutor:
        Analog = type('AnalogExecutor', (object,), {})
        Digital = type('DigitalExecutor', (object,), {})

        def __init__(self, atBoard: AqAbstractHardwareUnit.ArduinoUnit, atPin: str, isEnabled: bool, description: str):
            self.attrl = ['description', 'isEnabled']
            self.motherBoard = atBoard
            self.motherPinAddress = atPin
            self.motherPin = self.motherBoard.get_pin(f'{self.motherPinAddress}:i')
            self.isEnabled = isEnabled
            self.description = description

        def getId(self):
            return f'{self.motherBoard.motherPort}:{self.motherPinAddress}:{self.driverId}'


class AqArduinoHardwareModes:
    Input = INPUT
    Output = OUTPUT
    Analog = ANALOG
    PWM = PWM
    Servo = SERVO
    Off = UNAVAILABLE


import _asQammServerLibs.drivers as drivers
from _asQammServerLibs.statistic import AqStatist
from threading import Thread
from colorama import Fore as Fore, Style as Style


class AqHardwareSystem:
    def __init__(self):
        self.isOk = bool()
        self.installedArduinoHardware = []
        self.monitors = []
        self.logger = AqLogger('Server>HardwareSystem')
        self.statisticAgent = AqStatist()

        self.logger.debug('Инициализация оборудования')
        with open('data/system/~!hardware!~.asqd', 'r', encoding = 'utf-8') as configFile:
            try: 
               jsonString = loadJson(configFile.read())

               for hardwareObject in jsonString:
                   self.logger.debug(f'Подключение к устройству на {hardwareObject["comPort"]}...')
                   try:
                       if   hardwareObject['driverId'] == 1071: #КОСТЫЛЬ: Использование driverId для выявления типа устройства
                            instance = drivers.AqArduinoUnoR3(hardwareObject['comPort'], hardwareObject['pinMap'],
                                                              hardwareObject['isEnabled'], hardwareObject['description'])
                            self.logger.debug(f'Инициализация Arduino Uno R3 на {hardwareObject["comPort"]}...')
                            self.installedArduinoHardware.append(instance)

                       elif hardwareObject['driverId'] == 1072:
                            instance = drivers.AqSeeeduinoV4WithBaseShield(hardwareObject['comPort'], hardwareObject['pinMap'],
                                                                           hardwareObject['isEnabled'], hardwareObject['description'])
                            self.logger.debug(f'Инициализация Seeeduino V4 на {hardwareObject["comPort"]}...')
                            self.installedArduinoHardware.append(instance)

                   except SerialException:
                       self.logger.error(f'''Не удалось инициализировать Arduino-устройство типа {hardwareObject["driverId"]} на портy '''
                                        f'''{hardwareObject["comPort"]} из-за ошибки 0104: не удалось найти запрашиваемое устройство''')
                       continue
                                       

            except JSONDecodeError:
                self.logger.error(f'''Не удалось получить данные JSON из файла "data/system/~!hardware!~.asqd", проверьте файл на синтаксические ошибки''')

        if len(self.installedArduinoHardware) == 0:
            self.logger.critical(f'''Не удалось инициализировать Arduino-устройство, используя информацию из файла "~!hardware!~.asqd". '''
                                 f'''Пожалуйста, убедитесь, что файл не повреждён и не пуст, что все модули подключены и находятся'''
                                 '''в рабочем состоянии. Для решения данной проблемы попробуйте переустановить AsQammServer, при'''
                                 '''переустановке внимательно следите за правильностью вводимой информации о модулях''')
            self.isOk = False
            self.logger.critical(f'Аварийное завершение работы')
        else:
            self.isOk = True


    def startMonitoring(self):
        for unit in self.installedArduinoHardware:
           if unit.isEnabled:
               instance = AqArduinoUnitMonitor(self, unit)
               self.monitors.append(instance)
           else:
               pass

        for monitor in self.monitors:
            self.logger.debug('Запуск мониторинга')
            monitor.start()

    
    def getHardwareDataSheet(self):
        mq = 0
        eq = 0
        ds = []
        for unit in self.installedArduinoHardware: #КОСТЫЛЬ: проверки типа устройства нет
            for pin, module in unit.getPinMap():
                if module != None:
                    mq += 1
                    print(module)
                    if (module[1])['isEnabled']:
                        eq += 1
                    continue

            ds.append({ 'unitType'   : 'AqArduino',
                        'isEnabled'  : unit.isEnabled,
                        'driverId'   : unit.driverId,
                        'comPort'    : unit.motherPort,
                        'description': unit.description,
                        'pinMap'     : dict(unit.getPinMap()),
                        'modulesQty' : mq,
                        'enabledQty' : eq})

        return ds


class AqArduinoUnitMonitor(Thread):
    def __init__(self, hardwareSystem: AqHardwareSystem, assignToBoard: AqAbstractHardwareUnit.ArduinoUnit):
        Thread.__init__(self, target = self.run, args = (), name = f'{assignToBoard.getId()}:monitor')
        self.assignedBoard = assignToBoard
        self.hardwareSystem = hardwareSystem
        self.assignedBoardModules = []
        self.assignedBoardMonitors = []
        

    def run(self):
        for pin, module in (self.assignedBoard.getPinMap(mode = object)):
            try:
                print(module)
                if module.driverId in range(1101, 1199):
                    self.assignedBoardModules.append(module)
                else:
                    continue
            except AttributeError:
                continue

        for module in self.assignedBoardModules:
            try:
                if module.driverId in range(1101, 1199):
                    instance = AqArduinoSensorMonitor(self.hardwareSystem, module)
                    self.assignedBoardMonitors.append(instance)
            except AttributeError:
                continue

        blinker = AqArduinoD13Blinker(self.hardwareSystem, (self.assignedBoard.pinMap)['d:13'])
        blinker.start()

        for monitor in self.assignedBoardMonitors:
            monitor.start()


class AqArduinoSensorMonitor(Thread):
    def __init__(self, hardwareSystem: AqHardwareSystem, assignToSensor: AqAbstractHardwareModule.ArduinoSensor):
        Thread.__init__(self, target = self.run, args = (), name = f'{assignToSensor.getId()}:monitor', daemon = True)
        self.statistic = hardwareSystem.statisticAgent
        self.assignedSensor = assignToSensor


    def run(self):
        while True:
            try:
                self.statistic.registerStatistic(self.assignedSensor.getId(), self.assignedSensor.baked())
            except AssertionError:
                slp(0.48)
                continue

            slp(self.assignedSensor.probeFrequency)


class AqArduinoD13Blinker(Thread):
    def __init__(self, hardwareSystem: AqHardwareSystem, assignToExecutor: AqAbstractHardwareModule.ArduinoExecutor):
        Thread.__init__(self, target = self.run, args = (), name = f'{assignToExecutor.getId()}:monitor', daemon = True)
        self.assignedExecutor = assignToExecutor


    def run(self):
        while True:
            if self.assignedExecutor.checkState():
                slp(0.64)
                self.assignedExecutor.setState(False)
            else:
                self.assignedExecutor.setState(True)
            slp(0.64)
            