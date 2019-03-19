from UI import FEMMUtil
from StatorDL import StatorDL
from RotorSMPM import RotorSMPM

fmutil = FEMMUtil()
fmutil.register(StatorDL, 3)
fmutil.register(RotorSMPM, 4)
fmutil.initUI()
