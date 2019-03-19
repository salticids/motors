## Construct.py
# Contains Construct class from which physical motor components derive

from abc import ABC, abstractmethod # abstract base class
import femmutil as fm

class Construct(ABC):

    class ParameterBase():

        def __init__(self):
            self.autoUpdate = False

        def params(self):
            return [i for i in self.__dict__.keys() if i[:1] != '_'] # s/o https://stackoverflow.com/questions/9058305/getting-attributes-of-a-class

    class Material():

        def __init__(self, matName):
            self.matName = matName

    class Circuit():

        def __init__(self, circName, current):
            self.circName = circName
            self.current = current

    def __init__(self):
        self.p = False
        self.drawState = 0 # 0 hidden; 1 segment; 2 completed
        self.group = 0
        self.angle = 0

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def drawSegment(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    def hide(self):
        fm.clearGroup(self.group)
        self.drawState = 0

    @property
    @abstractmethod
    def rInner(self):
        pass

    @property
    @abstractmethod
    def rOuter(self):
        pass

    def update(self):
        if self.drawState == 0:
            pass
        elif self.drawState == 1:
            self.hide()
            self.drawSegment()
            fm.zoom()
        elif self.drawState == 2:
            self.hide()
            self.drawSegment()
            self.draw()
            fm.zoom()

    def testDraw(self):
        self.drawSegment()
        self.draw()
        