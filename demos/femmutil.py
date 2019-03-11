import femm
import cmath as cm
# from materials import *
from math import pi, asin, sin

from settings import *

def rad(x):
    return x * pi / 180.

def addNode(r, phi):
    n = cm.rect(r, rad(phi))
    femm.mi_addnode(n.real, n.imag)

def addBlockLabel(r, phi):
    n = cm.rect(r, rad(phi))
    femm.mi_addblocklabel(n.real, n.imag)

# draw arc using polar coordinates (deg)
def addArc(r1, phi1, r2, phi2):
    n1 = cm.rect(r1, rad(phi1))
    n2 = cm.rect(r2, rad(phi2))
    femm.mi_addarc(n1.real, n1.imag, n2.real, n2.imag, abs(phi1-phi2), 10)

# draw line using polar coordinates
def addLine(r1, phi1, r2, phi2):
    n1 = cm.rect(r1, rad(phi1))
    n2 = cm.rect(r2, rad(phi2))
    femm.mi_addsegment(n1.real, n1.imag, n2.real, n2.imag)

def setMat(r, phi, mat, group=0):
    n = cm.rect(r, rad(phi))
    femm.mi_selectlabel(n.real, n.imag)
    femm.mi_setblockprop(mat, 1, 0, '<None>', 0, group, 0)
    femm.mi_clearselected()
def setMatxy(x, y, mat, group=0):
    femm.mi_selectlabel(x, y)
    femm.mi_setblockprop(mat, 1, 0, '<None>', 0, group, 0)
    femm.mi_clearselected()

def setCirc(r, phi, mat, circuit, turns):
    n = cm.rect(r, rad(phi))
    femm.mi_selectlabel(n.real, n.imag)
    femm.mi_setblockprop(mat, 1, 0, circuit, 0, 0, turns)
    femm.mi_clearselected()

def setMagnet(r, phi, mat, magdir, group=0):
    n = cm.rect(r, rad(phi))
    femm.mi_selectlabel(n.real, n.imag)
    femm.mi_setblockprop(mat, 1, 0, '<None>', magdir, group, 0)
    femm.mi_clearselected()

def rot(r, angle):
    femm.mi_selectgroup(rotorGroup)
    femm.mi_moverotate(0, 0, angle)
    femm.mi_clearselected()

def emodesine(circuits, Imax, angle):
    for i in range(circuits):
        circuit = chr(ord('A')+i)
        I = Imax * sin(rad(angle) + (2.*pi*i/circuits))
        femm.mi_modifycircprop(circuit, 1, I)

# Number of magnets, 
# fractional magnet width,
# shaft radius,
# rotor body radius, 
# height of magnets,
# rotor material,
# magnet material
# array of magnet block labels
def rotor(Nm, Mfrac, rsh, rr, hm, matRotor, matMagnet, magnetBlockLabels):

    # find pitch of magnets
    pitchMagnet = 360. * Mfrac / Nm

    # shaft
    femm.mi_drawarc(rsh, 0, -rsh, 0, 180, 10)
    femm.mi_drawarc(-rsh, 0, rsh, 0, 180, 10)
    # rotor
    femm.mi_drawarc(rr, 0, -rr, 0, 180, 10)
    femm.mi_drawarc(-rr, 0, rr, 0, 180, 10)

    # draw rotor magnets
    for i in range(Nm):
        # magnet center position
        phi = 360 * i / Nm
        # ccw magnet edge
        phi_plus = phi + pitchMagnet / 2.
        # cw magnet edge
        phi_minus = phi - pitchMagnet / 2.

        # add block label to magnet
        magnetBlockLabels.append([(rr + rr + hm) / 2., phi])
        addBlockLabel(magnetBlockLabels[len(magnetBlockLabels)-1][0],magnetBlockLabels[len(magnetBlockLabels)-1][1])
        if i % 2 == 0:
            setMagnet(magnetBlockLabels[len(magnetBlockLabels)-1][0],magnetBlockLabels[len(magnetBlockLabels)-1][1], matMagnet, phi, rotorGroup)
        else:
            setMagnet(magnetBlockLabels[len(magnetBlockLabels)-1][0],magnetBlockLabels[len(magnetBlockLabels)-1][1], matMagnet, phi - 180., rotorGroup)

        
        r = rr + hm
        z = cm.rect(r, rad(phi))
        z1 = cm.rect(r, rad(phi_minus))
        z1s = cm.rect(rr, rad(phi_minus))
        z2 = cm.rect(r, rad(phi_plus))
        z2s = cm.rect(rr, rad(phi_plus))
        femm.mi_addnode(z.real, z.imag)
        femm.mi_addnode(z1s.real, z1s.imag)
        femm.mi_addnode(z2s.real, z2s.imag)
        femm.mi_drawarc(z1.real, z1.imag, z2.real, z2.imag, pitchMagnet, 10)
        femm.mi_addsegment(z1s.real, z1s.imag, z1.real, z1.imag)
        femm.mi_addsegment(z2s.real, z2s.imag, z2.real, z2.imag)

    # shaft block label
    if(rsh > 0):
        addBlockLabel(0, 0)
        setMat(0, 0, 'Air')
    # rotor body block label
    addBlockLabel((rsh + rr) / 2., 0)
    setMat((rsh + rr) / 2., 0, 'M-27 Steel', 1)

    femm.mi_selectcircle(0, 0, rr + hm + 1, 4)
    femm.mi_setgroup(rotorGroup)
    femm.mi_clearselected()


