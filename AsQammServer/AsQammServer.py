import uvicorn
from typing import Optional
from fastapi import FastAPI
from random import uniform

from _asQammServerLibs.functions import *
from _asQammServerLibs.users import *


class AqServer:
    def __init__(self):
        self.api = FastAPI()
        self.mkdirs()

    def mkdirs(self):
        neededDirs = ['/log', '/data', '/data/personal', '/data/config', '/data/system']
        rootdir = os.getcwd()

        for i in neededDirs:
            try:
                os.makedirs(str(rootdir + i))
            except FileExistsError:
                continue
            

if __name__ == '__main__':
    server = AqServer()
    userCore = AqUserSystem()

    @server.api.get('/getUserdata')
    def getUserdata():
        return userCore.getUserData()

    @server.api.get('/getUserRg')
    def getUserRg():
        return userCore.getUserRegistry()

    uvicorn.run(server.api)
