from enum import Enum

class Haircut(Enum):
    NORMAL = ("Normal Haircut", 15, 20)
    DRY = ("Dry Haircut", 10, 15)
    NORMAL_WASH = ("Haircut + Wash", 17, 30)
    BEARD_TRIM = ("Beard Trim", 10, 10)
    BEARD_SHAVE = ("Beard Shave", 12, 15)
    HAIR_BEARD = ("Hair + Beard", 25, 40)
    KIDS_CUT = ("Kids Haircut", 12, 15)

    def __init__(self, label, price, base_duration):
        self.label = label
        self.price = price
        self.base_duration = base_duration

