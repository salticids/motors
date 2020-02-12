from Construct import Construct
import femmutil as fm

class RotorSMPM(Construct):

    class Parameters(Construct.ParameterBase):
        def __init__(self):
            super().__init__()
            self.Nm = 4
            self.rsh = 6 # shaft radius
            self.rr = 26 # rotor metal radius
            self.wm = 7 # width of magnet
            self.dm = 6 # depth of magnet
            self.mf = 0.5 # magnet phase fraction
            self.metal = Construct.Material('M-27 Steel')
            self.magnet = Construct.Material('NdFeB 32 MGOe')

    def __init__(self):
        super().__init__()
        self.p = self.Parameters()
        self.group = 10

    def setup(self):
        fm.getMat(self.p.metal.matName)
        fm.getMat(self.p.magnet.matName)

    def drawSegment(self):
        phi = 360/self.p.Nm

        # shaft boundary
        if self.p.rsh > 0:
            fm.addNode(self.p.rsh, phi/2)
            fm.addNode(self.p.rsh, -phi/2)
            fm.addArc(self.p.rsh, -phi/2, self.p.rsh, phi/2)

        # draw magnet
        ri = min(self.p.rr, self.p.rr-self.p.dm)
        ro = self.p.rr - self.p.dm + self.p.wm
        fm.addNode(ri, phi*self.p.mf/2)
        fm.addNode(ro, phi*self.p.mf/2)
        fm.addLine(ri, (phi*self.p.mf)/2, ro, (phi*self.p.mf)/2)    # counterclockwise radial edge
        fm.addNode(ri, -phi*self.p.mf/2)
        fm.addNode(ro, -phi*self.p.mf/2)
        fm.addLine(ri, -(phi*self.p.mf)/2, ro, -(phi*self.p.mf)/2)  # clockwise radial edge
        ri = self.p.rr - self.p.dm
        fm.addNode(ri, -phi*self.p.mf/2)
        fm.addNode(ri, phi*self.p.mf/2)
        fm.addArc(ri, -phi*self.p.mf/2, ri, phi*self.p.mf/2) # inner edge
        fm.addArc(ro, -phi*self.p.mf/2, ro, phi*self.p.mf/2) # outer edge

        # draw rotor barrier
        fm.addNode(self.p.rr, phi/2)
        fm.addNode(self.p.rr, -phi/2)
        if self.p.rr - self.p.dm + self.p.wm < self.p.rr: # magnet buried
            fm.addArc(self.p.rr, -phi/2, self.p.rr, phi/2)
        else:
            fm.addNode(self.p.rr, phi*self.p.mf/2)
            fm.addNode(self.p.rr, -phi*self.p.mf/2)
            fm.addArc(self.p.rr, -phi/2, self.p.rr, -phi*self.p.mf/2)
            fm.addArc(self.p.rr, phi*self.p.mf/2, self.p.rr, phi/2)

    def draw(self):
        fm.revolve(self.p.Nm, self.group)

        # rotor metal material
        r = (self.p.rsh + self.p.rr - self.p.dm) / 2
        fm.addBlockLabel(r, 0)
        fm.setMat(r, 0, self.p.metal.matName)

        # magnets
        r = (self.p.rr - self.p.dm + self.p.rr - self.p.dm + self.p.wm) / 2
        phi = 360/self.p.Nm
        for i in range(int(self.p.Nm)):
            fm.addBlockLabel(r, i*phi)
            if i%2 == 0:
                fm.setMagnet(r, i*phi, self.p.magnet.matName, i*phi)
            else:
                fm.setMagnet(r, i*phi, self.p.magnet.matName, i*phi-180)

        # stator air is handled by utility

    @property
    def rInner(self):
        return self.p.rsh

    @property
    def rOuter(self):
        return max(self.p.rr, self.p.rr + self.p.wm - self.p.dm)


if __name__ == '__main__':
    s = RotorSMPM()
    fm.femmgroupmode = s.group
    fm.initFemm()
    s.testDraw()
    fm.zoom()
    input()
    fm.closeFemm()
