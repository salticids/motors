from Construct import Construct
import femmutil as fm
import math, cmath

class AMB(Construct):

    class Parameters(Construct.ParameterBase):
        def __init__(self):
            super().__init__()
            self.ri = 10        # inner radius
            self.aofs = 20      # offset of one tooth from pole centerline (deg)
            self.phi = 20
            self.w = 4          # tooth width
            self.l = 15         # tooth length
            self.wbi = 8        # back iron thickness
            self.g = .1         # air gap
            self.coilth = 1     # coil thickness
            self.coilm = 1      # coil margin
            self.metal = Construct.Material('M-27 Steel')

    def __init__(self):
        super().__init__()
        self.p = self.Parameters()
        self.group = 55
        self.circuits = [] # r, phi tuples
        self.matlabel = None # r, phi tuple

    def reset(self):
        self.circuits = []
        self.matlabel = None

    def setup(self):
        fm.getMat(self.p.metal.matName)

    def drawSegment(self):
        self.reset()

        # see sketch for point definitions
        r1 = self.p.ri
        phi1 = self.p.phi
        r2 = self.p.ri
        phi2 = self.p.phi - fm.deg((self.p.w/2)/self.p.ri)
        r3 = self.p.ri
        phi3 = self.p.phi + fm.deg((self.p.w/2)/self.p.ri)
        r4, phi4 = fm.vectorsumPP(r2, phi2, self.p.coilm, self.p.phi)
        r5, phi5 = fm.vectorsumPP(r3, phi3, self.p.coilm, self.p.phi)
        r6, phi6 = fm.vectorsumPP(r5, phi5, self.p.coilth, self.p.phi + 90)
        r7, phi7 = fm.vectorsumPP(r4, phi4, self.p.coilth, self.p.phi - 90)
        r8, phi8 = fm.vectorsumPP(r6, phi6, (self.p.l - 2 * self.p.coilm)/2, self.p.phi)
        r9, phi9 = fm.vectorsumPP(r8, phi8, self.p.coilth/2, self.p.phi - 90)
        r10, phi10 = fm.vectorsumPP(r9, phi9, self.p.coilth + self.p.w, self.p.phi - 90)
        r11, phi11 = fm.vectorsumPP(r6, phi6, self.p.l - 2 * self.p.coilm, self.p.phi)
        r12, phi12 = fm.vectorsumPP(r5, phi5, self.p.l - 2 * self.p.coilm, self.p.phi)
        r13, phi13 = fm.vectorsumPP(r4, phi4, self.p.l - 2 * self.p.coilm, self.p.phi)
        r14, phi14 = fm.vectorsumPP(r7, phi7, self.p.l - 2 * self.p.coilm, self.p.phi)
        r15 = self.p.ri + self.p.l
        phi15 = self.p.phi - fm.deg((self.p.w/2)/r15)
        r16 = self.p.ri + self.p.l
        phi16 = self.p.phi + fm.deg((self.p.w/2)/r16)
        r17 = self.p.ri + self.p.l
        phi17 = 45
        r18 = self.p.ri + self.p.l + self.p.wbi
        phi18 = 45
        r19 = self.p.ri + self.p.l + self.p.wbi/2
        phi19 = 0
        r20 = r10
        phi20 = -phi10
        r21 = r9
        phi21 = -phi9
        r22 = r23 = r24 = r25 = r26 = r27 = r28 = r29 = r30 = r31 = r32 = r33 = r9
        phi22 = phi9 - 90
        phi23 = phi10 - 90
        phi24 = phi20 - 90
        phi25 = phi21 - 90
        phi26 = phi22 - 90
        phi27 = phi23 - 90
        phi28 = phi24 - 90
        phi29 = phi25 - 90
        phi30 = phi26 - 90
        phi31 = phi27 - 90
        phi32 = phi28 - 90
        phi33 = phi29 - 90
        r34 = self.p.ri + self.p.l
        phi34 = 0
        r35 = self.p.ri + self.p.l + self.p.wbi
        phi35 = 0


        fm.addNode(r2, phi2)
        fm.addNode(r3, phi3)
        fm.addNode(r4, phi4)
        fm.addNode(r5, phi5)
        fm.addNode(r6, phi6)
        fm.addNode(r7, phi7)
        fm.addNode(r11, phi11)
        fm.addNode(r12, phi12)
        fm.addNode(r13, phi13)
        fm.addNode(r14, phi14)
        fm.addNode(r15, phi15)
        fm.addNode(r16, phi16)
        fm.addNode(r17, phi17)
        fm.addNode(r18, phi18)
        fm.addNode(r34, phi34)
        fm.addNode(r35, phi35)

        self.matlabel = (r19, phi19)

        self.circuits.append((r9, phi9))        
        self.circuits.append((r10, phi10))        
        self.circuits.append((r20, phi20))        
        self.circuits.append((r21, phi21))        
        self.circuits.append((r22, phi22))        
        self.circuits.append((r23, phi23))        
        self.circuits.append((r24, phi24))        
        self.circuits.append((r25, phi25))        
        self.circuits.append((r26, phi26))        
        self.circuits.append((r27, phi27))        
        self.circuits.append((r28, phi28))        
        self.circuits.append((r29, phi29))        
        self.circuits.append((r30, phi30))        
        self.circuits.append((r31, phi31))        
        self.circuits.append((r32, phi32))        
        self.circuits.append((r33, phi33))        

        fm.addArc(r2, phi2, r3, phi3)
        fm.addLine(r3, phi3, r5, phi5)
        fm.addLine(r5, phi5, r6, phi6)
        fm.addLine(r2, phi2, r4, phi4)
        fm.addLine(r4, phi4, r7, phi7)
        fm.addLine(r6, phi6, r11, phi11)
        fm.addLine(r5, phi5, r12, phi12)
        fm.addLine(r11, phi11, r12, phi12)
        fm.addLine(r12, phi12, r16, phi16)
        fm.addArc(r16, phi16, r17, phi17)
        fm.addLine(r7, phi7, r14, phi14)
        fm.addLine(r4, phi4, r13, phi13)
        fm.addLine(r13, phi13, r15, phi15)
        fm.addLine(r13, phi13, r14, phi14)
        fm.addArc(r34, phi34, r15, phi15)
        fm.addArc(r35, phi35, r18, phi18)

        fm.mirrorZZ(0, 1, self.group)
        

    def drawSegmentOld(self):
        # find midpoint of tooth in cartesian
        rtmid = self.p.ri
        phitmid = self.p.aofs
        tmid = cmath.rect(rtmid, fm.rad(phitmid))
        # find inner corners of tooth
        tilower = tmid + (self.p.w/2)*math.sin(fm.rad(self.p.aofs)) - (self.p.w/2)*math.cos(fm.rad(self.p.aofs))*1j
        tiupper = tmid - (self.p.w/2)*math.sin(fm.rad(self.p.aofs)) + (self.p.w/2)*math.cos(fm.rad(self.p.aofs))*1j
        fm.addNode(fm.polar(tilower)[0], fm.polar(tilower)[1])
        fm.addNode(fm.polar(tiupper)[0], fm.polar(tiupper)[1])
        fm.addLine(fm.polar(tilower)[0], fm.polar(tilower)[1], fm.polar(tiupper)[0], fm.polar(tiupper)[1])
        # find outer corners of tooth
        tolower = tilower + (self.p.l)*math.cos(fm.rad(self.p.aofs)) + (self.p.l)*math.sin(fm.rad(self.p.aofs))*1j
        toupper = tiupper + (self.p.l)*math.cos(fm.rad(self.p.aofs)) + (self.p.l)*math.sin(fm.rad(self.p.aofs))*1j
        fm.addNodeZ(tolower)
        fm.addNodeZ(toupper)
        fm.addLineZZ(tilower, tolower)
        fm.addLineZZ(tiupper, toupper)

        # add inner backiron arc
        biinner0 = abs(tolower) # 0 degrees
        fm.addNodeZ(biinner0)
        fm.addArcZZ(biinner0, tolower)
        biinner1 = cmath.rect(biinner0, fm.rad(45)) # 45 degrees
        fm.addNodeZ(biinner1)
        fm.addArcZZ(toupper, biinner1)
        # add outer backiron arc
        fm.addNode(biinner0+self.p.wbi, 0)
        fm.addNode(biinner0+self.p.wbi, 45)
        fm.addArc(biinner0+self.p.wbi, 0, biinner0+self.p.wbi, 45)

        # mirror around 0degrees
        fm.mirrorZZ(0, 1, self.group)

    def draw(self):
        fm.revolve(4, self.group)

        fm.addNode(self.p.ri - self.p.g, 0)
        fm.addNode(self.p.ri - self.p.g, 180)
        fm.addArc(self.p.ri - self.p.g, 0, self.p.ri - self.p.g, 180)
        fm.addArc(self.p.ri - self.p.g, 180, self.p.ri - self.p.g, 0)

        for rphi in self.circuits:
            fm.addBlockLabel(rphi[0], rphi[1])

    @property
    def rInner(self):
        return 0

    @property
    def rOuter(self):
        return 0
