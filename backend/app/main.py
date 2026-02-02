from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .model_runner import run_model

app = FastAPI()

# 🔴 ADD THIS BLOCK (CORS FIX)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],   # allows OPTIONS, POST, etc.
    allow_headers=["*"],
)

class Input(BaseModel):
    flow_ml_min: float
    P_in_atm: float
    T_K: float
    eps: float
    rho_s_L: float
    L_m: float
    D_bed_m: float

@app.post("/simulate")
def simulate_case(inp: Input):
    return run_model(inp.dict())
