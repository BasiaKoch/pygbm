from fastapi import FastAPI
from pygbm.gbm_simulator import GBMSimulator

app = FastAPI(
    title="pygbm API",
    description="API for simulating Geometric Brownian Motion paths.",
    version="0.1.0"
)

@app.get("/")
def home():
    return {"message": "Welcome to the pygbm API"}

@app.post("/simulate")
def simulate(y0: float, mu: float, sigma: float, T: float, N: int):
    simulator = GBMSimulator(y0, mu, sigma)
    t, y = simulator.simulate_path(T, N)
    return {"t_values": t.tolist(), "y_values": y.tolist()}
