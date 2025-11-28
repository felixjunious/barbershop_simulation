from threading import Thread
from time import sleep
from config import TIME_DESCALE, NUM_BARBERS

class Barber(Thread):
    def __init__(self,name, order_queue, lock, working=False):
        super().__init__()
        self.name = name
        self.order_queue = order_queue
        self.lock = lock
        self.working = working
        self.current_order = None

    def serve_order(self):
        with self.lock:
            if not self.order_queue:
                self.current_order = None
                return False
            order = self.order_queue.pop()
            self.current_order = order
        self.process_order(order)
        self.current_order = None
        return True

    def process_order(self, order):
        print(f"{self.name} Serving {order.customer.name} ({order.haircut.name}, {order.duration} min)")
        sleep(order.duration / TIME_DESCALE)
        print(f"{self.name} Finished {order.customer.name}")

    def start_working(self):
        self.working = True

    def stop_working(self):
        self.working = False

    @staticmethod
    def generate_barbers(order_queue, queue_lock, num_of_barbers=NUM_BARBERS):
        return [Barber(f"Barber-{i+1}", order_queue, queue_lock) for i in range(num_of_barbers)]

    def run(self):
        self.start_working()

        while self.working or self.order_queue:
            served = self.serve_order()
            if not served:
                sleep(0.1)
