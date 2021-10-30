'''
Модуль, в котором представлены мелкие функциональные классы.
'''

import json, base64, os, glob, ffmpeg, hashlib, logging, time, secrets
from colorama import Fore as Fore, Style as Style, init as initColorama
from playsound import *
initColorama()

sessionLogFilename = f'logs/{(time.strftime("""%d.%m.%Y_%H%M%S""", time.localtime()))}_AsQammLog.log'


class AqCrypto:
    '''
    Статический класс для работы с криптографией.
    '''

    @staticmethod
    def decryptContent(string: str) -> str:
        '''
        Преобразовать зашифрованную Base-64 строку в обыкновенную.

        :param 'string': str
            Зашифрованная Base-64 строка

        :returns: str
            Расшифрованная из Base-64 cтрока
        '''
        return (base64.b64decode(string.encode('utf-8'))).decode('utf-8')

    
    @staticmethod
    def encryptContent(string: str) -> str:
        '''
        Преобразовать обыкновенную строку в зашифрованную строку
        Base-64.

        :param 'string': str
            Обыкновенная cтрока для зашифровки

        :returns: str
            Зашифрованная Base-64 строка
        '''
        return (base64.b64encode(string.encode('utf-8'))).decode('utf-8')

    
    @staticmethod
    def rawContent(string: str) -> str:
        '''
        Неиспользуемый метод
        '''
        return str(r'{0}'.format(string))

    
    @staticmethod
    def getHmta() -> bytes:
        '''
        Получить случайные 32 байта и вернуть их.

        :returns: bytes
        '''
        return os.urandom(32)

    
    @staticmethod
    def getCut(string: str, byteSet: bytes) -> str:
        return (hashlib.pbkdf2_hmac('sha256', string.encode('utf-8'), byteSet, 256256).hex())


