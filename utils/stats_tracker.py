from threading import Lock
from config import HOURLY_WAGES

class StatsTracker:
    """
    Tracks and summarizes statistics for the barbershop simulation.

    Attributes:
        lock (threading.Lock): Thread lock to synchronize updates.
        total_haircuts (dict): Total haircuts per barber.
        total_service_time (dict): Total service time per barber (in minutes).
        total_idle_time (dict): Total idle time per barber (in minutes).
        total_work_time (dict): Total work time per barber (in minutes).
        customer_wait_times (list of float): Wait times for all customers.
        peak_queue_length (int): Maximum queue length observed.
        total_revenue (float): Total revenue from haircuts.
        customers_lost (int): Number of customers who left due to full waiting room.
        service_distribution (dict): Count of haircuts per haircut type.
    """

    def __init__(self):
        """Initialize the StatsTracker with empty statistics."""
        self.lock = Lock()

        self.total_haircuts = {}        # per barber
        self.total_service_time = {}    # per barber
        self.total_idle_time = {}       # per barber
        self.total_work_time = {}       # per barber

        self.customer_wait_times = []   # in minutes
        self.peak_queue_length = 0

        self.total_revenue = 0
        self.customers_lost = 0         # left due to full waiting room
        self.service_distribution = {}  # per haircut type name

    def record_new_customer(self, queue_length):
        """Update peak queue length if the current queue is longer."""
        with self.lock:
            if queue_length > self.peak_queue_length:
                self.peak_queue_length = queue_length

    def record_customer_lost(self):
        """Increment the counter for customers who left due to full waiting room."""
        with self.lock:
            self.customers_lost += 1

    def record_wait_time(self, wait_time):
        """Record the wait time for a customer."""
        with self.lock:
            self.customer_wait_times.append(wait_time)

    def record_haircut(self, barber, service_time, revenue, haircut_type):
        """
        Record statistics for a completed haircut.

        Args:
            barber (str): Name of the barber.
            service_time (float): Duration of the haircut in minutes.
            revenue (float): Revenue earned from the haircut.
            haircut_type (str): Type of haircut performed.
        """
        with self.lock:
            self.total_haircuts[barber] = self.total_haircuts.get(barber, 0) + 1
            self.total_service_time[barber] = self.total_service_time.get(barber, 0) + service_time
            self.total_revenue += revenue
            self.service_distribution[haircut_type] = self.service_distribution.get(haircut_type, 0) + 1

    def record_idle_time(self, barber, idle_time):
        """Record idle time for a barber."""
        with self.lock:
            self.total_idle_time[barber] = self.total_idle_time.get(barber, 0) + idle_time

    def record_work_time(self, barber, duration):
        """Record working time for a barber."""
        with self.lock:
            self.total_work_time[barber] = self.total_work_time.get(barber, 0) + duration

    def print_summary(self):
        """Print a summary report of the simulation statistics."""
        print("\n=== Simulation Summary ===\n")

        # Customers
        total_customers_served = sum(self.total_haircuts.values())
        print(f"Total Customers Served: {total_customers_served}")
        print(f"Customers Lost: {self.customers_lost}")
        print(f"Peak Queue Length: {self.peak_queue_length}")

        # Revenue, Wages, Profit
        total_wages = 0
        for barber in self.total_haircuts:
            service = self.total_service_time.get(barber, 0)
            idle = self.total_idle_time.get(barber, 0)
            service_r = round(service)
            idle_r = round(idle)
            total_time_rounded = service_r + idle_r
            total_wages += HOURLY_WAGES * total_time_rounded / 60  # wages based on rounded minutes

        profit = self.total_revenue - total_wages
        print(f"\nTotal Revenue: ${self.total_revenue:.2f}")
        print(f"Total Wages: ${total_wages:.2f}")
        print(f"Profit: ${profit:.2f}")

        # Customer wait times
        if self.customer_wait_times:
            avg_wait = sum(self.customer_wait_times) / len(self.customer_wait_times)
            max_wait = max(self.customer_wait_times)
            print(f"\nAverage Customer Wait Time: {round(avg_wait,2)} min")
            print(f"Maximum Customer Wait Time: {round(max_wait,2)} min")

        # Per-Barber metrics
        print("\nPer-Barber Stats:")
        overall_service_time = sum(self.total_service_time.values())
        overall_idle_time = sum(self.total_idle_time.values())
        overall_total_time = overall_service_time + overall_idle_time

        for barber in self.total_haircuts:
            haircuts = self.total_haircuts[barber]
            service = self.total_service_time.get(barber, 0)
            idle = self.total_idle_time.get(barber, 0)

            # Round for display
            service_r = round(service)
            idle_r = round(idle)
            total_time_rounded = service_r + idle_r

            utilization_r = round(service_r / total_time_rounded * 100, 2) if total_time_rounded > 0 else 0
            idle_ratio_r = round(idle_r / total_time_rounded * 100, 2) if total_time_rounded > 0 else 0
            avg_service_r = round(service / haircuts, 2) if haircuts > 0 else 0
            wages_r = round(HOURLY_WAGES * total_time_rounded / 60, 2)

            print(f"{barber}: Haircuts={haircuts}, Service={service_r} min, Idle={idle_r} min, "
                  f"Utilization={utilization_r}%, Idle Ratio={idle_ratio_r}%, Avg Service={avg_service_r} min, Wages=${wages_r}")

        # Shop-Level metrics
        overall_utilization = (overall_service_time / overall_total_time * 100) if overall_total_time > 0 else 0
        avg_idle_per_barber = (overall_idle_time / len(self.total_haircuts)) if self.total_haircuts else 0
        avg_revenue_per_customer = (self.total_revenue / total_customers_served) if total_customers_served else 0

        print("\nShop-Level Metrics:")
        print(f"Overall Barber Utilization: {round(overall_utilization, 2)}%")
        print(f"Average Idle Time per Barber: {round(avg_idle_per_barber, 2)} min")
        print(f"Average Revenue per Customer Served: ${round(avg_revenue_per_customer, 2)}")

        # Haircut distribution
        print("\nHaircut Distribution:")
        for haircut, count in self.service_distribution.items():
            print(f"{haircut}: {count}")
