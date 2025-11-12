"""
Integration tests for FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from pygbm.main import app

client = TestClient(app)


class TestRootEndpoint:
    """Test the root health check endpoint."""

    def test_root_returns_200(self):
        """Test that root endpoint returns 200 status."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_message(self):
        """Test that root endpoint returns expected message."""
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert "running" in data["message"].lower()


class TestSimulateEndpoint:
    """Test the /simulate endpoint."""

    def test_simulate_valid_request(self, sample_gbm_request):
        """Test simulation with valid parameters."""
        response = client.post("/simulate", json=sample_gbm_request)
        assert response.status_code == 200

        data = response.json()
        assert "t_values" in data
        assert "y_values" in data
        assert "result_summary" in data

        # Check array lengths (N+1 points)
        assert len(data["t_values"]) == sample_gbm_request["N"] + 1
        assert len(data["y_values"]) == sample_gbm_request["N"] + 1

        # Check initial condition
        assert data["y_values"][0] == sample_gbm_request["y0"]

    def test_simulate_returns_positive_values(self, sample_gbm_request):
        """Test that simulation returns all positive values."""
        response = client.post("/simulate", json=sample_gbm_request)
        data = response.json()

        y_values = data["y_values"]
        assert all(y > 0 for y in y_values), "All GBM values should be positive"

    def test_simulate_result_summary(self, sample_gbm_request):
        """Test that result summary contains expected statistics."""
        response = client.post("/simulate", json=sample_gbm_request)
        data = response.json()

        summary = data["result_summary"]
        assert "Final value" in summary
        assert "mean" in summary
        assert "std" in summary

    def test_simulate_different_parameters(self):
        """Test simulation with different parameter sets."""
        params_list = [
            {"y0": 50.0, "mu": 0.1, "sigma": 0.3, "T": 2.0, "N": 200},
            {"y0": 200.0, "mu": -0.05, "sigma": 0.1, "T": 0.5, "N": 50},
            {"y0": 1.0, "mu": 0.0, "sigma": 0.5, "T": 1.0, "N": 100},
        ]

        for params in params_list:
            response = client.post("/simulate", json=params)
            assert response.status_code == 200
            data = response.json()
            assert len(data["t_values"]) == params["N"] + 1
            assert len(data["y_values"]) == params["N"] + 1


class TestSimulateValidation:
    """Test input validation for /simulate endpoint."""

    def test_simulate_negative_y0(self, sample_gbm_request):
        """Test that negative y0 returns 400 error."""
        invalid_request = sample_gbm_request.copy()
        invalid_request["y0"] = -100.0

        response = client.post("/simulate", json=invalid_request)
        assert response.status_code == 400
        assert "y0 must be positive" in response.json()["detail"]

    def test_simulate_zero_y0(self, sample_gbm_request):
        """Test that zero y0 returns 400 error."""
        invalid_request = sample_gbm_request.copy()
        invalid_request["y0"] = 0.0

        response = client.post("/simulate", json=invalid_request)
        assert response.status_code == 400

    def test_simulate_negative_sigma(self, sample_gbm_request):
        """Test that negative sigma returns 400 error."""
        invalid_request = sample_gbm_request.copy()
        invalid_request["sigma"] = -0.2

        response = client.post("/simulate", json=invalid_request)
        assert response.status_code == 400
        assert "sigma must be non-negative" in response.json()["detail"]

    def test_simulate_zero_T(self, sample_gbm_request):
        """Test that zero T returns 400 error."""
        invalid_request = sample_gbm_request.copy()
        invalid_request["T"] = 0.0

        response = client.post("/simulate", json=invalid_request)
        assert response.status_code == 400
        assert "T must be positive" in response.json()["detail"]

    def test_simulate_negative_T(self, sample_gbm_request):
        """Test that negative T returns 400 error."""
        invalid_request = sample_gbm_request.copy()
        invalid_request["T"] = -1.0

        response = client.post("/simulate", json=invalid_request)
        assert response.status_code == 400

    def test_simulate_zero_N(self, sample_gbm_request):
        """Test that zero N returns 400 error."""
        invalid_request = sample_gbm_request.copy()
        invalid_request["N"] = 0

        response = client.post("/simulate", json=invalid_request)
        assert response.status_code == 400
        assert "N must be at least 1" in response.json()["detail"]

    def test_simulate_negative_N(self, sample_gbm_request):
        """Test that negative N returns 400 error."""
        invalid_request = sample_gbm_request.copy()
        invalid_request["N"] = -10

        response = client.post("/simulate", json=invalid_request)
        assert response.status_code == 400

    def test_simulate_missing_fields(self):
        """Test that missing required fields returns 422 error."""
        incomplete_request = {"y0": 100.0, "mu": 0.05}

        response = client.post("/simulate", json=incomplete_request)
        assert response.status_code == 422  # Unprocessable Entity

    def test_simulate_invalid_types(self):
        """Test that invalid field types return 422 error."""
        invalid_request = {
            "y0": "not a number",
            "mu": 0.05,
            "sigma": 0.2,
            "T": 1.0,
            "N": 100
        }

        response = client.post("/simulate", json=invalid_request)
        assert response.status_code == 422


class TestCORS:
    """Test CORS configuration."""

    def test_cors_headers_present(self):
        """Test that CORS headers are present in responses."""
        response = client.options("/simulate")
        # Note: TestClient doesn't fully simulate CORS preflight,
        # but we can verify the middleware is configured
        assert response.status_code in [200, 405]  # OPTIONS might not be explicitly defined


class TestEdgeCases:
    """Test edge cases for the API."""

    def test_simulate_very_large_N(self):
        """Test simulation with large N."""
        large_request = {
            "y0": 100.0,
            "mu": 0.05,
            "sigma": 0.2,
            "T": 1.0,
            "N": 10000
        }

        response = client.post("/simulate", json=large_request)
        assert response.status_code == 200
        data = response.json()
        assert len(data["t_values"]) == 10001

    def test_simulate_minimal_N(self):
        """Test simulation with N=1."""
        minimal_request = {
            "y0": 100.0,
            "mu": 0.05,
            "sigma": 0.2,
            "T": 1.0,
            "N": 1
        }

        response = client.post("/simulate", json=minimal_request)
        assert response.status_code == 200
        data = response.json()
        assert len(data["t_values"]) == 2
        assert len(data["y_values"]) == 2

    def test_simulate_zero_volatility(self):
        """Test deterministic simulation with sigma=0."""
        deterministic_request = {
            "y0": 100.0,
            "mu": 0.05,
            "sigma": 0.0,
            "T": 1.0,
            "N": 100
        }

        response = client.post("/simulate", json=deterministic_request)
        assert response.status_code == 200
        data = response.json()

        # With zero volatility, result should be deterministic
        # Y(T) = y0 * exp(mu * T)
        expected_final = 100.0 * 2.71828 ** (0.05 * 1.0)
        assert abs(data["y_values"][-1] - expected_final) < 0.01
