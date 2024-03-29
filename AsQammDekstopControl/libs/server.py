from libs.exceptions import ServerConnectionError, ServerResponseException
import libs.utils, requests, http, json, socket


class AqServerCommutator:
    '''
    Класс коммутатора сервера, который необходим для обмена информацией с
    сервером. Инициализируется сразу после запуска ядра AqMainWindow. Для
    работы классу коммутатора необходимо знать IP-адрес сервера, (и, оп-
    ционально, его порт). Эта информация хранится в файле по адресу
    'data/config/~!serverdata!~.asqd' и загружается при инициализации
    коммутатора. Установить IP и порт сервера нужно при установке вершителя
    AsQammDekstop, а изменить его можно через настройки вершителя или через
    AsQammCrashHandler, если возникла ошибка соединения с сервером.    

    При отправке каждого запроса коммутатор прикрепляет к нему токен, что-
    бы сервер мог индентифицировать источник запроса как верифицированного
    вершителя.

    :attrib 'ip': str
        IP-адрес сервера

    :attrib 'port': int
        Порт сервера
    '''
    def __init__(self, root):
        '''
        Конструктор коммутатора сервера.

        :param 'root': AqMainWindow
            Ядро
        '''
        with open('data/config/~!serverdata!~.asqd', 'r') as configFlie:
            fileString = libs.utils.AqCrypto.decryptContent(configFlie.read())
            jsonString = json.loads(fileString)
            self.ip = jsonString['ip']

            if jsonString['port']: self.port = jsonString['port']
            else: pass
            
        self.__token__ = b'''\x1e\xe62S4\xf9\xc0@2\xf8/xq\xb2\x8e\xbf\xed\x82\x95\x08\xb6\xf3f\xb0mx\xd7WE\xe1\xa3\xadH\x8fsy\x96/z=\x94\xdd\x00\xaf\x8f\x97$\x10\x02\xaa:\xcc\xea\xae\x03j\x00QD\x8em\x95\xda:\x9e\xf0\xc0\'\x9a*\x13V\xdf\x8dB_\xdf\xb5\xab\x83\xba\xba\xa4\xae\xd5\xba\xd2\xab\xa3\x06\xa3\xd7I\xee\xab\x89\x91\x88\tC\x94z\x80u\x06\xcdR\xcfx\xdeO\x96\x12\x08\x14\xb6\x8dK\x7fx\xcf\xaf\xb2\n\xc5\xc5\xb9\x017`\xe9\xd8\xc0\nf^#\xbf\xff}\xf2B\x13\x8e*\x93\x83@\xdd6\xb6\x83\x95$\xfeq\xc1\xeb\xcax\xd2\r#\xcd\xc1*\x92\xffB]Z*\x9b\x0er\x7f\xf8P\xed\x8d)\xf1\x86\x98\xe4\x01U\x96\x07D\xa0\x17JN#n\xcd\xea\xf7\xcd\x11\xe5\x89\xe0T\x17;\x86\xd8W\xc4\r\xf5\x1b\x94;\x87\xc9\x81\xe3@5\x88\xbe\x15\x15t\xc45\xef\x83\xdc\x9a\xf8\x91\xf2a\xe6e\x1c\x17\xfaCs`r\'8\xfe\x17(br\xe46\xb8W\x17a$,u\xfc\xe7Pi\xf8\x04\x9dZ\xb6z\x8a\xdcu\x9e\x93\x81\xcbH\xc8K\x08\xb5\xa2\xbb\x14H\x1b\x10\xa46\x81\x93\xd9\x8c\x82\x9e\xb9\xda\xd9p\x8bJf+e2\xa2\x1d\xdfd\x86xCN\xff\xd1\tg\xc5\xa4iPz\tZ.\xf0\xa2n_;!N2\x95c\xae\x9a\xb0\xfb\xe5\xe1R_\xc3\xc5\xf0y\x92\x04\xbb\x8d\x17\xce\x06\xa1\xc0\xda\xc7\xb1\xf7D\'Yb\xa3&\xcf\x95\x1b\xc9\xa0(8\xd6\xeen\x0c\xd50N\n\x00\xc8Hc\x84\xa4\x07\x99\x05o\x9a\xa6\x9a\x03\x9f\xc2l\xb3p-\x8f\xec\xd7\xeeS!O?u\x9b\x00\xf6\xdag\xbb\xf8\xbe\xa0\x0c\xb4\x1fAt\xbc\x96\'\xe1\xb4o@\xb6(\xc0VXg\xfd9\xba\x02\x83=R\xef\xeb\xe3@\x9b\xe3\x8a\xc8h\xf0c\x82=EU\x8e\x87\xa5\xafV]\x88\xf8\xb5\xbb&F\x1e\xf0Crd\xd8/\xef\xec\xc25\xd8\xe7\xe1\xdc\xa3Y\x10\x9e?\xd5\xa1\xcf\xbat\xc3a\xb7\xac\xbe\xcb\x87J\x9b\xca\xc7\x97\x17F\x96~\x862\x11k?*]\x16\xdb$\xbbyh\x1e\xe3\xa2U$q:\xd0\x81nI!\x1f\xfdRA\x82\xad\xb6e)\x1f\xff\xb23!\xaf\xc2fZ\x15>\xda\xb6\xa2\xaf\xbe\xa4\xbe\x91\x82\x7f\xac}X\xe2\xe0DZF\xdej\x85\xe5IU\xf4\xf6/_k\xb8\xf6\xd7\x98N|\x8dy\x9aR\xa9\xd16\xb0n+\xc66\xea\xbd\x0f\x0c}\xfcD\xb6\x17\x87\xad\x9e\xfc\xd5\xd9t{}\x85P\x1c\x12\xc5\\\xb2\xbc\xd5j\x85%\x18\xa5\xfeT-\xdcV\x02\xd1\x07\xe9\x91c{^s\x1b\xa2h@\xf5Z\x0c\xc0\xa2\xdd<\trY\xb66\x9fy{m\xbf4\xd1J{\xa1\xa5\xbdn\xf2\xa4\x0bEd\x18\x1a\xed\x15H\xd7\xdd-Z/I\xd0 \xc5u\x9f\tu\x8f\xa9f\xf1I\xaa\x18\x8f\x0bk\x10\xfd\xb1n\xf7\xa4>i!\x94\xab\x1f\x14\xcb\xc2\'\xecu\x16\'\xda\x97,\xcf\xa9#\x97\xa1\x8a\x94\x86v\xc9\x95"\xf5\xa1@\xc0\x18Fr\x0c&\x13F\xae;\xe0\x8d\xfc\xf6_\xa9\xa3#]A\xabb\x92djV\x98\x82\xac\xb0\xabe\xf5\xa6\x94]</\xad|u\xd7\x18c\x1e\xdb\x11\xef\x9c\x12s3\x96\x05W%!%\x86\x8bU7\x18\xbc\x1e%\n\xf5\x12\xbaB]=\x85=n"\x15\xe9\xe0H\xda\xe91\x04u\xa2:\xf2|\xe2[fT\xea\xa8\x9d\xfcT=\xd4s\xf1\x9cV2t0\x9cv\xfa\xc7|\xe6If}\xe6\xe0M\xc4\xb4I\xca<]\x88\xa1E\x18\xe2\xff\xed\xdd\xf3\x13\xb2]\xd7:k\'\x13k\xb0\x1a\xb2\xef\xcb\x04\xdf\x94\xc9A,#\x17\x90~\xe10\xa2\xd4\xfds\xdc\xbe\x02\x14\xe4\xbes\x07\xd0\xc18\xacN.\xd7`\x85~S\tmH=\xf4y\xae[\xde\xdf\xb9\xca\x9d\xce\xd0E\xdf\xf5\xaau\x95\xa0=\xa9\xde6\x1b\xe3\xb4\xa6P\xd7\xc5,\xbe\x9a\xfb\x14\xe9\x10K\xc4\x93\x86\t\x0f_\x9cYD>~\x92.G\x17U\xca\xd8\xf1%:\xe3\x80\xd6p\x0b\x00D+\x04_\x1eD\xceD,\x83\xf9\xf9,h*\xe3\xab\x83\xfa\xb3"\x95\xee\n\xff\xe4\x06\x9d\r\xcf\xf5\xc7L\x1c,\x90B\xf0*\xd7\xa5W\xe1\x8b\xe6I\x7f\xc8d\xabi/\x94\x01\xfc\x94\xf5*\xf0\xc5\xaf&\x1b\x1fm\x02S\xdb\x13\xdb\xc5$\xda\xbd\xf51\x04\xac\xbb\r\xf1\x9d\x03\xb4\xf6\x8ak\x83\xdf\x82n\r\x18D\xac\x9f\xa1y\x9d5(\x10\xd4\xfa\xd8\x93v\xc5\x8c\xb0\xb5\xa6B<S\x98M+Rp\xb5E\x83e\xad\x05e\xa7\xfc\x8d\xb30\t+\xf2myQ\x1am\xa7\xdf\xbe\xf1C\xae\xc3Y\xf5\x0f\x85\xd0\xd1\xf6\x0f>\xd1UQf\xd6j\xc5\xf6B\x8d\x9a\x8a\xd7 \xc8G\xcb\xf4\x99\xfe\x17\x896\xbbg\x10/"\x0e\xfa7\x9e3\x12\x1a\xb2\x1f\xd5\xb2\x99[\xdas\x9e\x15+~\xf6\x93\x83p\xd8\x00\x9cQP!,<\nX:\xbe\xb3\xb7\x17\x81\x97\xb1\xe0\xfaz:\x15\x86#\x99l\x1a\xea{\xef\xcf\x15\x18\x8f\x1f\xbd\xd1\x16\x07\x83\x0b\xbf\xea[\x11\xb61l-\x82\xd6(g\x00|\xc0\xe0/*a\xb5gt\xe1\xc5r\x8b\xfe9\xff\x82\x01\x0c\x8f\xfa\xb1+x\xdb\xd9\xc72.7E\x8f\n\x1b\x19\xb8d*\x9e\x91\xef+<$1Z\x08\xc4\xc9uy\xf0\xb5G\xcaW\x97\xd5r="E\xb9R\xdf\xf2\xb6\xa2KD:\xe4]\xe4m4\x83nU\x81\xaa+\xaf\x80\xad\xab\x97\x9c8\xde\x06\xcc\x0b\x94\xa5\xf1\xc1\xfcC;\xeffa\xee\xdf\xd1*G\xe3\xaf}Q(?\x93j\xb8\xc5l8tS\x82)\xd7 \x1f\xe9\x95J\xcb\x0b\xc3n\xdeOPD\xd8\x82,+\xd8\x1fM\xa8\xfbvQ\x8f\xb5\x0bN\x05\x07jN,\x91\xcd-oT\xb8\xb67\x07\xeb~\xeb\xad\x85~\x9d\xcaUS&\x18\x17\x87\xcdmd\x85~\x05\x1c6a\x8fo\xde\xae\x0f\xc42)w\xab\xfb\x94\xd0\x03\xee:\xc5$\x94\xa1\xa9\x8e\xc5\xcf\x06\x7f_\x9aZ\x11}\xe6\xc8-\x8e,?[\x92\x8a\x8d\xc4\x16l\x96:\x1e\xd5\th\xd2\xc0\xdc[qZ3\x0cRY\x17\xbd\x9czm\x87\x97\x1b\x8f\xb9-\xf1\x9bi\x12KOS\x88\xb2hB2\xdbv\xe0Rm\xe0\xa8o\x07i\xe4\xc6\r\xb8\x13p\xde\x10\x8b2$fa\x89B\x8f\xcb^d[6\x14<\xdd\xd2\xa5(n\xb9^}c\xa1Y\x91\x86\xad\xb6}\x8b\xc7%\xa1FA\x8e\xffn\x1f\x9b\xd9>?EP\xb0T\xb3\xa4\x92\x840\xf4a\x8c\xbe\x9d\x04\xd3\xdd\x08La:\x87\x1b\x98\xb6\xc5\xaa\x81 \xee\xf0SrC\xbaZz\xb8v\xa8\xa2\x1e\xb0u\xf7\xa0i\xb4\xa3\xa2\x81\xc1\xdb\xa8b\x9b%|\xf0CQ\xb6\x96y\x11\xcaMk\xb7\xa0\xf3\x9fl\xc5\x9d\xf9\x01\x81\xc1\xa8\x17\xcf\xac\xfdvZ#W6\x17\xfa\xc8\xc8\xae\xcb\xd6,\xd9\xf5\x9d\xc7\x8fw)\x19\x97\xb3\xcf\xb7\xe4\xf2\xa9\xc3\xdd0h\xcb\xf6\xca\xf7\xee\x9d\xbb@~2\xb6\x8e\xf0\xb3\x97\xc5\xa2\xbc\xb1\x14\x02\xac\xfd\x89\x95$`\xed\xb0\x85\x8a\xf7\r*rW\x07\xbb\xa6\xd2\xc0\x9b\xe3aV.\x0e\xe4I=\xaf\x1d\x9c6\xa8\x8f\x9d\x9fo+\x17\xd9\n\xd6\x08\xbai~\xe5\x18\xa6\x1f\xfd\xee>\x1e)\xd3n\x99\x8c)\x8c\xe6\xd0\nX\xdcK\xb4\xd7\xfa\x18}\xb9E\xe1`\x11\x14\x95\x82\x03z\xf32s\xd6\x19\x85|a\xe5\x97\xde[\xc5\xf6:\xd7\xa3\x9e;GQ\x12\xc8\xc4`\x0e\xee\xd7\x9e\xd1\x92]z\x1dE9\x1aF\xda)\x0b\xe4\x85\xe4\x06<\xe4\xc1\x92\xcf\xf6\xdax\xdd5h\x8at#\xcd\x8d\x9f\x17\x94\x84\xfe\x9c\xc5\xe3\xa7l\xdc\xdfY(g\x8c\xf2\x83\xb9@\x18hC\xee\xbbUA&\xd8\xb5X\xe2\xd7\xe3\x85\x16\x10\xa7\x19\xdb\x05\x11\x19\xc5\x012\xd4\xc7\xa0\xf0\xb1\xf6\xf1\x8c`?n\xe23\x1a\xed!\xe8u?\'\xc82\xa1r\x96]\xdcs\x1f\xd3\x88\xf9\x96\xf2\xee\x0e\x1e\xbf\xd6\xd1\xe6yp\x86\xfff\x96\xb6\xefE\xea\xbe\x9eJ\xa2j\xf5\x8f'''.hex()
        self.commutatorLogger = libs.utils.AqLogger('ServerCommutator')

        if jsonString['port']: self.commutatorLogger.debug(f'Известный адрес сервера: {self.ip}:{self.port}')
        else: self.commutatorLogger.debug(f'Известный адрес сервера: {self.ip}')


    def get(self, methodId: str, returnMode, data: dict = None):
        '''
        Переслать серверу HTTP-запрос GET для вызова какого-либо метода
        сервера и получения от него какой-либо информации.

        :param 'methodId': str
            Название метода сервера, которого необходимо вызвать. Это
            должен быть GET-метод (то есть, нельзя переслать GET-запрос
            для выполнения POST-метода, и тому подобное)

        :param 'returnMode': type
            Режим возврата ответа на запрос, задаётся типами int, str,
            bytes и json. Возможны следующие режимы:
                int   —— метод вернёт только статус-код HTTP;
                str   —— метод вернёт содержимое ответа в виде текста;
                bytes —— метод вернёт содержимое ответа в виде байтов;
                json  —— метод вернёт содержимое ответа в виде структу-
                         ры (списка, словаря).

        :kwparam 'data': dict = None
            Опциональные данные, которые нужно передать серверу при
            передаче запроса.
        '''
        if data:
            try: response = requests.get(f'http://{self.ip}:{self.port}/{methodId}', json = {'tok': self.__token__, **data})
            except AttributeError: response = requests.get(f'http://{self.ip}/{methodId}', json = {'tok': self.__token__, **data})
            except:
                try:
                    self.commutatorLogger.error(f'Не удалось подключиться к серверу по адресу {self.ip}:{self.port}')
                    raise ServerConnectionError(data = (f'{self.ip}:{self.port}',))
                except NameError:
                    self.commutatorLogger.error(f'Не удалось подключиться к серверу по адресу {self.ip}')
                    raise ServerConnectionError(data = (f'{self.ip}',))

        else:
            try: response = requests.get(f'http://{self.ip}:{self.port}/{methodId}', json = {'tok': self.__token__})
            except AttributeError: response = requests.get(f'http://{self.ip}/{methodId}', json = {'tok': self.__token__})
            except:
                try:
                    self.commutatorLogger.error(f'Не удалось подключиться к серверу по адресу {self.ip}:{self.port}')
                    raise ServerConnectionError(data = (f'{self.ip}:{self.port}',))
                except NameError:
                    self.commutatorLogger.error(f'Не удалось подключиться к серверу по адресу {self.ip}')
                    raise ServerConnectionError(data = (f'{self.ip}',))


        if response.json()['responseCode'] != 200:
            #Если сервер вернул нестандартный код ответа на запрос не из-за ошибки, а для передачи какого-либо
            #состояния и т. п., то исключение, вызываемое ниже, будет обработано там, откуда был вызван метод.
            #Если это всё же ошибка, то исключение будет вызвано повторно и уже будет обрабатываться как крити-
            #ческая ошибка
            try: raise ServerResponseException(data = (f'{self.ip}:{self.port}', response.json()['responseCode']))
            except NameError: raise ServerResponseException(data = (f'{self.ip}', response.json()['responseCode']))


        if returnMode == int: return response
        elif returnMode == str: return response.text
        elif returnMode == bytes: return response.content
        elif returnMode == json:
            if 'content' in response.json().keys(): return response.json()['content']
            else: return response.json()


    def post(self, methodId: str, inputMode, returnMode, data):
        '''
        Переслать серверу HTTP-запрос POST для вызова какого-либо метода
        сервера и передачи ему какой-либо информации.

        :param 'methodId': str
            Название метода сервера, которого необходимо вызвать. Это
            должен быть POST-метод (то есть, нельзя переслать POST-запрос
            для выполнения GET-метода, и тому подобное)

        :param 'inputMode': type
            Режим обработки входящих данных перед отправкой серверу,
            задаётся типами list и json. Возможны следующие режимы:
                list —— метод не будет преобразовывать данные для отправки
                        в JSON и оставит их в чистом виде
                        (НЕ РЕКОМЕНДУЕТСЯ);
                json —— метод преобразует данные для отправки в JSON.

        :param 'returnMode': type
            Режим возврата ответа на запрос, задаётся типами int, str,
            bytes и json. Возможны следующие режимы:
                int   —— метод вернёт только статус-код HTTP;
                str   —— метод вернёт содержимое ответа в виде текста;
                bytes —— метод вернёт содержимое ответа в виде байтов;
                json  —— метод вернёт содержимое ответа в виде структу-
                         ры (списка, словаря).

        :param 'data': 
            Обязательные данные, которые нужно передать серверу при
            передаче запроса.
        '''
        try:
            if inputMode == list:
                response = requests.post(f'http://{self.ip}:{self.port}/{methodId}', data = {'tok': self.__token__, 'content': data})
            elif inputMode == json:
                response = requests.post(f'http://{self.ip}:{self.port}/{methodId}', json = {'tok': self.__token__, 'content': data})
        except AttributeError:
            if inputMode == list:
                response = requests.post(f'http://{self.ip}/{methodId}', data = data)
            elif inputMode == json:
                response = requests.post(f'http://{self.ip}/{methodId}', json = data)
        except:
            try:
                self.commutatorLogger.error(f'Не удалось подключиться к серверу по адресу {self.ip}:{self.port}')
                raise ServerConnectionError(data = (f'{self.ip}:{self.port}',))
            except NameError:
                self.commutatorLogger.error(f'Не удалось подключиться к серверу по адресу {self.ip}')
                raise ServerConnectionError(data = (f'{self.ip}',))

        if response.json():
            if response.json()['responseCode'] != 200:
                #Если сервер вернул нестандартный код ответа на запрос не из-за ошибки, а для передачи какого-либо
                #состояния и т. п., то исключение, вызываемое ниже, будет обработано там, откуда был вызван метод.
                #Если это всё же ошибка, то исключение будет вызвано повторно и уже будет обрабатываться как крити-
                #ческая ошибка
                try: raise ServerResponseException(data = (f'{self.ip}:{self.port}', response.json()['responseCode']))
                except NameError: raise ServerResponseException(data = (f'{self.ip}', response.json()['responseCode']))


        if returnMode == int: return response
        elif returnMode == str: return response.text
        elif returnMode == bytes: return response.content
        elif returnMode == json:
            if 'content' in response.json().keys(): return response.json()['content']
            else: return response.json()


    def delete(self, methodId: str, inputMode, data):
        '''
        Переслать серверу HTTP-запрос DELETE для вызова какого-либо
        метода сервера и удаления с него какой-либо информации.

        :param 'methodIdStr': str
            Название метода сервера, которого необходимо вызвать. Это
            должен быть DELETE-метод (то есть, нельзя переслать
            DELETE-запрос для выполнения POST-метода, и тому подобное)

        :param 'inputMode': type
            Режим обработки входящих данных перед отправкой серверу,
            задаётся типами list и json. Возможны следующие режимы:
                list —— метод не будет преобразовывать данные для
                        отправки в JSON и оставит их в чистом виде
                        (НЕ РЕКОМЕНДУЕТСЯ);
                json —— метод преобразует данные для отправки в JSON.

        :param 'data': 
            Обязательные данные, которые нужно передать серверу при
            передаче запроса.
        '''
        try:
            if inputMode == (list or dict):
                response = requests.delete(f'http://{self.ip}:{self.port}/{methodId}', data = {'tok': self.__token__, 'content': data})
            elif inputMode == json:
                response = requests.delete(f'http://{self.ip}:{self.port}/{methodId}', json = {'tok': self.__token__, 'content': data})
        except AttributeError:
            if inputMode == (list or dict):
                response = requests.delete(f'http://{self.ip}/{methodId}', data = {'tok': self.__token__, 'content': data})
            elif inputMode == json:
                response = requests.delete(f'http://{self.ip}/{methodId}', json = {'tok': self.__token__, 'content': data})
        except:
            try:
                self.commutatorLogger.error(f'Не удалось подключиться к серверу по адресу {self.ip}:{self.port}')
                raise ServerConnectionError(f'Не удалось подключиться к серверу по адресу {self.ip}:{self.port}', 
                                            data = (f'{self.ip}:{self.port}',))
            except NameError:
                self.commutatorLogger.error(f'Не удалось подключиться к серверу по адресу {self.ip}')
                raise ServerConnectionError(f'Не удалось подключиться к серверу по адресу {self.ip}',
                                            data = (f'{self.ip}',))

        if response: return response