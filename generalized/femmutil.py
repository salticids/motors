### FEMMUtil.py
# utilities for drawing with FEMM using polar coordinates and other common tasks
# phi in degrees in all cases

import femm
import cmath
import math

def initFemm(depth = 50, sm = False, filename = 'test.fem'):
    femm.openfemm()
    femm.newdocument(0)
    femm.mi_probdef(0, 'millimeters', 'planar', 1.e-8, depth, 30)
    femm.mi_hidegrid()
    femm.smartmesh(sm)
    femm.mi_saveas(filename)

def closeFemm(filename = 'test.fem'):
    femm.mi_saveas(filename)
    femm.closefemm()

def makeCircuit(name, current = 0, series = 1):
    femm.mi_addcircprop(name, current, series)

def rad(x):
    return x * math.pi / 180

def zoom():
    femm.mi_refreshview()
    femm.mi_zoomnatural()

def clearGroup(group):
    if group != 0:
        clearGroup(0)
    femm.mi_selectgroup(group)
    femm.mi_deleteselected()
    femm.mi_clearselected()

def addNode(r, phi, group = 0):
    n = cmath.rect(r, rad(phi))
    femm.mi_addnode(n.real, n.imag)
    femm.mi_selectnode(n.real, n.imag)
    femm.mi_setgroup(group)
    femm.mi_clearselected()

def addBlockLabel(r, phi, group = 0):
    n = cmath.rect(r, rad(phi))
    femm.mi_addblocklabel(n.real, n.imag)
    femm.mi_selectlabel(n.real, n.imag)
    femm.mi_setgroup(group)
    femm.mi_clearselected()
    return n

def addArc(r1, phi1, r2, phi2, group = 0):
    n1 = cmath.rect(r1, rad(phi1))
    n2 = cmath.rect(r2, rad(phi2))
    femm.mi_addarc(n1.real, n1.imag, n2.real, n2.imag, abs(phi1-phi2), 10)
    # select middle of arc for adding group
    # (unpredictable if r1 != r2)
    n = cmath.rect((r1+r2)/2., rad((phi1+phi2)/2.))
    femm.mi_selectarcsegment(n.real, n.imag)
    femm.mi_setgroup(group)
    femm.mi_clearselected()

# draw line using polar coordinates
def addLine(r1, phi1, r2, phi2, group = 0):
    n1 = cmath.rect(r1, rad(phi1))
    n2 = cmath.rect(r2, rad(phi2))
    femm.mi_addsegment(n1.real, n1.imag, n2.real, n2.imag)
    # select middle of arc for adding group
    # (unpredictable if phi1 != phi2)
    n = cmath.rect((r1 + r2)/2., rad((phi1 + phi2)/2.))
    femm.mi_selectsegment(n.real, n.imag)
    femm.mi_setgroup(group)
    femm.mi_clearselected()

def getMat(mat):
    femm.mi_getmaterial(mat)

def setMat(r, phi, mat, group=0):
    n = cmath.rect(r, rad(phi))
    femm.mi_selectlabel(n.real, n.imag)
    femm.mi_setblockprop(mat, 1, 0, '<None>', 0, group, 0)
    femm.mi_clearselected()

def setCirc(r, phi, mat, circuit, turns, group = 0):
    n = cmath.rect(r, rad(phi))
    femm.mi_selectlabel(n.real, n.imag)
    femm.mi_setblockprop(mat, 1, 0, circuit, 0, group, turns)
    femm.mi_clearselected()

# setCirc but with complex position instead of r,phi
def setCircZ(n, mat, circuit,  turns, group = 0):
    femm.mi_selectlabel(n.real, n.imag)
    femm.mi_setblockprop(mat, 1, 0, circuit, 0, group, turns)
    femm.mi_clearselected()

def setMagnet(r, phi, mat, magdir, group = 0):
    n = cmath.rect(r, rad(phi))
    femm.mi_selectlabel(n.real, n.imag)
    femm.mi_setblockprop(mat, 1, 0, '<None>', magdir, group, 0)
    femm.mi_clearselected()

def revolve(segments, group):
    femm.mi_selectgroup(group)
    phiStep = 360/segments
    femm.mi_copyrotate(0, 0, phiStep, segments-1)
    femm.mi_clearselected

def rot(angle, group):
    femm.mi_selectgroup(group)
    femm.mi_moverotate(0, 0, angle)
    femm.mi_clearselected()

