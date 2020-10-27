import json, base64, os, glob, ffmpeg, hashlib, logging, time, secrets
from colorama import Fore as Fore, Style as Style, init as initColorama
from playsound import *
initColorama()


class AqCrypto:
    def __init__(self):
        self.cryptoLogger = AqLogger('Crypto')

    def getFileNamesList(self, exportList):

        for i in range(10, 99):
            self.initialFilename = str(r'customuser_' + str(r'{0}').format(i))
            self.initialFilename = self.initialFilename.encode('utf-8')
            self.initialFilename = base64.b64encode(self.initialFilename)
            self.initialFilename = self.initialFilename.decode('utf-8')
            self.initialFilename = self.initialFilename[0:-2]
            self.initialFilename = self.initialFilename.encode('utf-8')
            
            exportList.append(self.initialFilename)


    def seekForFiles(self, importList, exportList, flag):

        for item in importList:
                self.gotName = glob.glob(str(r'data/personal/~!{0}!~.asqd'.format(str(item.decode('utf-8')))))

                if flag:
                    if self.gotName == []:
                        continue
                    else:
                        exportList.append(r'{0}'.format(self.gotName[0]))

                else:
                    if self.gotName != []:
                        continue
                    else:
                        exportList.append(r'data/personal/~!{0}!~.asqd'.format(str(item.decode('utf-8'))))


    def decryptContent(self, s):
        return (base64.b64decode(s.encode('utf-8'))).decode('utf-8')


    def encryptContent(self, s):
        return (base64.b64encode(s.encode('utf-8'))).decode('utf-8')


    def getHmta(self):
        return os.urandom(32)


    def getCut(self, _str, bytes):
        return (hashlib.pbkdf2_hmac('sha256', _str.encode('utf-8'), bytes, 256256).hex())


    def createInstanceToken(self):
        __sig__ = secrets.token_urlsafe(128)
        with open('data/ffd32.bin', 'rb+') as dataFile:
            fileByteString = dataFile.readline()
            fileString = fileByteString.decode('ascii')
            jsonObject = json.loads(fileString)
            jsonObject.append(str(__sig__))
        return __sig__


