from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from pygbm.gbm_simulator import GBMSimulator

app = FastAPI(
    title="PyGBM API",
    description="RESTful API to simulate Geometric Brownian Motion paths.",
    version="0.1.0"
)

# CORS middleware for frontend access
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


# Request/Response Models
class GBMRequest(BaseModel):
    """Input parameters for a GBM simulation."""
    y0: float
    mu: float
    sigma: float
    T: float
    N: int


class GBMResponse(BaseModel):
    """Response model for a GBM simulation result."""
    t_values: List[float]
    y_values: List[float]
    result_summary: str


# Endpoints
@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "PyGBM API running ✅"}


@app.post("/simulate", response_model=GBMResponse)
def simulate(data: GBMRequest):
    """
    Perform a GBM simulation.

    Args:
        data: GBM parameters (y0, mu, sigma, T, N)

    Returns:
        GBMResponse with time values, simulated values, and summary
    """
    # Validate inputs before trying simulation
    if data.y0 <= 0:
        raise HTTPException(status_code=400, detail="y0 must be positive")
    if data.sigma < 0:
        raise HTTPException(status_code=400, detail="sigma must be non-negative")
    if data.T <= 0:
        raise HTTPException(status_code=400, detail="T must be positive")
    if data.N < 1:
        raise HTTPException(status_code=400, detail="N must be at least 1")

    try:
        # Run simulation using the core pygbm package
        simulator = GBMSimulator(data.y0, data.mu, data.sigma)
        t, y = simulator.simulate_path(data.T, data.N)

        return GBMResponse(
            t_values=t.tolist(),
            y_values=y.tolist(),
            result_summary=f"Final value: {y[-1]:.4f}, mean: {y.mean():.4f}, std: {y.std():.4f}"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")
