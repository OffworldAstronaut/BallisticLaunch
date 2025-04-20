# Imports the class
from BallisticLaunch import BallisticLaunch

# Creates a Simulation object with all the data necessary 
sim = BallisticLaunch.Simulation(v0=100, theta=45, g=10, launch_coord=(0, 0), step=0.1)

# Launches the projectile 
sim.launch()
# Generates a plot
#sim.generate_plot()
sim.generate_animation()