class AqTokChecker:
    '''
    Класс агента проверки токена.
    Любой вершитель, подключающийся к серверу, должен предоставлять
    определённый `токен` — крупный набор байтов — при каждом обраще-
    нии к серверу. Если токен не будет соответствовать или будет от-
    сутствовать, сервер будет игнорировать любые запросы. При этом,
    каждый ВИД вершителя должен использовать свой собственный токен.
    '''
    tok = [b'''MWVlNjMyNTMzNGY5YzA0MDMyZjgyZjc4NzFiMjhlYmZlZDgyOTUwOGI2ZjM2NmIwNmQ3OGQ3NTc0NWUxYTNhZDQ4OGY3Mzc5OTYyZjdhM2Q5NGRkMDBhZjhmOTcyNDEwMDJhYTNhY2NlYWFlMDM2YTAwNTE0NDhlNmQ5NWRhM2E5ZWYwYzAyNzlhMmExMzU2ZGY4ZDQyNWZkZmI1YWI4M2JhYmFhNGFlZDViYWQyYWJhMzA2YTNkNzQ5ZWVhYjg5OTE4ODA5NDM5NDdhODA3NTA2Y2Q1MmNmNzhkZTRmOTYxMjA4MTRiNjhkNGI3Zjc4Y2ZhZmIyMGFjNWM1YjkwMTM3NjBlOWQ4YzAwYTY2NWUyM2JmZmY3ZGYyNDIxMzhlMmE5MzgzNDBkZDM2YjY4Mzk1MjRmZTcxYzFlYmNhNzhkMjBkMjNjZGMxMmE5MmZmNDI1ZDVhMmE5YjBlNzI3ZmY4NTBlZDhkMjlmMTg2OThlNDAxNTU5NjA3NDRhMDE3NGE0ZTIzNmVjZGVhZjdjZDExZTU4OWUwNTQxNzNiODZkODU3YzQwZGY1MWI5NDNiODdjOTgxZTM0MDM1ODhiZTE1MTU3NGM0MzVlZjgzZGM5YWY4OTFmMjYxZTY2NTFjMTdmYTQzNzM2MDcyMjczOGZlMTcyODYyNzJlNDM2Yjg1NzE3NjEyNDJjNzVmY2U3NTA2OWY4MDQ5ZDVhYjY3YThhZGM3NTllOTM4MWNiNDhjODRiMDhiNWEyYmIxNDQ4MWIxMGE0MzY4MTkzZDk4YzgyOWViOWRhZDk3MDhiNGE2NjJiNjUzMmEyMWRkZjY0ODY3ODQzNGVmZmQxMDk2N2M1YTQ2OTUwN2EwOTVhMmVmMGEyNmU1ZjNiMjE0ZTMyOTU2M2FlOWFiMGZiZTVlMTUyNWZjM2M1ZjA3OTkyMDRiYjhkMTdjZTA2YTFjMGRhYzdiMWY3NDQyNzU5NjJhMzI2Y2Y5NTFiYzlhMDI4MzhkNmVlNmUwY2Q1MzA0ZTBhMDBjODQ4NjM4NGE0MDc5OTA1NmY5YWE2OWEwMzlmYzI2Y2IzNzAyZDhmZWNkN2VlNTMyMTRmM2Y3NTliMDBmNmRhNjdiYmY4YmVhMDBjYjQxZjQxNzRiYzk2MjdlMWI0NmY0MGI2MjhjMDU2NTg2N2ZkMzliYTAyODMzZDUyZWZlYmUzNDA5YmUzOGFjODY4ZjA2MzgyM2Q0NTU1OGU4N2E1YWY1NjVkODhmOGI1YmIyNjQ2MWVmMDQzNzI2NGQ4MmZlZmVjYzIzNWQ4ZTdlMWRjYTM1OTEwOWUzZmQ1YTFjZmJhNzRjMzYxYjdhY2JlY2I4NzRhOWJjYWM3OTcxNzQ2OTY3ZTg2MzIxMTZiM2YyYTVkMTZkYjI0YmI3OTY4MWVlM2EyNTUyNDcxM2FkMDgxNmU0OTIxMWZmZDUyNDE4MmFkYjY2NTI5MWZmZmIyMzMyMWFmYzI2NjVhMTUzZWRhYjZhMmFmYmVhNGJlOTE4MjdmYWM3ZDU4ZTJlMDQ0NWE0NmRlNmE4NWU1NDk1NWY0ZjYyZjVmNmJiOGY2ZDc5ODRlN2M4ZDc5OWE1MmE5ZDEzNmIwNmUyYmM2MzZlYWJkMGYwYzdkZmM0NGI2MTc4N2FkOWVmY2Q1ZDk3NDdiN2Q4NTUwMWMxMmM1NWNiMmJjZDU2YTg1MjUxOGE1ZmU1NDJkZGM1NjAyZDEwN2U5OTE2MzdiNWU3MzFiYTI2ODQwZjU1YTBjYzBhMmRkM2MwOTcyNTliNjM2OWY3OTdiNmRiZjM0ZDE0YTdiYTFhNWJkNmVmMmE0MGI0NTY0MTgxYWVkMTU0OGQ3ZGQyZDVhMmY0OWQwMjBjNTc1OWYwOTc1OGZhOTY2ZjE0OWFhMTg4ZjBiNmIxMGZkYjE2ZWY3YTQzZTY5MjE5NGFiMWYxNGNiYzIyN2VjNzUxNjI3ZGE5NzJjY2ZhOTIzOTdhMThhOTQ4Njc2Yzk5NTIyZjVhMTQwYzAxODQ2NzIwYzI2MTM0NmFlM2JlMDhkZmNmNjVmYTlhMzIzNWQ0MWFiNjI5MjY0NmE1Njk4ODJhY2IwYWI2NWY1YTY5NDVkM2MyZmFkN2M3NWQ3MTg2MzFlZGIxMWVmOWMxMjczMzM5NjA1NTcyNTIxMjU4NjhiNTUzNzE4YmMxZTI1MGFmNTEyYmE0MjVkM2Q4NTNkNmUyMjE1ZTllMDQ4ZGFlOTMxMDQ3NWEyM2FmMjdjZTI1YjY2NTRlYWE4OWRmYzU0M2RkNDczZjE5YzU2MzI3NDMwOWM3NmZhYzc3Y2U2NDk2NjdkZTZlMDRkYzRiNDQ5Y2EzYzVkODhhMTQ1MThlMmZmZWRkZGYzMTNiMjVkZDczYTZiMjcxMzZiYjAxYWIyZWZjYjA0ZGY5NGM5NDEyYzIzMTc5MDdlZTEzMGEyZDRmZDczZGNiZTAyMTRlNGJlNzMwN2QwYzEzOGFjNGUyZWQ3NjA4NTdlNTMwOTZkNDgzZGY0NzlhZTViZGVkZmI5Y2E5ZGNlZDA0NWRmZjVhYTc1OTVhMDNkYTlkZTM2MWJlM2I0YTY1MGQ3YzUyY2JlOWFmYjE0ZTkxMDRiYzQ5Mzg2MDkwZjVmOWM1OTQ0M2U3ZTkyMmU0NzE3NTVjYWQ4ZjEyNTNhZTM4MGQ2NzAwYjAwNDQyYjA0NWYxZTQ0Y2U0NDJjODNmOWY5MmM2ODJhZTNhYjgzZmFiMzIyOTVlZTBhZmZlNDA2OWQwZGNmZjVjNzRjMWMyYzkwNDJmMDJhZDdhNTU3ZTE4YmU2NDk3ZmM4NjRhYjY5MmY5NDAxZmM5NGY1MmFmMGM1YWYyNjFiMWY2ZDAyNTNkYjEzZGJjNTI0ZGFiZGY1MzEwNGFjYmIwZGYxOWQwM2I0ZjY4YTZiODNkZjgyNmUwZDE4NDRhYzlmYTE3OTlkMzUyODEwZDRmYWQ4OTM3NmM1OGNiMGI1YTY0MjNjNTM5ODRkMmI1MjcwYjU0NTgzNjVhZDA1NjVhN2ZjOGRiMzMwMDkyYmYyNmQ3OTUxMWE2ZGE3ZGZiZWYxNDNhZWMzNTlmNTBmODVkMGQxZjYwZjNlZDE1NTUxNjZkNjZhYzVmNjQyOGQ5YThhZDcyMGM4NDdjYmY0OTlmZTE3ODkzNmJiNjcxMDJmMjIwZWZhMzc5ZTMzMTIxYWIyMWZkNWIyOTk1YmRhNzM5ZTE1MmI3ZWY2OTM4MzcwZDgwMDljNTE1MDIxMmMzYzBhNTgzYWJlYjNiNzE3ODE5N2IxZTBmYTdhM2ExNTg2MjM5OTZjMWFlYTdiZWZjZjE1MTg4ZjFmYmRkMTE2MDc4MzBiYmZlYTViMTFiNjMxNmMyZDgyZDYyODY3MDA3Y2MwZTAyZjJhNjFiNTY3NzRlMWM1NzI4YmZlMzlmZjgyMDEwYzhmZmFiMTJiNzhkYmQ5YzczMjJlMzc0NThmMGExYjE5Yjg2NDJhOWU5MWVmMmIzYzI0MzE1YTA4YzRjOTc1NzlmMGI1NDdjYTU3OTdkNTcyM2QyMjQ1Yjk1MmRmZjJiNmEyNGI0NDNhZTQ1ZGU0NmQzNDgzNmU1NTgxYWEyYmFmODBhZGFiOTc5YzM4ZGUwNmNjMGI5NGE1ZjFjMWZjNDMzYmVmNjY2MWVlZGZkMTJhNDdlM2FmN2Q1MTI4M2Y5MzZhYjhjNTZjMzg3NDUzODIyOWQ3MjAxZmU5OTU0YWNiMGJjMzZlZGU0ZjUwNDRkODgyMmMyYmQ4MWY0ZGE4ZmI3NjUxOGZiNTBiNGUwNTA3NmE0ZTJjOTFjZDJkNmY1NGI4YjYzNzA3ZWI3ZWViYWQ4NTdlOWRjYTU1NTMyNjE4MTc4N2NkNmQ2NDg1N2UwNTFjMzY2MThmNmZkZWFlMGZjNDMyMjk3N2FiZmI5NGQwMDNlZTNhYzUyNDk0YTFhOThlYzVjZjA2N2Y1ZjlhNWExMTdkZTZjODJkOGUyYzNmNWI5MjhhOGRjNDE2NmM5NjNhMWVkNTA5NjhkMmMwZGM1YjcxNWEzMzBjNTI1OTE3YmQ5YzdhNmQ4Nzk3MWI4ZmI5MmRmMTliNjkxMjRiNGY1Mzg4YjI2ODQyMzJkYjc2ZTA1MjZkZTBhODZmMDc2OWU0YzYwZGI4MTM3MGRlMTA4YjMyMjQ2NjYxODk0MjhmY2I1ZTY0NWIzNjE0M2NkZGQyYTUyODZlYjk1ZTdkNjNhMTU5OTE4NmFkYjY3ZDhiYzcyNWExNDY0MThlZmY2ZTFmOWJkOTNlM2Y0NTUwYjA1NGIzYTQ5Mjg0MzBmNDYxOGNiZTlkMDRkM2RkMDg0YzYxM2E4NzFiOThiNmM1YWE4MTIwZWVmMDUzNzI0M2JhNWE3YWI4NzZhOGEyMWViMDc1ZjdhMDY5YjRhM2EyODFjMWRiYTg2MjliMjU3Y2YwNDM1MWI2OTY3OTExY2E0ZDZiYjdhMGYzOWY2Y2M1OWRmOTAxODFjMWE4MTdjZmFjZmQ3NjVhMjM1NzM2MTdmYWM4YzhhZWNiZDYyY2Q5ZjU5ZGM3OGY3NzI5MTk5N2IzY2ZiN2U0ZjJhOWMzZGQzMDY4Y2JmNmNhZjdlZTlkYmI0MDdlMzJiNjhlZjBiMzk3YzVhMmJjYjExNDAyYWNmZDg5OTUyNDYwZWRiMDg1OGFmNzBkMmE3MjU3MDdiYmE2ZDJjMDliZTM2MTU2MmUwZWU0NDkzZGFmMWQ5YzM2YTg4ZjlkOWY2ZjJiMTdkOTBhZDYwOGJhNjk3ZWU1MThhNjFmZmRlZTNlMWUyOWQzNmU5OThjMjk4Y2U2ZDAwYTU4ZGM0YmI0ZDdmYTE4N2RiOTQ1ZTE2MDExMTQ5NTgyMDM3YWYzMzI3M2Q2MTk4NTdjNjFlNTk3ZGU1YmM1ZjYzYWQ3YTM5ZTNiNDc1MTEyYzhjNDYwMGVlZWQ3OWVkMTkyNWQ3YTFkNDUzOTFhNDZkYTI5MGJlNDg1ZTQwNjNjZTRjMTkyY2ZmNmRhNzhkZDM1Njg4YTc0MjNjZDhkOWYxNzk0ODRmZTljYzVlM2E3NmNkY2RmNTkyODY3OGNmMjgzYjk0MDE4Njg0M2VlYmI1NTQxMjZkOGI1NThlMmQ3ZTM4NTE2MTBhNzE5ZGIwNTExMTljNTAxMzJkNGM3YTBmMGIxZjZmMThjNjAzZjZlZTIzMzFhZWQyMWU4NzUzZjI3YzgzMmExNzI5NjVkZGM3MzFmZDM4OGY5OTZmMmVlMGUxZWJmZDZkMWU2Nzk3MDg2ZmY2Njk2YjZlZjQ1ZWFiZTllNGFhMjZhZjU4Zg==''',
           b'''OGJhMDAzNTQxZDc0MjZjYTM1MTFlZjFlZDBhZTliYjc2ZjQ2ODA3YzI0N2E1OGNiMzY0NzI0ZmJiMGYyYTY0YWFlODI3NmIyMTM3ZmI5NjBiODM5ZDVhYjFlOTYxNDJkYWRkYmY5ZDI1ZWNkNTc5YWQ2OGI5MGUyZGQwODQ0ZTJmNzYxOWY3NzQwODE1ZWQwYjgwYzMyYWI4OWQxNDZkZjgxNDlhNzFjMWFjZjk1NDVmNTE4NTQwODFhYTQ4NWNiMzI4ZDMyZTUxNTI2Nzg1NGUwYTE5ZDYzYTc4MzgxN2IyMTQxMWE0ODY0ZWRjOGVjMWMxNTgyMjBmNTdlZTk5Y2ExN2JkYjE1Njc4ZWVkMDk4MWQ1NmI5MDQ1NGQxY2JiY2JmYTU1ZTgxOGFhMDkzZTUxYzQ2ZmZkMDczNDg4ZjdjNGIxZDY5YWUxZTM4YmM5NDFlMzMwOTE1MmNkMTQ4NWMzZDI5MzVmMDA4NzAwZGJiZmI5NjI0MmQ5Njk3NDdmZThhMWY3M2ZmZjVkOWM5ZTA3ZWQ2Y2I5N2U4OWY2ZmJhZjdjMDIyYWVkMmFiYzIwNTE5MGYwYzFkNTE3YWRkNTMzNjNhODFiNWQ3MDBiYWE3NWE4MWYzZjk0ZDQ1M2YwNDE1MWQ4NzVlZjc4OWEyZjcyNWZlOGI3MTdjOGY2NTk4NTEwNzAxYjE3NTM4YjFkMWVlOWYxYmVhODRlMTA4YmM1ZjgxODAwNWI0M2FlZTNmZmEwZTNhMDU3MTYyZjk1MGUwNzZlZDY0MTg3ZjBhOTY3ZTU0ODA1ZTExOGNkMjc0NGRmZDYxNTllNWVmMzc5OGYxYzA1OGI3YjZjZGM1M2ZkYTYwNzE4YWJkMDcwMDAwYTA0YzBlNjMyM2QxNTEwNmJlYmI5OTI0MWQxNjM3ZjY2YzgxOWUyNWI5ODZlMTJjMDhlODIwODQ2Njk0YjdhNzFmZDE3Nzk0YTAwZTgxYTM4YzNhM2FjYjE5NWUxOGY0OWRhYmYyMjk3ZjM5Y2RlYjgyZTdlOGZhYzI0NWQ1ZjhhNTI2NmIyZjAzZGFjZDNmMWY1ZDlkNjE1M2Y2ZWMwZGQ4MWY4MzQ5YzRhZjFhNGNiZTgzYTVkYWE1NzgyMjYwYTA0NWM3MDliNjA4Nzk5ODhkNzYzNjM4OGE5MzQwNmQ4ZmIwMzc1ODAzNDcwODc3MzI0MTNkODRhNTJiYTBiMjE0MTAxNjgwNDNlYjJkZTgxMTk0YTBlMWUyZWJhOTI0NGNlMjdkOGFmMjUxMzQxMDE3M2I2NmMzZmQxNjcyNzU2NGE4Zjc1MDE2YjFiNjBlNTA0NjA2NjVjM2UzY2ViZDUwZTU2ZTU1YTE5NmE2ZGU4OWIyMDBmODJiZTIwMWViMGZkNjFkNWRhMjc2MDI1NmM3MTA3MmM2Y2YxNDczMzUxNDRmMjE5MzdlMmRkYzJkMjUxNWFiN2NiYjNiZTkwNDk5MDhiOTAzOTNjYmY5MzYzOWVkY2UzYTFjMWY3MjU5NjQ0ZmM4NDFmZjY0YzFkMzczMDcwMDhiMTIzYTYxN2E2Yjg4OWIyMjM3NGU4NTZjYjkzYjA0ZDI4ZDUzYWUxNjRiYTNkODcxNjA5OWU5NDJjZmFkYzgxYWQ1ODA1YTgwODNhZjViN2Q3MzFlNGJlMjZkZTMzMzIwN2UyYmU2MzFiYzkxMzE2ZDg4ZjE4OTBlZThkMzA1NjNmMjU5YjdiZmQwYTYwZTEzNWFlZDc1NGU0OWVhMmJjMTE2ZjNiOWFjZDc5M2I5NDdiNTM0NjkxYTEyNWY3MWVjNzYzYTBlOGFkZDA4ZGFkZmM0N2ZiM2VkNTczYzc2MTU0YTdmM2M0NzA2MjYxMTI1MzRhYzRlYWVmM2VkMGEzYTViYjBiNjgyY2VkNDhkNTJmYzg1N2JlYzZjZmY4OWM3OTQ1YjE2MTQ2MDlhM2NlYTNkNGJjY2MxNTVjMTJlNmM1MWE2YjQ2MzY2OTZlYTcxYjZkMmQxZDdiMTFlMDY1MjFlZmFlYTUyMzkyNzNhOTY0NDI4Y2ZlZGJhZjE2YmM2YTFlZTZhNjYwNDM3Y2M2ZDVjMzAyY2I0ZmVmZmY2ZWY3YWIwNjZlNzg4ZjZkMjQ5OTM1NjcwYmQ1YWViY2QyOGQxZWMyYmEzNDJlYTgyZGJmN2YwZmNhNjA2Yjk5NTUxMzE2OGNkNWE5NmE1OGQ3MTJhMzdjNjQ5ZTg3YTExMzc4YjBhNGEyMGQ2NWM3ZmE3NmNjMjQ4ZDQ4ZDgzNjg1MTk3MDM0ZWMzYzBhZDExZTJmYjVjYzNmYzcyMjI4ZWU0ZWY5ZGFmNGJiOGUxYjZjODQzNjRiYzdmYWNmMGNkYjUzNjE5YzlkN2E3ZDcyNDc0NjEwZmFkN2Y2MjlkYTIxMWJlNWNjYjA4NjVlZjY1ZDY4ZWM4ZTUxYjQxNjMzNDUxODA3NDRiYTY3OGQwNDQyNzdlMzEyYTI1OWI4OWYyYTc5MWEwM2FjZTkxOTc3ZjljMWY4YWMyN2Q2ZDcxNWUxYzNiNWU1MDFmODQ1ZTY0ZTNiMmMxMTBkNzkwZTFlYjExYWI0MmVmMzE0NTYxZjkxM2RjNzcxOTMzNGJjNzkyMmEwNGM1OGZmMTc2Njk5MWQ2NjE0ZjI2ZDkwMDIzODM1YWZlOTRiMWU2YjYwNWY0NzJjZDFkZTNlY2E2MTA2YTg4ZjY4ODcxNWVjMDZhN2QwNTA2NjZhODczMGJhNWM0Y2FlODkzOTcyZDc4NDcxZjM5MDI3OTJhYjZkZWU1NDFiYjJlMThmODhhOWU1NmI5MjYyOGI2NDNlMmFlMWQzNGVkMzdhNzBlYWM0NTM3ZDFmNzA2NjVmYjk2OTgzZWFlMWQ2N2NmMjNhNTllYWZmZTI1MjA2ZjRlZjNhY2QyMjk4Njg5NjAxOTQ0MDMyYzVhYTUxZDFmN2E3MTA0MjQyZGZmNDk3ODliZjE3MmE4Nzc0OTQ0YTY0ZGE2YjEwNmE2MzFiYzBhZDYwNDIzOTlmMGFlMTUzMjM0NWM5OTM3Yzc3YWZlYjE1MTUwZDc0N2IwM2RjY2Q4ZDBlYjNkMGZiMDk0Njc2MWZjOTJjODI3MGVjYmJlZmVhY2NhODJhYjE2M2Y2MzY3YzViY2RjYzAxOThkYmUwYmE2M2Q2MTA2YmEzMDM2ZjA3NTU3YzhhODk0MDY0ZWJlOTMzODA4ZWRjMmE4NTQ4Yzg3YWMyZjQ4ZTZkMGQ4Mzk0NTQ5YTU3ZjkxMzlmNjYyMWY3MDcwNTFjZTk2MDBkNGY0NjBiMDljN2UwNTQ0YWNkMmI2ZTE0NmIzYjE3NWY1NjhmMDUyOWU0ZTEyMmM2ODkwN2NlNzhjODY4OTVlZGNhMzhhYWMzY2M0NjE2MzA2NmZjZTU3ZjI4NDg5ZTEzZTQyZWE1ZjM3MTRmYjk1YzE4ZDA0YmUzZjM5NTlkZWNjMmIzMGFjZjM3ZmQ3NjgwMWM2Y2M3YjBmNDBkZWQ3MWZmOGQ3N2ZkMGI0MmQwM2ZmODFmOWYyNTZmY2E3M2ZlMTMyOTdhY2YyMTk2MWE5ZjRjN2U5Njk5OTZlNjVmMDBiOGZmOGQ1MmFjMjQ0ZGQxYmIwMTdlYzZjMDdhMTFlMDMxY2EyZTMxYTEzNDgwMGIwODAxYjU2NmUwMzY1MWE3NTM5MzhlZTI2NDg2MTdkNTczOThmZTgzYTQ0NmNlYWM4ZDAyYzAyNDc0MTdjMzAyYjUwMjM0NTU4ZTYxMDJhYzFhNGM1OGFmMTIyYWYzMjU3ODIzMDRjZTg1YWYwMzA2Y2Y5OWI0NDQxODgyZDU1NzQxOGNmYzVkNThjZjQwYzQ0MmE1NjBjZTlmMWY1OThhMzBmY2FkMzc0OWI2YTZlMGQxZWU1ZTQzOGE1N2MzYzE2MDhhNjljN2M2NDk1MjZmZWQ0NWE0YzIwNTFiMTk3ZjQ3YjZlZDViZGQ3YWQzN2RmNjgxMDkyYTEzNzAwMWFkNWY2NmNkNGQ1NzljZGE5OTk3MTZhYTM0ZmM2NTM1Mjg2NWFhYWM0ODkxNzA1ZTM0ZDJjM2I4ZTg4ZmJkM2Y0ZmY5ZjlhNDBlZjc0OTc1NjkwZmE1YzI1ZDQ0YWY4OThiM2Q0MDdmNTE2Yzk3YTFlNjRiNTI0YTI3MjhiNzdlNzM1NzNiOTY2MmFlYjRjYzU5MzE2ZjgxZmU3YzZmMTA2ZWUzZjhlZTc0MDNiYTdhMWIzNGQzNDEwMjdhNDBiNjlhNTJhMWY5ZTQ4NzBmZjVjMjJjNzk2M2ViNjc2MTZhZWMwMmFlZGZkODBlODRjZTNmMjJjMjI3ZjA4NGMwMjc0YTNlNmIwZTc2ZDQyZTYwNjc3OTc2ZmQzMDU0NmZmOWFlNWE2MTQ4NjM0ZDNiNWM0ODU4ZWI0NjA3MDhkOTUwZThhZGJmMjRmMWEzNGE4ZGM5NmU2YjM1YmY2MDNjODE2NDk5YzZjOTRiNTM3YjY1NDkyOGIzMDM5Y2U4MWQ4MjZkYjY1YzEzNmNiZGYzYjI2ZjNjNWQ5Mjc3ZGM0ZTBkYTkxMWNlZTc2NzFkYTlkY2MxNTc2ZWJhZDZkYjkxODUzNDVhY2U2MWU0NWVhNDE4ZjcyNGU5N2YzZDcyMTQ5OTNiMzIzMTEzYzBlODE1ZGQ0NmNmNDYzNmFiNzI2ZjNhYzlmZTllOWY2N2U2Y2NiZDgwNmJjZDUxZWJiYWMzYjljMzRiOWIwNTFiMGU5NDVhYTMyMjhlMzAzOGQ3OTVjMjA0ZTAxZTRmNjlmZjU3ZTFlMzdkMzZiYjliMTMyMjkzOGI0MmZkYTFmNmRlMDAxMmZiYTZkZTVlMDRlNGVkZjBjYWRmMWY1MzEzYjUyNTIyMDNiMmYyYmY5MWU1NzlmODY4NjM4ZDZkOWY0NDYzODk3YzhkNmVjYTUxYjRjNmQ3MzYyMmMxNGU5ZTFjZWRhZjQ4YTVlYTE5YWE4MWVhNzJiZDAzYzEyNTdkOTI2NTM3MTU1NTExNzE0M2U0MWExNzIyYzA1NWY4N2Q5YjkwNGZhNGQ3MjRmNWNjMzEzM2U1YWE1NTcyOWE0MTc5NGI1OTM2OTU5YmY2ZGE3NGQ5ODhmYzUwMjc4YjhhMTA4YThkNjYwN2UzZTU1MzYxNGUyMDdlMzg0YjU2YzRlOTdhZDQ3MDQzMTVhNzViMTM0MDhkZDE4MWRiYzkwNjc3OTk3ZDJkMTQ1ZjdhMTYyMzgyY2I5NWUwYWQ2NjJmMzkwOWFiMDYwNjc3Y2VmZjQ1NDdiZjUxYzdkY2UzMmMyZDJmMDRiMTBhMDAxMWNlNjQ4NA==''']


    def isOk(self, tok: str) -> bool:
        '''
        Проверить полученный токен на действительность.

        :param 'tok': str
            Полученный токен

        :returns: bool
        '''
        return bytes(AqCrypto.encryptContent(tok), 'utf-8') in self.tok


