'''
Модуль, в котором представлен основополагающий код для работы
с `комплексами`, `исполнителями` (или, упрощённо, `устройствами`),
классы вышеперечисленных объектов, а также код Системы оборудования.
'''

from time import       sleep       as sleep 
from json import       (loads      as loadJson,
                        JSONDecodeError)

from libs import       *
from enum import       *
from libs.utils import AqLogger
from serial.serialutil import SerialException
import sys, libs.exceptions, pandas, glob, importlib, typing


class AqHardwareConnectionType(Enum):
    '''
    Класс перечисления возможных способов подключения к какому-то исполнителю.
    '''
    WireSerial = 1
    WireFirmata = 2
    WirelessWiFi = 3
    WirelessBluetooth = 4
    WirelessMobile = 5


class AqHardwareComplex:
    '''
    Класс `комплекса` - высокоуровневого объединения нескольких исполнителей.
    Пока не разработан.
    '''
    pass


class AqHardwareDevice:
    '''
    Класс, представляющий любого `исполнителя` (или, упрощённо, `устройство`)
    — устройство, находящееся в подчинении сервера. Все классы поддерживаемых
    типов устройств-исполнителей являются потомками этого класса.
    `Исполнители` и `устройства` есть одно и то же, если не указано иное!
    `Устройства` могут иметь подчинённых себе других `устройств`, если это пре-
    дусмотрено типом устройства. Они могут быть объединены в `комплексы` для более
    глубокого взаимодействия друг с другом.

    Информация о них находится в hardware.asqd в виде JSON-списка по схеме ниже.
    Там хранятся базовые настройки устройства, а также информация обо всех под-
    чинённых ему устройствах и их настройках:

    [
        /*Объект устройства, где:
          a —— ID драйвера устройства (любой ID драйвера представляет из себя
               строку длиной 4 символа, состоящую из символов латиницы и цифр
               от 0 до 9);
          b —— адрес (его форма зависит от типа исполнителя), на котором он
               располагается;
          c —— Настройки исполнителя в виде "имя параметра: значение";
          d —— какой-либо определитель способа подключения к подчинённому ис-
               полнителю (например, для Arduino-исполнителя — адрес пина, на
               котором располагается подчинённый исполнитель);
          e —— ID драйвера подчинённого исполнителя;
          f —— Настройки подчинённого исполнителя в виде 
               "имя параметра: значение"
        */

        [a, b, {
            c,
            "pinMap": {
                //В параметре pinMap хранится информация о подчинённых испол-
                //нителях, привязанных к исполнителю, если они им поддержива-
                //ются
                d: [e, {
                    f
                    },

                //другие определения подчинённых исполнителей по той же схеме
                }
            }        
        ],

        //другие определения исполнителей по той же схеме
    ]

    :attrib 'isEnabled': bool
        Атрибут, определяющий, используется ли исполнитель в системе

    :attrib 'isControllable': bool
        Атрибут, определяющий, контролируется ли исполнитель сервером напрямую
        (True) или он контролируется своим материнским исполнителем (False)

    :attrib 'isFertile': bool
        Атрибут, определяющий, способен ли исполнитель иметь других исполните-
        лей в подчинении

    :attrib 'parent': AqHardwareDevice
        Если исполнитель является подчинённым, то в этом атрибуте будет нахо-
        диться ссылка на объект материнского исполнителя, иначе — None
        
    :attrib 'platform': str
        Индентификатор протокола

    :attrib 'deviceId': str
        Индентификатор исполнителя. Генерируется при его инициализации, пред-
        ставляет из себя строку длиной 4 символа, состоящую из символов лати-
        ницы и цифр от 0 до 9

    :attrib 'deviceAddress': str
        Адрес (его форма зависит от типа исполнителя), на котором он располага-
        ется

    :attrib 'driverId': str
        Индентификатор драйвера исполнителя, представляет из себя строку дли-
        ной 4 символа, состоящую из символов латиницы и цифр от 0 до 9. Задаётся
        в определении драйвера исполнителя

    :attrib 'typeDisplayName': str
        Необязательное отоботображаемое имя исполнителя. По умолчанию — имя класса
        исполнителя. Используется для отображения в интерфейсах вершителей
        
    :attrib 'typeDescription': str
        Обязательное описание типа исполнителя. Может быть пустым, но не рекомен-
        дуется оставлять его таким. Задаётся в драйвере исполнителя. Используется
        для отображения в интерфейсах вершителей
    
    :attrib 'instanceName': str
        Обязательное отображаемое имя конкретного исполнителя. Может быть пустым.
        Используется для отображения в интерфейсах вершителей

    :attrib 'instanceDescription': str
        Обязательное описание конкретного исполнителя. Может быть пустым.
        Используется для отображения в интерфейсах вершителей
    '''
    class ConnectionType(Enum):
        '''
        Класс перечисления возможных способов подключения к какому-то исполнителю.
        '''
        WireSerial = 1
        WireFirmata = 2
        WirelessWiFi = 3
        WirelessBluetooth = 4
        WirelessMobile = 5


    isEnabled, isControllable, isFertile = bool(), bool(), bool()
    parent = None
    platform, deviceId, deviceAddress, driverId = str(), str(), str(), str()
    typeDisplayName, typeDescription, instanceName, instanceDescription = str(), str(), str(), str()


    def __init__(self, isEnabled: bool, id: str, platform: str, address: str, parent = None,
            isFertile: bool = False, instanceName: str = '', instanceDescription: str = ''):
        '''
        Инициализировать объект абстрактного исполнителя. Этот конструктор пре-
        имущественно используется в драйверах исполнителей.

        :param 'isEnabled': bool
            Используется ли этот исполнитель в системе или нет.

        :param 'platform': str
            Индентификатор протокола

        :param 'address': str
            Адрес (его форма зависит от типа исполнителя), на котором он распо-
            лагается

        :kwparam 'parent': AqHardwareDevice = None
            Если исполнитель является подчинённым, то — объект материнского испол-
            нителя

        :kwparam 'isFertile': bool = True
            Способен ли исполнитель иметь других исполнителей в подчинении
    
        :kwparam 'instanceName': str = ''
            Отображаемое имя конкретного исполнителя. Может быть пустым.
            Используется для отображения в интерфейсах вершителей

        :kwparam 'instanceDescription': str = ''
            Описание конкретного исполнителя. Может быть пустым.
            Используется для отображения в интерфейсах вершителей
        '''
        self.parent, self.isEnabled, self.isFertile = parent, isEnabled, isFertile
        self.platform, self.deviceId, self.deviceAddress = platform, id, address
        self.isControllable = not self.parent
        if self.isFertile: self.children = []


    def getChildren(self) -> list:
        '''
        Получить список подчинённых исполнителей данного исполнителя. Метод
        не принимает никаких аргументов.

        :returns: list<AqHardwareDevice>
        '''
        if not self.isFertile: 
            raise NotImplementedError('Этот исполнитель не может иметь других исполнителей в подчинении')

        return self.children


