# 🧮 PyGBM — Geometric Brownian Motion Simulator

A modern full-stack application for simulating **Geometric Brownian Motion (GBM)** — a stochastic process used in finance and physics to model multiplicative growth.

**Tech Stack:**
- **Backend:** FastAPI + Python 3.9+
- **Frontend:** Next.js 16 + TypeScript + Tailwind CSS
- **Testing:** pytest + 40 comprehensive tests
- **Deployment:** Docker + Docker Compose

---

## 📁 Project Structure

```
pygbm/
├── src/pygbm/              # Python package (installable)
│   ├── __init__.py         # Package exports
│   ├── base.py             # Abstract base class for stochastic processes
│   ├── gbm_simulator.py    # Core GBM simulation logic
│   └── main.py             # FastAPI application
│
├── tests/                  # Backend test suite (40 tests)
│   ├── conftest.py         # Pytest fixtures
│   ├── test_gbm_simulator.py  # Core logic tests
│   └── test_api.py         # API integration tests
│
├── frontend/               # Next.js frontend
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx        # Main simulation UI
│   │   └── globals.css
│   ├── public/
│   └── package.json
│
├── docs/                   # Sphinx documentation
├── archive/                # Archived old code
├── pyproject.toml          # Python project configuration
├── package.json            # Root-level dev scripts
├── docker-compose.yml      # Multi-service orchestration
├── Dockerfile              # Backend container
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 20+
- npm or yarn
- Docker (optional)

### Option 1: Local Development (Recommended)

#### 1. Install Backend Dependencies
```bash
# Install the Python package in editable mode with test dependencies
pip install -e ".[dev]"
```

#### 2. Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

#### 3. Run Backend Server
```bash
# Using npm script
npm run dev:backend

# Or directly with uvicorn
uvicorn pygbm.main:app --reload --port 8000
```

Backend will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### 4. Run Frontend (in a separate terminal)
```bash
# Using npm script
npm run dev:frontend

# Or directly
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:3000

---

### Option 2: Docker Compose

Run both services with a single command:

```bash
# Build and start both services
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

Access:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

---

## 🧪 Testing

### Run Backend Tests
```bash
# Run all tests
npm run test:backend
# Or: pytest

# Run with coverage
npm run test:backend:cov
# Or: pytest --cov=pygbm tests/ --cov-report=html

# Run specific test file
pytest tests/test_gbm_simulator.py -v

# Run specific test
pytest tests/test_api.py::TestSimulateEndpoint::test_simulate_valid_request -v
```

**Test Coverage:** 40 tests covering:
- Core GBM simulation logic (21 tests)
- API endpoints and validation (19 tests)
- Edge cases and error handling

### Run Frontend Tests
```bash
npm run test:frontend
# Or: cd frontend && npm test
```

---

## 📦 Available Scripts

The root `package.json` provides convenient scripts for development:

```bash
# Development
npm run dev:backend          # Start FastAPI server
npm run dev:frontend         # Start Next.js dev server
npm run dev                  # Show instructions for both

# Testing
npm run test:backend         # Run pytest
npm run test:backend:cov     # Run pytest with coverage
npm run test:frontend        # Run frontend tests

# Building
npm run build:backend        # Build Python package
npm run build:frontend       # Build Next.js for production

# Installation
npm run install:backend      # Install Python dependencies
npm run install:frontend     # Install Node dependencies
npm run install              # Install both

# Docker
npm run docker:build         # Build Docker image
npm run docker:up            # Start with docker-compose
npm run docker:down          # Stop docker-compose

# Code Quality
npm run lint:backend         # Lint Python code with ruff
npm run lint:frontend        # Lint Next.js code
npm run format:backend       # Format with black

