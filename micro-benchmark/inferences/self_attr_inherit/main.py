class Inference:
    def __init__(self) -> None:
        pass
    def func1(self):
        pass

class MyClass:
    def __init__(self, infer: Inference) -> None:
        self._infer = infer
    def func2(self):
        pass

class MyClass2(MyClass):
    def func3(self):
        self._infer.func1()

