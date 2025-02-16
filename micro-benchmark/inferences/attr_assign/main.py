class Inference:
    def func1():
        pass

class MyClass:
    data: Inference = None
    def func2(self):
        temp = self.data
        temp.func1() # type: ignore