import drivers                                  #Драйверы оборудования могут быть инициализированы
                                                #лишь после того, как будут готовы к работе все
                                                #классы, необходимые им для функционирования

from libs.statistic import AqStatist
from threading import Thread


class AqHardwareSystem:
    '''
    Класс системы управления оборудованием. Она осуществляет инициализацию
    всех исполнителей и комплексов; занимается мониторингом (записью
    значений) датчиков; осуществляет следование правилам (отдаёт команды 
    исполнителям, работающим на вывод, в соответствии с ними).

    Описание важнейших атрибутов:

    :attrib 'isOk': bool
        Атрибут флага состояния системы. Если в системе при её инициализации
        пройзойдёт критическая ошибка, флаг будет установлен на False, и сер-
        вер узнает об ошибке по отрицательному значению этого флага

    :attrib 'installedHardware': dict<str, list<AqHardwareDevice>>
        Этот словарь, после успешной инициализации системы, содержит все объек-
        ты установленных исполнителей. Ключами словаря являются имена поддержи-
        ваемых протоколов, а значениями — списки с объектами установленных ис-
        полнителей. Эти объекты инициализируются конструктором системы управле-
        ния оборудованием последовательно и добавляются в словарь. Если при ин-
        ициализации какого-то конкретного исполнителя произойдёт ошибка, то он
        не будет включён в этот словарь

    :attrib 'monitors': list
        Этот список заполняется при вызове метода startMonitoring(), содержит
        объекты мониторов (см. документацию к AqArduinoDeviceMonitor) для каждо-
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
            ставляет из себя строку длиной 4 символа, состоящую из символов латини-
            цы и цифр от 0 до 9);

         —— Затем, берётся значение из словаря drivers.__init__.Devices, при этом в
            качестве ключа используется тот самый ID драйвера. В качестве значения
            будет получен драйвер этого исполнителя, т. е. его КЛАСС;

         —— Сразу после этого этот полученный драйвер инициализируется с использо-
            ванием параметров, указанных в определении этого исполнителя, за исклю-
            чением параметра 'pinMap'. Инициализированный объект добавляется в сло-
            варь;

         —— Если какой-то из вышеперечисленных этапов провален, то исполнитель не
            будет включён в словарь 'installedHardware'.
        '''
        self.isOk = bool()
        self.installedHardware = {}
        self.monitors = []
        self.logger = AqLogger('Hardware')

        #Объект AqStatist инициализируется только один раз во всём коде, и только
        #в этом классе.
        self.statisticAgent = AqStatist()

        #Инициализация протоколов
        self.logger.info('Инициализация протоколов...')

        for fileName in glob.glob('drivers\\platforms\\*.py'):
            nameToImport = fileName.replace('\\', '.')[:-3]
            platformName = fileName.replace('\\', '.')[:-3].split('.')[-1]
            classNames = []

            with open(fileName, 'r', encoding = 'utf-8') as file:
                for line in file.readlines():
                    if line.startswith('class '):
                        try:
                            if ('AqHardwareDevice' in line.split('(')[1]):
                                classNames.append(line[6:line.index('(')])
                                self.logger.debug(f'Класс устройства {line[6:line.index("(")]} инициализирован')
                        except IndexError: continue

            drivers.Platforms.update(
                {platformName: [getattr(importlib.import_module(nameToImport), name) for name in classNames]})


        #Инициализация драйверов
        self.logger.info('Инициализация драйверов устройств...')

        for folderName in glob.glob('drivers\\devices\\*'):
            if '.' in folderName: continue
            for installedPlatformName in drivers.Platforms.keys():
                if installedPlatformName in folderName:
                    deviceDriverClasses = {}

                    for fileName in glob.glob(f'{folderName}\\**\\*.py'):
                        with open(fileName, 'r', encoding = 'utf-8') as file:
                            for line in file.readlines():
                                if line.startswith('class '):
                                    try:
                                        for platformClass in drivers.Platforms[installedPlatformName]:
                                            if platformClass.__name__ in line.split('(')[1]:
                                                if fileName in deviceDriverClasses.keys():
                                                    deviceDriverClasses[fileName].append(line[6:line.index('(')])
                                                else: deviceDriverClasses.update({fileName: [line[6:line.index('(')]]})
                                                self.logger.debug(f'Драйвер устройства {line[6:line.index("(")]} инициализирован')

                                            else: continue
                                    except IndexError: continue

                    for driverFile, driverClassList in deviceDriverClasses.items():
                        nameToImport = driverFile.replace('\\', '.')[:-3]

                        for className in driverClassList:
                            driverClass = getattr(importlib.import_module(nameToImport), className)
                            drivers.Devices.update({driverClass.driverId: driverClass})


        self.logger.info('Инициализация оборудования...')
        with open('data/system/~!hardware!~.asqd', 'r', encoding = 'utf-8') as configFile:
            try: 
               jsonString = loadJson(configFile.read())

               for hardwareObject in jsonString:
                   self.logger.debug(f'Подключение к устройству по адресу {hardwareObject[1]}...')
                   try:
                       instance = (drivers.Devices[hardwareObject[0]])(hardwareObject[1], drivers, **hardwareObject[2])
                       if instance.platform not in self.installedHardware.keys():
                           self.installedHardware.update({instance.platform: [instance]})
                       else: self.installedHardware[instance.platform].append(instance)
                       self.logger.info(f'Устройство типа {hardwareObject[0]} по адресу {hardwareObject[1]} подключено.')
                       self.logger.debug(self.installedHardware)
                   #except SerialException:
                    #   self.logger.error(f'Не удалось инициализировать устройство типа {hardwareObject[0]} по адресу '
                     #                    f'{hardwareObject[1]} из-за ошибки 511: не удалось найти запрашиваемое устройство')
                      # continue
                   except Exception as e: raise e
                                       

            except JSONDecodeError:
                self.logger.error(f'Не удалось получить данные JSON из файла "data/system/~!hardware!~.asqd", проверьте файл на'
                                   'синтаксические ошибки')

        if not self.installedHardware:
            self.logger.critical(f'Не удалось инициализировать yстройства, используя информацию из файла "~!hardware!~.asqd". '
                                 'Пожалуйста, убедитесь, что файл не повреждён и не пуст, что все устройства подключены и находятся'
                                 'в рабочем состоянии. Для решения данной проблемы попробуйте переустановить AsQammServer, при '
                                 'переустановке внимательно следите за правильностью вводимой информации об оборудовании')
            self.isOk = False
            self.logger.critical(f'Аварийное завершение работы')
        else: self.isOk = True


    def startMonitoring(self) -> None:
        '''
        Инициализировать и запустить мониторы (см. документацию к
        AqArduinoDeviceMonitor) для каждого исполнителя.

        Монитор не будет инициализирован, если параметр 'isEnabled'
        у исполнителя не истиннен. Каждый инициализированный монитор
        будет добавлен в список 'monitors' и запущен.

        Метод не принимает агрументов.

        :returns: None
        '''
        for unit in self.installedHardware['arduino']:

            if unit.isEnabled:
                instance = unit.Monitor(self, unit)
                self.monitors.append(instance)

        for monitor in self.monitors:
            self.logger.debug(f'Запуск мониторинга для Arduino-устройства {monitor.assignedBoard.motherPort}')
            monitor.start()

    
    def getHardwareDataSheet(self) -> list:
        '''
        Получить полную информацию об установленном оборудовании в виде списка
        словарей, где каждый словарь представляет одного исполнителя. Отключен-
        ные исполнители НЕ исключаются из списка. Метод используется для отобра-
        жения информации об оборудовании в вершителях. Представление идёт по сле-
        дующей схеме:

        [
            /*Объект исполнителя, где:
              a —— Тип исполнителя;
              b —— Используется ли исполнитель (значение параметра 'isEnabled' для
                   данного исполнителя);
              c —— ID драйвера исполнителя (любой ID драйвера представляет из себя
                   строку длиной 4 символа, состоящую из символов латиницы и цифр
                   от 0 до 9);
              d —— Адрес исполнителя;
              e —— Обязательное описание исполнителя. Может быть пустым.
                   Используется для отображения в интерфейсах вершителей;
              f —— Словарь с информацией о подчинённых исполнителях
            */

            {"unitType": a,
             "isEnabled": b,
             "driverId": c,
             "comPort": d,
             "instanceDescription": e,
             "children": f},

             //другие определения исполнителей по той же схеме
        ]
        '''
        modulesQty = 0   #Количество подчинённых, которые подключены к исполнителю
        enabledQty = 0   #Количество подчинённых, которые подключены к исполнителю и ис-
                         #пользуются
        dataSheet = []
        for unitList in self.installedHardware.values(): #КОСТЫЛЬ: проверки типа устройства нет
            for unit in unitList:
                for pin, child in unit.getChildren():
                    if child != None:
                        modulesQty += 1
                        if (child[1])['isEnabled']: enabledQty += 1
                        continue

                dataSheet.append({'platform'           : unit.platform,
                                  'isEnabled'          : unit.isEnabled,
                                  'driverId'           : unit.driverId,
                                  'deviceAddress'      : unit.motherPort,
                                  'typeDisplayName'    : unit.typeDisplayName,
                                  'typeDescription'    : unit.typeDescription,
                                  'instanceName'       : unit.instanceName,
                                  'instanceDescription': unit.instanceDescription,
                                  'children'           : dict(unit.getChildren())})
                modulesQty = 0

        return dataSheet
