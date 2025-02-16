class Inference:
    def func1():
        pass

class MyClass:
    data: Inference = None
    def func2(self):
        self.data.func1() # type: ignore