class AqLogger:
    '''
    Класс канала журналирования.

    Журналирование необходимо для отборажения пользователю информацию о 
    текущих действиях сервера, сообщения о предупреждениях и об ошибках.

    Каналов журналирования (или `логгеров`) может быть сколько угодно.
    При этом итоговый журнал всегда сохраняется в ОДИН файл, имя которого
    определяется при запуске самого ПЕРВОГО канала журналирования.
    Каждый из этих каналов имеет своё имя и настраивается по уровню жур-
    налирования (насколько важные сообщения нужно выводить в консоль и
    сохранять в журнал?).

    Любые файлы журналов сохраняются в папке
    '{папка местонаждения программы}/logs'.
    '''
    class LogLevel:
        'Объект для представления в коде уровня журналирования'
        def __init__(self, lm: int):
            self._level = lm


        def __repr__(self):
            repr(self._level)


        def __eq__(self, other):
            if not hasattr(other, '_level'):
                return self._level == other
            else: return self._level == other._level


        def __gt__(self, other):
            if not hasattr(other, '_level'):
                return self._level > other
            else: return self._level > other._level


        def __lt__(self, other):
            if not hasattr(other, '_level'):
                return self._level < other
            else: return self._level < other._level


        def __ge__(self, other):
            if not hasattr(other, '_level'):
                return self._level >= other
            else: return self._level >= other._level


        def __le__(self, other):
            if not hasattr(other, '_level'):
                return self._level <= other
            else: return self._level <= other._level


    #Возможные уровни журналирования:
    DEBUG = LogLevel(logging.DEBUG)       #Уровень ОТЛАДКА (все сообщения, по умолчанию)
    INFO = LogLevel(logging.INFO)         #Уровень ИНФОРМАЦИЯ (важные сообщения)

    WARNING = LogLevel(logging.WARNING)   #Уровень ПРЕДУПРЕЖДЕНИЯ (сообщения важностью
                                          #ПРЕДУПРЕЖДЕНИЕ и выше)

    ERROR = LogLevel(logging.ERROR)       #Уровень ОШИБКИ (только сообщения об ошибках и
                                          #критические сообщения)

    CRITICAL = LogLevel(logging.CRITICAL) #Уровень ТОЛЬКО КРИТИЧЕСКИЕ (только критические
                                          #сообщения)


    def __init__(self, name: str, logLevel: LogLevel = DEBUG,
                                  disableStdPrint: bool = False,
                                  useColorama: (0, 1, 2) = 1):
        '''
        Инициализировать один канал журналирования.

        :param 'name': str
            Имя канала журналирования

        :param 'logLevel': AqLogger.LogLevel = DEBUG
            Необходимый уровень журналирования.

            Возможные уровни журналирования:
             —— DEBUG (все сообщения, по умолчанию);
             —— INFO (важные сообщения);
             —— WARNING (сообщения важностью 
                ПРЕДУПРЕЖДЕНИЕ и выше);
             —— ERROR (только сообщения об ошибках и
                критические сообщения);
             —— CRITICAL (только критические сообщения)

        :param 'disableStdPrint': bool = False
            По умолчанию, сообщения журнала выводятся в консоль.
            Если этот параметр ложен, то вывод в консоль не будет
            производиться

        :param 'useColorama': int = 1
            Использовать ли цветной текст Colorama, и если да, то
            как. Имеются следующие варианты:
            0 —— отключить использование цветного текста;
            1 —— использовать цветной текст для вывода
                 сообщений в консоль;
            2 —— использовать цветной текст для вывода
                 сообщений в консоль и для файла журнала
        '''
        self.name, self.logLevel, self.printDsb, self.useColorama = name, logLevel, disableStdPrint, useColorama
        self.filenames = list()

        self.Logger = logging.getLogger(name)
        self.formatString = ''
        self.getFilename()
        
        self.Logger.setLevel(self.logLevel._level)

        self.handler = logging.FileHandler(rf'{self.filenames[0]}', 'a+', 'utf-8')
        self.Logger.addHandler(self.handler)


    def setLogLevel(self, logLevel: LogLevel):
        '''
        Установить уровень журналирования.

        :param 'logLevel': AqLogger.LogLevel
            Необходимый уровень журналирования.

            Возможные уровни журналирования:
             —— DEBUG (все сообщения, по умолчанию);
             —— INFO (важные сообщения);
             —— WARNING (сообщения важностью 
                ПРЕДУПРЕЖДЕНИЕ и выше);
             —— ERROR (только сообщения об ошибках и
                критические сообщения);
             —— CRITICAL (только критические сообщения)

        :returns: None
        '''
        self.logLevel = logLevel
        self.Logger.setLevel(logLevel._level)


    def getFilename(self):
        '''
        Сгенерировать имя файла для сохранения лога и сохранить его в список
        'self.filenames'. Метод вызывается при инициализации канала журнали-
        рования, но при этом для сохранения логов всегда используется файл с
        именем, которое было получено при инициализации ПЕРВОГО по счёту
        канала.

        :returns: None
        '''
        self.filenames.append(f'logs/{(time.strftime("""%d.%m.%Y_%H%M%S""", time.localtime()))}_AsQammLog.log')


    def debug(self, message: str):
        '''
        Опубликовать сообщение с уровнем DEBUG (ОТЛАДКА).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        callerInfo = self.Logger.findCaller(stacklevel = 1)
        fileName = callerInfo[0]
        lineNo = str(callerInfo[1])
        moduleName = ('UNKNOWN' if callerInfo[0] == '(unknown file)' else callerInfo[0][:callerInfo[0].index('.')])
        funcName = callerInfo[2]

        if self.useColorama <= 1 and self.logLevel == self.DEBUG:
            self.formatString = ('{%(asctime)s} [%(name)s:%(levelname)s] '
                                 f'[{fileName} <{lineNo}>: {moduleName}.{funcName}]: '
                                 '%(message)s')
        elif self.useColorama <= 1 and self.logLevel >= self.INFO:
            self.formatString = '{%(asctime)s} [%(name)s:%(levelname)s] %(message)s'

        elif self.useColorama == 2 and self.logLevel == self.DEBUG:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   fileName         + str(Style.RESET_ALL) + ' <'  +
                                 str(Fore.WHITE)  +   lineNo           + str(Style.RESET_ALL) + '>: ' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   +
                                                      funcName         + ': %(message)s')

        elif self.useColorama == 2 and self.logLevel >= self.INFO:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   + 
                                                      funcName + ': %(message)s')
        self.handler.setFormatter(logging.Formatter(self.formatString))

        self.Logger.debug(message, stacklevel = 7)
        if self.logLevel == self.DEBUG and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}DEBUG{Style.RESET_ALL}]: {message}')
        

    def info(self, message: str):
        '''
        Опубликовать сообщение с уровнем INFO (ИНФОРМАЦИЯ).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        callerInfo = self.Logger.findCaller()
        fileName = callerInfo[0]
        lineNo = str(callerInfo[1])
        moduleName = ('UNKNOWN' if callerInfo[0] == '(unknown file)' else callerInfo[0][:callerInfo[0].index('.')])
        funcName = callerInfo[2]

        if self.useColorama <= 1 and self.logLevel == self.DEBUG:
            self.formatString = ('{%(asctime)s} [%(name)s:%(levelname)s] '
                                 f'[{fileName} <{lineNo}>: {moduleName}.{funcName}]: '
                                 '%(message)s')
        elif self.useColorama <= 1 and self.logLevel >= self.INFO:
            self.formatString = '{%(asctime)s} [%(name)s:%(levelname)s] %(message)s'

        elif self.useColorama == 2 and self.logLevel == self.DEBUG:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   fileName         + str(Style.RESET_ALL) + ' <'  +
                                 str(Fore.WHITE)  +   lineNo           + str(Style.RESET_ALL) + '>: ' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   +
                                                      funcName         + ': %(message)s')

        elif self.useColorama == 2 and self.logLevel >= self.INFO:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   + 
                                                      funcName + ': %(message)s')
        self.handler.setFormatter(logging.Formatter(self.formatString))

        self.Logger.info(message)
        if self.logLevel <= self.INFO and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}INFO{Style.RESET_ALL}]: {message}')


    def warning(self, message: str):
        '''
        Опубликовать сообщение с уровнем WARNING (ПРЕДУПРЕЖДЕНИE).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        callerInfo = self.Logger.findCaller()
        fileName = callerInfo[0]
        lineNo = str(callerInfo[1])
        moduleName = ('UNKNOWN' if callerInfo[0] == '(unknown file)' else callerInfo[0][:callerInfo[0].index('.')])
        funcName = callerInfo[2]

        if self.useColorama <= 1 and self.logLevel == self.DEBUG:
            self.formatString = ('{%(asctime)s} [%(name)s:%(levelname)s] '
                                 f'[{fileName} <{lineNo}>: {moduleName}.{funcName}]: '
                                 '%(message)s')
        elif self.useColorama <= 1 and self.logLevel >= self.INFO:
            self.formatString = '{%(asctime)s} [%(name)s:%(levelname)s] %(message)s'

        elif self.useColorama == 2 and self.logLevel == self.DEBUG:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   fileName         + str(Style.RESET_ALL) + ' <'  +
                                 str(Fore.WHITE)  +   lineNo           + str(Style.RESET_ALL) + '>: ' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   +
                                                      funcName         + ': %(message)s')

        elif self.useColorama == 2 and self.logLevel >= self.INFO:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   + 
                                                      funcName + ': %(message)s')
        self.handler.setFormatter(logging.Formatter(self.formatString))

        self.Logger.warning(message)
        if self.logLevel <= self.WARNING and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}WARN{Style.RESET_ALL}]: {message}')


    def error(self, message: str):
        '''
        Опубликовать сообщение с уровнем ERROR (ОШИБКА).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        callerInfo = self.Logger.findCaller()
        fileName = callerInfo[0]
        lineNo = str(callerInfo[1])
        moduleName = ('UNKNOWN' if callerInfo[0] == '(unknown file)' else callerInfo[0][:callerInfo[0].index('.')])
        funcName = callerInfo[2]

        if self.useColorama <= 1 and self.logLevel == self.DEBUG:
            self.formatString = ('{%(asctime)s} [%(name)s:%(levelname)s] '
                                 f'[{fileName} <{lineNo}>: {moduleName}.{funcName}]: '
                                 '%(message)s')
        elif self.useColorama <= 1 and self.logLevel >= self.INFO:
            self.formatString = '{%(asctime)s} [%(name)s:%(levelname)s] %(message)s'

        elif self.useColorama == 2 and self.logLevel == self.DEBUG:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   fileName         + str(Style.RESET_ALL) + ' <'  +
                                 str(Fore.WHITE)  +   lineNo           + str(Style.RESET_ALL) + '>: ' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   +
                                                      funcName         + ': %(message)s')

        elif self.useColorama == 2 and self.logLevel >= self.INFO:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   + 
                                                      funcName + ': %(message)s')
        self.handler.setFormatter(logging.Formatter(self.formatString))

        self.Logger.error(message)
        if self.logLevel <= self.ERROR and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}ERROR{Style.RESET_ALL}]: {message}')


    def critical(self, message: str):
        '''
        Опубликовать сообщение с уровнем CRITICAL (КРИТИЧЕСКИЙ).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        callerInfo = self.Logger.findCaller()
        fileName = callerInfo[0]
        lineNo = str(callerInfo[1])
        moduleName = ('UNKNOWN' if callerInfo[0] == '(unknown file)' else callerInfo[0][:callerInfo[0].index('.')])
        funcName = callerInfo[2]

        if self.useColorama <= 1 and self.logLevel == self.DEBUG:
            self.formatString = ('{%(asctime)s} [%(name)s:%(levelname)s] '
                                 f'[{fileName} <{lineNo}>: {moduleName}.{funcName}]: '
                                 '%(message)s')
        elif self.useColorama <= 1 and self.logLevel >= self.INFO:
            self.formatString = '{%(asctime)s} [%(name)s:%(levelname)s] %(message)s'

        elif self.useColorama == 2 and self.logLevel == self.DEBUG:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   fileName         + str(Style.RESET_ALL) + ' <'  +
                                 str(Fore.WHITE)  +   lineNo           + str(Style.RESET_ALL) + '>: ' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   +
                                                      funcName         + ': %(message)s')

        elif self.useColorama == 2 and self.logLevel >= self.INFO:
            self.formatString = (str(Fore.CYAN)   +  '{%(asctime)s} [' + str(Style.RESET_ALL) +
                                 str(Fore.GREEN)  +   '%(name)s'       + str(Style.RESET_ALL) + ':'   +
                                 str(Fore.YELLOW) +   '%(levelname)s'  + str(Style.RESET_ALL) + '] [' +
                                 str(Fore.BLUE)   +   moduleName       + str(Style.RESET_ALL) + '.'   + 
                                                      funcName + ': %(message)s')
        self.handler.setFormatter(logging.Formatter(self.formatString))
        
        self.Logger.critical(message)
        if self.logLevel <= self.CRITICAL and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}CRITICAL{Style.RESET_ALL}]: {message}')


    def critical(self, message: str):
        '''
        Опубликовать сообщение с уровнем CRITICAL (КРИТИЧЕСКИЙ).

        :param 'message': str
            Текст сообщения

        :returns: None
        '''
        self.Logger.critical(message)
        if self.logLevel <= self.CRITICAL and not self.printDsb:
            print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}CRITICAL{Style.RESET_ALL}]: {message}')


    def exception(self, _exception: Exception):
        '''
        Опубликовать сообщение о возникновении исключения

        :param '_exception': Exception
            Объект исключения.

        :returns: None
        '''
        print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}CRITICAL{Style.RESET_ALL}]: '
              f'Программа аварийно завершила работу из-за исклоючения {type(exception)}:')
        self.Logger.exception(f'Программа аварийно завершила работу из-за исклоючения {type(exception)}:',
                                exc_info = _exception)


    def openLogFolder():
        '''
        Открыть папку с файлами журналов.

        :returns: None
        '''
        os.system('explorer %cd%\logs')
