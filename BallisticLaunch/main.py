import numpy as np                              # numerical utilities 
from matplotlib import pyplot as plt            # plotting 
import matplotlib.animation as animation        # animated plotting
from time import time                           # time utilities
from typing import Tuple, List, LiteralString   # typing

class FlightTimeException(Exception): 
    pass

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
        # Initial parameter setting - projectile 
        self.initial_velocity = v0
        self.y_initial_velocity = self.initial_velocity * np.sin(np.deg2rad(theta))
        self.x_initial_velocity = self.initial_velocity * np.cos(np.deg2rad(theta))
        self.launch_angle = theta
        
        # Initial parameter setting - environment
        self.grav_acc = g 
        self.launch_coordx = launch_coord[0]
        self.launch_coordy = launch_coord[1]
        self.step = step
        
    def launch(self) -> List[Tuple] | LiteralString:
        """Launches the projectile
        
        Returns:
            Tuple containing the positions of the trajectory of the projectile
        """
        # Timestamp before simulation
        before = time() 
        
        # Bounds the simulation time
        t = 0
        t_max = self.get_time_flight() 

        # Stores the simulation step
        h = self.get_step()
        
        # Stores the projectile's positions over time
        positions_array = []
    
        # Avoids starting a simulation with a invalid time of flight
        if t_max <= 0:
            raise FlightTimeException(f"Warning! Time of flight ({self.get_time_flight()}) is insuficient. Maybe try to increase speed or launch angle?")
        
        # Evolves the simulation over time
        while t < t_max: 
            new_position = self._evolve_system(t)
            positions_array.append(new_position)
            t += h 
            
        # Calculates the total time elapsed since the beginning of the simulation
        time_past = time() - before
        print(f"Simulation concluded with exec time: {time_past} seconds")
        
        # Stores the trajectory and returns it
        self.trajectory_array = positions_array
        return positions_array
    
    def _evolve_system(self, t: float) -> Tuple[float, float]:
        """Updates the projectile's position to the current time

        Args:
            t (float): Current time

        Returns:
            Tuple[float, float]: Current projectile's coordinates
        """
        # Matrix for position updating
        transf_matrix = np.array([[self.get_vx0(), 0, self.get_launch_coord()[0]],
                                    [self.get_vy0(), -1 * 0.5 * self.get_g(), self.get_launch_coord()[1]]
                                    ])
        
        # Current time in matrix form 
        time_matrix = np.array([[t], [t ** 2.0], [1]])
            
        # Applying the linear transform to the time vector
        positions_matrix = np.dot(transf_matrix, time_matrix)
        
        # Returning the current x-y coordinates
        return (float(positions_matrix[0]), float(positions_matrix[1]))

    def get_time_flight(self) -> float:
        """Returns the time of flight of the projectile, by analytical means

        Returns:
            float: time of flight of the projectile
        """
        
        return 2.0 * self.get_vy0() / self.get_g()

    def get_max_height(self) -> float:
        """Returns the max height of the projectile, by analytical means

        Returns:
            float: max height of the projectile
        """

        return (self.get_vy0() ** 2.0) / (2.0 * self.get_g())

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
    
    def generate_animation(self) -> None:
        """Generates an animation of the projectile's trajectory."""

        # Parses the data for the animation        
        x_values = [coords[0] for coords in self.trajectory_array]
        y_values = [coords[1] for coords in self.trajectory_array]
        total_frames = len(self.trajectory_array)

        # Builds the plot structure for the animation 
        fig, ax = plt.subplots()
        scat = ax.scatter([], [], c='blue')

        ax.set_xlim(min(x_values) - 1, max(x_values) + 1)
        ax.set_ylim(min(y_values) - 1, max(y_values) + 1)
        ax.set_xlabel('Distance')
        ax.set_ylabel('Height')
        ax.set_title(f'Trajectory Animation (theta={self.get_theta()}, v={self.get_v0()}), g={self.get_g()}')

        # Callback for initializing the animation frame
        def init():
            scat.set_offsets(np.empty((0, 2)))
            return scat,

        # Callback for animation updating 
        def update(frame):
            current_x = x_values[:frame+1]
            current_y = y_values[:frame+1]
            scat.set_offsets(list(zip(current_x, current_y)))
            return scat,

        ani = animation.FuncAnimation(
            fig, update, frames=total_frames, init_func=init,
            interval=10, blit=True, repeat=False
            )

        # Saves a GIF of the animation 
        ani.save(f"ballistic_motion.gif", fps=24)
    
    # Getters and Setters
    
    # Velocity
    
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

    # Angle 

    def set_theta(self, theta: float) -> None: 
        self.launch_angle = theta

    def get_theta(self) -> float:
        return self.launch_angle

    # Gravitational acceleration 

    def set_g(self, g: float): 
        self.grav_acc = g

    def get_g(self) -> float:
        return self.grav_acc

    # Launch coordinates

    def set_launch_coord(self, launch_coord: Tuple[float, float]):
        self.launch_coordx = launch_coord[0]
        self.launch_coordy = launch_coord[1]

    def get_launch_coord(self) -> Tuple[float, float]:
        return (self.launch_coordx, self.launch_coordy)

    # Simulation step

    def set_step(self, step: float):
        self.step = step

    def get_step(self) -> float:
        return self.step