# adsorption_model.py
# AUTHORITATIVE PACKED-BED MODEL — DO NOT SIMPLIFY

import math
import numpy as np

# ---------------- 1) USER INPUT DEFAULTS ----------------
P_in_atm    = 1.0
T_K         = 298.15
eps         = 0.30
rho_s_L     = 0.60
L_m         = 0.50
D_bed_m     = 0.08

y1_in = 415e-6
y3_in = 0.20946
y2_in = 1.0 - y1_in - y3_in

qmax1, qmax2, qmax3 = 2.38, 1.0, 0.01
b1, b2, b3 = 599.0, 0.09, 0.01
t1, t2, t3 = 0.403, 0.829, 1.0

k1, k2, k3 = 3.26e-4, 1.0e-8, 1.0e-8

Nz, t_end_s, d_p = 30, 14400.0, 6.0e-4

# ---------------- 2) CONSTANTS ----------------
P_in_bar = P_in_atm * 1.01325
rho_s = rho_s_L * 1000.0
A_m2  = math.pi * (D_bed_m/2.0)**2
z  = np.linspace(0.0, L_m, Nz+1)
dz = z[1] - z[0]
R_bar = 8.314e-5

# ---------------- 3) HELPERS ----------------
def qstar_toth_ternary(y1, y2, y3, P):
    P1 = np.clip(P*y1, 1e-300, None)
    P2 = np.clip(P*y2, 1e-300, None)
    P3 = np.clip(P*y3, 1e-300, None)

    th1 = (b1*P1)**t1
    th2 = (b2*P2)**t2
    th3 = (b3*P3)**t3

    denom = 1.0 + th1 + th2 + th3
    return (
        qmax1*th1/(denom**(1/t1)),
        qmax2*th2/(denom**(1/t2)),
        qmax3*th3/(denom**(1/t3)),
    )

def ergun_dPdz_bar_per_m(u, d_p, eps):
    mu, rho = 1e-5, 1.8
    return (
        (150*(1-eps)**2*mu*u)/(eps**3*d_p**2)
      + (1.75*(1-eps)*rho*u**2)/(eps**3*d_p)
    ) / 1e5

def thin(x, y, n=300):
    if len(x) <= n:
        return x, y
    idx = np.linspace(0, len(x)-1, n, dtype=int)
    return x[idx], y[idx]

def envelope(x, y, w=200):
    yenv = np.copy(y)
    for i in range(len(y)):
        yenv[i] = np.max(y[max(0,i-w):i+1])
    return x, yenv

# ---------------- 4) SIMULATION ----------------
def simulate(flow_ml_min, P_in_atm, T_K, eps, rho_s_L, L_m, D_bed_m):

    global P_in_bar, rho_s, A_m2, z, dz

    P_in_bar = P_in_atm * 1.01325
    rho_s = rho_s_L * 1000.0
    A_m2 = math.pi * (D_bed_m / 2.0) ** 2
    z = np.linspace(0.0, L_m, Nz + 1)
    dz = z[1] - z[0]



    flow_m3_s = flow_ml_min * 1e-6 / 60.0
    u_in = flow_m3_s / A_m2
    beta = ((1-eps)/eps) * (rho_s*R_bar*T_K/P_in_bar)

    y1 = np.zeros(Nz+1)
    y2 = np.zeros(Nz+1)
    y3 = np.zeros(Nz+1)
    q1 = np.zeros(Nz+1)

    y1[0], y2[0], y3[0] = y1_in, y2_in, y3_in

    CFL = 0.30
    dt = 0.5 * min(
        CFL*dz/(u_in/eps),
        0.30/max(k1,k2,k3)
    )
    Nt = int(np.ceil(t_end_s/dt))

    times = np.zeros(Nt)
    Nads  = np.zeros(Nt)
    Fout  = np.zeros(Nt)
    yout  = np.zeros(Nt)
    Pprof = np.zeros(Nz+1)

    for n in range(Nt):

        # ---- Pressure + velocity profiles
        Pprof[0] = P_in_bar
        u = np.zeros(Nz+1)
        for j in range(1, Nz+1):
            u[j-1] = u_in * Pprof[0]/max(Pprof[j-1],1e-12)
            Pprof[j] = Pprof[j-1] - ergun_dPdz_bar_per_m(u[j-1], d_p, eps)*dz
        u[-1] = u_in * Pprof[0]/max(Pprof[-1],1e-12)

        # ---- Equilibrium & kinetics
        q1s, _, _ = qstar_toth_ternary(y1,y2,y3,Pprof)
        dq1dt = k1*(q1s - q1)

        # ---- Convection (upwind)
        a = u/eps
        F = np.zeros(Nz+1)
        F[0] = a[0]*(y1_in if a[0]>=0 else y1[0])
        for j in range(1,Nz):
            F[j] = a[j]*(y1[j-1] if a[j]>=0 else y1[j])
        F[Nz] = a[-1]*y1[-2]

        # ---- Gas-phase update
        y1n = y1.copy()
        for j in range(Nz):
            y1n[j] = (
                y1[j]
              - (dt/dz)*(F[j+1]-F[j])
              - dt*beta*dq1dt[j]
            )
        y1n[-1] = y1n[-2]
        y1 = np.clip(y1n,0,1)

        # ---- Solid phase
        q1 += dt*dq1dt

        # ---- Diagnostics
        seg = A_m2*dz
        Nads[n] = np.sum(q1*(1-eps)*rho_s*seg)
        C = Pprof[-1]/(R_bar*T_K)
        yout[n] = y1[-1]
        Fout[n] = y1[-1]*C*u_in*A_m2
        times[n] = (n+1)*dt

    # ---- POST-PROCESS (MATCH ORIGINAL)
    tmin = times/60.0
    ppm  = yout*1e6

    tA, A  = thin(tmin, Nads)
    tF, Fe = envelope(tmin, Fout*60.0)
    tF, Fe = thin(tF, Fe)
    tP, Pe = envelope(tmin, ppm)
    tP, Pe = thin(tP, Pe)

    return {
        "z": z.tolist(),
        "pressure": (P_in_bar-Pprof).tolist(),
        "time_ads": tA.tolist(),
        "co2_adsorbed": A.tolist(),
        "time_flow": tF.tolist(),
        "co2_outlet_flow": Fe.tolist(),
        "time_ppm": tP.tolist(),
        "co2_outlet_ppm": Pe.tolist()
    }
