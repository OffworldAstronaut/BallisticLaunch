# 🚀 BallisticLaunch

This repository is a simple experiment in simulating a conservative ballistic trajectory (that is, without dissipative forces, like air resistance) using matrix multiplication instead of simple arithmetic functions in a loop. 
That is, given a certain time $t$, the current coordinates of the projectile are given by:

$$
\begin{bmatrix}
x \\ 
y
\end{bmatrix}
=
\begin{bmatrix} 
v_{x_0} & 0 & x_0 \\ 
v_{y_0} & -\dfrac{1}{2}g & y_0
\end{bmatrix}
\begin{bmatrix}
t \\ 
t^2 \\ 
1 
\end{bmatrix}
$$

An old project, the main motivation was the thrill of the "what if?".

Repository revamped in September 2025.

## Structure

### Classes

- ``BallisticLaunch``: the main and only class in the module. Simulates the environment of the projectile (and the projectile's properties too). The main function, launch(), launches the projectile. The others help the user control other aspects of the simulation.

---

## Setup

The requirements are only ``numpy`` and ``matplotlib``, available via ``pip``.

## Usage
 
Clone and run ``pip install .``, then it's ready to use!

```py
# example.py

# Imports
from BallisticLaunch import BallisticLaunch

# Creates a Simulation object with all the data necessary 
sim = BallisticLaunch.Simulation(v0=100, theta=45, g=10, launch_coord=(0, 0), step=0.1)

# Launches the projectile 
sim.launch()
# Generates a plot
#sim.generate_plot()
sim.generate_animation()
```

### Generated .gif

![](/examples/example_anim.gif)