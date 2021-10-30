from drivers.dependencies import *
from pyfirmata import (Arduino     as DefaultArduino,
                       util        as ArduinoUtil,
                       UNAVAILABLE, ANALOG, SERVO,
                       PWM, INPUT, OUTPUT,
                       START_SYSEX, END_SYSEX)
from pyfirmata.boards import BOARDS as Templates
from enum             import *
import datetime


class ArduinoDevice(AqHardwareDevice, pyfirmata.Board):
        '''
        Класс Arduino-исполнителя. Имеет функциональность PyFirmata,
        функциональность приёма и отправки строковых сообщений ASCII,
        функциональность работы с модулями.

        Любой объект Arduino-исполнителя имеет следующие атрибуты:

        :attrib 'motherPort': str
            COM-порт, на котором распологается исполнитель и на котором
            находится его PyFirmata-служба, если он включён

        :attrib 'instanceDescription': str
            Обязательное описание исполнителя. Может быть пустым.
            Используется для отображения в интерфейсах вершителей

        :attrib 'typeDescription': str
            Обязательное описание ТИПА исполнителя. Может быть пустым,
            но не рекомендуется оставлять его таким. Задаётся в драйвере
            ТИПА исполнителя.
            Используется для отображения в интерфейсах вершителей
        '''
        class BoardTemplates(Enum):
            '''
            Шаблоны платы pyfirmata, которые можно инициализировать
            '''
            ArduinoUno  = Templates['arduino']
            ArduinoMega = Templates['arduino_mega']
            ArduinoDue  = Templates['arduino_due']
            ArduinoNano = Templates['arduino_nano']


        class Monitor(Thread):
            '''
            Класс `монитора` для исполнителя. `Монитор` представляет из себя
            подвид потока; для исполнителей он выполняет лишь запуск отслежи-
            вания значений датчиков. Некоторые вaжные атрибуты:

            :attrib 'assignedBoardMonitors': list
                Список содержит мониторы датчиков для всех таких модулей, ко-
                торые подключены к исполнителю
            '''
            def __init__(self, hardwareSystem: AqHardwareSystem, assignToBoard):
                '''
                Конструктор `монитора` для исполнителя.

                :param 'hardwareSystem': AqHardwareSystem
                    Ссылка на объект системы управления оборудованием. 

                :param 'assignToBoard': ArduinoDevice
                    Ссылка на объект исполнителя, с которым работает монитор.
                '''
                Thread.__init__(self, target = self._run, args = [hardwareSystem, assignToBoard],
                                name = f'{assignToBoard.getId()}:monitor')
                self.assignedBoard = assignToBoard
                self.assignedBoardMonitors = []
        

            def _run(self, hardwareSystem: AqHardwareSystem, assignedBoard):
                '''
                Рабочий метод `монитора` для исполнителя.

                :param 'hardwareSystem': AqHardwareSystem
                    Ссылка на объект системы управления оборудованием. 

                :param 'assignedBoard': ArduinoDevice
                    Ссылка на объект исполнителя, с которым работает монитор.
                '''
                for unit in dict(assignedBoard.getChildren(mode = object)).values():
                    try:
                        if issubclass(type(unit), ArduinoSensor):
                            for vt in unit.retrieves:
                                instance = ArduinoSensor.Monitor(hardwareSystem.statisticAgent, vt)
                                self.assignedBoardMonitors.append(instance)
                        else: continue
                    except AttributeError: continue

                for monitor in self.assignedBoardMonitors: 
                    monitor.start()
                    sleep(1)


        class AqArduinoHardwareModes:
            '''
            В этом классе содержатся определители режимов работы пинов Arduino. Класс
            используется в работе с PyFirmata
            '''
            Input = INPUT
            Output = OUTPUT
            Analog = ANALOG
            PWM = PWM
            Servo = SERVO
            Off = UNAVAILABLE


        class FirmataStringResponse:
            '''
            Класс для работы со строковыми сообщениями-ответами от Arduino-
            исполнителя. Firmata посылает ответы на строковые команды в виде
            строк, кото- рые могут быть двух видов: бeз ошибки и с ошибкой.

            Схема безошибочного строкового ответа от исполнителя:
            'OK;{a};{b}', где:
                a —— Имя метода, который вызывался и на который исполнитель
                     отправляет ответ;
                b —— Результат выполнения метода. Может представлять из себя
                     число или строку. Если результат представляет собой спи-
                     сок, то каждый его элемент записывается через точку с 
                     запятой.

            Схема строкового сообщения об ошибке (ответа) от исполнителя:
            'ERR;{a};{b}', где:
                a —— Имя метода, который вызывался и на который исполнитель
                     отправляет ответ;
                b —— Код ошибки, зависит от вызываемого метода (для каждого 
                     метода существуют свои коды ошибки, о них можно узнать
                     в документации к функциональным библиотекам
                     AsQamm Arduino).
            '''
            class MessageType(Enum):
                OK = 1
                Error = 0

            def __init__(self, string: str):
                '''
                Инициализировать обработчик строкового сообщения. Если после-
                днее не соответствует синтаксису строковых сообщений, будет
                вызвано исключение.

                :param 'string': str
                    Строковое сообщение от Arduino-исполнителя в виде сырой
                    строки.
                '''
                print(string)

                if len(string.split(';')) < 2:
                    raise SyntaxError('От Arduino-исполнителя получено некорректное строковое сообщение')

                self.statusCode, self.methodName = string.split(';')[0], string.split(';')[1]

                if self.statusCode == 'OK': #если сообщение без ошибки
                    self.type = self.MessageType.OK
                    self.receivedInfo = string.split(';')[2:]

                elif self.statusCode == 'ERR': #если сообщение об 
                    self.type = self.MessageType.Error
                    self.errorCode = string.split(';')[2]

                self.receivedAt = datetime.datetime.now()
        

        def __init__(self, comPort: str, isEnabled: bool,
                instanceName: str, desc: str,
                template: (BoardTemplates, dict) = BoardTemplates.ArduinoUno):
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

            :param 'instanceName': str
                Обязательное отображаемое имя исполнителя. Может быть пустым,
                но не рекомендуется оставлять его таким.
                Используется для отображения в интерфейсах вершителей

            :param 'desc': str
                Обязательное описание исполнителя. Может быть пустым.
                Используется для отображения в интерфейсах вершителей

            :kwparam 'template': BoardTemplates = BoardTemplates.ArduinoUno
                Шаблон платы pyfirmata, который необходимо инициализировать.
                Если нужна плата с определёнными настройками, словарь настроек
                pyfirmata
            '''
            AqHardwareDevice.__init__(self, isEnabled, f'{comPort}:{self.driverId}', 'arduino',
                comPort, isFertile = True, instanceName = instanceName,
                instanceDescription = desc)
            self.motherPort = comPort
            if isEnabled: 
                if type(template) == self.BoardTemplates:
                   pyfirmata.pyfirmata.Board.__init__(self, comPort, template.value)
                else: pyfirmata.pyfirmata.Board.__init__(self, comPort, template)

                self.iterator = ArduinoUtil.Iterator(self)
            self.result = float()

            self.receivedFirmataMessages = []
            self.add_cmd_handler(0x71, self.parseString)
            self.senderBusy = False


        def __repr__(self):
            return f'{self.driverId} type Arduboard at {self.motherPort}'
        

        def getId(self) -> str:
            '''
            Каждый объект оборудования в Hyrex AsQamm имеет собственный внут-
            ренний индентификатор. У Arduino-исполнителей он формируется по
            следующей схеме:

            '{x}:{y}'
            где x = COM-порт, на котором находится исполнитель;
                y = ID драйвера исполнителя.

            :returns: None
            '''
            return f'{self.motherPort}:{self.driverId}'


        def startIterator(self) -> None:
            '''
            Запустить итератор PyFirmata
            
            :returns: None
            '''
            self.iterator.start()


        def setChildren(self, _map: dict, drv: module) -> None:
            '''
            Установить карту распиновки.

            Карта распиновки — словарь, ключами которого являются адреса пинов
            Arduino в нижеследующей форме:
            '{тип пинá (d для цифровых пинов, а для анáлоговых)}:{номер пина}',
            а значениями являются объекты подчинённых исполнителей, подключенных к этим пинам.

            Метод используется при инициализации оборудования из файла hardware.asqd

            :param '_map': mapObject
                JSON-объект, который хранится в hardware.asqd и определяет, какие
                модули нужно инициализировать на этом Arduino-исполнителе

            :param 'drv': module
                Модуль drivers.__init__

            :returns: None
            '''
            self.pinMap = {}
            for definer in self.analogPins: self.pinMap.update({definer: None})
            self.pinMap.update(
                {'d:13': drv.Devices['A001'](self,
                    'd:13', isEnabled = True, instanceName = 'D13Led', instanceDescription = 'D13 Built-in LED')})
            for pin, unit in _map.items():
                self.pinMap.update({pin: drv.Devices[unit[0]](self, pin, **(unit[1]))})


        def getChildren(self, mode = None) -> list:
            '''
            Получить карту распиновки.

            Карта распиновки — словарь, ключами которого являются адреса пинов
            Arduino в нижеследующей форме:
            '{тип пинá (d для цифровых пинов, а для анáлоговых)}:{номер пина}',
            а значениями являются объекты подчинённых исполнителей, подключенных
            к этим пинам.

            Имеется 2 режима:
                режим None (по умолчанию): получить список словарей в виде списка
                кортежей, где ключи — адреса пинов, а значения — списки из ID драй-
                вера модуля, значения его атрибута isEnabled и словаря его настроек

                pежим object: получить список словарей в виде списка кортежей, где
                ключи — адреса пинов, а значения — объекты модулей.

            :param 'mode': type 'object' or None = None
                Режим, который требуется.

            :returns: None
            '''
            if not mode:
                items = []
                unitDict = {}
                for pin, unit in self.pinMap.items():
                    if not unit: continue
                    elif unit.driverId == 'A001': continue
                    else:
                        for attrib in unit.attrl:
                            unitDict.update({attrib: getattr(unit, attrib)})
                        items.append(tuple([pin, [unit.driverId, unitDict]]))
                        continue

            if mode == object:
                items = []
                for pin, unit in self.pinMap.items():
                    if not unit: continue
                    else:
                        items.append(tuple([pin, unit]))
                        continue

            return items


        def sendString(self, string: str) -> None:
            '''
            Отправить ASCII-совместимую строку на Arduino (никаких 
            символов Юникода!)

            Отправка строковых команд Arduino-исполнителям производится
            в том случае, если необходимо, чтобы исполнитель выполнл ка-
            кую-то ФУНКЦИЮ в своём коде со своей стороны и послал ответ.
            Например, поддержка цифровых датчиков была реализована имен-
            но по такому принципу.

            :param 'string': str
                Строка, которую необходимо отправить

            :returns: None
            '''
            self.send_sysex(0x71, ArduinoUtil.str_to_two_byte_iter(string))
            sleep(2)


        def send_sysex(self, sysexCmd: int, data: list = []) -> None:
            '''
            Отправить сообщение SysEx (фикс метода из pyfirmata).

            :param 'sysexCmd': byte
                Байт с командой SysEx

            :param 'data': bytearray
                Массив байтов с необходимой информацией в виде
                семибайтовых групп.
            '''
            msg = bytearray([START_SYSEX, sysexCmd])
            msg.extend(data)
            msg.append(END_SYSEX)
            self.sp.write(msg)


        def parseString(self, *args, **kwargs):
            '''
            Обработать полученную от Arduino-исполнителя строку.
            Вызывается автоматически при получении строкового сообщения.

            :returns: None
            '''
            received = ArduinoUtil.two_byte_iter_to_str(args)
            self.receivedFirmataMessages.append(self.FirmataStringResponse(received))


        def getLastMessage(self, messageType = -1) -> FirmataStringResponse:
            '''
            Получить последнее полученное от платы сообщение Firmata.

            :param 'messageType': FirmataStringResponse.MessageType

            :returns: FirmataStringResponse
            '''
            if messageType == -1:
                currentTime = datetime.datetime.now()
                for message in self.receivedFirmataMessages:
                    if ((currentTime - message.receivedAt) == 
                        (min([currentTime - _message.receivedAt for _message in self.receivedFirmataMessages]))):
                        return message

            else:
                currentTime = datetime.datetime.now()
                for message in self.receivedFirmataMessages:
                    if ((currentTime - message.receivedAt) == 
                        (min([currentTime - _message.receivedAt for _message
                              in self.receivedFirmataMessages if _message.type == messageType]))):
                        return message


class ArduinoSensor(AqHardwareDevice):
    '''
    Класс Аrduino-датчика, являющегося исполнителем. 
    Они имеют два подтипа: Analog (для аналоговых) и Digital (для цифровых
    датчиков).

    Любой объект Arduino-датчика имеет следующие атрибуты:

    :attrib 'attrl': list
        Список атрибутов, которые инициализируются из JSON-словаря в
        'hardware.asqd'
        
    :attrib 'motherBoard': ArduinoDevice
        Ссылка на объект Arduino-исполнителя, к которому подключён датчик

    :attrib 'instanceName': str
        Обязательное отображаемое имя датчика. Может быть пустым.
        Используется для отображения в интерфейсах вершителей

    :attrib 'instanceDescription': str
        Обязательное описание датчика. Может быть пустым.
        Используется для отображения в интерфейсах вершителей

    :attrib 'typeDescription': str
        Обязательное описание ТИПА датчика. Может быть пустым,
        но не рекомендуется оставлять его таким. Задаётся в драйвере
        ТИПА исполнителя.
        Используется для отображения в интерфейсах вершителей

    :attrib 'retrieves': list<AqHardwareValueType>
        Список типов значений, которые можно получить от датчика
    '''
    class Monitor(Thread):
        '''
        Класс `монитора` для значения. `Монитор` представляет из себя под-
        вид потока; для датчиков он выполняет работу по регистрации значе-
        ний с них через каждый, задаваемый для каждого отдельного значения,
        промежуток времени. Каждый монитор регистрирует только одно значение
        датчика.
        '''
        def __init__(self, statisticAgent: AqStatist, assignToValueType: AqHardwareValueType):
            '''
            Конструктор `монитора` для датчика.

            :param 'statisticAgent': AqStatist
                Ссылка на объект регистратора статистики. 

            :param 'assignToValueType': ArduinoSensor
                Ссылка на объект типа значения датчика, с которым работает монитор.
            '''
            Thread.__init__(self, target = self._run, args = [assignToValueType, statisticAgent],
                name = f'{assignToValueType.parent.getId()}:{assignToValueType.id}', daemon = True)


        def _run(self, assignedValueType: AqHardwareValueType, statistic: AqStatist):
            '''
            Рабочий метод `монитора` для датчика.

            :param 'assignedValueType': AqHardwareValueType
                Ссылка на объект типа значения, с которым работает монитор.
  
            :param 'statistic': AqStatist
                Ссылка на объект регистратора статистики. 
            '''
            while True:
                value = assignedValueType()

                try:
                    if not statistic.isBusy:
                        statistic.registerStatistic(datetime.datetime.now(),
                            f'{assignedValueType.parent.getId()}:{assignedValueType.id}', value)
                    else:
                        while statistic.isBusy: sleep(1)
                        statistic.registerStatistic(datetime.datetime.now(),
                            f'{assignedValueType.parent.getId()}:{assignedValueType.id}', value)

                    print(f'{self.getName()} working')

                except AssertionError:
                    sleep(1)
                    print(473)
                    continue

                sleep(assignedValueType.frequency)


    Analog = typemark('AnalogSensor')       #Маркер аналогового типа
    Digital = typemark('DigitalSensor')     #Маркер цифрового типа

    attrl = ['instanceDescription', 'isEnabled']

    def __init__(self, atBoard: ArduinoDevice, atPin: str, isEnabled: bool,
            instanceName: str, desc: str, **kwargs):
        '''
        Инициализировать Аrduino-датчик.

        :param 'atBoard': ArduinoDevice
            Объект Arduino-исполнителя, к которому подключён датчик

        :param 'atPin': str
            Адрес пина Arduino-исполнителя, к которому подключён датчик

        :param 'isEnabled': bool
            Использовать ли этот датчик или нет. Если этот параметр
            отключить, то регистрация его значений системой статистики
            не будет выполняться, а также частично или полностью перес-
            танут работать правила, в условиях которых фигурирует данный
            датчик

        :param 'instanceName': str
            Обязательное отображаемое имя датчика. Может быть пустым,
            но не рекомендуется оставлять его таким.
            Используется для отображения в интерфейсах вершителей

        :param 'desc': str
            Обязательное описание датчика. Может быть пустым.
            Используется для отображения в интерфейсах вершителей
        '''
        AqHardwareDevice.__init__(self, isEnabled, f'{atBoard.deviceAddress}:{atPin}:{self.driverId}', 
            'arduino', f'{atBoard.deviceAddress}:{atPin}',
            parent = atBoard, instanceName = instanceName, instanceDescription = desc)
        try: self.motherPin = self.parent.get_pin(f'{atPin}:i')
        except AttributeError: pass


    def __repr__(self):
        return f'{self.driverId} device at {self.parent} ({self.deviceAddress})'


    def getId(self) -> str:
        '''
        Каждый объект оборудования в Hyrex AsQamm имеет собственный внут-
        ренний индентификатор. У подчинённых Arduino-исполнителей он фор-
        мируется по следующей схеме:

        '{x}:{y}', где:
            x = Адрес подчинённого исполнителя;
            y = ID драйвера подчинённого исполнителя.

        :returns: str
        '''
        return f'{self.deviceAddress}:{self.driverId}'


class ArduinoExecutor(AqHardwareDevice):
    '''
    Класс подчинённых исполнителей, работающих на вывод, для Arduino-
    исполнителя (например, сервопривод). 
    Они имеют два подтипа: Analog (для аналоговых) и Digital (для циф-
    ровых устройств исполнения).

    Любой объект таких модулей исполнения имеет следующие атрибуты:

    :attrib 'attrl': list
        Список атрибутов, которые инициализируются из JSON-словаря в
        'hardware.asqd'
        
    :attrib 'motherBoard': ArduinoDevice
        Ссылка на объект Arduino-исполнителя, к которому подключён
        модуль исполнения
    '''
    Analog = typemark('AnalogExecutor')     #Маркер аналогового типа
    Digital = typemark('DigitalExecutor')   #Маркер цифрового типа
        
    attrl = ['instanceDescription', 'isEnabled']


    def __init__(self, atBoard: ArduinoDevice, atPin: str, isEnabled: bool,
            instanceName: str, instanceDescription: str):
        '''
        Инициализировать подчиненного исполнителя, работающего на вывод,
        для Arduino-исполнителя.

        :param 'atBoard': ArduinoDevice
            Материнский Aruino-исполнитель

        :param 'atPin': str
            Адрес пина Arduino-исполнителя, к которому подключён подчинённый

        :param 'isEnabled': bool
            Использовать ли этого исполнителя или нет. Если этот 
            параметр отключить, то на исполнителя невозможно будет отдавать
            какие-либо команды, а также частично или полностью перестанут
            работать правила, в действиях которых фигурирует данный
            исполнитель

        :param 'instanceName': str
            Обязательное отображаемое имя исполнителя. Может быть
            пустым, но не рекомендуется оставлять его таким.
            Используется для отображения в интерфейсах вершителей

        :param 'instanceDescription': str
            Обязательное описание исполнителя. Может быть пустым.
            Используется для отображения в интерфейсах вершителей
        '''
        AqHardwareDevice.__init__(self, isEnabled, f'{atBoard.deviceAddress}:{atPin}:{self.driverId}', 'arduino', 
            f'{atBoard.deviceAddress}:{atPin}', parent = atBoard,
            instanceName = instanceName, instanceDescription = instanceDescription)
        self.motherPinAddress = atPin
        try: self.motherPin = self.parent.get_pin(f'{atPin}:i')
        except AttributeError: pass


    def getId(self) -> str:
        '''
        Каждый объект оборудования в Hyrex AsQamm имеет собственный внут-
        ренний индентификатор. У подчинённых Arduino-исполнителей он фор-
        мируется по следующей схеме:

        '{x}:{y}', где:
            x = Адрес подчинённого исполнителя;
            y = ID драйвера подчинённого исполнителя.

        :returns: str
        '''
        return f'{self.deviceAddress}:{self.driverId}'
