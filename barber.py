from threading import Thread
from time import sleep

TIME_DESCALE = 4

class Barber(Thread):
    def __init__(self,name, order_queue, lock):
        super().__init__()
        self.name = name
        self.order_queue = order_queue
        self.lock = lock

    def serve_order(self):
        with self.lock:
            if not self.order_queue:
                return False
            order = self.order_queue.pop()
        self.process_order(order)
        return True

    def process_order(self, order):
        print(f"{self.name } Serving {order.customer} ({order.haircut.name}, {order.duration} min)")
        sleep(order.duration / TIME_DESCALE)
        print(f"{self.name } Finished {order.customer}")

    def run(self):
        while True:
            served = self.serve_order()
            if not served:
                break