class AqTokChecker:
    def __init__(self):
        self.tok = [b'''MWVlNjMyNTMzNGY5YzA0MDMyZjgyZjc4NzFiMjhlYmZlZDgyOTUwOGI2ZjM2NmIwNmQ3OGQ3NTc0NWUxYTNhZDQ4OGY3Mzc5OTYyZjdhM2Q5NGRkMDBhZjhmOTcyNDEwMDJhYTNhY2NlYWFlMDM2YTAwNTE0NDhlNmQ5NWRhM2E5ZWYwYzAyNzlhMmExMzU2ZGY4ZDQyNWZkZmI1YWI4M2JhYmFhNGFlZDViYWQyYWJhMzA2YTNkNzQ5ZWVhYjg5OTE4ODA5NDM5NDdhODA3NTA2Y2Q1MmNmNzhkZTRmOTYxMjA4MTRiNjhkNGI3Zjc4Y2ZhZmIyMGFjNWM1YjkwMTM3NjBlOWQ4YzAwYTY2NWUyM2JmZmY3ZGYyNDIxMzhlMmE5MzgzNDBkZDM2YjY4Mzk1MjRmZTcxYzFlYmNhNzhkMjBkMjNjZGMxMmE5MmZmNDI1ZDVhMmE5YjBlNzI3ZmY4NTBlZDhkMjlmMTg2OThlNDAxNTU5NjA3NDRhMDE3NGE0ZTIzNmVjZGVhZjdjZDExZTU4OWUwNTQxNzNiODZkODU3YzQwZGY1MWI5NDNiODdjOTgxZTM0MDM1ODhiZTE1MTU3NGM0MzVlZjgzZGM5YWY4OTFmMjYxZTY2NTFjMTdmYTQzNzM2MDcyMjczOGZlMTcyODYyNzJlNDM2Yjg1NzE3NjEyNDJjNzVmY2U3NTA2OWY4MDQ5ZDVhYjY3YThhZGM3NTllOTM4MWNiNDhjODRiMDhiNWEyYmIxNDQ4MWIxMGE0MzY4MTkzZDk4YzgyOWViOWRhZDk3MDhiNGE2NjJiNjUzMmEyMWRkZjY0ODY3ODQzNGVmZmQxMDk2N2M1YTQ2OTUwN2EwOTVhMmVmMGEyNmU1ZjNiMjE0ZTMyOTU2M2FlOWFiMGZiZTVlMTUyNWZjM2M1ZjA3OTkyMDRiYjhkMTdjZTA2YTFjMGRhYzdiMWY3NDQyNzU5NjJhMzI2Y2Y5NTFiYzlhMDI4MzhkNmVlNmUwY2Q1MzA0ZTBhMDBjODQ4NjM4NGE0MDc5OTA1NmY5YWE2OWEwMzlmYzI2Y2IzNzAyZDhmZWNkN2VlNTMyMTRmM2Y3NTliMDBmNmRhNjdiYmY4YmVhMDBjYjQxZjQxNzRiYzk2MjdlMWI0NmY0MGI2MjhjMDU2NTg2N2ZkMzliYTAyODMzZDUyZWZlYmUzNDA5YmUzOGFjODY4ZjA2MzgyM2Q0NTU1OGU4N2E1YWY1NjVkODhmOGI1YmIyNjQ2MWVmMDQzNzI2NGQ4MmZlZmVjYzIzNWQ4ZTdlMWRjYTM1OTEwOWUzZmQ1YTFjZmJhNzRjMzYxYjdhY2JlY2I4NzRhOWJjYWM3OTcxNzQ2OTY3ZTg2MzIxMTZiM2YyYTVkMTZkYjI0YmI3OTY4MWVlM2EyNTUyNDcxM2FkMDgxNmU0OTIxMWZmZDUyNDE4MmFkYjY2NTI5MWZmZmIyMzMyMWFmYzI2NjVhMTUzZWRhYjZhMmFmYmVhNGJlOTE4MjdmYWM3ZDU4ZTJlMDQ0NWE0NmRlNmE4NWU1NDk1NWY0ZjYyZjVmNmJiOGY2ZDc5ODRlN2M4ZDc5OWE1MmE5ZDEzNmIwNmUyYmM2MzZlYWJkMGYwYzdkZmM0NGI2MTc4N2FkOWVmY2Q1ZDk3NDdiN2Q4NTUwMWMxMmM1NWNiMmJjZDU2YTg1MjUxOGE1ZmU1NDJkZGM1NjAyZDEwN2U5OTE2MzdiNWU3MzFiYTI2ODQwZjU1YTBjYzBhMmRkM2MwOTcyNTliNjM2OWY3OTdiNmRiZjM0ZDE0YTdiYTFhNWJkNmVmMmE0MGI0NTY0MTgxYWVkMTU0OGQ3ZGQyZDVhMmY0OWQwMjBjNTc1OWYwOTc1OGZhOTY2ZjE0OWFhMTg4ZjBiNmIxMGZkYjE2ZWY3YTQzZTY5MjE5NGFiMWYxNGNiYzIyN2VjNzUxNjI3ZGE5NzJjY2ZhOTIzOTdhMThhOTQ4Njc2Yzk5NTIyZjVhMTQwYzAxODQ2NzIwYzI2MTM0NmFlM2JlMDhkZmNmNjVmYTlhMzIzNWQ0MWFiNjI5MjY0NmE1Njk4ODJhY2IwYWI2NWY1YTY5NDVkM2MyZmFkN2M3NWQ3MTg2MzFlZGIxMWVmOWMxMjczMzM5NjA1NTcyNTIxMjU4NjhiNTUzNzE4YmMxZTI1MGFmNTEyYmE0MjVkM2Q4NTNkNmUyMjE1ZTllMDQ4ZGFlOTMxMDQ3NWEyM2FmMjdjZTI1YjY2NTRlYWE4OWRmYzU0M2RkNDczZjE5YzU2MzI3NDMwOWM3NmZhYzc3Y2U2NDk2NjdkZTZlMDRkYzRiNDQ5Y2EzYzVkODhhMTQ1MThlMmZmZWRkZGYzMTNiMjVkZDczYTZiMjcxMzZiYjAxYWIyZWZjYjA0ZGY5NGM5NDEyYzIzMTc5MDdlZTEzMGEyZDRmZDczZGNiZTAyMTRlNGJlNzMwN2QwYzEzOGFjNGUyZWQ3NjA4NTdlNTMwOTZkNDgzZGY0NzlhZTViZGVkZmI5Y2E5ZGNlZDA0NWRmZjVhYTc1OTVhMDNkYTlkZTM2MWJlM2I0YTY1MGQ3YzUyY2JlOWFmYjE0ZTkxMDRiYzQ5Mzg2MDkwZjVmOWM1OTQ0M2U3ZTkyMmU0NzE3NTVjYWQ4ZjEyNTNhZTM4MGQ2NzAwYjAwNDQyYjA0NWYxZTQ0Y2U0NDJjODNmOWY5MmM2ODJhZTNhYjgzZmFiMzIyOTVlZTBhZmZlNDA2OWQwZGNmZjVjNzRjMWMyYzkwNDJmMDJhZDdhNTU3ZTE4YmU2NDk3ZmM4NjRhYjY5MmY5NDAxZmM5NGY1MmFmMGM1YWYyNjFiMWY2ZDAyNTNkYjEzZGJjNTI0ZGFiZGY1MzEwNGFjYmIwZGYxOWQwM2I0ZjY4YTZiODNkZjgyNmUwZDE4NDRhYzlmYTE3OTlkMzUyODEwZDRmYWQ4OTM3NmM1OGNiMGI1YTY0MjNjNTM5ODRkMmI1MjcwYjU0NTgzNjVhZDA1NjVhN2ZjOGRiMzMwMDkyYmYyNmQ3OTUxMWE2ZGE3ZGZiZWYxNDNhZWMzNTlmNTBmODVkMGQxZjYwZjNlZDE1NTUxNjZkNjZhYzVmNjQyOGQ5YThhZDcyMGM4NDdjYmY0OTlmZTE3ODkzNmJiNjcxMDJmMjIwZWZhMzc5ZTMzMTIxYWIyMWZkNWIyOTk1YmRhNzM5ZTE1MmI3ZWY2OTM4MzcwZDgwMDljNTE1MDIxMmMzYzBhNTgzYWJlYjNiNzE3ODE5N2IxZTBmYTdhM2ExNTg2MjM5OTZjMWFlYTdiZWZjZjE1MTg4ZjFmYmRkMTE2MDc4MzBiYmZlYTViMTFiNjMxNmMyZDgyZDYyODY3MDA3Y2MwZTAyZjJhNjFiNTY3NzRlMWM1NzI4YmZlMzlmZjgyMDEwYzhmZmFiMTJiNzhkYmQ5YzczMjJlMzc0NThmMGExYjE5Yjg2NDJhOWU5MWVmMmIzYzI0MzE1YTA4YzRjOTc1NzlmMGI1NDdjYTU3OTdkNTcyM2QyMjQ1Yjk1MmRmZjJiNmEyNGI0NDNhZTQ1ZGU0NmQzNDgzNmU1NTgxYWEyYmFmODBhZGFiOTc5YzM4ZGUwNmNjMGI5NGE1ZjFjMWZjNDMzYmVmNjY2MWVlZGZkMTJhNDdlM2FmN2Q1MTI4M2Y5MzZhYjhjNTZjMzg3NDUzODIyOWQ3MjAxZmU5OTU0YWNiMGJjMzZlZGU0ZjUwNDRkODgyMmMyYmQ4MWY0ZGE4ZmI3NjUxOGZiNTBiNGUwNTA3NmE0ZTJjOTFjZDJkNmY1NGI4YjYzNzA3ZWI3ZWViYWQ4NTdlOWRjYTU1NTMyNjE4MTc4N2NkNmQ2NDg1N2UwNTFjMzY2MThmNmZkZWFlMGZjNDMyMjk3N2FiZmI5NGQwMDNlZTNhYzUyNDk0YTFhOThlYzVjZjA2N2Y1ZjlhNWExMTdkZTZjODJkOGUyYzNmNWI5MjhhOGRjNDE2NmM5NjNhMWVkNTA5NjhkMmMwZGM1YjcxNWEzMzBjNTI1OTE3YmQ5YzdhNmQ4Nzk3MWI4ZmI5MmRmMTliNjkxMjRiNGY1Mzg4YjI2ODQyMzJkYjc2ZTA1MjZkZTBhODZmMDc2OWU0YzYwZGI4MTM3MGRlMTA4YjMyMjQ2NjYxODk0MjhmY2I1ZTY0NWIzNjE0M2NkZGQyYTUyODZlYjk1ZTdkNjNhMTU5OTE4NmFkYjY3ZDhiYzcyNWExNDY0MThlZmY2ZTFmOWJkOTNlM2Y0NTUwYjA1NGIzYTQ5Mjg0MzBmNDYxOGNiZTlkMDRkM2RkMDg0YzYxM2E4NzFiOThiNmM1YWE4MTIwZWVmMDUzNzI0M2JhNWE3YWI4NzZhOGEyMWViMDc1ZjdhMDY5YjRhM2EyODFjMWRiYTg2MjliMjU3Y2YwNDM1MWI2OTY3OTExY2E0ZDZiYjdhMGYzOWY2Y2M1OWRmOTAxODFjMWE4MTdjZmFjZmQ3NjVhMjM1NzM2MTdmYWM4YzhhZWNiZDYyY2Q5ZjU5ZGM3OGY3NzI5MTk5N2IzY2ZiN2U0ZjJhOWMzZGQzMDY4Y2JmNmNhZjdlZTlkYmI0MDdlMzJiNjhlZjBiMzk3YzVhMmJjYjExNDAyYWNmZDg5OTUyNDYwZWRiMDg1OGFmNzBkMmE3MjU3MDdiYmE2ZDJjMDliZTM2MTU2MmUwZWU0NDkzZGFmMWQ5YzM2YTg4ZjlkOWY2ZjJiMTdkOTBhZDYwOGJhNjk3ZWU1MThhNjFmZmRlZTNlMWUyOWQzNmU5OThjMjk4Y2U2ZDAwYTU4ZGM0YmI0ZDdmYTE4N2RiOTQ1ZTE2MDExMTQ5NTgyMDM3YWYzMzI3M2Q2MTk4NTdjNjFlNTk3ZGU1YmM1ZjYzYWQ3YTM5ZTNiNDc1MTEyYzhjNDYwMGVlZWQ3OWVkMTkyNWQ3YTFkNDUzOTFhNDZkYTI5MGJlNDg1ZTQwNjNjZTRjMTkyY2ZmNmRhNzhkZDM1Njg4YTc0MjNjZDhkOWYxNzk0ODRmZTljYzVlM2E3NmNkY2RmNTkyODY3OGNmMjgzYjk0MDE4Njg0M2VlYmI1NTQxMjZkOGI1NThlMmQ3ZTM4NTE2MTBhNzE5ZGIwNTExMTljNTAxMzJkNGM3YTBmMGIxZjZmMThjNjAzZjZlZTIzMzFhZWQyMWU4NzUzZjI3YzgzMmExNzI5NjVkZGM3MzFmZDM4OGY5OTZmMmVlMGUxZWJmZDZkMWU2Nzk3MDg2ZmY2Njk2YjZlZjQ1ZWFiZTllNGFhMjZhZjU4Zg==''',
                    b'''OGJhMDAzNTQxZDc0MjZjYTM1MTFlZjFlZDBhZTliYjc2ZjQ2ODA3YzI0N2E1OGNiMzY0NzI0ZmJiMGYyYTY0YWFlODI3NmIyMTM3ZmI5NjBiODM5ZDVhYjFlOTYxNDJkYWRkYmY5ZDI1ZWNkNTc5YWQ2OGI5MGUyZGQwODQ0ZTJmNzYxOWY3NzQwODE1ZWQwYjgwYzMyYWI4OWQxNDZkZjgxNDlhNzFjMWFjZjk1NDVmNTE4NTQwODFhYTQ4NWNiMzI4ZDMyZTUxNTI2Nzg1NGUwYTE5ZDYzYTc4MzgxN2IyMTQxMWE0ODY0ZWRjOGVjMWMxNTgyMjBmNTdlZTk5Y2ExN2JkYjE1Njc4ZWVkMDk4MWQ1NmI5MDQ1NGQxY2JiY2JmYTU1ZTgxOGFhMDkzZTUxYzQ2ZmZkMDczNDg4ZjdjNGIxZDY5YWUxZTM4YmM5NDFlMzMwOTE1MmNkMTQ4NWMzZDI5MzVmMDA4NzAwZGJiZmI5NjI0MmQ5Njk3NDdmZThhMWY3M2ZmZjVkOWM5ZTA3ZWQ2Y2I5N2U4OWY2ZmJhZjdjMDIyYWVkMmFiYzIwNTE5MGYwYzFkNTE3YWRkNTMzNjNhODFiNWQ3MDBiYWE3NWE4MWYzZjk0ZDQ1M2YwNDE1MWQ4NzVlZjc4OWEyZjcyNWZlOGI3MTdjOGY2NTk4NTEwNzAxYjE3NTM4YjFkMWVlOWYxYmVhODRlMTA4YmM1ZjgxODAwNWI0M2FlZTNmZmEwZTNhMDU3MTYyZjk1MGUwNzZlZDY0MTg3ZjBhOTY3ZTU0ODA1ZTExOGNkMjc0NGRmZDYxNTllNWVmMzc5OGYxYzA1OGI3YjZjZGM1M2ZkYTYwNzE4YWJkMDcwMDAwYTA0YzBlNjMyM2QxNTEwNmJlYmI5OTI0MWQxNjM3ZjY2YzgxOWUyNWI5ODZlMTJjMDhlODIwODQ2Njk0YjdhNzFmZDE3Nzk0YTAwZTgxYTM4YzNhM2FjYjE5NWUxOGY0OWRhYmYyMjk3ZjM5Y2RlYjgyZTdlOGZhYzI0NWQ1ZjhhNTI2NmIyZjAzZGFjZDNmMWY1ZDlkNjE1M2Y2ZWMwZGQ4MWY4MzQ5YzRhZjFhNGNiZTgzYTVkYWE1NzgyMjYwYTA0NWM3MDliNjA4Nzk5ODhkNzYzNjM4OGE5MzQwNmQ4ZmIwMzc1ODAzNDcwODc3MzI0MTNkODRhNTJiYTBiMjE0MTAxNjgwNDNlYjJkZTgxMTk0YTBlMWUyZWJhOTI0NGNlMjdkOGFmMjUxMzQxMDE3M2I2NmMzZmQxNjcyNzU2NGE4Zjc1MDE2YjFiNjBlNTA0NjA2NjVjM2UzY2ViZDUwZTU2ZTU1YTE5NmE2ZGU4OWIyMDBmODJiZTIwMWViMGZkNjFkNWRhMjc2MDI1NmM3MTA3MmM2Y2YxNDczMzUxNDRmMjE5MzdlMmRkYzJkMjUxNWFiN2NiYjNiZTkwNDk5MDhiOTAzOTNjYmY5MzYzOWVkY2UzYTFjMWY3MjU5NjQ0ZmM4NDFmZjY0YzFkMzczMDcwMDhiMTIzYTYxN2E2Yjg4OWIyMjM3NGU4NTZjYjkzYjA0ZDI4ZDUzYWUxNjRiYTNkODcxNjA5OWU5NDJjZmFkYzgxYWQ1ODA1YTgwODNhZjViN2Q3MzFlNGJlMjZkZTMzMzIwN2UyYmU2MzFiYzkxMzE2ZDg4ZjE4OTBlZThkMzA1NjNmMjU5YjdiZmQwYTYwZTEzNWFlZDc1NGU0OWVhMmJjMTE2ZjNiOWFjZDc5M2I5NDdiNTM0NjkxYTEyNWY3MWVjNzYzYTBlOGFkZDA4ZGFkZmM0N2ZiM2VkNTczYzc2MTU0YTdmM2M0NzA2MjYxMTI1MzRhYzRlYWVmM2VkMGEzYTViYjBiNjgyY2VkNDhkNTJmYzg1N2JlYzZjZmY4OWM3OTQ1YjE2MTQ2MDlhM2NlYTNkNGJjY2MxNTVjMTJlNmM1MWE2YjQ2MzY2OTZlYTcxYjZkMmQxZDdiMTFlMDY1MjFlZmFlYTUyMzkyNzNhOTY0NDI4Y2ZlZGJhZjE2YmM2YTFlZTZhNjYwNDM3Y2M2ZDVjMzAyY2I0ZmVmZmY2ZWY3YWIwNjZlNzg4ZjZkMjQ5OTM1NjcwYmQ1YWViY2QyOGQxZWMyYmEzNDJlYTgyZGJmN2YwZmNhNjA2Yjk5NTUxMzE2OGNkNWE5NmE1OGQ3MTJhMzdjNjQ5ZTg3YTExMzc4YjBhNGEyMGQ2NWM3ZmE3NmNjMjQ4ZDQ4ZDgzNjg1MTk3MDM0ZWMzYzBhZDExZTJmYjVjYzNmYzcyMjI4ZWU0ZWY5ZGFmNGJiOGUxYjZjODQzNjRiYzdmYWNmMGNkYjUzNjE5YzlkN2E3ZDcyNDc0NjEwZmFkN2Y2MjlkYTIxMWJlNWNjYjA4NjVlZjY1ZDY4ZWM4ZTUxYjQxNjMzNDUxODA3NDRiYTY3OGQwNDQyNzdlMzEyYTI1OWI4OWYyYTc5MWEwM2FjZTkxOTc3ZjljMWY4YWMyN2Q2ZDcxNWUxYzNiNWU1MDFmODQ1ZTY0ZTNiMmMxMTBkNzkwZTFlYjExYWI0MmVmMzE0NTYxZjkxM2RjNzcxOTMzNGJjNzkyMmEwNGM1OGZmMTc2Njk5MWQ2NjE0ZjI2ZDkwMDIzODM1YWZlOTRiMWU2YjYwNWY0NzJjZDFkZTNlY2E2MTA2YTg4ZjY4ODcxNWVjMDZhN2QwNTA2NjZhODczMGJhNWM0Y2FlODkzOTcyZDc4NDcxZjM5MDI3OTJhYjZkZWU1NDFiYjJlMThmODhhOWU1NmI5MjYyOGI2NDNlMmFlMWQzNGVkMzdhNzBlYWM0NTM3ZDFmNzA2NjVmYjk2OTgzZWFlMWQ2N2NmMjNhNTllYWZmZTI1MjA2ZjRlZjNhY2QyMjk4Njg5NjAxOTQ0MDMyYzVhYTUxZDFmN2E3MTA0MjQyZGZmNDk3ODliZjE3MmE4Nzc0OTQ0YTY0ZGE2YjEwNmE2MzFiYzBhZDYwNDIzOTlmMGFlMTUzMjM0NWM5OTM3Yzc3YWZlYjE1MTUwZDc0N2IwM2RjY2Q4ZDBlYjNkMGZiMDk0Njc2MWZjOTJjODI3MGVjYmJlZmVhY2NhODJhYjE2M2Y2MzY3YzViY2RjYzAxOThkYmUwYmE2M2Q2MTA2YmEzMDM2ZjA3NTU3YzhhODk0MDY0ZWJlOTMzODA4ZWRjMmE4NTQ4Yzg3YWMyZjQ4ZTZkMGQ4Mzk0NTQ5YTU3ZjkxMzlmNjYyMWY3MDcwNTFjZTk2MDBkNGY0NjBiMDljN2UwNTQ0YWNkMmI2ZTE0NmIzYjE3NWY1NjhmMDUyOWU0ZTEyMmM2ODkwN2NlNzhjODY4OTVlZGNhMzhhYWMzY2M0NjE2MzA2NmZjZTU3ZjI4NDg5ZTEzZTQyZWE1ZjM3MTRmYjk1YzE4ZDA0YmUzZjM5NTlkZWNjMmIzMGFjZjM3ZmQ3NjgwMWM2Y2M3YjBmNDBkZWQ3MWZmOGQ3N2ZkMGI0MmQwM2ZmODFmOWYyNTZmY2E3M2ZlMTMyOTdhY2YyMTk2MWE5ZjRjN2U5Njk5OTZlNjVmMDBiOGZmOGQ1MmFjMjQ0ZGQxYmIwMTdlYzZjMDdhMTFlMDMxY2EyZTMxYTEzNDgwMGIwODAxYjU2NmUwMzY1MWE3NTM5MzhlZTI2NDg2MTdkNTczOThmZTgzYTQ0NmNlYWM4ZDAyYzAyNDc0MTdjMzAyYjUwMjM0NTU4ZTYxMDJhYzFhNGM1OGFmMTIyYWYzMjU3ODIzMDRjZTg1YWYwMzA2Y2Y5OWI0NDQxODgyZDU1NzQxOGNmYzVkNThjZjQwYzQ0MmE1NjBjZTlmMWY1OThhMzBmY2FkMzc0OWI2YTZlMGQxZWU1ZTQzOGE1N2MzYzE2MDhhNjljN2M2NDk1MjZmZWQ0NWE0YzIwNTFiMTk3ZjQ3YjZlZDViZGQ3YWQzN2RmNjgxMDkyYTEzNzAwMWFkNWY2NmNkNGQ1NzljZGE5OTk3MTZhYTM0ZmM2NTM1Mjg2NWFhYWM0ODkxNzA1ZTM0ZDJjM2I4ZTg4ZmJkM2Y0ZmY5ZjlhNDBlZjc0OTc1NjkwZmE1YzI1ZDQ0YWY4OThiM2Q0MDdmNTE2Yzk3YTFlNjRiNTI0YTI3MjhiNzdlNzM1NzNiOTY2MmFlYjRjYzU5MzE2ZjgxZmU3YzZmMTA2ZWUzZjhlZTc0MDNiYTdhMWIzNGQzNDEwMjdhNDBiNjlhNTJhMWY5ZTQ4NzBmZjVjMjJjNzk2M2ViNjc2MTZhZWMwMmFlZGZkODBlODRjZTNmMjJjMjI3ZjA4NGMwMjc0YTNlNmIwZTc2ZDQyZTYwNjc3OTc2ZmQzMDU0NmZmOWFlNWE2MTQ4NjM0ZDNiNWM0ODU4ZWI0NjA3MDhkOTUwZThhZGJmMjRmMWEzNGE4ZGM5NmU2YjM1YmY2MDNjODE2NDk5YzZjOTRiNTM3YjY1NDkyOGIzMDM5Y2U4MWQ4MjZkYjY1YzEzNmNiZGYzYjI2ZjNjNWQ5Mjc3ZGM0ZTBkYTkxMWNlZTc2NzFkYTlkY2MxNTc2ZWJhZDZkYjkxODUzNDVhY2U2MWU0NWVhNDE4ZjcyNGU5N2YzZDcyMTQ5OTNiMzIzMTEzYzBlODE1ZGQ0NmNmNDYzNmFiNzI2ZjNhYzlmZTllOWY2N2U2Y2NiZDgwNmJjZDUxZWJiYWMzYjljMzRiOWIwNTFiMGU5NDVhYTMyMjhlMzAzOGQ3OTVjMjA0ZTAxZTRmNjlmZjU3ZTFlMzdkMzZiYjliMTMyMjkzOGI0MmZkYTFmNmRlMDAxMmZiYTZkZTVlMDRlNGVkZjBjYWRmMWY1MzEzYjUyNTIyMDNiMmYyYmY5MWU1NzlmODY4NjM4ZDZkOWY0NDYzODk3YzhkNmVjYTUxYjRjNmQ3MzYyMmMxNGU5ZTFjZWRhZjQ4YTVlYTE5YWE4MWVhNzJiZDAzYzEyNTdkOTI2NTM3MTU1NTExNzE0M2U0MWExNzIyYzA1NWY4N2Q5YjkwNGZhNGQ3MjRmNWNjMzEzM2U1YWE1NTcyOWE0MTc5NGI1OTM2OTU5YmY2ZGE3NGQ5ODhmYzUwMjc4YjhhMTA4YThkNjYwN2UzZTU1MzYxNGUyMDdlMzg0YjU2YzRlOTdhZDQ3MDQzMTVhNzViMTM0MDhkZDE4MWRiYzkwNjc3OTk3ZDJkMTQ1ZjdhMTYyMzgyY2I5NWUwYWQ2NjJmMzkwOWFiMDYwNjc3Y2VmZjQ1NDdiZjUxYzdkY2UzMmMyZDJmMDRiMTBhMDAxMWNlNjQ4NA==''']


    def isOk(self, tok: str):
        if bytes(AqCrypto.encryptContent(AqCrypto, tok), 'utf-8') in self.tok:
            return True
        else:
            return False


