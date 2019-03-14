### FEMM Groups
rotorGroup = 1

### MOTOR PARAMETERS
Nm = 4 # number of rotor magnets
rsh = 10. # shaft radius (mm)
rr = 40. # rotor inner radius (mm)
delta = 5. # air gap
Mfrac = 0.8
hm = 10.

Nt = 6 # number of teeth; number of slots
Tfrac = 0.6
ht = 5. # tooth height
bt = 20. # root width
hs = 20. # slot height
hstator = 30 # stator thickness

rm = rr + hm # radius to outer magnet surface
rti = rr + hm + delta # radius to inner tooth surface
rag = (rm + rti) / 2. # radius to middle of air gap
rto = rti + ht # radius to outer tooth surface
rsi = rto + hs # radius to inner stator surface

### ELECTRICAL PARAMETERS
I = 20

### BLOCK LABEL CACHE
coilBlockLabels = []
magnetBlockLabels = []

### MOTOR STATE
rotorAngle = 0
electricAngle = 0
electricMode = 'none'