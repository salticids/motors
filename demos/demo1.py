import femm
from materials import *

femm.openfemm()
femm.newdocument(0) # magnetics problem
femm.mi_probdef(0, 'millimeters', 'planar', 1.e-8, 50, 30)
femm.smartmesh(0)

femm.mi_addnode(0, 0)
femm.mi_addnode(1, 0)
femm.mi_addnode(0, 1)
femm.mi_addnode(1, 1)

femm.mi_addsegment(0, 0, 1, 0)
femm.mi_addsegment(1, 1, 0, 1)

femm.mi_addarc(1, 0, 1, 1, 180, 10)
femm.mi_addarc(0, 1, 0, 0, 180, 10)

femm.mi_addnode(0, 2)
femm.mi_addnode(1, 2)
femm.mi_addnode(0, -1)
femm.mi_addnode(1, -1)
femm.mi_addsegment(0, 2, 1, 2)
femm.mi_addsegment(1, 1, 1, 2)
femm.mi_addsegment(0, 1, 0, 2)
femm.mi_addsegment(0, -1, 0, 0)
femm.mi_addsegment(0, -1, 1, -1)
femm.mi_addsegment(1, -1, 1, 0)

femm.mi_addblocklabel(0.5, 0.5)
femm.mi_addblocklabel(0.5, -0.5)
femm.mi_addblocklabel(0.5, 1.5)
femm.mi_addblocklabel(-3, 0)

addMaterial(mat_M27Steel)
addMaterial(mat_Air)
addMaterial(mat_18AWG)

femm.mi_addcircprop('A', 20, 1)

femm.mi_selectlabel(0.5, 1.5)
femm.mi_setblockprop('18 AWG', 1, 0, 'A', 0, 0, 100)
femm.mi_clearselected()
femm.mi_selectlabel(0.5, -0.5)
femm.mi_setblockprop('18 AWG', 1, 0, 'A', 0, 0, -100)
femm.mi_clearselected()
femm.mi_selectlabel(0.5, 0.5)
femm.mi_setblockprop('M-27 Steel', 1, 0, '<None>', 0, 0, 0)
femm.mi_clearselected()
femm.mi_selectlabel(-3, 0)
femm.mi_setblockprop('Air', 1, 0, '<None>', 0, 0, 0)
femm.mi_clearselected()

femm.mi_makeABC()

input()