from config import SIMULATION_TIME, TIME_DESCALE
import time

class TimeManager:
    """
    Manages the simulation time for the barbershop simulation.

    Attributes:
        current (int): Current simulation time in minutes.
        total (int): Total simulation duration in minutes.
        descale (float): Factor to speed up or slow down simulation time.
    """

    def __init__(self, total_time=SIMULATION_TIME, descaler=TIME_DESCALE):
        """
        Initialize the TimeManager.

        Args:
            total_time (int, optional): Total simulation duration in minutes. Defaults to SIMULATION_TIME.
            descaler (float, optional): Factor to scale real-time speed of the simulation. Defaults to TIME_DESCALE.
        """
        self.current = 0
        self.total = total_time
        self.descale = descaler

    def tick(self):
        """
        Advance the simulation time by one minute, scaled by the descaler.
        """
        time.sleep(1 / self.descale)
        self.current += 1

    def check_time(self):
        """
        Check if the simulation has remaining time.

        Returns:
            bool: True if current time is less than total simulation time, False otherwise.
        """
        return self.current < self.total

    def reset(self):
        """
        Reset the simulation time to zero.
        """
        self.current = 0

    def formatted(self):
        """
        Return a formatted string representation of the current simulation time.

        Returns:
            str: Current simulation time in minutes.
        """
        return f"{self.current} min"
