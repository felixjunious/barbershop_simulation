import random
import time
import os
from collections import deque
from threading import Lock
from order_generator import OrderGenerator
from barber import Barber
from config import *

#Simulation Settings
SIMULATION_TIME = 60
CUSTOMER_ARRIVAL_RATE = 0.8
WAITING_ROOM_SIZE = 5
TIME_DESCALE = 0.25

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


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_state(barbers, order_queue):
    clear_console()

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


def main():

    order_queue = deque()
    queue_lock = Lock()
    order_gen = OrderGenerator()

    barbers = [
        Barber("Barber-1", order_queue, queue_lock),
        Barber("Barber-2", order_queue, queue_lock)
    ]

    for barber in barbers:
        barber.start()

    current_time = 0
    while current_time < SIMULATION_TIME:
        new_customer_msg = ""

        if random.random() < CUSTOMER_ARRIVAL_RATE:
            new_order = order_gen.generate_order()

            if len(order_queue) < WAITING_ROOM_SIZE:
                add_order(new_order, order_queue, queue_lock)
                new_customer_msg = f"[+] New Customer: {new_order.customer.name}"
            else:
                new_customer_msg = "[X] Customer Left (Waiting room full)"

        display_state(barbers, order_queue)
        print(f"Current Time: {current_time} min | {new_customer_msg}")

        time.sleep(1 / TIME_DESCALE)
        current_time += 1

    for barber in barbers:
        barber.stop_working()

    for barber in barbers:
        barber.join()

    print("Final Queue:")
    show_order(order_queue)

if __name__ == "__main__":
    main()
