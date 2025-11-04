FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install build
RUN python -m build
RUN pip install dist/pygbm-0.1.0-py3-none-any.whl
CMD ["python", "-c", "from pygbm.gbm_simulator import GBMSimulator; sim=GBMSimulator(1.0,0.05,0.2); t,y=sim.simulate_path(1.0,100); print('✅ GBM simulation ran inside Docker!')"]
