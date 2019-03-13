### Global settings
updateInstant = False

### FEMM Groups
groupMode = -1
rotorGroup = 1
statorGroup = 2

### STATOR PARAMETERS
Nt = 6 # number of teeth
rag = 30 # radius past air gap
wt = 8 # width of tooth
bt = 15
hs = 30
tfrac = 0.8
cfrac = 0.6
wbi = 10 # back iron width
statorOOD = False # Stator out of date
statorSingle = True # Draw one single tooth
statorCoilLabels = []

### ROTOR PARAMETERS
Nm = 8
rsh = 5
rr = 20
hm = 10
dm = 5
mfrac = 0.8
rotorOOD = False
rotorSingle = True

### CIRCUIT
IA = 0
IB = 0
IC = 0

# ### MOTOR PARAMETERS
# Nm = 4 # number of rotor magnets
# rsh = 10. # shaft radius (mm)
# rr = 40. # rotor inner radius (mm)
# delta = 5. # air gap
# Mfrac = 0.8
# hm = 10.

# Nt = 6 # number of teeth; number of slots
# Tfrac = 0.6
# ht = 5. # tooth height
# bt = 20. # root width
# hs = 20. # slot height
# hstator = 30 # stator thickness

# rm = rr + hm # radius to outer magnet surface
# rti = rr + hm + delta # radius to inner tooth surface
# rag = (rm + rti) / 2. # radius to middle of air gap
# rto = rti + ht # radius to outer tooth surface
# rsi = rto + hs # radius to inner stator surface

# ### ELECTRICAL PARAMETERS
# I = 20

# ### BLOCK LABEL CACHE
# coilBlockLabels = []
# magnetBlockLabels = []

# ### MOTOR STATE
# rotorAngle = 0
# electricAngle = 0
# electricMode = 'none'