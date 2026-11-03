class Account:
    def __init__(self):
        self.owner = "Sam"            # public
        self._balance = 100           # "protected" by convention only
        self.__pin = 1234             # name-mangled

acc = Account()
print(acc.owner)                      # Sam
print(acc._balance)                   # 100  (works, but you are told not to)
# print(acc.__pin)                    # AttributeError
print(acc._Account__pin)              # 1234 (mangled name, still reachable)
print(acc.__dict__)
# {'owner': 'Sam', '_balance': 100, '_Account__pin': 1234}