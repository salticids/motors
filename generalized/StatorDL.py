from Construct import Construct
import femmutil as fm

import math

class StatorDL(Construct):

    class Parameters(Construct.ParameterBase):
        def __init__(self):
            super().__init__()
            self.Nt = 6     # number of teeth
            self.ri = 30    # inner radius
            self.wt = 10    # width of tooth
            self.tf = 0.8   # tooth fractional phase
            self.bt = 10    # root thickness
            self.cf = 0.7   # coil fractional phase
            self.hs = 10    # height of slot
            self.wbi = 10   # width of back iron
            self.turns = 100 # coil windings
            self.statorMat = Construct.Material('M-27 Steel')
            self.coilMat = Construct.Material('18 AWG')
            self.coilA = Construct.Circuit('A', 0)
            self.coilB = Construct.Circuit('B', 10)
            self.coilC = Construct.Circuit('C', 0)
    
    def __init__(self):
        super().__init__()
        self.p = self.Parameters()

    def setup(self):
        fm.getMat(self.p.statorMat.matName)
        fm.getMat(self.p.coilMat.matName)
        fm.makeCircuit(self.p.coilA.circName, self.p.coilA.current)
        fm.makeCircuit(self.p.coilB.circName, self.p.coilB.current)
        fm.makeCircuit(self.p.coilC.circName, self.p.coilC.current)

    def sanitize(self):
        while(self.p.Nt % 3 != 0 or self.p.Nt < 1):
            self.p.Nt += 1
        self.p.ri = abs(self.p.ri)
        self.p.wt = abs(self.p.wt)
        self.p.tf = min(abs(self.p.tf), 1)
        self.p.bt = abs(self.p.bt)
        self.p.cf = min(abs(self.p.cf), 1)
        self.p.hs = abs(self.p.hs)
        self.p.wbi = abs(self.p.wbi)
        self.p.turns = abs(self.p.turns)

    def drawSegment(self):

        self.sanitize()

        p = self.p
        phi = 360. / p.Nt
        # Find tooth metal phase
        phiM = phi*p.tf

        # draw rotor-facing surface
        fm.addNode(p.ri, phiM/2)
        fm.addNode(p.ri, -phiM/2)
        fm.addArc(p.ri, -phiM/2., p.ri, phiM/2)

        # draw coil-facing surface
        phiRootInt = math.asin((p.bt/2)/(p.ri+p.wt)) * 180 / math.pi
        fm.addNode(p.ri+p.wt, phiRootInt)
        fm.addNode(p.ri+p.wt, phiM/2)
        fm.addArc(p.ri+p.wt, phiRootInt, p.ri+p.wt, phiM/2)
        fm.addNode(p.ri+p.wt, -phiRootInt)
        fm.addNode(p.ri+p.wt, -phiM/2)
        fm.addArc(p.ri+p.wt, -phiM/2, p.ri+p.wt, -phiRootInt)

        # Connect tooth surfaces
        fm.addLine(p.ri, phiM/2., p.ri+p.wt, phiM/2)
        fm.addLine(p.ri, -phiM/2., p.ri+p.wt, -phiM/2)

        # draw coil-facing stator surface
        r = p.ri + p.wt + p.hs
        phiRootExt = math.asin((p.bt/2)/r) * 180 / math.pi
        fm.addNode(r, phiRootExt)
        fm.addNode(r, phi/2)
        fm.addArc(r, phiRootExt, r, phi/2)
        fm.addNode(r, -phiRootExt)
        fm.addNode(r, -phi/2)
        fm.addArc(r, -phi/2, r, -phiRootExt)

        # Connect tooth to stator
        fm.addLine(p.ri+p.wt, phiRootInt, p.ri+p.wt+p.hs, phiRootExt)
        fm.addLine(p.ri+p.wt, -phiRootInt, p.ri+p.wt+p.hs, -phiRootExt)

        # draw back iron boundary
        r = p.ri + p.wt + p.hs + p.wbi
        fm.addNode(r, phi/2)
        fm.addNode(r, -phi/2)
        fm.addArc(r, -phi/2, r, phi/2)

        # draw coil surface
        r = p.ri + p.wt
        phiC = p.cf*phi
        fm.addNode(r, phiC/2)
        fm.addNode(r, -phiC/2)
        fm.addNode(r+p.hs, phiC/2)
        fm.addNode(r+p.hs, -phiC/2)
        if(p.cf > p.tf): # coil broader than tooth 
            fm.addArc(r, phiM/2., r, phiC/2)
            fm.addArc(r, -phiC/2., r, -phiM/2)
        elif(p.tf < p.cf): # tooth broader than coil
            fm.addArc(r, phiC/2., r, phiM/2)
            fm.addArc(r, -phiM/2., r, -phiC/2)
            # note no need for arc if tf == cf
        fm.addLine(r, phiC/2., r+p.hs, phiC/2)
        fm.addLine(r, -phiC/2., r+p.hs, -phiC/2)

    def draw(self):

        # Revolve StatorDL around origin
        fm.revolve(self.p.Nt, self.group)

        # Stator metal label
        r = (self.p.ri + self.p.wt + self.p.hs + self.p.ri + self.p.wt + self.p.hs + self.p.wbi) / 2
        fm.addBlockLabel(r, 0)
        fm.setMat(r, 0, self.p.statorMat.matName)

        # Add coil labels
        phiStep = 360/self.p.Nt
        phiOfs = phiStep * self.p.cf - 2 # 1 degree in from coil boundary... todo: better math
        r = (self.p.ri + self.p.wt + self.p.ri + self.p.wt + self.p.hs) / 2
        for i in range(int(self.p.Nt)):
            phi = phiStep * i
            circuit = chr(ord('A')+(i%3))
            n = fm.addBlockLabel(r, phi + phiOfs / 2)
            fm.setCircZ(n, self.p.coilMat.matName, circuit, self.p.turns)
            n = fm.addBlockLabel(r, phi - phiOfs / 2)
            fm.setCircZ(n, self.p.coilMat.matName, circuit, -(self.p.turns))

    @property
    def rInner(self):
        return self.p.ri

    @property
    def rOuter(self):
        return self.p.ri + self.p.wt + self.p.hs + self.p.wbi

if __name__ == '__main__':
    s = StatorDL()
    fm.femmgroupmode = s.group
    fm.initFemm()
    s.testDraw()
    fm.zoom()
    input()
    fm.closeFemm()
