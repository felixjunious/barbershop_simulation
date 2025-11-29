
def hour_to_min(hours):
    """
    Convert hours to minutes.

    Args:
        hours (float or int): Time in hours.

    Returns:
        int: Equivalent time in minutes.
    """
    minutes = hours * 60
    return minutes

# Simulation settings
SIMULATION_TIME = 60                # Simulation time in minutes
TIME_DESCALE = 5                    # Descale simulation time for faster simulation (default: 1)
CUSTOMER_ARRIVAL_RATE = 0.4         # Probability of a customer arriving per minute
WAITING_ROOM_SIZE = 5               # Size of the waiting room / the queue
NUM_BARBERS = 4                     # Number of barbers serving customers in parallel
HOURLY_WAGES = 13                   # Hourly wage for each barber


