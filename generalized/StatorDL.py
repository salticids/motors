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
            self.statorMat = Construct.Material('Air')
            self.coilMat = Construct.Material('18 AWG')
    
    def __init__(self):
        super().__init__()
        self.p = self.Parameters()
        self.group = 4

    def sanitize(self):
        while(self.p.Nt % 3 != 0):
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
        fm.addNode(p.ri, phiM/2., self.group)
        fm.addNode(p.ri, -phiM/2., self.group)
        fm.addArc(p.ri, -phiM/2., p.ri, phiM/2., self.group)

        # draw coil-facing surface
        phiRootInt = math.asin((p.bt/2)/(p.ri+p.wt)) * 180 / math.pi
        fm.addNode(p.ri+p.wt, phiRootInt, self.group)
        fm.addNode(p.ri+p.wt, phiM/2, self.group)
        fm.addArc(p.ri+p.wt, phiRootInt, p.ri+p.wt, phiM/2., self.group)
        fm.addNode(p.ri+p.wt, -phiRootInt, self.group)
        fm.addNode(p.ri+p.wt, -phiM/2, self.group)
        fm.addArc(p.ri+p.wt, -phiM/2, p.ri+p.wt, -phiRootInt, self.group)

        # Connect tooth surfaces
        fm.addLine(p.ri, phiM/2., p.ri+p.wt, phiM/2, self.group)
        fm.addLine(p.ri, -phiM/2., p.ri+p.wt, -phiM/2, self.group)

        # draw coil-facing stator surface
        r = p.ri + p.wt + p.hs
        phiRootExt = math.asin((p.bt/2)/r) * 180 / math.pi
        fm.addNode(r, phiRootExt, self.group)
        fm.addNode(r, phi/2, self.group)
        fm.addArc(r, phiRootExt, r, phi/2, self.group)
        fm.addNode(r, -phiRootExt, self.group)
        fm.addNode(r, -phi/2, self.group)
        fm.addArc(r, -phi/2, r, -phiRootExt, self.group)

        # Connect tooth to stator
        fm.addLine(p.ri+p.wt, phiRootInt, p.ri+p.wt+p.hs, phiRootExt, self.group)
        fm.addLine(p.ri+p.wt, -phiRootInt, p.ri+p.wt+p.hs, -phiRootExt, self.group)

        # draw back iron boundary
        r = p.ri + p.wt + p.hs + p.wbi
        fm.addNode(r, phi/2, self.group)
        fm.addNode(r, -phi/2, self.group)
        fm.addArc(r, -phi/2, r, phi/2, self.group)

        # draw coil surface
        r = p.ri + p.wt
        phiC = p.cf*phi
        fm.addNode(r, phiC/2, self.group)
        fm.addNode(r, -phiC/2, self.group)
        fm.addNode(r+p.hs, phiC/2, self.group)
        fm.addNode(r+p.hs, -phiC/2, self.group)
        if(p.cf > p.tf): # coil broader than tooth 
            fm.addArc(r, phiM/2., r, phiC/2, self.group)
            fm.addArc(r, -phiC/2., r, -phiM/2, self.group)
        elif(p.tf < p.cf): # tooth broader than coil
            fm.addArc(r, phiC/2., r, phiM/2, self.group)
            fm.addArc(r, -phiM/2., r, -phiC/2, self.group)
            # note no need for arc if tf == cf
        fm.addLine(r, phiC/2., r+p.hs, phiC/2, self.group)
        fm.addLine(r, -phiC/2., r+p.hs, -phiC/2, self.group)

    def draw(self):
        
        # Revolve StatorDL around origin
        fm.revolve(self.p.Nt, self.group)

        # Add coil labels
        phiStep = 360/self.p.Nt
        phiOfs = phiStep * self.p.cf - 2 # 1 degree in from coil boundary... todo: better math
        r = (self.p.ri + self.p.wt + self.p.ri + self.p.wt + self.p.hs) / 2
        for i in range(self.p.Nt):
            phi = phiStep * i
            circuit = chr(ord('A')+(i%3))
            n = fm.addBlockLabel(r, phi + phiOfs / 2, self.group)
            fm.setCircZ(n, self.p.coilMat.matName, circuit, self.p.turns, self.group)
            n = fm.addBlockLabel(r, phi - phiOfs / 2, self.group)
            fm.setCircZ(n, self.p.coilMat.matName, circuit, -(self.p.turns), self.group)

    @property
    def rInner(self):
        return self.p.ri

    @property
    def rOuter(self):
        return self.p.ri + self.p.wt + self.p.hs + self.p.wbi

if __name__ == '__main__':
    s = StatorDL()
    # for i in s.p.params():
    #     print(i, s.p.__dict__[i])
    fm.initFemm()
    s.testDraw()
    fm.zoom()
    input()
    fm.closeFemm()