import random

class Order:
    """
    Represents a customer order in the barbershop simulation.

    Attributes:
        customer (Customer): The customer placing the order.
        haircut (Haircut): The type of haircut requested.
        duration (int): Actual duration of the haircut in minutes (with some variance).
        arrival_time (float, optional): The simulated time when the customer arrives.
    """

    TIME_VARIANCE = 0.2  # Max ±20% variation on the haircut duration

    def __init__(self, customer, haircut, arrival_time=None):
        """
        Initialize an Order instance.

        Args:
            customer (Customer): The customer placing the order.
            haircut (Haircut): The type of haircut requested.
            arrival_time (float, optional): The time the customer arrives in simulation minutes.
        """
        self.customer = customer
        self.haircut = haircut
        self.duration = Order.random_duration(haircut)
        self.arrival_time = arrival_time

    @staticmethod
    def random_duration(haircut):
        """
        Generate a randomized haircut duration based on the base duration and TIME_VARIANCE.

        Args:
            haircut (Haircut): Haircut type to calculate duration for.

        Returns:
            int: Randomized haircut duration in minutes.
        """
        variation = haircut.base_duration * Order.TIME_VARIANCE
        return int(random.uniform(haircut.base_duration - variation,
                                  haircut.base_duration + variation))

    def __repr__(self):
        return f"Order({self.customer}, {self.haircut.name}, {self.duration}m)"
