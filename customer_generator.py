from customer_data.csv_to_bin import read_bin_to_list, FMT
from customer import Customer
import random
import os

class CustomerGenerator():
    def __init__(self, names_file=None):

        if names_file is None:
            names_file = os.path.join(os.path.dirname(__file__),"customer_data","names.bin")
        self.names = read_bin_to_list(names_file,FMT)

    def generate_customer(self):
        name = random.choice(self.names)
        return Customer(name)

    def generate_customers(self, number_of_customers):
        return [self.generate_customer() for _ in range(number_of_customers)]


