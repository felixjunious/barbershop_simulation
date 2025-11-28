import random
import os
from utils.csv_to_bin import read_bin_to_list, FMT
from models.customer import Customer

class CustomerGenerator:
    """
    Generates Customer Generator instances for the barbershop simulation.

    Attributes:
        names (list of str): List of customer names loaded from a binary file.
    """

    def __init__(self, names_file=None):
        """
        Initialize the CustomerGenerator.

        Args:
            names_file (str, optional): Path to a binary file containing customer names.
                                        Defaults to '../customer_data/names.bin' relative to this file.
        """
        if names_file is None:
            names_file = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "customer_data", "names.bin"))
        self.names = read_bin_to_list(names_file, FMT)

    def generate_customer(self):
        """
        Generate a single random Customer.

        Returns:
            Customer: A new Customer instance with a randomly chosen name.
        """
        name = random.choice(self.names)
        return Customer(name)

    def generate_customers(self, number_of_customers):
        """
        Generate multiple random Customers.

        Args:
            number_of_customers (int): Number of customers to generate.

        Returns:
            list of Customer: List containing the generated Customer instances.
        """
        return [self.generate_customer() for _ in range(number_of_customers)]
