from femm import *
import cmath
from math import pi

openfemm()
newdocument(0)
mi_probdef(0, 'millimeters', 'planar', 1.e-8, 50, 30)
mi_hidegrid()
mi_saveas('demo1.fem')

points = 10
angleBetweenPoints = 360 / points

for i in range(points):
    r = 1
    phi = i * angleBetweenPoints

    n = cmath.rect(r, phi * pi / 180)

    mi_addnode(n.real, n.imag)



input()

closefemm()