class ServerConnectionError(Exception):
    def __init__(self, msg: str, data: tuple):
        self.data = data
        super().__init__(msg)
