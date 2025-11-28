from enum import Enum

class Haircut(Enum):
    """
    Represents different types of haircuts offered in the barbershop simulation.

    Attributes:
        label (str): Human-readable name of the haircut.
        price (float): Price of the haircut in currency units.
        base_duration (int): Estimated duration of the haircut in minutes.
    """

    NORMAL = ("Normal Haircut", 15, 20)
    DRY = ("Dry Haircut", 10, 15)
    NORMAL_WASH = ("Haircut + Wash", 17, 30)
    BEARD_TRIM = ("Beard Trim", 10, 10)
    BEARD_SHAVE = ("Beard Shave", 12, 15)
    HAIR_BEARD = ("Hair + Beard", 25, 40)
    KIDS_CUT = ("Kids Haircut", 12, 15)

    def __init__(self, label, price, base_duration):
        """
        Initialize a Haircut enum member.

        Args:
            label (str): Human-readable name of the haircut.
            price (float): Price of the haircut.
            base_duration (int): Duration of the haircut in minutes.
        """
        self.label = label
        self.price = price
        self.base_duration = base_duration
