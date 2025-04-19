from time import time
from typing import Tuple, List, LiteralString
import numpy as np
from matplotlib import axis, pyplot as plt

class FlightTimeException(Exception): 
    pass

class Simulation: 
    
    # Constructor
    
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
        self.y_initial_velocity = self.initial_velocity * np.sin(np.deg2rad(theta))
        self.x_initial_velocity = self.initial_velocity * np.cos(np.deg2rad(theta))

        self.launch_angle = theta
        self.grav_acc = g 

        self.launch_coordx = launch_coord[0]
        self.launch_coordy = launch_coord[1]
        self.step = step
        
    # Important methods
    
    def launch(self) -> List[Tuple] | LiteralString:
        """Launches the projectile
        
        Returns:
            Tuple containing the positions of the trajectory of the projectile
        """
        before = time() 
        
        t = 0
        t_max = self.get_time_flight() 

        h = self.get_step()
        
        positions_array = []
    
        if t_max <= 0:
            raise FlightTimeException(f"Warning! Time of flight ({self.get_time_flight()}) is insuficient. Maybe try to increase speed or launch angle?")
        
        else:
            while t < t_max: 
                transf_matrix = np.array([[self.get_vx0(), 0, self.get_launch_coord()[0]],
                                        [self.get_vy0(), -1 * 0.5 * self.get_g(), self.get_launch_coord()[1]]
                                        ])
            
                time_matrix = np.array([[t], [t ** 2.0], [1]])
                
                positions_matrix = np.dot(transf_matrix, time_matrix)
                position = (float(positions_matrix[0]), float(positions_matrix[1]))
                positions_array.append(position)
                t = t + h
                
            
            time_past = time() - before
            print(f"Simulation concluded with exec time: {time_past} seconds")
            
            self.trajectory_array = positions_array
            
            return positions_array

    def get_time_flight(self) -> float:
        """Returns the time of flight of the projectile, by analytical means

        Returns:
            float: time of flight of the projectile, with four degrees of precision
        """
        
        return 2.0 * self.get_vy0() / self.get_g()

    def get_max_height(self) -> float:
        """Returns the max height of the projectile, by analytical means

        Returns:
            float: max height of the projectile, with four degrees of precision_description_
        """

        return (self.get_vy0() ** 2.0) / (2 * self.get_g())

    def get_range(self) -> float:
        """Returns the max range of the projectile, by analytical means

        Returns:
            float: max range of the projectile, with four degrees of precision
        """
        
        return self.get_v0() ** 2.0 * np.sin(np.deg2rad(2.0 * self.get_theta())) / self.get_g()
    
    def generate_plot(self) -> None:
        """Generates a plot for the projectile's trajectory. The file is identified by timestamp."""
        
        x_values = [coords[0] for coords in self.trajectory_array]
        y_values = [coords[1] for coords in self.trajectory_array]
    
        plt.scatter(x_values, y_values, s=0.5)
        
        plt.xlim(0, self.get_range() + 0.1)
        plt.ylim(0, self.get_max_height() + 0.2)
        
        plt.savefig(f"projectile_t={time()}.png", dpi=1500)
        
    
    # TODO: generate animation method
    
    # Getters and Setters
    
    def set_v0(self, v0: float) -> None: 
        self.initial_velocity = v0
        self.set_vx0(v0 * np.cos(self.get_theta()))
        self.set_vy0(v0 * np.sin(self.get_theta()))

    def get_v0(self) -> float:
        return self.initial_velocity
    
    def set_vy0(self, vy0: float) -> None: 
        self.y_initial_velocity = vy0

    def get_vy0(self) -> float: 
        return self.y_initial_velocity
    
    def set_vx0(self, vx0: float) -> None: 
        self.x_initial_velocity = vx0

    def get_vx0(self) -> float: 
        return self.x_initial_velocity

    def set_theta(self, theta: float) -> None: 
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