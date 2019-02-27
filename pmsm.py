import femm
from materials import *
import cmath as cm
from math import pi, asin

def rad(x):
    return x * pi / 180.

def addNode(r, phi):
    n = cm.rect(r, rad(phi))
    femm.mi_addnode(n.real, n.imag)

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

### PARAMETERS
rsh = 10. # shaft radius (mm)
rr = 40. # rotor inner radius (mm)
delta = 5. # air gap
Nm = 6 # number of rotor magnets
Mfrac = 0.8
hm = 10.

Nt = 50 # number of teeth
Ns = Nt # number of slots
Tfrac = 0.8
ht = 5. # tooth height
bt = 2. # tooth thickness
wRoot = bt # root width
hs = 20. # slot height

rstator = 100. # total machine radius

rti = rr + hm + delta # radius to inner tooth surface
rto = rti + ht # radius to outer tooth surface
rsi = rto + hs # radius to inner stator surface

# find angle between teeth
phiBetweenTeeth = (360. / Nt) * (1. - Tfrac)

# find angle between roots 
phiRoot = asin((wRoot / 2.)/rsi)
phiBetweenRoots = (360. / Nt) - (2. * phiRoot)

# find pitch of magnets
pitchMagnet = 360. * Mfrac / Nm
# find pitch of teeth
pitchTooth = 360. * Tfrac / Nm

femm.openfemm()

femm.newdocument(0); # magnetics problem
femm.mi_probdef(0, 'millimeters', 'planar', 1.e-8, 0, 30)

# draw rotor
femm.mi_drawarc(rsh, 0, -rsh, 0, 180, 10)
femm.mi_drawarc(-rsh, 0, rsh, 0, 180, 10)
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

# draw teeth
for i in range(Nt):
    phi = 360 * i / Nt
    pitchTooth = 360 * (Tfrac) / Nt
    phi_plus = phi + pitchTooth / 2.
    phi_minus = phi - pitchTooth / 2.
    r = rr + hm + delta
    z = cm.rect(r, rad(phi))
    z1 = cm.rect(r, rad(phi_minus))
    z1s = cm.rect(r + ht, rad(phi_minus))
    z2 = cm.rect(r, rad(phi_plus))
    z2s = cm.rect(r + ht, rad(phi_plus))
    femm.mi_addnode(z.real, z.imag)
    femm.mi_addnode(z1s.real, z1s.imag)
    femm.mi_addnode(z2s.real, z2s.imag)
    femm.mi_drawarc(z1.real, z1.imag, z2.real, z2.imag, pitchTooth, 10)
    femm.mi_addsegment(z1s.real, z1s.imag, z1.real, z1.imag)
    femm.mi_addsegment(z2s.real, z2s.imag, z2.real, z2.imag)

    phi_tooth = asin((bt/2.)/(r+ht)) * 180. / pi
    ztoothccw = cm.rect(r+ht, rad(phi+phi_tooth))
    ztoothcw = cm.rect(r+ht, rad(phi-phi_tooth))
    femm.mi_addnode(ztoothccw.real, ztoothccw.imag)
    femm.mi_addnode(ztoothcw.real, ztoothcw.imag)

    femm.mi_addarc(z1s.real, z1s.imag, ztoothcw.real, ztoothcw.imag, (pitchTooth - phi_tooth) / 2., 10)
    femm.mi_addarc(ztoothccw.real, ztoothccw.imag, z2s.real, z2s.imag, (pitchTooth - phi_tooth) / 2., 10)

    phi_toothbase = asin((bt/2.)/(r+ht+hs)) * 180. / pi
    ztoothbasecw = cm.rect(r+ht+hs, rad(phi - phi_toothbase))
    ztoothbaseccw = cm.rect(r+ht+hs, rad(phi + phi_toothbase))
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
    


# draw stator outside
femm.mi_drawarc(rstator, 0, -rstator, 0, 180, 10)
femm.mi_drawarc(-rstator, 0, rstator, 0, 180, 10)

addMaterial(mat_Air)
femm.mi_addblocklabel(0, 0)
femm.mi_selectlabel(0, 0)
femm.mi_setblockprop('Air', 0, 1, '<None>', 0, 0, 0)


femm.mi_makeABC()

femm.mi_zoomnatural()

femm.mi_saveas('pmsm.fem')

input()

femm.closefemm()