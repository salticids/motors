from UI import FEMMUtil
from StatorDL import StatorDL
from RotorSMPM import RotorSMPM
from amb import AMB

fmutil = FEMMUtil()
# fmutil.register(StatorDL, 3)
# fmutil.register(RotorSMPM, 4)
fmutil.register(AMB, 5)
fmutil.initUI()
