import random
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

N = 500
lam = 5 


dt_list = []
for _ in range(N):
    u = random.random() 
    dt = -math.log(1 - u) / lam
    dt_list.append(dt)

event_times = []
current_time = 0

for dt in dt_list:
    current_time += dt
    event_times.append(current_time)

# print("DT list",dt_list)
print("Event TIme",event_times)
# find max time to know how many bins we need
max_time = max(event_times)
num_bins = int(max_time) + 1

print(max_time,int(max_time),num_bins)

hist = {}
print(hist)

# histogram
for t in event_times:
    bin_index = int(t) 
    hist[bin_index] = hist.get(bin_index,0) +1
    # hist[bin_index] += 1
print("AFter",hist)
# # step 4: print histogram (bar-style)
for key, value in hist.items():
    print(f"Time {key}–{key+1}: {value} events")

counts_per_interval = list(hist.values())
freq = Counter(counts_per_interval)
print("Frew",freq)
sorted_event = sorted(freq.keys())
print("sorted_key",sorted_event)

total_intervals = sum(freq.values())
print("Total interval ",total_intervals)
for k in sorted_event:
    print(freq[k])
prob_exp = [freq[value] / total_intervals for value in sorted_event]
print("Probability",prob_exp)

max_event = max(sorted_event)
event_range = np.arange(0, max_event + 1)
poisson = [(lam**k * math.exp(-lam)) / math.factorial(k) for k in event_range]

print("Poission",poisson)
# scale theory to match histogram (important for comparison)
# scale = len(event_times)
# poisson_scaled = [p * scale for p in poisson]
# print("Poission",scale)

# print("Poission_scaled",poisson_scaled)
# plt.bar(hist.keys(),hist.values())
plt.figure(figsize=(8,5))

plt.bar(sorted_event, prob_exp, alpha=0.6, label="Experimental Probability")
plt.plot(event_range, poisson, 'r-o', label="Theoretical Poisson")

plt.xlabel("k = number of events per interval")
plt.ylabel("Probability P(k)")
plt.title("Poisson Process: Probability Comparison")
plt.legend()
plt.grid(True)

plt.show()
