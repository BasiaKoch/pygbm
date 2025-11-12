FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY . /app

# Install build tools and build the package
RUN pip install --upgrade pip && \
    pip install build && \
    python -m build && \
    pip install "dist/pygbm-0.1.0-py3-none-any.whl[test]"

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run FastAPI server
CMD ["uvicorn", "pygbm.main:app", "--host", "0.0.0.0", "--port", "8000"]