# Cleanup
npm run clean                # Remove cache and build artifacts
```

---

## 🔬 Features

### Backend (FastAPI)
- **RESTful API** for GBM simulations
- **Input validation** with Pydantic models
- **CORS enabled** for frontend communication
- **Interactive API docs** (Swagger UI + ReDoc)
- **Comprehensive error handling**
- **Type hints** throughout

### Frontend (Next.js)
- **Modern App Router** architecture
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Real-time simulation** with API integration
- **Responsive design**
- **Form validation**

### Core Logic
- Object-oriented GBM simulator
- Abstract base class for extensibility
- Configurable parameters (y0, μ, σ, T, N)
- Reproducible simulations with seed support
- Numpy-based efficient computation

---

## 📖 API Documentation

### Endpoints

#### `GET /`
Health check endpoint.

**Response:**
```json
{
  "message": "PyGBM API running ✅"
}
```

#### `POST /simulate`
Run a GBM simulation.

**Request Body:**
```json
{
  "y0": 100.0,      // Initial value (must be positive)
  "mu": 0.05,       // Drift coefficient
  "sigma": 0.2,     // Volatility (must be non-negative)
  "T": 1.0,         // Time horizon (must be positive)
  "N": 100          // Number of steps (must be >= 1)
}
```

**Response:**
```json
{
  "t_values": [0.0, 0.01, 0.02, ...],
  "y_values": [100.0, 100.5, 101.2, ...],
  "result_summary": "Final value: 105.1234, mean: 102.4567, std: 2.3456"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid parameters
- `422 Unprocessable Entity` - Missing or wrong type
- `500 Internal Server Error` - Simulation failure

---

## 🧮 Usage Examples

### Python API

```python
from pygbm import GBMSimulator

# Create simulator
sim = GBMSimulator(y0=100.0, mu=0.05, sigma=0.2, seed=42)

# Run simulation
t, y = sim.simulate_path(T=1.0, N=100)

# Plot results (optional)
sim.plot_path(t, y, output="gbm_path.png")
```

### HTTP API (curl)

```bash
curl -X POST "http://localhost:8000/simulate" \
  -H "Content-Type: application/json" \
  -d '{
    "y0": 100.0,
    "mu": 0.05,
    "sigma": 0.2,
    "T": 1.0,
    "N": 100
  }'
```

### Python + requests

```python
import requests

response = requests.post("http://localhost:8000/simulate", json={
    "y0": 100.0,
    "mu": 0.05,
    "sigma": 0.2,
    "T": 1.0,
    "N": 100
})

data = response.json()
print(f"Final value: {data['y_values'][-1]}")
```

---

## 🛠️ Development

### Project Configuration

- **pyproject.toml** - Python package configuration (PEP 517/518 compliant)
- **pytest.ini** - Test configuration (in pyproject.toml)
- **tsconfig.json** - TypeScript configuration
- **next.config.ts** - Next.js configuration
- **docker-compose.yml** - Multi-service orchestration

### Adding New Features

1. **Core Logic:** Add to `src/pygbm/`
2. **API Endpoints:** Update `src/pygbm/main.py`
3. **Tests:** Add to `tests/`
4. **Frontend:** Update `frontend/app/`

### Code Quality

```bash
# Format Python code
black src/ tests/

# Lint Python code
ruff check src/

# Lint frontend
cd frontend && npm run lint
```

---

## 📚 Mathematical Background

**Geometric Brownian Motion** is defined by the stochastic differential equation:

```
dY_t = μ * Y_t * dt + σ * Y_t * dW_t
```

Where:
- **Y_t** = value at time t
- **μ** = drift coefficient (expected return)
- **σ** = volatility (standard deviation of returns)
- **W_t** = standard Brownian motion (Wiener process)

**Solution:**
```
Y_t = Y_0 * exp((μ - σ²/2) * t + σ * W_t)
```

**Properties:**
- Always positive (if Y_0 > 0)
- Log-normal distribution
- Used to model stock prices, interest rates, etc.

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -ti:8000

# Try a different port
uvicorn pygbm.main:app --reload --port 8001
```

### Frontend can't connect to backend
1. Ensure backend is running on port 8000
2. Check CORS configuration in `src/pygbm/main.py`
3. Frontend expects: `http://127.0.0.1:8000` or `http://localhost:8000`

### Tests failing
```bash
# Reinstall dependencies
pip install -e ".[dev]"

# Clear cache
npm run clean
pytest --cache-clear
```

### Docker issues
```bash
# Rebuild without cache
docker-compose build --no-cache

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

---

## 📝 License

MIT License - see LICENSE file for details

---

## 👤 Author

**Basia Koch**

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🔗 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Geometric Brownian Motion (Wikipedia)](https://en.wikipedia.org/wiki/Geometric_Brownian_motion)
- [Stochastic Calculus](https://en.wikipedia.org/wiki/Stochastic_calculus)

---

**⭐ Star this repository if you find it helpful!**
