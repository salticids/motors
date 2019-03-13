# local
from femmutil import *
import settings as s
# elsewhere
import femm
import matplotlib.pyplot as plt

# Nt: Number of stator teeth
# rag: Radius, rotor + airgap
# wt: Width of tooth, radial
# bt: Thickness of root (constant wrt r)
# hs: Height of slot
# tfrac: metal phase/total tooth phase
def statorTooth(Nt = s.Nt, rag = s.rag, wt = s.wt, bt = float(s.bt), hs = s.hs, tfrac = s.tfrac, cfrac = s.cfrac, wbi = s.wbi):
    s.groupMode = s.statorGroup
    # Find tooth phase
    phi = 360. / Nt
    # Find tooth metal phase
    phiM = phi*tfrac

    # draw rotor-facing surface
    addNode(rag, phiM/2.)
    addNode(rag, -phiM/2.)
    addArc(rag, -phiM/2., rag, phiM/2.)

    # draw coil-facing surface
    phiRootInt = asin((bt/2.)/(rag+wt)) * 180. / pi
    addNode(rag+wt, phiRootInt)
    addNode(rag+wt, phiM/2.)
    addArc(rag+wt, phiRootInt, rag+wt, phiM/2.)
    addNode(rag+wt, -phiRootInt)
    addNode(rag+wt, -phiM/2.)
    addArc(rag+wt, -phiM/2., rag+wt, -phiRootInt)

    # Connect tooth surfaces
    addLine(rag, phiM/2., rag+wt, phiM/2.)
    addLine(rag, -phiM/2., rag+wt, -phiM/2.)

    # draw coil-facing stator surface
    r = rag + wt + hs
    phiRootExt = asin((bt/2.)/(r)) * 180. / pi
    addNode(r, phiRootExt)
    addNode(r, phi/2.)
    addArc(r, phiRootExt, r, phi/2.)
    addNode(r, -phiRootExt)
    addNode(r, -phi/2.)
    addArc(r, -phi/2., r, -phiRootExt)

    # Connect tooth to stator
    addLine(rag+wt, phiRootInt, rag+wt+hs, phiRootExt)
    addLine(rag+wt, -phiRootInt, rag+wt+hs, -phiRootExt)

    # draw back iron boundary
    r = rag + wt + hs + wbi
    addNode(r, phi/2.)
    addNode(r, -phi/2.)
    addArc(r, -phi/2., r, phi/2.)

    # draw coil surface
    r = rag + wt
    phiC = cfrac*phi
    addNode(r, phiC/2.)
    addNode(r, -phiC/2.)
    addNode(r+hs, phiC/2.)
    addNode(r+hs, -phiC/2.)
    if(cfrac > tfrac): # coil broader than tooth 
        addArc(r, phiM/2., r, phiC/2.)
        addArc(r, -phiC/2., r, -phiM/2.)
    elif(tfrac < cfrac): # tooth broader than coil
        addArc(r, phiC/2., r, phiM/2.)
        addArc(r, -phiM/2., r, -phiC/2.)
        # note no need for arc if tfrac == cfrac
    addLine(r, phiC/2., r+hs, phiC/2.)
    addLine(r, -phiC/2., r+hs, -phiC/2.)

    # glob['groupMode'] = -1
    s.groupMode = -1

def rotorTooth(Nm = s.Nm, rsh = s.rsh, rr = s.rr, hm = s.hm, dm = s.dm, mfrac = s.mfrac):
    # Let everything drawn be in rotorGroup
    s.groupMode = s.rotorGroup

    # Find tooth phase
    phi = 360./Nm

    ### Draw shaft region
    addNode(rsh, phi/2.)
    addNode(rsh, -phi/2.)
    addArc(rsh, -phi/2., rsh, phi/2.)

    ### Draw magnet
    r = rr - dm
    phiM = mfrac * phi
    # Interior surface
    addNode(r, phiM/2.)
    addNode(r, -phiM/2.)
    addArc(r, -phiM/2., r, phiM/2.)
    # Exterior surface
    r = rr - dm + hm
    addNode(r, phiM/2.)
    addNode(r, -phiM/2.)
    addArc(r, -phiM/2., r, phiM/2.)
    # Counterclockwise surface
    addLine(rr - dm, phiM/2., rr - dm + hm, phiM/2.)
    # Clockwise surface
    addLine(rr - dm, -phiM/2., rr - dm + hm, -phiM/2.)

    ### Draw rotor boundary
    # Counterclockwise segment
    addNode(rr, phiM/2.)
    addNode(rr, phi/2.)
    addArc(rr, phiM/2., rr, phi/2.)
    # Clockwise segment
    addNode(rr, -phiM/2.)
    addNode(rr, -phi/2.)
    addArc(rr, -phi/2., rr, -phiM/2.)               

    # Add magnet block label
    r = ((rr - dm) + (rr + hm - dm))/2.
    addBlockLabel(r, 0)
    setMat(r, 0, 'NdFeB 32 MGOe', s.rotorGroup)

    
    # Clear groupmode
    s.groupMode = -1 

def revolveStator(Nt):
    femm.mi_selectgroup(s.statorGroup)
    phi = 360./Nt
    femm.mi_copyrotate(0, 0, phi, Nt-1)
    femm.mi_clearselected()

