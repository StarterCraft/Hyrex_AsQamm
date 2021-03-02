'''
Модуль, в котором представлен основополагающий код для работы
с `комплексами`, `исполнителями` и `модулями`, классы вышеперечисленных
объектов, а также код Менеджера оборудования и Центра оборудования.
'''

from time import       sleep       as slp 
from pyfirmata import (Arduino     as DefaultArduino,
                       util        as ArduinoUtil,
                       UNAVAILABLE, ANALOG, SERVO,
                       PWM, INPUT, OUTPUT,
                       START_SYSEX, END_SYSEX)

from json import       (loads      as loadJson,
                        JSONDecodeError)

from libs import       *

from libs.functions import AqLogger
from serial.serialutil import SerialException
import libs.exceptions


class AqAbstractHardwareComplex:
    '''
    Класс `комплекса` - высокоуровневого объединения нескольких исполнителей.
    Пока не разработан.
    '''
    pass


class AqHardwareUnit:
    '''
    Класс, представляющий любого `исполнителя` — устройства, находящегося в 
    подчинении сервера. Все классы поддерживаемых типов устройств-исполнителей
    являются подклассами этого класса. Пока что, подерживаются только Arduino-
    исполнители.

    `Исполнители` могут иметь подчинённых себе `модулей`, если это предусмотрено
    типом этого исполнителя. Они могут быть объединены в `комплексы` для более
    глубокого взаимодействия друг с другом.

    Информация о них находится в hardware.asqd в виде JSON-списка по схеме ниже.
    Там хранятся базовые настройки исполнителя, а также информация обо всех под-
    чинённых ему модулях и их настройках:

    [
        /*Объект исполнителя, где:
          a —— ID драйвера исполнителя (любой ID драйвера представляет из себя
               целое число от 1000 до 9999);
          b —— Для Arduino-исполнителя — COM-порт, на котором он распологается;
          c —— Настройки исполнителя в виде "имя параметра: значение";
          d —— Для Arduino-исполнителя — адрес пина, на котором располагается
               модуль;
          e —— ID драйвера модуля;
          f —— Настройки модуля в виде "имя параметра: значение"
        */

        [a, b, {
            c,
            "pinMap": {
                //В параметре pinMap хранится информация о модулях,
                //привязанных к исполнителю
                d: [e, {
                    f
                    },

                //другие определения модулей по той же схеме
                }
            }        
        ],

        //другие определения исполнителей по той же схеме
    ]

    Абсолютно любого исполнителя можно отключить от системы, для этого существует
    атрибут 'isEnabled'.
    '''
    isEnabled = bool()

    class ArduinoUnit:
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

            OKMessage = typemark('OKMessage')
            ErrorMessage = typemark('ErrorMessage')

            def __init__(self, string: str):
                '''
                Инициализировать обработчик строкового сообщения. Если после-
                днее не соответствует синтаксису строковых сообщений, будет
                вызвано исключение.

                :param 'string': str
                    Строковое сообщение от Arduino-исполнителя в виде сырой
                    строки.
                '''
                if len(string.split(';')) < 2:
                    raise libs.exceptions.InvalidFirmataStringResponseError()

                self.statusCode, self.methodName = string.split(';')[0], string.split(';')[1]

                if self.statusCode == 'OK': #если сообщение без ошибки
                    self.type = self.OKMessage
                    self.receivedInfo = string.split(';')[2:]

                elif self.statusCode == 'ERR': #если сообщение об 
                    self.type = self.ErrorMessage
                    self.errorCode = string.split(';')[2]
        

        def __init__(self, comPort: str, isEnabled: bool,
                     instanceName: str, desc: str,
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

            :param 'instanceName': str
                Обязательное отображаемое имя исполнителя. Может быть пустым,
                но не рекомендуется оставлять его таким.
                Используется для отображения в интерфейсах вершителей

            :param 'desc': str
                Обязательное описание исполнителя. Может быть пустым.
                Используется для отображения в интерфейсах вершителей

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
            self.instanceDescription = desc
            self.result = float()

            self.add_cmd_handler(0x71, self.parseString)


        def __repr__(self):
            return f'{self.driverId} Arduboard at {self.motherPort}'
        

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


        def setPinMap(self, _map: dict, drv: module) -> None:
            '''
            Установить карту распиновки.

            Карта распиновки — словарь, ключами которого являются адреса пинов
            Arduino в нижеследующей форме:
            '{тип пинá (d для цифровых пинов, а для анáлоговых)}:{номер пина}',
            а значениями являются объекты модулей, подключенных к этим пинам.

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
            self.pinMap.update({'d:13': drv.Modules[1000](self, 'd:13', isEnabled = True,
                                                              instanceName = 'D13Led',
                                                              instanceDescription = 'D13 Built-in LED')})
            for pin, module in _map.items():
                self.pinMap.update({pin: drv.Modules[module[0]](self, pin, **(module[1]))})


        def getPinMap(self, mode = None) -> list:
            '''
            Получить карту распиновки.

            Карта распиновки — словарь, ключами которого являются адреса пинов
            Arduino в нижеследующей форме:
            '{тип пинá (d для цифровых пинов, а для анáлоговых)}:{номер пина}',
            а значениями являются объекты модулей, подключенных к этим пинам.

            Имеется 2 режима:
                режим None: получить список словарей в виде списка кортежей, где
                ключи — адреса пинов, а значения — списки из ID драйвера модуля и
                словаря его настроек

                pежим object: получить список словарей в виде списка кортежей, где
                ключи — адреса пинов, а значения — объекты модулей.

            :param 'mode': type 'object' or None = None
                Режим, который требуется.

            :returns: None
            '''
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
            print(f'{self.comPort}: {received}')


class AqHardwareModule:
    '''
    Класс, представляющий любой `модуль` — подчинённое устройство, которое
    может быть под контролем Arduino-исполнителя. Все классы поддерживаемых
    типов устройств-исполнителей являются подклассами этого класса.

    Модули для Arduino-исполнителея подразделяются на `датчики` и `средства 
    исполнения` (`executors`). 

    Как и лобой исполнитель, любой модуль можно отключить от системы, для
    чего можно использовать атрибут 'isEnabled'.
    '''
    class ArduinoSensor:
        '''
        Класс Аrduino-датчика. 
        Они имеют два подтипа: Analog (для аналоговых) и Digital (для цифровых
        датчиков).

        Любой объект Arduino-датчика имеет следующие атрибуты:

        :attrib 'attrl': list
            Список атрибутов, которые инициализируются из JSON-словаря в
            'hardware.asqd'
        
        :attrib 'motherBoard': AqHardwareUnit.ArduinoUnit
            Ссылка на объект Arduino-исполнителя, к которому подключён датчик

        :attrib 'isCalibrateable': bool
            Значение параметра определяется тем, может ли датчик, объект которого
            инициализируется, быть откалиброван (True) или нет (False). Если True,
            то должен существовать метод калибровки

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
        '''

        Analog = typemark('AnalogSensor')       #Маркер аналогового типа
        Digital = typemark('DigitalSensor')     #Маркер цифрового типа

        attrl = ['instanceDescription', 'isEnabled']

        def __init__(self, atBoard: AqHardwareUnit.ArduinoUnit, atPin: str, isEnabled: bool,
                     isCalib: bool, instanceName: str, desc: str, bkmeth: callable,
                     **kwargs):
            '''
            Инициализировать Аrduino-датчик.

            :param 'atBoard': AqHardwareUnit.ArduinoUnit
                Объект Arduino-исполнителя, к которому подключён датчик

            :param 'atPin': str
                Адрес пина Arduino-исполнителя, к которому подключён датчик

            :param 'isEnabled': bool
                Использовать ли этот датчик или нет. Если этот параметр
                отключить, то регистрация его значений системой статистики
                не будет выполняться, а также частично или полностью перес-
                танут работать правила, в условиях которых фигурирует данный
                датчик

            :param 'isCalib': bool
                Может ли датчик, объект которого инициализируется, быть отка-
                либрован (True) или нет (False). Если True, то должен быть
                по ключевому слову предоставлен аргумент 'clmeth', в противном
                случае будет вызвано исключение.

            :param 'instanceName': str
                Обязательное отображаемое имя датчика. Может быть пустым,
                но не рекомендуется оставлять его таким.
                Используется для отображения в интерфейсах вершителей

            :param 'desc': str
                Обязательное описание датчика. Может быть пустым.
                Используется для отображения в интерфейсах вершителей

            :param 'bkmeth': callable
                Метод получения готового значения датчика. В определении каж-
                дого из отдельных типов датчиков должен быть определён особый
                метод получения значения для этого типа датчика, который дол-
                жен быть направлен в этот агрумент. Это нужно для того, чтобы
                компоненты, которым неизвестно имя такого метода, могли вызвать
                его вызовом метода bakedValue

            :kwparam 'clmeth': callable
                Метод калибровки датчика. Если параметр 'isCalib' истиннен, то
                необходимо предоставить мeтод калибровки датчика.
                Это — параметр по ключевому слову!
            '''
            self.motherBoard = atBoard
            self.motherPinAddress = atPin
            try: self.motherPin = self.motherBoard.get_pin(f'{self.motherPinAddress}:i')
            except AttributeError: pass
            self.isEnabled = isEnabled

            if isCalib:
                self.isCalibrateable = isCalib
                try: self.calibrate = kwargs['clmeth']
                except: raise libs.exceptions.UndefinedCalibrationMethodError()

            self.instanceName = instanceName
            self.instanceDescription = desc
            self.bakedValue = bkmeth


        def __repr__(self):
            return f'{self.driverId} device at {self.motherBoard} ({self.motherPinAddress})'


        def getId(self) -> str:
            '''
            Каждый объект оборудования в Hyrex AsQamm имеет собственный внут-
            ренний индентификатор. У Arduino-исполнителей он формируется по
            следующей схеме:

            '{x}:{y}:{z}',
            где x = COM-порт Arduino-исполнителя, к которому подключён датчик;
                у = Адрес пина Arduino-исполнителя, к которому подключён датчик;
                z = ID драйвера датчика.

            :returns: None
            '''
            return f'{self.motherBoard.motherPort}:{self.motherPinAddress}:{self.driverId}'


    class ArduinoExecutor:
        '''
        Класс модулей исполнения для Arduino-исполнителя (например, серво-
        привода). 
        Они имеют два подтипа: Analog (для аналоговых) и Digital (для цифровых
        устройств исполнения).

        Любой объект таких модулей исполнения имеет следующие атрибуты:

        :attrib 'attrl': list
            Список атрибутов, которые инициализируются из JSON-словаря в
            'hardware.asqd'
        
        :attrib 'motherBoard': AqHardwareUnit.ArduinoUnit
            Ссылка на объект Arduino-исполнителя, к которому подключён
            модуль исполнения

        :attrib 'instanceName': str
            Обязательное отображаемое имя модуля исполнения. Может быть
            пустым. Используется для отображения в интерфейсах вершителей

        :attrib 'instanceDescription': str
            Обязательное описание модуля исполненияа. Может быть пустым.
            Используется для отображения в интерфейсах вершителей
        
        :attrib 'typeDescription': str
            Обязательное описание ТИПА модуля исполнения. Может быть пус-
            тым, но не рекомендуется оставлять его таким. Задаётся в 
            драйвере ТИПА исполнителя.
            Используется для отображения в интерфейсах вершителей
        '''
        
        Analog = typemark('AnalogExecutor')     #Маркер аналогового типа
        Digital = typemark('DigitalExecutor')   #Маркер цифрового типа
        
        attrl = ['instanceDescription', 'isEnabled']

        def __init__(self, atBoard: AqHardwareUnit.ArduinoUnit, atPin: str, isEnabled: bool,
                     instanceName: str, instanceDescription: str,):
            '''
            Инициализировать модуля исполнения для Arduino-исполнителя.

            :param 'atBoard': AqHardwareUnit.ArduinoUnit
                Объект Arduino-исполнителя, к которому подключён модуль ис-
                полнения

            :param 'atPin': str
                Адрес пина Arduino-исполнителя, к которому подключён модуль
                исполнения

            :param 'isEnabled': bool
                Использовать ли этот модуль исполнения или нет. Если этот 
                параметр отключить, то на модуль невозможно будет отдаавать
                какие-либо команды, а также частично или полностью перес-
                танут работать правила, в действиях которых фигурирует данный
                модуль исполнения

            :param 'instanceName': str
                Обязательное отображаемое имя модуля исполнения. Может быть
                пустым, но не рекомендуется оставлять его таким.
                Используется для отображения в интерфейсах вершителей

            :param 'desc': str
                Обязательное описание модуля исполнения. Может быть пустым.
                Используется для отображения в интерфейсах вершителей

            :param 'typeDesc': str
                Обязательное описание ТИПА модуля исполнения. Может быть пустым.
                Используется для отображения в интерфейсах вершителей
            '''
            self.motherBoard = atBoard
            self.motherPinAddress = atPin
            try: self.motherPin = self.motherBoard.get_pin(f'{self.motherPinAddress}:i')
            except AttributeError: pass
            self.instanceName = instanceName
            self.instanceDescription = instanceDescription


        def getId(self):
            '''
            Каждый объект оборудования в Hyrex AsQamm имеет собственный внут-
            ренний индентификатор. У Arduino-исполнителей он формируется по
            следующей схеме:

            '{x}:{y}:{z}',
            где x = COM-порт Arduino-исполнителя, к которому подключён датчик;
                у = Адрес пина модуля исполнения, к которому подключён датчик;
                z = ID драйвера модуля исполнения.

            :returns: None
            '''
            return f'{self.motherBoard.motherPort}:{self.motherPinAddress}:{self.driverId}'


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


import drivers                                  #Драйверы оборудования могут быть инициализированы
                                                #лишь после того, как будут готовы к работе все
                                                #классы, необходимые им для функционирования

from libs.statistic import AqStatist
from threading import Thread


class AqHardwareSystem:
    '''
    Класс системы управления оборудованием. Она осуществляет инициализацию
    всех исполнителей, коплексов и модулей; занимается мониторингом (записью
    значений) датчиков; осуществляет следование правилам (отдаёт команды мо-
    дулям исполнения в соответствии с ними).

    Описание важнейших атрибутов:

    :attrib 'isOk': bool
        Атрибут флага состояния системы. Если в системе при её инициализации
        пройзойдёт критическая ошибка, флаг будет установлен на False, и сер-
        вер узнает об ошибке по отрицательному значению этого флага

    :attrib 'installedArduinoHardware': list
        Этот список, после успешной инициализации системы, содержит все объек-
        ты установленных исполнителе. Они инициализируются конструктором после-
        довательно и добавляются в этот список. Если при инициализации какого-
        то конкретного исполнителя произойдёт ошибка, то он не будет включён в
        этот список

    :attrib 'monitors': list
        Этот список заполняется при вызове метода startMonitoring(), содержит
        объекты мониторов (см. документацию к AqArduinoUnitMonitor) для каждо-
        го исполнителя. Если при инициализации какого-либо из мониторов произой-
        дёт ошибка, то он не будет включён в этот список
    '''
    def __init__(self):
        '''
        Инициализировать систему управления оборудованием. Этот конструктор
        не принимает никаких аргументов.
        После создания всех необходимых объектов, этот метод-конструктор на-
        чинает инициализировать исполнителей, загружая и расшифровывая инфор-
        мацию о них из 'hardware.asqd'. Делается это так:

         —— В цикле, для каждого исполнителя, информация о котором есть в 
            'hardware.asqd', берётся ID драйвера этого исполнителя (такой ID пред-
            ставляет из себя целое число от 1000 до 9999);

         —— Затем, берётся значение из словаря drivers.__init__.Boards, при этом в
            качестве ключа используется тот самый ID драйвера. В качестве значения
            будет получен драйвер этого исполнителя, т. е. его КЛАСС;

         —— Сразу после этого этот полученный драйвер инициализируется с использо-
            ванием параметров, указанных в определении этого исполнителя, за исклю-
            чением параметра 'pinMap'. Инициализированный объект добавляется в спи-
            сок 'installedArduinoHardware';

         —— Если какой-то из вышеперечисленных этапов провален, то исполнитель не
            будет включён в список 'installedArduinoHardware'.
        '''
        self.isOk = bool()
        self.installedArduinoHardware = []
        self.monitors = []
        self.logger = AqLogger('Hardware')

        #Объект AqStatist инициализируется только один раз во всём коде, и только
        #в этом классе.
        self.statisticAgent = AqStatist()

        self.logger.debug('Инициализация оборудования начата')
        with open('data/system/~!hardware!~.asqd', 'r', encoding = 'utf-8') as configFile:
            try: 
               jsonString = loadJson(configFile.read())

               for hardwareObject in jsonString:
                   self.logger.debug(f'Подключение к устройству на {hardwareObject[1]}...')
                   try:
                       instance = (drivers.Boards[hardwareObject[0]])(hardwareObject[1], drivers, **hardwareObject[2])
                       self.installedArduinoHardware.append(instance)
                       self.logger.info(f'Устройство типа {hardwareObject[0]} на портy {hardwareObject[1]} подключено.')
                   except SerialException:
                       self.logger.error(f'Не удалось инициализировать Arduino-устройство типа {hardwareObject[0]} на портy '
                                         f'{hardwareObject[1]} из-за ошибки 0104: не удалось найти запрашиваемое устройство')
                       continue
                                       

            except JSONDecodeError:
                self.logger.error(f'Не удалось получить данные JSON из файла "data/system/~!hardware!~.asqd", проверьте файл на'
                                   'синтаксические ошибки')

        if len(self.installedArduinoHardware) == 0:
            self.logger.critical(f'Не удалось инициализировать Arduino-устройство, используя информацию из файла "~!hardware!~.asqd". '
                                 'Пожалуйста, убедитесь, что файл не повреждён и не пуст, что все модули подключены и находятся'
                                 'в рабочем состоянии. Для решения данной проблемы попробуйте переустановить AsQammServer, при'
                                 'переустановке внимательно следите за правильностью вводимой информации об оборудовании.')
            self.isOk = False
            self.logger.critical(f'Аварийное завершение работы')
        else:
            self.isOk = True


    def startMonitoring(self):
        '''
        Инициализировать и запустить мониторы (см. документацию к
        AqArduinoUnitMonitor) для каждого исполнителя.

        Монитор не будет инициализирован, если параметр 'isEnabled'
        у исполнителя не истиннен. Каждый инициализированный монитор
        будет добавлен в список 'monitors' и запущен.

        Метод не принимает агрументов.
        '''
        for unit in self.installedArduinoHardware:
           if unit.isEnabled:
               instance = AqArduinoUnitMonitor(self, unit)
               self.monitors.append(instance)

        for monitor in self.monitors:
            self.logger.debug(f'Запуск мониторинга для Arduino-устройства {monitor.assignedBoard.motherPort}')
            monitor.start()

    
    def getHardwareDataSheet(self):
        '''
        Получить полную информацию об установленном оборудовании в
        виде списка словарей, где каждый словарь представляет одно-
        го исполнителя. Отключенные исполнители НЕ исключаются из
        списка. Метод используется для отображения информации об 
        оборудовании в вершителях. Представление идёт по следующей
        схеме:

        [
            /*Объект исполнителя, где:
              a —— Тип исполнителя (на данный момент — возможен только 
                   "ArduinoUnit");
              b —— Используется ли исполнитель (значение параметра 'isEnabled'
                   для данного исполнителя);
              c —— ID драйвера исполнителя (любой ID драйвера представляет из
                   себя целое число от 1000 до 9999);
              d —— Для Arduino-исполнителя — адрес COM-порта, на котором он 
                   располагается;
              e —— Обязательное описание исполнителя. Может быть пустым.
                   Используется для отображения в интерфейсах вершителей;
              f —— Пин-карта исполнителя в виде словаря (см. документацию к
                   AqHardwareUnit.ArduinoUnit.setPinMap());
              g —— Количество модулей, которые подключены к исполнителю;
              h —— Количество модулей, которые подключены к исполнителю и ис-
                   пользуются
            */

            {"unitType": a,
             "isEnabled": b,
             "driverId": c,
             "comPort": d,
             "instanceDescription": e,
             "pinMap": f,
             "modulesQty": g,
             "enabledQty": h},

             //другие определения исполнителей по той же схеме
        ]
        '''
        modulesQty = 0   #Количество модулей, которые подключены к исполнителю
        enabledQty = 0   #Количество модулей, которые подключены к исполнителю и ис-
                         #пользуются
        dataSheet = []
        for unit in self.installedArduinoHardware: #КОСТЫЛЬ: проверки типа устройства нет
            for pin, module in unit.getPinMap():
                if module != None:
                    modulesQty += 1
                    if (module[1])['isEnabled']: enabledQty += 1
                    continue

            dataSheet.append({'unitType'           : 'AqArduino',
                              'isEnabled'          : unit.isEnabled,
                              'driverId'           : unit.driverId,
                              'comPort'            : unit.motherPort,
                              'instanceDescription': unit.instanceDescription,
                              'pinMap'             : dict(unit.getPinMap()),
                              'modulesQty'         : modulesQty,
                              'enabledQty'         : enabledQty})
            modulesQty = 0

        return dataSheet


class AqArduinoUnitMonitor(Thread):
    '''
    Класс `монитора` для исполнителя. `Монитор` представляет из себя
    подвид потока; для исполнителей он выполняет лишь запуск отслежи-
    вания значений датчиков. Некоторые вaжные атрибуты:

    :attrib 'assignedBoardMonitors': list
        Список содержит мониторы датчиков для всех таких модулей, ко-
        торые подключены к исполнителю
    '''
    def __init__(self, hardwareSystem: AqHardwareSystem, assignToBoard: AqHardwareUnit.ArduinoUnit):
        '''
        Конструктор `монитора` для исполнителя.

        :param 'hardwareSystem': AqHardwareSystem
            Ссылка на объект системы управления оборудованием. 

        :param 'assignToBoard': AqHardwareUnit.ArduinoUnit
            Ссылка на объект исполнителя, с которым работает монитор.
        '''
        Thread.__init__(self, target = self._run, args = [hardwareSystem, assignToBoard],
                        name = f'{assignToBoard.getId()}:monitor')
        self.assignedBoard = assignToBoard
        self.assignedBoardMonitors = []
        

    def _run(self, hardwareSystem: AqHardwareSystem, assignedBoard: AqHardwareUnit.ArduinoUnit):
        '''
        Рабочий метод `монитора` для исполнителя.

        :param 'hardwareSystem': AqHardwareSystem
            Ссылка на объект системы управления оборудованием. 

        :param 'assignedBoard': AqHardwareUnit.ArduinoUnit
            Ссылка на объект исполнителя, с которым работает монитор.
        '''
        for module in dict(assignedBoard.getPinMap(mode = object)).values():
            try:
                if type(module) == AqHardwareModule.ArduinoSensor:
                    instance = AqArduinoSensorMonitor(hardwareSystem.statisticAgent, module)
                    self.assignedBoardMonitors.append(instance)
                else: continue
            except AttributeError: continue

        for monitor in self.assignedBoardMonitors: monitor.start()


class AqArduinoSensorMonitor(Thread):
    '''
    Класс `монитора` для датчика. `Монитор` представляет из себя под-
    вид потока; для датчиков он выполняет работу по регистрации значе-
    ний с них через каждый, задаваемый для каждого отдельного датчика,
    промежуток времени.
    '''
    def __init__(self, statisticAgent: AqStatist, assignToSensor: AqHardwareModule.ArduinoSensor):
        '''
        Конструктор `монитора` для датчика.

        :param 'statisticAgent': AqStatist
            Ссылка на объект регистратора статистики. 

        :param 'assignToSensor': AqHardwareModule.ArduinoSensor
            Ссылка на объект датчика, с которым работает монитор.
        '''
        Thread.__init__(self, target = self._run, args = [assignToSensor, statisticAgent],
                        name = f'{assignToSensor.getId()}:monitor', daemon = True)


    def _run(self, assignedSensor: AqHardwareModule.ArduinoSensor, statistic: AqStatist):
        '''
        Рабочий метод `монитора` для датчика.

        :param 'assignedSensor': AqHardwareModule.ArduinoSensor
            Ссылка на объект датчика, с которым работает монитор.
  
        :param 'statistic': AqStatist
            Ссылка на объект регистратора статистики. 
        '''
        while True:
            try:
                if not self.statistic.isBusy:
                    self.statistic.registerStatistic(self.assignedSensor.getId(), self.assignedSensor.bakedValue())
                elif self.statistic.isBusy:
                    while self.statistic.isBusy: slp(0.48)
                    self.statistic.registerStatistic(self.assignedSensor.getId(), self.assignedSensor.bakedValue())
                    
            except AssertionError:
                slp(0.48)
                continue

            slp(self.assignedSensor.probeFrequency)
