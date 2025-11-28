from threading import Thread
from time import sleep
from config import TIME_DESCALE, NUM_BARBERS, HOURLY_WAGES


class Barber(Thread):
    """
    Represents a barber who serves customers in a barbershop simulation.

    Attributes:
        name (str): Barber's name.
        order_queue (list): Shared queue of customer orders.
        lock (threading.Lock): Lock to synchronize access to the queue.
        working (bool): Whether the barber is currently working.
        wage (float): Hourly wage of the barber.
        stats_tracker (object): Optional tracker for recording simulation statistics.
        time_manager (object): Optional manager for tracking current simulation time.
        current_order (object): The order currently being served.
    """

    def __init__(self, name, order_queue, lock, working=False, wage=HOURLY_WAGES, stats_tracker=None,
                 time_manager=None):
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
        """
        Serve the next customer order if available.

        Args:
            current_time (float, optional): Current simulation time in minutes.

        Returns:
            bool: True if an order was served, False if no orders were available.
        """
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
        """
        Simulate serving a customer order.

        Args:
            order (Order): Customer order containing haircut details and duration.
        """
        print(f"{self.name} serving {order.customer.name} ({order.haircut.name}, {order.duration} min)")
        sleep(order.duration / TIME_DESCALE)
        print(f"{self.name} finished {order.customer.name}")

    def start_working(self):
        """Set the barber as working."""
        self.working = True

    def stop_working(self):
        """Set the barber as not working."""
        self.working = False

    @staticmethod
    def generate_barbers(order_queue, queue_lock, stats_tracker=None, time_manager=None, num_of_barbers=NUM_BARBERS):
        """
        Generate a list of Barber instances.

        Args:
            order_queue (deque): Shared queue of customer orders.
            queue_lock (threading.Lock): Lock for synchronizing queue access.
            stats_tracker (object, optional): Tracker for recording statistics.
            time_manager (object, optional): Manager for simulation time.
            num_of_barbers (int): Number of barbers to generate.

        Returns:
            list: List of Barber instances.
        """
        return [
            Barber(
                f"Barber-{i + 1}",
                order_queue,
                queue_lock,
                stats_tracker=stats_tracker,
                time_manager=time_manager
            )
            for i in range(num_of_barbers)
        ]

    def run(self):
        """
        Main thread loop for the barber. Continuously serves orders while working
        or while there are orders in the queue. Records idle time when no orders are available.
        """
        self.start_working()

        while self.working or self.order_queue:
            served = self.serve_order(current_time=self.time_manager.current if self.time_manager else None)
            if not served:
                idle_duration = 0.1
                sleep(0.1 / TIME_DESCALE)
                if self.stats_tracker:
                    self.stats_tracker.record_idle_time(self.name, idle_duration)
