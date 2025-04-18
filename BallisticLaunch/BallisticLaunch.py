from time import time
from typing import Tuple, List
import numpy as np

class Simulation: 
    def __init__(self, v0: float, theta: float, g: float, launch_coord: Tuple[float, float], step: float):
        """Initializes the simulation with all the necessary parameters

        Args:
            v0 (float): initial magnitude of the velocity vector 
            theta (float): launch angle
            g (float): gravitational acceleration
            launch_coord (Tuple[float, float]): cartesian coordinates of the launch position
            step (float): step size of each motion "snapshot" - smaller numbers mean sharper simulations
        """
        self.initial_velocity = v0
        self.launch_angle = theta
        self.grav_acc = g 
        self.launch_coordx = launch_coord[0]
        self.launch_coordy = launch_coord[1]
        self.step = step
        
    def set_v0(self, v0: float): 
        self.initial_velocity = v0

    def get_v0(self) -> float:
        return self.initial_velocity

    def set_theta(self, theta: float): 
        self.launch_angle = theta

    def get_theta(self) -> float:
        return self.launch_angle

    def set_g(self, g: float): 
        self.grav_acc = g

    def get_g(self) -> float:
        return self.grav_acc

    def set_launch_coord(self, launch_coord: Tuple[float, float]):
        self.launch_coordx = launch_coord[0]
        self.launch_coordy = launch_coord[1]

    def get_launch_coord(self) -> Tuple[float, float]:
        return (self.launch_coordx, self.launch_coordy)

    def set_step(self, step: float):
        self.step = step

    def get_step(self) -> float:
        return self.step 

    def launch(self, exec_time: bool) -> Tuple:
        """Executes the launch of the created projectile 

        Returns:
            Tuple: Data of the launch (coordinates, associated time, velocities) and the method's running time, if asked
        """
        ...

    def get_flight_time(self) -> float:
        """Returns the flight time of the projectile, by analytical means

        Returns:
            float: flight time of the projectile, with four degrees of precision
        """
        ...

    def get_max_height(self) -> float:
        """Returns the max height of the projectile, by analytical means

        Returns:
            float: max height of the projectile, with four degrees of precision_description_
        """
        ...

    def get_range(self) -> float:
        """Returns the max range of the projectile, by analytical means

        Returns:
            float: max range of the projectile, with four degrees of precision
        """
        ... 