import femm
from femmutil import *
from materials import *
from math import pi, asin

depth = 50 # depth into plane (mm)

femm.openfemm()
femm.newdocument(0) # magnetics problem
femm.mi_probdef(0, 'millimeters', 'planar', 1.e-8, depth, 30)

addMaterial(mat_Air)
addMaterial(mat_18AWG)
addMaterial(mat_NdFeB52MGOe)
addMaterial(mat_M27Steel)
femm.mi_addcircprop('A', 20, 1)
femm.mi_addcircprop('B', 0, 1)
femm.mi_addcircprop('C', -20, 1)
circuits = ['A', 'B', 'C']

### PARAMETERS

Nm = 18 # number of rotor magnets
rsh = 10. # shaft radius (mm)
rr = 40. # rotor inner radius (mm)
delta = 5. # air gap
Mfrac = 0.8
hm = 10.

Nt = 20 # number of teeth; number of slots
Tfrac = 0.8
ht = 5. # tooth height
bt = 10. # root width
hs = 20. # slot height
hstator = 30 # stator thickness

rm = rr + hm # radius to outer magnet surface
rti = rr + hm + delta # radius to inner tooth surface
rto = rti + ht # radius to outer tooth surface
rsi = rto + hs # radius to inner stator surface

coilBlockLabels = []
magnetBlockLabels = []

rotor(4, Mfrac, rsh, rr, hm, 'M-27 Steel', 'NdFeB 52 MGOe', magnetBlockLabels)
stator(6, Tfrac, rti, ht, bt, hs, hstator, coilBlockLabels)
airgap(rr+hm, rti)
singlelayerwind(3, 100, circuits, coilBlockLabels)

femm.mi_makeABC()

femm.main_maximize()

femm.mi_zoomnatural()

femm.mi_saveas('pmsm.fem')

input()

femm.closefemm()