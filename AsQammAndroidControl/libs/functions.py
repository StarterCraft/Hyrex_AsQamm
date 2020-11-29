import json, base64, os, glob, ffmpeg, hashlib, time, math
from libs.logging import AqLogger
from playsound import *
from threading import Thread

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

    def seekForFiles(self, root, importList, exportList, flag):

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


    def rawContent(s):
        return str(r'{0}'.format(s))


    def getHmta(self):
        return os.urandom(32)


    def getCut(self, _str, bytes):
        return (hashlib.pbkdf2_hmac('sha256', _str.encode('utf-8'), bytes, 256256).hex())

class AqThread(Thread):
    def __init__(self, target, args=()):
        Thread.__init__(self, target=target, args=args)