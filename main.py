from collections import deque
from customer import Customer
from haircut import Haircut
from order import Order
from customer_generator import CustomerGenerator
import random
from barber import Barber
from threading import Lock

TIME_DESCALE = 4

order_queue = deque()
queue_lock = Lock()

def add_order(order):
    with queue_lock:
        order_queue.appendleft(order)

def show_order(order_deque):

    SCALE = 1

    if order_deque:
        for order in order_deque:
            bar = "#" * int(order.duration * SCALE)
            print(f"{order.customer.name:10} | {order.haircut:12} | {bar} ({order.duration}m)")
    else:
        print("Queue Empty")

    print()


customer_gen = CustomerGenerator()
customers = customer_gen.generate_customers(5)

for cust in customers:
    haircut = random.choice(list(Haircut))
    order = Order(cust, haircut)
    add_order(order)

print("Initial order :")
show_order(order_queue)

barbers = [Barber(name, order_queue, queue_lock) for name in ["Barber-1", "Barber-2"]]  # e.g., 2 barbers
for b in barbers:
    b.start()

for b in barbers:
    b.join()

show_order(order_queue)