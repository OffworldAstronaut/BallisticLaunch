# Imports the class
from BallisticLaunch import BallisticLaunch

# Creates a Simulation object with all the data necessary 
sim = BallisticLaunch.Simulation(v0=10, theta=45, g=10, launch_coord=(0, 0), step=0.01)

# Launches the projectile 
sim.launch()

# Generates a plot for the projectile's trajectory 

