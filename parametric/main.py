# local
from femmutil import *
import settings as s
# elsewhere
import femm

# Nt: Number of stator teeth
# rag: Radius, rotor + airgap
# wt: Width of tooth, radial
# bt: Thickness of root (constant wrt r)
# hs: Height of slot
# tfrac: metal phase/total tooth phase
def statorTooth(Nt = s.Nt, rag = s.rag, wt = s.wt, bt = float(s.bt), hs = s.hs, tfrac = s.tfrac, cfrac = s.cfrac):
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

def rotorTooth():
    # Let everything drawn be in rotorGroup
    s.groupMode = s.rotorGroup

    


    # Clear groupmode
    s.groupMode = -1 

def revolveStator(Nt):
    femm.mi_selectgroup(s.statorGroup)
    phi = 360./Nt
    femm.mi_copyrotate(0, 0, phi, Nt-1)
    femm.mi_clearselected()

def initFemm(depth = 50):
    femm.openfemm()
    femm.newdocument(0)
    femm.mi_probdef(0, 'millimeters', 'planar', 1.e-8, depth, 30)
    femm.mi_hidegrid()
    femm.mi_saveas('parametric.fem')

def deinitFemm():
    femm.closefemm()

def main():
    initFemm()
    statorTooth(6, 30, 8, 15, 30, .8, .6)
    revolveStator(6)
    input()
    deinitFemm()

if __name__ == '__main__':
    main()