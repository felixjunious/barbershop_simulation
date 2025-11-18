from collections import deque
from threading import Lock

from order_generator import OrderGenerator
from barber import Barber


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



order_gen = OrderGenerator()
orders = order_gen.generate_orders(5)

for order in orders:
    add_order(order)

print("Initial Orders:")
show_order(order_queue)



barbers = [
    Barber("Barber-1", order_queue, queue_lock),
    Barber("Barber-2", order_queue, queue_lock)
]

for barber in barbers:
    barber.start()

for barber in barbers:
    barber.join()



print("Final Queue:")
show_order(order_queue)
