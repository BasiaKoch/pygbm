from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import uuid
import numpy as np  # if you want to add a fake simulation

app = FastAPI(
    title="PyGBM API",
    description="RESTful API to simulate Geometric Brownian Motion and manage simulations.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# MODELS
# ---------------------------

class GBMRequest(BaseModel):
    """Input parameters for a GBM simulation."""
    y0: float
    mu: float
    sigma: float
    T: float
    N: int

class GBMResult(BaseModel):
    """Example response model for a GBM simulation result."""
    id: str
    y0: float
    mu: float
    sigma: float
    T: float
    N: int
    result_summary: str


# ---------------------------
# ENDPOINTS
# ---------------------------

@app.get("/")
def root():
    return {"message": "Backend running ✅"}

@app.post("/simulate", response_model=GBMResult)
def simulate(data: GBMRequest):
    """Perform a mock GBM simulation."""
    try:
        # Fake GBM path calculation for now (optional)
        np.random.seed(0)
        dt = data.T / data.N
        t = np.linspace(0, data.T, data.N)
        W = np.random.standard_normal(size=data.N)
        W = np.cumsum(W) * np.sqrt(dt)
        Y = data.y0 * np.exp((data.mu - 0.5 * data.sigma**2) * t + data.sigma * W)

        result = GBMResult(
            id=str(uuid.uuid4()),
            y0=data.y0,
            mu=data.mu,
            sigma=data.sigma,
            T=data.T,
            N=data.N,
            result_summary=f"Final value: {Y[-1]:.4f}, mean: {Y.mean():.4f}"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
