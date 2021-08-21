VERSION = 'pre-α 115'
VERSIONTUPLE = ('pre-α', '115')


class AqProtectedAttribute:
    def __init__(self, _value):
        self.hidden = True
        self.value = _value


    def __repr__(self):
        return str(self.value)
        

    def __str__(self):
        return str(self.value)
    

    def __setattr__(self, name, value):
        if name == 'hidden' and not value: return
        else: self.__dict__[name] = value


    def __getitem__(self, key):
        if type(self.value) == dict: return self.value[key]


    def __setitem__(self, key, value):
        if type(self.value) == dict: self.value[key] = value


    def __eq__(self, other):
        if not hasattr(other, 'value'):
            return self.value == other
        else: return self.value == other.value


    def __gt__(self, other):
        if not hasattr(other, 'value'):
            return self.value > other
        else: return self.value > other.value


    def __lt__(self, other):
        if not hasattr(other, 'value'):
            return self.value < other
        else: return self.value < other.value


    def __ge__(self, other):
        if not hasattr(other, 'value'):
            return self.value >= other
        else: return self.value >= other.value


    def __le__(self, other):
        if not hasattr(other, 'value'):
            return self.value <= other
        else: return self.value <= other.value


    def set(self, new):
        self.value = new


STKTOKEN = AqProtectedAttribute(b'\xff\xfe\x00\x00k\x00\x00\x00y\x00\x00\x00}\x00\'x00\x00!\x00\x00\x00b\x00\x00\x009\x00\x00\x00u\x00\x00\x00n\x00\x00\x00r\x00\x00\x00i\x00\x00\x00F\x00\x00\x00K\x00\x00\x00g\x00\x00\x00v\x00\x00\x00C\x00\x00\x00*\x00\x00\x00m\x00\x00\x00P\x00\x00\x007\x00\x00\x00:\x00\x00\x00t\x00\x00\x00E\x00\x00\x00q\x00\x00\x00')
