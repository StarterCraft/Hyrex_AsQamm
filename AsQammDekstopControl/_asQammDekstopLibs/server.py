import requests, http, json
from _asQammDekstopLibs.logging import *


class AqServerCommutator:
    def __init__(self, root, crypto):
        with open('data/config/~!serverdata!~.asqd', 'r') as configFlie:
            fileString = crypto.decryptContent(crypto, (configFlie.read()))
            jsonString = json.loads(fileString)
            self.ip = jsonString['ip']
            if jsonString['port'] != None:
                self.port = jsonString['port']
            else:
                pass

        self.commutatorLogger = AqLogger('ServerCommutator')


    def get(self, methodIdStr: str, returnModeCode):
        try:
            response = requests.get('http://{0}:{1}/{2}'.format(self.ip, self.port, methodIdStr))
        except AttributeError:
            response = requests.get('http://{0}/{1}'.format(self.ip, methodIdStr))

        if returnModeCode == int:
            return response
        elif returnModeCode == str:
            return response.text
        elif returnModeCode == bytes:
            return response.content
        elif returnModeCode == json:
            return response.json()


    def post(self, methodIdStr: str, inputModeCode, returnModeCode, postData):
        try:
            if inputModeCode == list:
                response = requests.post('http://{0}:{1}/{2}'.format(self.ip, self.port, methodIdStr), data = postData)
            elif inputModeCode == json:
                response = requests.post('http://{0}:{1}/{2}'.format(self.ip, self.port, methodIdStr), json = postData)
        except AttributeError:
            if inputModeCode == list:
                response = requests.post('http://{0}/{1}'.format(self.ip, methodIdStr), data = postData)
            elif inputModeCode == json:
                response = requests.post('http://{0}/{1}'.format(self.ip, methodIdStr), json = postData)

        if returnModeCode == int:
            return response
        elif returnModeCode == str:
            return response.text
        elif returnModeCode == bytes:
            return response.content
        elif returnModeCode == json:
            return response.json()


    def delete(self, methodIdStr: str, inputModeCode, delData):
        try:
            if inputModeCode == (list or dict):
                response = requests.delete('http://{0}:{1}/{2}'.format(self.ip, self.port, methodIdStr), data = delData)
            elif inputModeCode == json:
                response = requests.delete('http://{0}:{1}/{2}'.format(self.ip, self.port, methodIdStr), json = delData)
        except AttributeError:
            if inputModeCode == (list or dict):
                response = requests.delete('http://{0}/{1}'.format(self.ip, methodIdStr), data = delData)
            elif inputModeCode == json:
                response = requests.delete('http://{0}/{1}'.format(self.ip, methodIdStr), json = delData)

        return response
