import json, base64, os, glob, ffmpeg, hashlib, time, math
from libs.logging import AqLogger
from playsound import *
from threading import Thread

class AqCrypto:
    @staticmethod
    def getFileNamesList(exportList):
        for i in range(10, 99):
            initialFilename = str(r'customuser_' + str(r'{0}').format(i))
            initialFilename = initialFilename.encode('utf-8')
            initialFilename = base64.b64encode(initialFilename)
            initialFilename = initialFilename.decode('utf-8')
            initialFilename = initialFilename[0:-2]
            initialFilename = initialFilename.encode('utf-8')
            
            exportList.append(initialFilename)

        
    @staticmethod
    def seekForFiles(root, importList, exportList, flag):
        for item in importList:
                gotName = glob.glob(str(r'data/personal/~!{0}!~.asqd'.format(str(item.decode('utf-8')))))

                if flag:
                    if gotName == []:
                        continue
                    else:
                        exportList.append(r'{0}'.format(gotName[0]))

                else:
                    if gotName != []:
                        continue
                    else:
                        exportList.append(r'data/personal/~!{0}!~.asqd'.format(str(item.decode('utf-8'))))


    @staticmethod
    def decryptContent(s):
        return (base64.b64decode(s.encode('utf-8'))).decode('utf-8')

    
    @staticmethod
    def encryptContent(s):
        return (base64.b64encode(s.encode('utf-8'))).decode('utf-8')

    
    @staticmethod
    def rawContent(s):
        return str(r'{0}'.format(s))

    
    @staticmethod
    def getHmta():
        return os.urandom(32)

    
    @staticmethod
    def getCut(_str, bytes):
        return (hashlib.pbkdf2_hmac('sha256', _str.encode('utf-8'), bytes, 256256).hex())

class AqThread(Thread):
    def __init__(self, target, args=()):
        Thread.__init__(self, target=target, args=args)