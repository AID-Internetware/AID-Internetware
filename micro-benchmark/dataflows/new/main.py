class MyClass:
    def __init__(self) -> None:
        pass

class Dependency:
    def __init__(self, data) -> None:
        self._data = MyClass()
    def func(self):
        return self._data