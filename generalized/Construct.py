## Construct.py
# Contains Construct class from which physical motor components derive

from abc import ABC, abstractmethod # abstract base class
# import femmutil

class Construct(ABC):

    class ParameterBase():

        def __init__(self):
            pass

        def params(self):
            return [i for i in self.__dict__.keys() if i[:1] != '_'] # s/o https://stackoverflow.com/questions/9058305/getting-attributes-of-a-class

    class Material():

        def __init__(self, matName):
            self.matName = matName

    def __init__(self):
        self.p = False

    @abstractmethod
    def drawSegment(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @property
    @abstractmethod
    def rInner(self):
        pass

    @property
    @abstractmethod
    def rOuter(self):
        pass

    def testDraw(self):
        self.drawSegment()
        self.draw()