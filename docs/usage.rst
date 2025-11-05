Usage
=====

Here’s how to simulate a Geometric Brownian Motion using ``pygbm``:

.. code-block:: python

   from pygbm.gbm_simulator import GBMSimulator
   import matplotlib.pyplot as plt

   y0, mu, sigma, T, N = 1.0, 0.05, 0.2, 1.0, 100
   simulator = GBMSimulator(y0, mu, sigma)
   t_values, y_values = simulator.simulate_path(T, N)

   plt.plot(t_values, y_values)
   plt.show()
