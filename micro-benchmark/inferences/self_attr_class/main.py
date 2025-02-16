class MyClass:
    def func0():
        pass
class Inference:
    def __init__(self, data: MyClass) -> None:
        self._data = data
    def func2(self):
        self._data.func0()
