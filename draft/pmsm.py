import femm
import matplotlib.pyplot as plt
from math import pi, sin, asin

# local files
from femmutil import *
from materials import *
from settings import *

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
femm.smartmesh(0) # turn off smartmeshing (dirty coarsen mesh line)

rotor(Nm, Mfrac, rsh, rr, hm, 'M-27 Steel', 'NdFeB 52 MGOe', magnetBlockLabels)
stator(Nt, Tfrac, rti, ht, bt, hs, hstator, coilBlockLabels)
airgap(rr+hm, rti)
doublelayerwind(3, 100, circuits, coilBlockLabels)
femm.mi_makeABC()

eStepCt = 20
eSteps = range(eStepCt + 1)
Imax = 20

A = []
B = []
C = []
torque = []

# for i in eSteps:
#     eAngle = 4.*pi*i/eStepCt
#     A.append(Imax*sin(eAngle))
#     femm.mi_modifycircprop('A', 1, A[i])
#     B.append(Imax*sin(eAngle+(2.*pi/3.)))
#     femm.mi_modifycircprop('B', 1, B[i])
#     C.append(Imax*sin(eAngle+(4.*pi/3.)))
#     femm.mi_modifycircprop('C', 1, C[i])
#     femm.mi_saveas('pmsm.fem')
#     femm.mi_analyze()
#     femm.mi_loadsolution()
#     femm.mo_groupselectblock(1)
#     # print(femm.mo_blockintegral(22))
#     torque.append(femm.mo_blockintegral(22))

# plt.subplot(2, 1, 1)
# plt.plot(eSteps, A)
# plt.plot(eSteps, B)
# plt.plot(eSteps, C)
# plt.subplot(2, 1, 2)
# plt.plot(eSteps, torque)
# plt.show()
# femm.mi_saveas('pmsm.fem')

#femm.main_maximize()

#femm.mi_zoomnatural()

# 

rotorAngle = 0
electricAngle = 0
command = ['quit']
while(True):
    userinput = input().split()
    if(len(userinput) > 0):
        command = userinput
    
    if command[0] == 'quit':
        break
    elif command[0] == 'rot' and len(command) == 2:
        rotorAngle = rotorAngle + int(command[1])
        rot(rag, command[1])
    elif command[0] == 'rotset' and len(command) == 2:
        rot(rag, int(command[1]) - rotorAngle)
        rotorAngle = int(command[1])
    elif command[0] == 'circ' and len(command) == 3:
        femm.mi_modifycircprop(command[1], 1, command[2])
    elif command[0] == 'emode' and len(command) >= 2:
        if(len(command) == 2):
            command.append(0)
        if command[1][:3] == 'sin':
            electricMode = 'sin'
            emodesine(3, I, float(command[2]))


femm.closefemm()