class AqConfig:
    def __init__(self, configDict):
        
        self.language = configDict['language']
        self.theme = configDict['theme']
        self.popupOpacity = configDict['popupOpacity']

        self.loggingMode = configDict['loggingMode']
        self.logSavingMode = configDict['logSavingMode']
        self.logSavingDuration = configDict['logSavingDuration']

        self.keyBindings = configDict['keyBindings']


    def setup(self, configDict):
        self.language = configDict['language']
        self.theme = configDict['theme']
        self.popupOpacity = configDict['popupOpacity']

        self.loggingMode = configDict['loggingMode']
        self.logSavingMode = configDict['logSavingMode']
        self.logSavingDuration = configDict['logSavingDuration']


    def setupByParam(self, param, value):
        
        if param == 'language':
            self.language = value
        elif param == 'theme':
            self.theme = value
        elif param == 'popupOpacity':
            self.popupOpacity = value

        elif param == 'loggingMode':
            self.loggingMode = value
        elif param == 'logSavingMode':
            self.logSavingMode = value
        elif param == 'logSavingDuration':
            self.logSavingDuration = value


    def setKeyBindings(self, keyBindingsDict):
        self.keyBindings = keyBindingsDict


    def getDict(self):
        return {'preset': None,
                'language': (self.language),
                'theme': (self.theme),
                'popupOpacity': (self.popupOpacity),
                'loggingMode': (self.loggingMode),
                'logSavingMode': (self.logSavingMode),
                'logSavingDuration': (self.logSavingDuration),
                'keyBindings': (self.keyBindings)}


