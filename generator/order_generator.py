import random
from models.order import Order
from models.haircut import Haircut
from generator.customer_generator import CustomerGenerator


class OrderGenerator:
    """
    Generates customer orders for the barbershop simulation.

    Attributes:
        customer_gen (CustomerGenerator): Instance for generating random customers.
    """

    def __init__(self):
        """
        Initialize an OrderGenerator instance.
        """
        self.customer_gen = CustomerGenerator()

    def generate_order(self):
        """
        Generate a single random order.

        Returns:
            Order: A new Order instance with a random customer and haircut type.
        """
        customer = self.customer_gen.generate_customer()
        haircut = random.choice(list(Haircut))
        return Order(customer, haircut)

    def generate_orders(self, count):
        """
        Generate multiple random orders.

        Args:
            count (int): Number of orders to generate.

        Returns:
            list of Order: List containing the generated orders.
        """
        return [self.generate_order() for _ in range(count)]