# number of teeth,
# fractional tooth pitch
# radius to inner tooth surface,
# radial thickness of tooth
# thickness of root
# slot height
# stator radial thickness
# array of coil block labels
def stator(Nt, Tfrac, rt, ht, bt, hs, hstator, coilBlockLabels):

    # radius to outer tooth surface
    rto = rt + ht
    # radius to inner stator surface
    rsi = rto + hs
    # total machine radius
    rstator = rsi + hstator

    # find angle between teeth
    phiBetweenTeeth = (360. / Nt) * (1. - Tfrac)

    # find angle between roots 
    phiRoot = asin((bt / 2.)/rsi) * 180. / pi
    phiBetweenRoots = (360. / Nt) - (2. * phiRoot)


    # draw teeth
    for i in range(Nt):
        phi = 360 * i / Nt
        pitchTooth = 360 * (Tfrac) / Nt
        phi_plus = phi + pitchTooth / 2.
        phi_minus = phi - pitchTooth / 2.
        r = rt
        z = cm.rect(rt, rad(phi))
        z1 = cm.rect(rt, rad(phi_minus))
        z1s = cm.rect(rt + ht, rad(phi_minus))
        z2 = cm.rect(rt, rad(phi_plus))
        z2s = cm.rect(rt + ht, rad(phi_plus))
        femm.mi_addnode(z.real, z.imag)
        femm.mi_addnode(z1s.real, z1s.imag)
        femm.mi_addnode(z2s.real, z2s.imag)
        femm.mi_drawarc(z1.real, z1.imag, z2.real, z2.imag, pitchTooth, 10)
        femm.mi_addsegment(z1s.real, z1s.imag, z1.real, z1.imag)
        femm.mi_addsegment(z2s.real, z2s.imag, z2.real, z2.imag)

        phi_tooth = asin((bt/2.)/(rt+ht)) * 180. / pi
        ztoothccw = cm.rect(rt+ht, rad(phi+phi_tooth))
        ztoothcw = cm.rect(rt+ht, rad(phi-phi_tooth))
        femm.mi_addnode(ztoothccw.real, ztoothccw.imag)
        femm.mi_addnode(ztoothcw.real, ztoothcw.imag)

        femm.mi_addarc(z1s.real, z1s.imag, ztoothcw.real, ztoothcw.imag, (pitchTooth - phi_tooth) / 2., 10)
        femm.mi_addarc(ztoothccw.real, ztoothccw.imag, z2s.real, z2s.imag, (pitchTooth - phi_tooth) / 2., 10)

        phi_toothbase = asin((bt/2.)/(rt+ht+hs)) * 180. / pi
        ztoothbasecw = cm.rect(rt+ht+hs, rad(phi - phi_toothbase))
        ztoothbaseccw = cm.rect(rt+ht+hs, rad(phi + phi_toothbase))
        femm.mi_addnode(ztoothbasecw.real, ztoothbasecw.imag)
        femm.mi_addnode(ztoothbaseccw.real, ztoothbaseccw.imag)

        femm.mi_drawline(ztoothcw.real, ztoothcw.imag, ztoothbasecw.real, ztoothbasecw.imag)
        femm.mi_drawline(ztoothccw.real, ztoothccw.imag, ztoothbaseccw.real, ztoothbaseccw.imag)

    # Draw coil regions & stator zone
    for i in range(Nt):

        # offset to the space between teeth
        phi = (360. * i + 180.) / Nt

        # add nodes for interior coil boundary
        addNode(rto, phi)
        # add nodes for exterior coil boundary (abutt stator)
        addNode(rsi, phi)
        # draw coil separator between teeth
        addLine(rto, phi, rsi, phi)

        ### connect coil regions to teeth
        # add clockwise connection
        addArc(rto, phi - (phiBetweenTeeth / 2.), rto, phi)
        # add counterclockwise connection
        addArc(rto, phi, rto, phi + (phiBetweenTeeth / 2.))

        ### draw stator interior
        # draw clockwise connection
        addArc(rsi, phi - (phiBetweenRoots / 2.), rsi, phi)
        # draw counterclockwise connection
        addArc(rsi, phi, rsi, phi + (phiBetweenRoots / 2.))

        ### add block labels
        # clockwise segment
        coilBlockLabels.append([(rto + rsi) / 2., (phi + (phi - (phiBetweenRoots / 2.))) / 2.])
        addBlockLabel(coilBlockLabels[len(coilBlockLabels)-1][0], coilBlockLabels[len(coilBlockLabels)-1][1])
        #setCirc(coilBlockLabels[len(coilBlockLabels)-1][0], coilBlockLabels[len(coilBlockLabels)-1][1], '18 AWG', 'B', 1)
        # counterclockwise segment
        coilBlockLabels.append([(rto + rsi) / 2., (phi + (phi + (phiBetweenRoots / 2.))) / 2.])
        addBlockLabel(coilBlockLabels[len(coilBlockLabels)-1][0], coilBlockLabels[len(coilBlockLabels)-1][1])
        #setCirc(coilBlockLabels[len(coilBlockLabels)-1][0], coilBlockLabels[len(coilBlockLabels)-1][1], '18 AWG', 'B', 1)

    # draw stator outside
    femm.mi_drawarc(rstator, 0, -rstator, 0, 180, 10)
    femm.mi_drawarc(-rstator, 0, rstator, 0, 180, 10)

    # stator block label
    addBlockLabel((rsi + rstator) / 2., 0)
    setMat((rsi+rstator) / 2., 0, 'M-27 Steel')
    # beyond stator 
    addBlockLabel(rstator + 10., 0)
    setMat(rstator + 10., 0, 'Air')

