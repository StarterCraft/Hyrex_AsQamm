VERSION = 'pre-α 114'
VERSIONTUPLE = ('pre-α', '114')


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
