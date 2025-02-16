def func1():
    return 0

class Dependency:
    def __init__(self, data) -> None:
        self._data = data
    def func2(self):
        return self._data
    def func3(self):
        temp = func1()
        self._data = temp