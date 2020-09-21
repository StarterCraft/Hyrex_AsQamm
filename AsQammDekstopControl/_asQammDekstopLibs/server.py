import requests, http, json
from _asQammDekstopLibs.logging import *


class AqServerCommutator:
    def __init__(self, root, serverIP: str):
        self.ip = serverIP
        self.commutatorLogger = AqLogger('ServerCommutator')

    def get(self, methodIdStr: str, returnModeCode):
        response = requests.get('http://{0}/{1}'.format(self.ip, methodIdStr))
        #добавить логирование
        if returnModeCode == int:
            return response
        elif returnModeCode == str:
            return response.text
        elif returnModeCode == bytes:
            return response.content
        elif returnModeCode == json:
            return response.json()


    def post(self, methodIdStr: str, inputModeCode, returnModeCode, postData):
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
        if inputModeCode == (list or dict):
            response = requests.post('http://{0}/{1}'.format(self.ip, methodIdStr), data = delData)
        elif inputModeCode == json:
            response = requests.post('http://{0}/{1}'.format(self.ip, methodIdStr), json = delData)

        return response
