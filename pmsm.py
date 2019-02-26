import femm
import cmath as cm
from math import pi, asin

def rad(x):
    return x * pi / 180.

# PARAMETERS
rsh = 25. # shaft radius (mm)
rs = 40. # rotor inner radius (mm)
delta = 5. # air gap
Nm = 6 # number of rotor magnets
Mfrac = 0.8
hm = 10.

Nt = 36 # number of teeth
Tfrac = 0.8
ht = 5. # tooth height
bt = 5. # tooth thickness
hs = 20. # slot height

rstator = 100. # total machine radius

femm.openfemm()

femm.newdocument(0); # magnetics problem
femm.mi_probdef(0, 'millimeters', 'planar', 1.e-8, 0, 30)

# draw rotor
femm.mi_drawarc(rsh, 0, -rsh, 0, 180, 10)
femm.mi_drawarc(-rsh, 0, rsh, 0, 180, 10)
femm.mi_drawarc(rs, 0, -rs, 0, 180, 10)
femm.mi_drawarc(-rs, 0, rs, 0, 180, 10)

# draw rotor magnets
for i in range(Nm):
    phi = 360 * i / Nm
    phi_total = 360 * (Mfrac) / Nm
    phi_plus = phi + phi_total / 2.
    phi_minus = phi - phi_total / 2.
    r = rs + hm
    z = cm.rect(r, rad(phi))
    z1 = cm.rect(r, rad(phi_minus))
    z1s = cm.rect(rs, rad(phi_minus))
    z2 = cm.rect(r, rad(phi_plus))
    z2s = cm.rect(rs, rad(phi_plus))
    femm.mi_addnode(z.real, z.imag)
    femm.mi_addnode(z1s.real, z1s.imag)
    femm.mi_addnode(z2s.real, z2s.imag)
    femm.mi_drawarc(z1.real, z1.imag, z2.real, z2.imag, phi_total, 10)
    femm.mi_addsegment(z1s.real, z1s.imag, z1.real, z1.imag)
    femm.mi_addsegment(z2s.real, z2s.imag, z2.real, z2.imag)

# draw teeth
for i in range(Nt):
    phi = 360 * i / Nt
    phi_total = 360 * (Tfrac) / Nt
    phi_plus = phi + phi_total / 2.
    phi_minus = phi - phi_total / 2.
    r = rs + hm + delta
    z = cm.rect(r, rad(phi))
    z1 = cm.rect(r, rad(phi_minus))
    z1s = cm.rect(r + ht, rad(phi_minus))
    z2 = cm.rect(r, rad(phi_plus))
    z2s = cm.rect(r + ht, rad(phi_plus))
    femm.mi_addnode(z.real, z.imag)
    femm.mi_addnode(z1s.real, z1s.imag)
    femm.mi_addnode(z2s.real, z2s.imag)
    femm.mi_drawarc(z1.real, z1.imag, z2.real, z2.imag, phi_total, 10)
    femm.mi_addsegment(z1s.real, z1s.imag, z1.real, z1.imag)
    femm.mi_addsegment(z2s.real, z2s.imag, z2.real, z2.imag)

    phi_tooth = asin((bt/2.)/(r+ht)) * 180. / pi
    ztoothccw = cm.rect(r+ht, rad(phi+phi_tooth))
    ztoothcw = cm.rect(r+ht, rad(phi-phi_tooth))
    femm.mi_addnode(ztoothccw.real, ztoothccw.imag)
    femm.mi_addnode(ztoothcw.real, ztoothcw.imag)

    femm.mi_addarc(z1s.real, z1s.imag, ztoothcw.real, ztoothcw.imag, (phi_total - phi_tooth) / 2., 10)
    femm.mi_addarc(ztoothccw.real, ztoothccw.imag, z2s.real, z2s.imag, (phi_total - phi_tooth) / 2., 10)

    phi_toothbase = asin((bt/2.)/(r+ht+hs)) * 180. / pi
    ztoothbasecw = cm.rect(r+ht+hs, rad(phi - phi_toothbase))
    ztoothbaseccw = cm.rect(r+ht+hs, rad(phi + phi_toothbase))
    femm.mi_addnode(ztoothbasecw.real, ztoothbasecw.imag)
    femm.mi_addnode(ztoothbaseccw.real, ztoothbaseccw.imag)

    femm.mi_drawline(ztoothcw.real, ztoothcw.imag, ztoothbasecw.real, ztoothbasecw.imag)
    femm.mi_drawline(ztoothccw.real, ztoothccw.imag, ztoothbaseccw.real, ztoothbaseccw.imag)

    rstatorint = r + ht + hs
    # draw stator inside
    phistator1 = phi - phi_toothbase
    phistator2 = phi - (360. / Nt) + phi_toothbase
    phistatortotal = (360. / Nt) - (2 * phi_toothbase)
    zstator1 = cm.rect(rstatorint, rad(phistator1))
    zstator2 = cm.rect(rstatorint, rad(phistator2))
    femm.mi_drawarc(zstator2.real, zstator2.imag, zstator1.real, zstator1.imag, phistatortotal, 10)

# draw stator outside
femm.mi_drawarc(rstator, 0, -rstator, 0, 180, 10)
femm.mi_drawarc(-rstator, 0, rstator, 0, 180, 10)

femm.mi_makeABC()

femm.mi_zoomnatural()

femm.mi_saveas('pmsm.fem')

input()
