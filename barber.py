from threading import Thread
from time import sleep
from config import TIME_DESCALE, NUM_BARBERS, HOURLY_WAGES

class Barber(Thread):
    def __init__(self,name, order_queue, lock, working=False, wage=HOURLY_WAGES, stats_tracker=None, time_manager=None):
        super().__init__()
        self.name = name
        self.order_queue = order_queue
        self.lock = lock
        self.working = working
        self.wage = wage
        self.stats_tracker = stats_tracker
        self.time_manager = time_manager
        self.current_order = None

    def serve_order(self, current_time=None):
        with self.lock:
            if not self.order_queue:
                self.current_order = None
                return False
            order = self.order_queue.pop()
            self.current_order = order

        wait_time = current_time - order.arrival_time if current_time is not None else 0

        if self.stats_tracker:
            self.stats_tracker.record_wait_time(wait_time)

        self.process_order(order)

        if self.stats_tracker:
            self.stats_tracker.record_haircut(
                barber=self.name,
                service_time=order.duration,
                revenue=order.haircut.price,
                haircut_type=order.haircut.name
            )
            self.stats_tracker.record_work_time(self.name, order.duration)

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
    def generate_barbers(order_queue, queue_lock, stats_tracker=None, time_manager=None, num_of_barbers=NUM_BARBERS):
        return [
            Barber(f"Barber-{i + 1}", order_queue, queue_lock, stats_tracker=stats_tracker, time_manager=time_manager)
            for i in range(num_of_barbers)
        ]

    def run(self):
        self.start_working()

        while self.working or self.order_queue:
            served = self.serve_order(current_time=self.time_manager.current)
            if not served:
                idle_duration = 0.1  # convert sleep to simulation minutes
                sleep(0.1/TIME_DESCALE)
                if self.stats_tracker:
                    self.stats_tracker.record_idle_time(self.name, idle_duration)

