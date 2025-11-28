import random
from collections import deque
from threading import Lock
from order_generator import OrderGenerator
from barber import Barber
from config import *
from stats_tracker import StatsTracker
from time_manager import TimeManager


def add_order(order, queue, lock):
    with lock:
        queue.appendleft(order)


def show_order(order_deque):
    scale = 1
    if order_deque:
        for order in order_deque:
            bar = "#" * int(order.duration * scale)
            print(f"{order.customer.name:10} | {order.haircut:12} | {bar} ({order.duration}m)")
    else:
        print("Queue Empty")
    print()


def display_state(barbers, order_queue):
    print("\n" * 5)
    print("=== Barbershop Simulation ===")
    print("\nBarbers:")
    for barber in barbers:
        if barber.current_order:
            order = barber.current_order
            print(f"{barber.name:10} -> {order.customer.name} ({order.haircut.name}, {order.duration}m)")
        else:
            print(f"{barber.name:10} -> Idle")

    print("\nQueue:")
    if order_queue:
        for order in order_queue:
            bar = "#" * order.duration
            print(f"{order.customer.name:10} | {order.haircut.name:12} | {bar} ({order.duration}m)")
    else:
        print("Empty")


def handle_customer_arrival(order_gen, order_queue, queue_lock, stats_tracker, current_time):
    if random.random() < CUSTOMER_ARRIVAL_RATE:
        new_order = order_gen.generate_order()
        new_order.arrival_time = current_time  # Track arrival

        if len(order_queue) < WAITING_ROOM_SIZE:
            add_order(new_order, order_queue, queue_lock)
            stats_tracker.record_new_customer(len(order_queue))
            return f"[+] New Customer: {new_order.customer.name}", new_order
        else:
            stats_tracker.record_customer_lost()
            return "[X] Customer Left (Waiting room full)", None
    return "", None


def start_barbers(barbers):
    for barber in barbers:
        barber.start()


def shutdown_barbers(barbers):
    for barber in barbers:
        barber.stop_working()
    for barber in barbers:
        barber.join()


def barbers_busy(barbers):
    return any(barber.current_order is not None for barber in barbers)


def main():
    order_queue = deque()
    queue_lock = Lock()
    order_gen = OrderGenerator()
    time_manager = TimeManager()
    stats_tracker = StatsTracker()

    # Create barbers with access to stats and time manager
    barbers = Barber.generate_barbers(
        order_queue,
        queue_lock,
        stats_tracker=stats_tracker,
        time_manager=time_manager
    )

    start_barbers(barbers)

    while time_manager.check_time() or order_queue or barbers_busy(barbers):
        if time_manager.check_time():
            new_customer_msg, _ = handle_customer_arrival(
                order_gen,
                order_queue,
                queue_lock,
                stats_tracker,
                time_manager.current
            )
        else:
            new_customer_msg = ""

        display_state(barbers, order_queue)
        print(f"Current Time: {time_manager.formatted()} | {new_customer_msg}")

        time_manager.tick()

    shutdown_barbers(barbers)
    display_state(barbers, order_queue)
    print(f"Current Time: {time_manager.formatted()} | ")

    # Print final simulation stats
    stats_tracker.print_summary()


if __name__ == "__main__":
    main()
