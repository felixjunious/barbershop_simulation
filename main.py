from collections import deque
from customer import Customer
from haircut import Haircut
from order import Order
import random
import time

TIME_DESCALE = 4

order_queue = deque()

def add_order(order):
    order_queue.appendleft(order)

def serve_order():
    order = order_queue.pop()
    process_order(order)
    return order

def process_order(order):
    print(f"Serving {order.customer} ({order.haircut.name}, {order.duration} min)")
    time.sleep(order.duration / TIME_DESCALE)
    print(f"Finished {order.customer}")


customers = [Customer(name) for name in ["Alice", "Bob", "Charlie", "Diana", "Ethan"]]

for cust in customers:
    haircut = random.choice(list(Haircut))
    order = Order(cust, haircut)
    add_order(order)


print("Initial queue:")
print(order_queue, "\n")


while order_queue:
    order = serve_order()
    process_order(order)

print("Queue empty:", order_queue)