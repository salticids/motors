from Construct import Construct
import femmutil as fm
import math, cmath

class AMB(Construct):

    class Parameters(Construct.ParameterBase):
        def __init__(self):
            super().__init__()
            self.ri = 0         # inner radius
            self.aofs = 20      # offset of one tooth from pole centerline (deg)
            self.w = 4          # tooth width
            self.l = 15         # tooth length
            self.wbi = 8        # back iron thickness
            self.metal = Construct.Material('M-27 Steel')

    def __init__(self):
        super().__init__()
        self.p = self.Parameters()
        self.group = 55

    def setup(self):
        fm.getMat(self.p.metal.matName)

    def drawSegment(self):
        # find midpoint of tooth in cartesian
        rtmid = self.p.ri
        phitmid = self.p.aofs
        tmid = cmath.rect(rtmid, phitmid)
        tlower = tmid + (self.p.w/2)*math.sin(fm.rad(self.p.aofs)) - (self.p.w/2)*math.cos(fm.rad(self.p.aofs))*1j
        tupper = tmid - (self.p.w/2)*math.sin(fm.rad(self.p.aofs)) + (self.p.w/2)*math.cos(fm.rad(self.p.aofs))*1j
        fm.addNode(fm.polar(tlower)[0], fm.polar(tlower)[1])
        fm.addNode(fm.polar(tupper)[0], fm.polar(tupper)[1])
        fm.addLine(fm.polar(tlower)[0], fm.polar(tlower)[1], fm.polar(tupper)[0], fm.polar(tupper)[1])
        
    def draw(self):
        pass

    @property
    def rInner(self):
        return 0

    @property
    def rOuter(self):
        return 0