### Label Air Gap
# ri = outermost rotor surface radius
# ro = innermost stator surface radius
def airgap(ri, ro):
    # air gap block label
    addBlockLabel((ri + ro) / 2., 0)
    setMat((ri + ro) / 2., 0, 'Air')

### Single Layer Winding
def singlelayerwind(poles, windings, circuits, coilBlockLabels):
    polarity = 1
    n = len(coilBlockLabels)
    for index in range(n):
        coilindex = int(((index % (n-2))+2)/4) 
        # coil = int(((slots + 1 - index) % slots) / 2)
        setCirc(coilBlockLabels[index][0], coilBlockLabels[index][1], '18 AWG', circuits[coilindex], windings*polarity)
        # setCirc(coilBlockLabels[index+1][0], coilBlockLabels[index+1][1], '18 AWG', circuits[coil], windings*polarity)
        if(index%2 == 1):
            polarity = polarity * (-1)

def doublelayerwind(poles, windings, circuits, coilBlockLabels):
    polarity = 1
    n = len(coilBlockLabels)
    for index in range(n):
        coilindex = int(((index+1)%6)/2) 
        # coil = int(((slots + 1 - index) % slots) / 2)
        setCirc(coilBlockLabels[index][0], coilBlockLabels[index][1], '18 AWG', circuits[coilindex], windings*polarity)
        # setCirc(coilBlockLabels[index+1][0], coilBlockLabels[index+1][1], '18 AWG', circuits[coil], windings*polarity)
        # if(index%2 == 1):
        polarity = polarity * (-1)
