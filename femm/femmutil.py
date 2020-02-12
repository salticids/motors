### FEMMUtil.py
# utilities for drawing with FEMM using polar coordinates and other common tasks
# phi in degrees in all cases

import cmath
import math

import femm

femmgroupmode = 0

def initFemm(depth = 50, sm = False, filename = 'test.fem'):
    femm.openfemm()
    femm.newdocument(0)
    femm.mi_probdef(0, 'millimeters', 'planar', 1.e-8, depth, 30)
    femm.mi_hidegrid()
    # femm.smartmesh(sm)
    femm.mi_saveas(filename)

def closeFemm(filename = 'test.fem'):
    femm.mi_saveas(filename)
    femm.closefemm()

def makeCircuit(name, current = 0, series = 1):
    femm.mi_addcircprop(name, current, series)

def modCircuit(name, current = 0, series = 1):
    femm.mi_modifycircprop(name, series, current)

def abc():
    femm.mi_makeABC()

def analyze(flag=1):
    femm.mi_analyze(flag)
    femm.mi_loadsolution()

def postGetTorque(group):
    femm.mo_groupselectblock(group)
    T = femm.mo_blockintegral(22)
    femm.mo_clearblock()
    return T

def rad(x):
    return x * math.pi / 180

def deg(x):
    return x * 180 / math.pi

# x is complex number
# returns r, phi pair with phi in degrees
def polar(x):
    r, phi = cmath.polar(x)
    phi = deg(phi)
    return r, phi

def zoom():
    femm.mi_refreshview()
    femm.mi_zoomnatural()

def clearGroup(group):
    if group != 0:
        clearGroup(0)
    femm.mi_selectgroup(group)
    femm.mi_deleteselected()
    femm.mi_clearselected()

def addNode(r, phi, group = -1):
    if group == -1:
        group = femmgroupmode
    n = cmath.rect(r, rad(phi))
    femm.mi_addnode(n.real, n.imag)
    femm.mi_selectnode(n.real, n.imag)
    femm.mi_setgroup(group)
    femm.mi_clearselected()

def addBlockLabel(r, phi, group = -1):
    if group == -1:
        group = femmgroupmode
    n = cmath.rect(r, rad(phi))
    femm.mi_addblocklabel(n.real, n.imag)
    femm.mi_selectlabel(n.real, n.imag)
    femm.mi_setgroup(group)
    femm.mi_clearselected()
    return n

def addArc(r1, phi1, r2, phi2, group = -1):
    if group == -1:
        group = femmgroupmode
    n1 = cmath.rect(r1, rad(phi1))
    n2 = cmath.rect(r2, rad(phi2))
    femm.mi_addarc(n1.real, n1.imag, n2.real, n2.imag, abs(phi1-phi2), 10)
    # select middle of arc for adding group
    # todo: better guess at point on arc (unpredictable if r1 != r2)
    n = cmath.rect((r1+r2)/2., rad((phi1+phi2)/2.))
    femm.mi_selectarcsegment(n.real, n.imag)
    femm.mi_setgroup(group)
    femm.mi_clearselected()

# draw line using polar coordinates
def addLine(r1, phi1, r2, phi2, group = -1):
    if group == -1:
        group = femmgroupmode
    n1 = cmath.rect(r1, rad(phi1))
    n2 = cmath.rect(r2, rad(phi2))
    femm.mi_addsegment(n1.real, n1.imag, n2.real, n2.imag)
    # select middle of arc for adding group
    # todo: better guess at point on line (unpredictable if phi1 != phi2)
    n = cmath.rect((r1 + r2)/2., rad((phi1 + phi2)/2.))
    femm.mi_selectsegment(n.real, n.imag)
    femm.mi_setgroup(group)
    femm.mi_clearselected()

def getMat(mat):
    femm.mi_getmaterial(mat)

def setMat(r, phi, mat, group = -1):
    if group == -1:
        group = femmgroupmode
    n = cmath.rect(r, rad(phi))
    femm.mi_selectlabel(n.real, n.imag)
    femm.mi_setblockprop(mat, 1, 0, '<None>', 0, group, 0)
    femm.mi_clearselected()

