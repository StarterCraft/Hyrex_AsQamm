'''
Модуль, в котором представлен основополагающий код для работы
с `комплексами`, `исполнителями` и `модулями`, классы вышеперечисленных
объектов, а также код Менеджера оборудования и Центра оборудования.
===
Последний раз обновлялся: предварительный патч к обновлению pre-α 115,
дата изменения: 6 февраля 2021
'''

from time import      (sleep       as slp)
from pyfirmata import (Arduino     as DefaultArduino,
                       util        as ArduinoUtil,
                       UNAVAILABLE, ANALOG, SERVO,
                       PWM, INPUT, OUTPUT)

from json import       (loads      as loadJson,
                        JSONDecodeError)

from libs.functions import AqLogger
from serial.serialutil import SerialException


class AqAbstractHardwareComplex:
    '''
    Класс `комплекса` - высокоуровневого объединения нескольких исполнителей.
    Пока не разработан.
    '''
    pass


class AqAbstractHardwareUnit:
    '''
    Класс, представляющий любого `исполнителя` — устройства, находящегося в 
    подчинении сервера. Все классы поддерживаемых типов устройств-исполнителей
    являются подклассами этого класса.

    `Исполнители` могут иметь подчинённых себе `модулей`, если это предусмотрено
    типом этого исполнителя. Они могут быть объединены в `комплексы` для более
    глубокого взаимодействия друг с другом.

    Абсолютно любого исполнителя можно отключить от системы, для этого существует
    атрибут 'isEnabled'.
    '''
    isEnabled = bool()

    class ArduinoUnit:
        '''
        Класс Arduino-исполнителя. Имеет базовую функциональность PyFirmata,
        функциональность приёма и отправки строковых сообщений ASCII,
        функциональность работы с модулями.
        '''
        def __init__(self, comPort: str, isEnabled: bool, desc: str,
                     overrideDefaultTemplate: bool = False):
            '''
            Инициализировать экземпляр базового класса Arduino-исполнителя.
            Такие исполнители работают на базе протокола Firmata, сервер
            использует библиотеку PyFirmata для коммутации с ними.
            PyFirmata.Arduino инициализируется по умолчанию здесь, но эту
            возможность можно отключить лля того, чтобы не использовать
            стандартный внутренний шаблон PyFirmata (не рyirmata.Arduino)

            :param 'comPort': str
                COM-порт, на котором необходимо запустить службу PyFirmata
                для этого исполнителя

            :param 'isEnabled': bool
                Использовать ли это устройство или нет. Если задан False, то
                итератор PyFirmata не будет запущен (его можно запустить с 
                помощью метода startIterator()), регистрация данных с датчиков,
                отслеживание правил и отправка команд на модули вывода осущест-
                ляться не будут

            :param 'desc': str
                Обязательное описание исполнителя. Может быть пустым

            :param 'overrideDefaultTemplate': bool = False
                Этот параметр позволяет отключить инициализацию стандартного
                pyfirmata.Arduino. Если True, то стандартный внутренний шаблон
                PyFirmata не будет инициализирован, и будет необходимо дополни-
                тельно инициализировать другой объект pyfirmata.Board
            '''

            self.motherPort = comPort
            if isEnabled and not overrideDefaultTemplate: DefaultArduino.__init__(self, comPort)
            if isEnabled: self.iterator = ArduinoUtil.Iterator(self)
            self.isEnabled = isEnabled
            self.description = desc
            self.result = float()

            self.add_cmd_handler(0x71, self.parseString)


        def __repr__(self):
            return f'{self.driverId} Arduboard at {self.motherPort}'
        

        def getId(self):
            '''
            Каждый объект оборудования в Hyrex AsQamm имеет собственный внут-
            ренний индентификатор. У Arduino-исполнителей он формируется по
            следующей схеме:

            '{COM-порт, на котором находится исполнитель}:{ID драйвера}'
            '''
            return f'{self.motherPort}:{self.driverId}'


        def startIterator(self):
            '''
            Запустить итератор PyFirmata
            '''
            self.iterator.start()


        def setPinMap(self, _map, drv):
            self.pinMap = {}
            for definer in self.analogPins: self.pinMap.update({definer: None})
            self.pinMap.update({'d:13': drv.arduModules[1000](self, 'd:13', isEnabled = True,
                                                              name = 'D13Led', description = 'D13 Built-in LED')})
            for pin, module in _map.items():
                self.pinMap.update({pin: drv.arduModules[module[0]](self, pin, **(module[1]))})


        def getPinMap(self, mode = None):
            if mode == None:
                items = []
                moduleDict = {}
                for pin, module in self.pinMap.items():
                    if not module: continue
                    elif module.driverId == 1000: continue
                    else:
                        for attrib in module.attrl:
                            moduleDict.update({attrib: getattr(module, attrib)})
                        items.append(tuple([pin, [module.driverId, moduleDict]]))
                        continue

            if mode == object:
                items = []
                for pin, module in self.pinMap.items():
                    if not module: continue
                    else:
                        items.append(tuple([pin, module]))
                        continue

            return items


        def sendString(self, string: str):
            '''
            Отправить ASCII-совместимую строку на Arduino (никаких 
            символов Юникода!)

            :param 'string': str
                Строка, которую необходимо отправить

            :returns: None
            '''
            self.send_sysex(0x71, ArduinoUtil.str_to_two_byte_iter(string))


        def send_sysex(self, sysexCmd, data = []):
            '''
            Отправить сообщение SysEx (фикс метода из pyfirmata).

            :param 'sysexCmd': byte
                Байт с командой SysEx

            :param 'data': bytearray
                Массив байтов с необходимой информацией в виде
                семибайтовых групп.
            '''
            msg = bytearray([pyfirmata.pyfirmata.START_SYSEX, sysexCmd])
            msg.extend(data)
            msg.append(pyfirmata.pyfirmata.END_SYSEX)
            self.sp.write(msg)


        def parseString(self, *args, **kwargs):
            '''
            Обработать полученную от Arduino-исполнителя строку.
            Вызывается автоматически при получении строкового сообщения.

            :returns: None
            '''
            received = ArduinoUtil.two_byte_iter_to_str(args)


