import random
import math
import heapq
from collections import deque
import matplotlib.pyplot as plt


ARRIVAL = "arrival"
DEPARTURE = "departure"


# Exponential random variable
def exp_rv(rate):
    return -math.log(1 - random.random()) / rate
def avg_queue_length(event_log):

    total_area = 0.0
    prev_time = 0.0
    prev_q = 0

    for e in event_log:
        if e["event"] == "arrival":
            current_time = e["time"]
            q_len = e["queue_length"]
        else:
            current_time = e["departure_time"]
            q_len = e["queue_length_after"]

        # convert system size → waiting queue size
        waiting_q = max(q_len - 1, 0)

        duration = current_time - prev_time
        total_area += prev_q * duration

        prev_time = current_time
        prev_q = waiting_q

    total_time = prev_time
    return total_area / total_time if total_time > 0 else 0.0


def plot_wait_queue(event_log):
    times = []
    queue_lengths = []

    for e in event_log:
        times.append(e["time"] if e["event"] == "arrival" else e["departure_time"])
        
        if e["event"] == "arrival":
            queue_lengths.append(e["queue_length"])
        else:
            queue_lengths.append(e["queue_length_after"])

    waits = []
    customers = []
    i = 0
    for e in event_log:
        if e["event"] == "departure":
            wait = e["start_time"] - e["arrival_time"]
            waits.append(wait)
            customers.append(i)
            i += 1

    fig, axs = plt.subplots(2, 1, figsize=(8, 8))

    axs[0].step(times, queue_lengths, where='post')
    axs[0].set_xlabel("Time")
    axs[0].set_ylabel("Queue Length")
    axs[0].set_title("M/M/1 Queue Length Over Time")
    axs[0].grid(True)

    axs[1].plot(customers, waits, marker='o')
    axs[1].set_xlabel("Customer Index")
    axs[1].set_ylabel("Waiting Time")
    axs[1].set_title("Waiting Time per Customer")
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()


def print_event_log(event_log):
    print("************************************")

    for i, e in enumerate(event_log, 1):
        if e["event"] == "arrival":
            print(f"[{i}] ARRIVAL")
            print(f"    Time           : {e['time']:.4f}")
            print(f"    Queue Length   : {e['queue_length']}")
            print(f"    Server Busy    : {e['server_busy']}")
        else:
            print(f"[{i}] DEPARTURE")
            print(f"    Arrival Time   : {e['arrival_time']:.4f}")
            print(f"    Start Time     : {e['start_time']:.4f}")
            print(f"    Departure Time : {e['departure_time']:.4f}")
            print(f"    Service Time   : {e['service_time']:.4f}")
            print(f"    Queue After    : {e['queue_length_after']}")
        print("-" * 40)



def mm1_simulation(lam, mu, sample_size):
    event_queue = []
    queue = deque()

    arrival_events = []
    departure_events = []
    event_log = []
    # server state
    server_busy = False

    # statistics
    time = 0.0
    total_wait = 0.0
    total_system_time = 0.0
    num_served = 0

    # first arrival
    heapq.heappush(event_queue, (exp_rv(lam), ARRIVAL))

    while event_queue and num_served < sample_size:
        time, event_type = heapq.heappop(event_queue)
        if event_type == ARRIVAL:
            arrival_events.append(time)
            # log arrival
            event_log.append({
                "event": "arrival",
                "time": time,
                "queue_length": len(queue),
                "server_busy": server_busy
            })


            #next arrival
            next_arrival = time + exp_rv(lam)
            heapq.heappush(event_queue, (next_arrival, ARRIVAL))

            if server_busy:
                queue.append({
                    "arrival_time": time,
                    "service_time": None,
                    "start_time": None
                })
            else:
                server_busy = True
                customer = {
                    "arrival_time": time,
                    "service_time": exp_rv(mu),
                    "start_time": time
                }
                queue.appendleft(customer)

                departure_time = time + customer["service_time"]
                heapq.heappush(event_queue, (departure_time, DEPARTURE))

         
        elif event_type == DEPARTURE:
            departure_events.append(time)
            customer = queue.popleft()

            arrival_time = customer["arrival_time"]
            service_time = customer["service_time"]
            start_time = customer["start_time"]

            num_served += 1

            system_time = time - arrival_time
            total_system_time += system_time
            wait_time = start_time - arrival_time
            total_wait += wait_time

            # log departure
            event_log.append({
                "event": "departure",
                "arrival_time": arrival_time,
                "start_time": start_time,
                "departure_time": time,
                "service_time": service_time,
                "queue_length_after": len(queue)
            })

       
            # start next event if queue not empty
            if queue:
                next_customer = queue[0]
                next_customer["service_time"] = exp_rv(mu)
                next_customer["start_time"] = time

                departure_time = time + next_customer["service_time"]
                heapq.heappush(event_queue, (departure_time, DEPARTURE))
                server_busy = True

            else:
                server_busy = False

    # for e in event_log:
    #     print(e)

    avg_wait = total_wait / num_served if num_served > 0 else 0.0
    avg_system = total_system_time / num_served if num_served > 0 else 0.0

    print("Numbered Served",num_served)
    print("Average Wait",avg_wait)
    print("Average system time",avg_system)

    print("Utilization factor",lam/mu)
    print("Average Number of Customer in System",lam/(mu-lam))
    print("Average time a customer spends in the system (W)",1/(mu-lam))
    print("Average Queue length(Theoretical)",(lam*lam)/(mu*(mu-lam)))
    print("Average Queue length(Experimental)",avg_queue_length(event_log))
    print("Average time waiting in the line (W_q)",lam/(mu*(mu-lam)))


    return event_log

def main():
    lam = 19
    sample = 100000
    meu = 20
    log = mm1_simulation(lam,meu,sample)
    # print_event_log(log)
    plot_wait_queue(log)


if __name__ == "__main__":
    main()


# import random
# import math
#  # for priority queue (sorted event list)

# # Exponential random variable
# def exp_rv(rate):
#     return -math.log(1 - random.random()) / rate

# def mm1_simulation(lam, mu, max_events=1000):
#     # Event types
#     ARRIVAL = "arrival"
#     DEPARTURE = "departure"

#     # Event list (priority queue)
#     event_list = []

#     # Initialize with first arrival at t=0
#     heapq.heappush(event_list, (0, ARRIVAL))

#     # Queue (FIFO)
#     queue = []

#     # Server state
#     server_busy = False

#     # Stats
#     current_time = 0
#     num_in_system = 0

#     for _ in range(max_events):
#         if not event_list:
#             break

#         # 1. Get next event
#         current_time, event_type = heapq.heappop(event_list)

#         if event_type == ARRIVAL:
#             # 2. Arrival event
#             queue.append(current_time)
#             num_in_system += 1

#             # Schedule next arrival
#             next_arrival = current_time + exp_rv(lam)
#             heapq.heappush(event_list, (next_arrival, ARRIVAL))

#         elif event_type == DEPARTURE:
#             # 3. Departure event
#             server_busy = False
#             num_in_system -= 1

#         # 4. If server is free, try to serve next packet
#         if not server_busy and queue:
#             arrival_time = queue.pop(0)  # FIFO
#             server_busy = True

#             service_time = exp_rv(mu)
#             departure_time = current_time + service_time

#             heapq.heappush(event_list, (departure_time, DEPARTURE))

#     return