def generateWindings(Nt, wind = 100):
    s.groupMode = s.statorGroup
    for i in range(int(Nt)):
        r = ((s.rag + s.wt) + (s.rag + s.wt + s.hs))/2.
        phi = 360./s.Nt
        phii = (360. * i / s.Nt)
        phiofs = ((phi*s.cfrac)/2.) - 1
        addBlockLabel(r, phii-phiofs, s.statorCoilLabels)
        # setCircZ(s.statorCoilLabels[2*i], '18 AWG', circ, wind)
        addBlockLabel(r, phii+phiofs, s.statorCoilLabels)
        # setCircZ(s.statorCoilLabels[2*i + 1], '18 AWG', circ, -wind)
    s.groupMode = -1

def windSingleLayer(Nt, wind = 100, mat = '18 AWG', circuits = 3):
    for i in range(0, int(Nt), 2):
        circ = chr(ord('A') + (int(i/2)%circuits))
        setCircZ(s.statorCoilLabels[2*i], mat, circ, -wind, s.statorGroup)
        setCircZ(s.statorCoilLabels[2*i+1], mat, circ, wind, s.statorGroup)

def windDoubleLayer(Nt, wind = 100, mat = '18 AWG', circuits = 3):
    for i in range(int(Nt)):
        circ = chr(ord('A') + (i%circuits))
        setCircZ(s.statorCoilLabels[2*i], mat, circ, -wind, s.statorGroup)
        setCircZ(s.statorCoilLabels[2*i+1], mat, circ, wind, s.statorGroup)

def revolveRotor(Nm):
    femm.mi_selectgroup(s.rotorGroup)
    phi = 360./Nm
    femm.mi_copyrotate(0, 0, phi, Nm-1)
    femm.mi_clearselected()
    # add radial labels
    s.groupMode = s.rotorGroup
    if s.rsh > 0:
        addBlockLabel(0, 0)
        setMat(0, 0, 'Air', s.rotorGroup)
    r = (s.rsh + s.rr - s.dm)/2.
    addBlockLabel(r, 0)
    setMat(r, 0, 'M-27 Steel', s.rotorGroup)
    # flip every other magnet
    phi = 360./Nm
    r = ((s.rr - s.dm) + (s.rr + s.hm - s.dm))/2.
    for i in range(int(Nm)):
        if i % 2 == 1:
            phii = i*phi
            setMagnet(r, phii, 'NdFeB 32 MGOe', phii + 180, s.rotorGroup)
    s.groupMode = -1
            
def finish():
    clearGroup(0)
    # add air gap label
    r = ((s.rr + s.hm - s.dm) + s.rag)/2.
    addBlockLabel(r, 0)
    setMat(r, 0, 'Air')
    # add stator block label
    r = ((s.rag + s.wt + s.hs) + (s.rag + s.wt + s.hs + s.wbi))/2.
    addBlockLabel(r, 0)
    setMat(r, 0, 'M-27 Steel')
    # add external air gap label
    r = s.rag + s.wt + s.hs + s.wbi + 5
    addBlockLabel(r, 0)
    setMat(r, 0, 'Air')
    zoom()
    femm.mi_makeABC()

def reset():
    clearGroup(0)
    clearGroup(s.rotorGroup)
    clearGroup(s.statorGroup)

def initFemm(depth = 50):
    femm.openfemm()
    femm.newdocument(0)
    femm.mi_probdef(0, 'millimeters', 'planar', 1.e-8, depth, 30)
    femm.mi_hidegrid()
    femm.smartmesh(0) # coarsens mesh
    initMaterials()
    initCircuits()
    femm.mi_saveas('parametric.fem')

def initMaterials():
    femm.mi_getmaterial('Air')
    femm.mi_getmaterial('18 AWG')
    femm.mi_getmaterial('NdFeB 32 MGOe')
    femm.mi_getmaterial('M-27 Steel')

def initCircuits():
    femm.mi_addcircprop('A', s.IA, 1)
    femm.mi_addcircprop('B', s.IB, 1)
    femm.mi_addcircprop('C', s.IC, 1)

def updateCircuits():
    femm.mi_modifycircprop('A', 1, s.IA)
    femm.mi_modifycircprop('B', 1, s.IB)
    femm.mi_modifycircprop('C', 1, s.IC)

def rotateRotor(angle):
    rot(angle - s.rotorAngle)
    s.rotorAngle = angle

def procRotorTorque():
    femm.mi_saveas('parametric.fem')
    femm.mi_analyze()
    femm.mi_loadsolution()
    femm.mo_groupselectblock(s.rotorGroup)
    print(femm.mo_blockintegral(22))
    return femm.mo_blockintegral(22)

def deinitFemm():
    femm.closefemm()

def plot(x, y, show = True):
    plt.plot(x, y)
    if show:
        plt.show()

def plotshow():
    plt.show()

def main():
    initFemm()
    rotorTooth()
    statorTooth()
    # revolveRotor(s.Nm)
    revolveStator(s.Nt)
    generateWindings(s.Nt)
    windDoubleLayer(s.Nt)
    revolveRotor(s.Nm)
    finish()
    zoom()
    input()
    deinitFemm()

if __name__ == '__main__':
    main()