import random

class Order:
    TIME_VARIANCE = 0.2

    def __init__(self, customer, haircut):
        self.customer = customer
        self.haircut = haircut
        self.duration = Order.random_duration(haircut)

    @staticmethod
    def random_duration(haircut):
        variation = haircut.base_duration * Order.TIME_VARIANCE
        return int(random.uniform(haircut.base_duration - variation, haircut.base_duration + variation))

    def __repr__(self):
        return f"Order({self.customer}, {self.haircut.name}, {self.duration}m)"