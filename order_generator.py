import random
from order import Order
from haircut import Haircut
from customer_generator import CustomerGenerator


class OrderGenerator:
    def __init__(self):
        self.customer_gen = CustomerGenerator()

    def generate_order(self):
        """Generate exactly one order."""
        customer = self.customer_gen.generate_customer()
        haircut = random.choice(list(Haircut))
        return Order(customer, haircut)

    def generate_orders(self, count):
        """Generate a list of orders by calling generate_order repeatedly."""
        return [self.generate_order() for _ in range(count)]
