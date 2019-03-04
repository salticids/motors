import femm
import matplotlib.pyplot as plt
from femmutil import *
from materials import *
from math import pi, sin, asin


depth = 50 # depth into plane (mm)

femm.openfemm()
femm.newdocument(0) # magnetics problem
femm.mi_probdef(0, 'millimeters', 'planar', 1.e-8, depth, 30)

addMaterial(mat_Air)
addMaterial(mat_18AWG)
addMaterial(mat_NdFeB52MGOe)
addMaterial(mat_M27Steel)

femm.mi_addcircprop('A', 0, 1)
femm.mi_addcircprop('B', 0, 1)
femm.mi_addcircprop('C', 0, 1)
circuits = ['A', 'B', 'C']
femm.smartmesh(0)

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
bt = 20. # root width
hs = 20. # slot height
hstator = 30 # stator thickness

rm = rr + hm # radius to outer magnet surface
rti = rr + hm + delta # radius to inner tooth surface
rag = (rm + rti) / 2. # radius to middle of air gap
rto = rti + ht # radius to outer tooth surface
rsi = rto + hs # radius to inner stator surface

### FEMM Groups
rotorGroup = 1

coilBlockLabels = []
magnetBlockLabels = []

rotor(4, Mfrac, rsh, rr, hm, 'M-27 Steel', 'NdFeB 52 MGOe', magnetBlockLabels)
stator(6, Tfrac, rti, ht, bt, hs, hstator, coilBlockLabels)
airgap(rr+hm, rti)
singlelayerwind(3, 100, circuits, coilBlockLabels)
femm.mi_makeABC()

femm.mi_selectcircle(0, 0, rag, 4) # doesn't move block labels?
femm.mi_moverotate(0, 0, 45)
femm.mi_selectgroup(rotorGroup)
femm.mi_moverotate(0, 0, 45)

eStepCt = 20
eSteps = range(eStepCt + 1)
Imax = 20

A = []
B = []
C = []
torque = []

for i in eSteps:
    eAngle = 2.*pi*i/eStepCt
    A.append(Imax*sin(eAngle))
    femm.mi_modifycircprop('A', 1, A[i])
    B.append(Imax*sin(eAngle+(2.*pi/3.)))
    femm.mi_modifycircprop('B', 1, B[i])
    C.append(Imax*sin(eAngle+(4.*pi/3.)))
    femm.mi_modifycircprop('C', 1, C[i])
    femm.mi_saveas('pmsm.fem')
    femm.mi_analyze()
    femm.mi_loadsolution()
    femm.mo_groupselectblock(1)
    # print(femm.mo_blockintegral(22))
    torque.append(femm.mo_blockintegral(22))

plt.subplot(2, 1, 1)
plt.plot(eSteps, A)
plt.plot(eSteps, B)
plt.plot(eSteps, C)
plt.subplot(2, 1, 2)
plt.plot(eSteps, torque)
plt.show()
femm.mi_saveas('pmsm.fem')

#femm.main_maximize()

#femm.mi_zoomnatural()

input()

femm.closefemm()