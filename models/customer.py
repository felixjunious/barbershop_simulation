class Customer:
    """
    Represents a customer in the barbershop simulation.

    Attributes:
        name (str): The name of the customer.
    """

    def __init__(self, name):
        """
        Initialize a Customer instance.

        Args:
            name (str): The name of the customer.
        """
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Customer(name='{self.name}')"