class AqLogger:

    def __init__(self, name: str):
        self.name = name
        self.filenames = list()
        self.Logger = logging.getLogger(name)
        self.getFilename()
        
        self.Logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("""{%(asctime)s} [%(name)s:%(levelname)s] [%(filename)s <%(lineno)s>: %(module)s.%(funcName)s] %(message)s""")
        handler = logging.FileHandler((r'{0}'.format(self.filenames[0])), 'a+', 'utf-8')
        handler.setFormatter(formatter)

        self.Logger.addHandler(handler)


    def getFilename(self):
        self.filenames.append(str( 'log/' + (time.strftime("""%d.%m.%Y_%H%M%S""", (time.localtime())))  + '_AsQammLog.log'))


    def debug(self, message: str):
        self.Logger.debug(message)
        print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}DEBUG{Style.RESET_ALL}]: {message}')
        

    def info(self, message: str):
        self.Logger.info(message)
        print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}INFO{Style.RESET_ALL}]: {message}')


    def warning(self, message: str):
        self.Logger.warning(message)
        print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.YELLOW}WARN{Style.RESET_ALL}]: {message}')


    def error(self, message: str):
        self.Logger.error(message)
        print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.RED}ERROR{Style.RESET_ALL}]: {message}')


    def critical(self, message: str):
        self.Logger.critical(message)
        print(f'[{Fore.GREEN}{self.name}{Style.RESET_ALL}@{Fore.RED}CRITICAL{Style.RESET_ALL}]: {message}')