class AqAbstractHardwareModule:
    class ArduinoSensor:
        Analog = type('AnalogSensor', (object,), {})
        Digital = type('DigitalSensor', (object,), {})

        def __init__(self, atBoard: AqAbstractHardwareUnit.ArduinoUnit, atPin: str, isEnabled: bool, isCalib: bool,
                     name: str, desc: str, typeDesc: str, bkmeth):
            self.attrl = ['description', 'isEnabled']
            self.motherBoard = atBoard
            self.motherPinAddress = atPin
            try: self.motherPin = self.motherBoard.get_pin(f'{self.motherPinAddress}:i')
            except AttributeError: pass
            self.isEnabled = isEnabled
            self.isCalibrateable = isCalib
            self.name = name
            self.description = desc
            self.typeDescription = typeDesc
            self.baked = bkmeth


        def __repr__(self):
            return f'{self.driverId} device at {self.motherBoard} ({self.motherPinAddress})'


        def getId(self):
            return f'{self.motherBoard.motherPort}:{self.motherPinAddress}:{self.driverId}'


    class ArduinoExecutor:
        Analog = type('AnalogExecutor', (object,), {})
        Digital = type('DigitalExecutor', (object,), {})

        def __init__(self, atBoard: AqAbstractHardwareUnit.ArduinoUnit, atPin: str, isEnabled: bool,
                     name: str, desc: str, typeDesc: str):
            self.attrl = ['description', 'isEnabled']
            self.motherBoard = atBoard
            self.motherPinAddress = atPin
            try: self.motherPin = self.motherBoard.get_pin(f'{self.motherPinAddress}:i')
            except AttributeError: pass
            self.name = name
            self.description = desc
            self.typeDescription = typeDesc


        def getId(self):
            return f'{self.motherBoard.motherPort}:{self.motherPinAddress}:{self.driverId}'