def setCirc(r, phi, mat, circuit, turns, group = -1):
    if group == -1:
        group = femmgroupmode
    n = cmath.rect(r, rad(phi))
    femm.mi_selectlabel(n.real, n.imag)
    femm.mi_setblockprop(mat, 1, 0, circuit, 0, group, turns)
    femm.mi_clearselected()

# setCirc but with complex position instead of r,phi
def setCircZ(n, mat, circuit,  turns, group = -1):
    if group == -1:
        group = femmgroupmode
    femm.mi_selectlabel(n.real, n.imag)
    femm.mi_setblockprop(mat, 1, 0, circuit, 0, group, turns)
    femm.mi_clearselected()

def setMagnet(r, phi, mat, magdir, group = -1):
    if group == -1:
        group = femmgroupmode
    n = cmath.rect(r, rad(phi))
    femm.mi_selectlabel(n.real, n.imag)
    femm.mi_setblockprop(mat, 1, 0, '<None>', magdir, group, 0)
    femm.mi_clearselected()

def revolve(segments, group):
    femm.mi_selectgroup(group)
    phiStep = 360/segments
    femm.mi_copyrotate(0, 0, phiStep, segments-1)
    femm.mi_clearselected()

def rot(angle, group):
    femm.mi_selectgroup(group)
    femm.mi_moverotate(0, 0, angle)
    femm.mi_clearselected()

# Fill space between constructs with material label
# determines all regions without constructs & assigns material to them
# radii: array of construct radii, organized [inner, outer, inner, outer, ...
def fillEmpty(radii, mat='Air', group=0):
    assert len(radii)%2 == 0 # assert only pairs are included
    for radius in radii:
        assert radius >= 0
    # Get first pair
    zones = []
    for i in range(int(len(radii)/2)): # for regions passed...
        newZones = [radii[i*2], radii[(i*2)+1]]
        for j in range(int(len(zones)/2)): # for nonoverlapping regions...
            # left overlap: replace newZones leftbound with zones leftbound
            if zones[(j*2)] < newZones[0] and zones[(j*2)+1] >= newZones[0] and zones[(j*2)+1] <= newZones[1]:
                newZones[0] = zones[j*2]
            # right overlap: replace newZones rightbound with zones rightbound
            elif zones[j*2] >= newZones[0] and zones[j*2] <= newZones[1] and zones[(j*2)+1] > newZones[1]:
                newZones[1] = zones[(j*2)+1]
            # total eclipse: replace newZone with zone
            elif zones[j*2] < newZones[0] and zones[(j*2)+1] > newZones[1]:
                newZones[0] = zones[j*2]
                newZones[1] = zones[(j*2)+1]
            # total inside: ignore zone
            elif zones[j*2] >= newZones[0] and zones[(j*2)+1] <= newZones[1]:
                pass
            # no overlap: append zone to newZone
            else:
                newZones.append(zones[j*2])
                newZones.append(zones[(j*2)+1])
        zones = newZones
    zonePairs = []
    for i in range(int(len(zones)/2)):
        zonePairs.append([zones[2*i], zones[(2*i)+1]])
    def sortbyfirst(pair):
        return pair[0]
    zonePairs.sort(key=sortbyfirst)

    if len(zonePairs) > 0:
        # innermost label
        r = zonePairs[0][0]/2
        if r > 0:
            addBlockLabel(r, 0, group)
            setMat(r, 0, mat, group)
        # outermost label
        r = zonePairs[-1][1] + 5
        addBlockLabel(r, 0, group)
        setMat(r, 0, mat, group)
        # other labels
        for i in range(len(zonePairs)-1):
            r = (zonePairs[i][1] + zonePairs[i+1][0])/2
            addBlockLabel(r, 0, group)
            setMat(r, 0, mat, group)
    else:
        addBlockLabel(0, 0, group)
        setMat(0, 0, mat, group)