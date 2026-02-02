from .adsorption_model import simulate

def run_model(data):
    return simulate(
        data["flow_ml_min"],
        data["P_in_atm"],
        data["T_K"],
        data["eps"],
        data["rho_s_L"],
        data["L_m"],
        data["D_bed_m"],
    )