class AqArduinoHardwareModes:
    Input = INPUT
    Output = OUTPUT
    Analog = ANALOG
    PWM = PWM
    Servo = SERVO
    Off = UNAVAILABLE


import drivers
from libs.statistic import AqStatist
from threading import Thread


class AqHardwareSystem:
    def __init__(self):
        self.isOk = bool()
        self.installedArduinoHardware = []
        self.monitors = []
        self.logger = AqLogger('Hardware')
        self.statisticAgent = AqStatist()

        self.logger.debug('Инициализация оборудования')
        with open('data/system/~!hardware!~.asqd', 'r', encoding = 'utf-8') as configFile:
            try: 
               jsonString = loadJson(configFile.read())

               for hardwareObject in jsonString:
                   self.logger.debug(f'Подключение к устройству на {hardwareObject[1]}...')
                   try:
                       instance = (drivers.arduBoards[hardwareObject[0]])(hardwareObject[1], drivers, **hardwareObject[2])
                       self.installedArduinoHardware.append(instance)
                       self.logger.info(f'Устройство типа {hardwareObject[0]} на портy {hardwareObject[1]} подключено.')
                   except SerialException:
                       self.logger.error(f'''Не удалось инициализировать Arduino-устройство типа {hardwareObject[0]} на портy '''
                                        f'''{hardwareObject[1]} из-за ошибки 0104: не удалось найти запрашиваемое устройство''')
                       continue
                                       

            except JSONDecodeError:
                self.logger.error(f'''Не удалось получить данные JSON из файла "data/system/~!hardware!~.asqd", проверьте файл на'''
                                  f'''синтаксические ошибки''')

        if len(self.installedArduinoHardware) == 0:
            self.logger.critical(f'''Не удалось инициализировать Arduino-устройство, используя информацию из файла "~!hardware!~.asqd". '''
                                 f'''Пожалуйста, убедитесь, что файл не повреждён и не пуст, что все модули подключены и находятся'''
                                 '''в рабочем состоянии. Для решения данной проблемы попробуйте переустановить AsQammServer, при'''
                                 '''переустановке внимательно следите за правильностью вводимой информации об оборудовании.''')
            self.isOk = False
            self.logger.critical(f'Аварийное завершение работы')
        else:
            self.isOk = True


    def startMonitoring(self):
        for unit in self.installedArduinoHardware:
           if unit.isEnabled:
               instance = AqArduinoUnitMonitor(self, unit)
               self.monitors.append(instance)

        for monitor in self.monitors:
            self.logger.debug(f'Запуск мониторинга для Arduino-устройства {monitor.assignedBoard.motherPort}')
            monitor.start()

    
    def getHardwareDataSheet(self):
        mq = 0
        eq = 0
        ds = []
        for unit in self.installedArduinoHardware: #КОСТЫЛЬ: проверки типа устройства нет
            for pin, module in unit.getPinMap():
                if module != None:
                    mq += 1
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

        if self.assignedBoard.motherPort == 'COM5': AqArduinoD13Blinker(self.hardwareSystem, (self.assignedBoard.pinMap)['d:13'], (self.assignedBoard.pinMap)['a:0']).start()

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
                if not self.statistic.isBusy: self.statistic.registerStatistic(self.assignedSensor.getId(), self.assignedSensor.baked())
                elif self.statistic.isBusy:
                    while self.statistic.isBusy:
                        slp(0.48)
                    self.statistic.registerStatistic(self.assignedSensor.getId(), self.assignedSensor.baked())
                    
            except AssertionError:
                slp(0.48)
                continue

            slp(self.assignedSensor.probeFrequency)
