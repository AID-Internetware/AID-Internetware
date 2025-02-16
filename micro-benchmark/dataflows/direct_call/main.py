def func1():
    return 0

class Dependency:
    def __init__(self) -> None:
        self._data = func1()
    def func2(self):
        return self._data
