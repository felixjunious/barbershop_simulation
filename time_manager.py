from config import SIMULATION_TIME, TIME_DESCALE
import time

class TimeManager:
    def __init__(self, total_time=SIMULATION_TIME, descaler=TIME_DESCALE):
        self.current = 0
        self.total = total_time
        self.descale = descaler

    def tick(self):
        time.sleep(1 / self.descale)
        self.current += 1

    def check_time(self):
        return self.current < self.total

    def reset(self):
        self.current = 0

    def formatted(self):
        return f"{self.current} min"