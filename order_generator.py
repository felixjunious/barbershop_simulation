import random
from order import Order
from haircut import Haircut
from customer_generator import CustomerGenerator


class OrderGenerator:
    def __init__(self):
        self.customer_gen = CustomerGenerator()

    def generate_orders(self, count):
        customers = self.customer_gen.generate_customers(count)
        orders = []

        for cust in customers:
            haircut = random.choice(list(Haircut))
            order = Order(cust, haircut)
            orders.append(order)

        return orders
