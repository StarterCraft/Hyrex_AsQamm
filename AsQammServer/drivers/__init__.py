'Модуль с кодом для работы с драйверами'

from libs          import *
from libs.hardware import AqHardwareDevice
import glob, importlib

Platforms, Devices = {}, {}


def getDeviceClass(platform: str, name: str):
    '''
    Получить класс исполнителя по имени протокола, по которому работает
    этот класс и имени класса
    '''
    return [device for device in Platforms[platform] if device.__name__ == name][0]
