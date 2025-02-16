class MyClass:
    def func1():
        pass

class Inference:
    def func2(a:MyClass):
        b = a
        b.func1()
        
