import femm

def addMaterial(mat):
    femm.mi_addmaterial(mat["BlockName"],
        mat["Mu_x"],
        mat["Mu_y"],
        mat["H_c"],
        mat["H_cAngle"],
        mat["J_re"],
        mat["J_im"],
        mat["Sigma"],
        mat["d_lam"],
        mat["Phi_h"],
        mat["Phi_hx"],
        mat["Phi_hy"],
        mat["LamType"],
        mat["LamFill"],
        mat["NStrands"],
        mat["WireD"],
        mat["BHPoints"])

mat_Air = {
    "BlockName": "Air",
    "Mu_x": 1,
    "Mu_y": 1,
    "H_c": 0,
    "H_cAngle": 0,
    "J_re": 0,
    "J_im": 0,
    "Sigma": 0,
    "d_lam": 0,
    "Phi_h": 0,
    "Phi_hx": 0,
    "Phi_hy": 0,
    "LamType": 0,
    "LamFill": 1,
    "NStrands": 0,
    "WireD": 0,
    "BHPoints": 0
}