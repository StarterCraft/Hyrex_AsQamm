class ServerConnectionError(Exception):
    '''
    Исключение вызывается, когда произошёл провал
    подключения клиента к серверу
    '''
    def __init__(self, data: tuple, msg: str = ''):
        if not msg: msg = f'Не удалось подключиться к серверу по адресу {data[0]}'
        self.data = data
        super().__init__(msg)


class ServerResponseException(Exception):
    '''
    Исключение вызывается, когда сервер в ответ на
    запрос от клиента переслал сообщение об ошибке
    '''
    def __init__(self, data: tuple, msg: str = ''):
        if not msg: msg = f'Сервер по адресу {data[0]} вернул код {data[1]} в ответ на запрос'
        self.data = data
        super().__init__(msg)