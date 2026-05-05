import random
import math
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np


def Datapreparation(lam,sample):
    hist = {}
    dt_list = []
    event_times = []
    poisson = []
    current_time = 0

    for _ in range(sample):
        u = random.random() 
        dt = -math.log(1 - u) / lam
        dt_list.append(dt)

    current_time = 0
    for dt in dt_list:
        current_time += dt
        event_times.append(current_time)

    # bins identification
    max_event = math.ceil(max(event_times))
    print("Max event",max_event)
    num_bins = int(max_event) + 1
  
    for t in event_times:
        bin_index = int(t) 
        hist[bin_index] = hist.get(bin_index,0) +1

    counts_per_interval = [hist.get(i, 0) for i in range(num_bins)]
    print("Count per intervals",counts_per_interval)
    freq = Counter(counts_per_interval)
    print(freq.keys())
    max_k = max(counts_per_interval)
    # event_range = np.arange(0, max_k + 1)
    # prob_exp = [freq.get(k, 0) / len(counts_per_interval) for k in event_range]
    sorted_event = sorted(freq.keys())
    total_intervals = len(counts_per_interval)
    prob_exp = [freq[value] / total_intervals for value in sorted_event]
    
    event_range = np.arange(0, max_k + 1)
    print("sorted intervals",sorted_event,sorted(freq.keys()))
    p0 = math.exp(-lam)  
    poisson.append(p0)
    for k in range(1, max_k + 1):
          pk = poisson[k-1] * lam / k
          poisson.append(pk)
    print(len(poisson))
    #poisson = [(lam**k * math.exp(-lam)) / math.factorial(k) for k in event_range]

    return sorted_event,prob_exp,event_range,poisson



def different_lam(lam_values, sample):
    n = len(lam_values)
    print("LENgth",n)
    # dynamic height: 4 per subplot, but minimum 5
    height = max(8, 8)

    fig, axes = plt.subplots(2, 3, figsize=(8, 8))
    axes = axes.flatten()
    if n == 1:
        axes = [axes]
        
    for i, lam in enumerate(lam_values):
        sorted_event, prob_exp, event_range, poisson = Datapreparation(lam, sample)

        axes[i].bar(sorted_event, prob_exp, alpha=0.6, label="Experimental")
        axes[i].plot(event_range, poisson, 'r-o', label="Theoretical")

        axes[i].set_title(f"λ = {lam}")
        axes[i].set_xlabel("k = number of events")
        axes[i].set_ylabel("P(k)= probability")
        axes[i].legend()
        axes[i].grid(True)
    plt.suptitle(f"Poisson Distribution for Multiple λ (n = {sample})", fontsize=18)
    plt.tight_layout()
    plt.show()

def different_lam_same_plot(lam_values, sample):
    plt.figure(figsize=(10,6))
    for lam in lam_values:
        sorted_event, prob_exp, event_range, poisson = Datapreparation(lam, sample)
        plt.plot(sorted_event, prob_exp,label=f"Exp λ={lam}")

        # Theoretical
        # plt.plot(event_range, poisson, marker='o', linestyle='-',label=f"Theory λ={lam}")
    plt.xlabel("k = number of events")
    plt.ylabel("P(k)")
    plt.title("Poisson Distribution for Multiple λ")
    plt.legend()
    plt.grid(True)

    plt.show()

def DataPreparation(lam_values,sample):
    all_event_times = []
    max_lam = max(lam_values)
    print("Lllll",max_lam)
    max_event_time = None

    for lam in lam_values:
        event_times = []
        current_time = 0

        for _ in range(sample):
            u = random.random()
            dt = -math.log(1 - u) / lam
            current_time += dt
            event_times.append(current_time)

        print("Event Times #######",event_times)

        if lam == max_lam:
            print("Event Times*******************",event_times,lam)
            max_event_time = math.ceil(max(event_times))
            max_time = int(event_times[-1]) + 1
            print("MAx even time",max_event_time)
            print("MAXXX",max_time)

        # now merge everything
        all_event_times.extend(event_times)
    print("Upper event",sorted(all_event_times))
    return all_event_times, max_event_time

def SuperpositionSimulation(lam_values,sample):
    poisson = []

    all_event_times,max_event_time = DataPreparation(lam_values,sample)
    print("ALLL event times",)
    # least_event = DatapPreparation(lam_values,sample)
    # max_time = int(least_event[-1]) + 1

    all_event_times_sorted = sorted(all_event_times)
    print("ALL time events",all_event_times_sorted)
    hist = {}
    # max_time = int(all_event_times_sorted[-1]) + 1
    num_bins = int(max_event_time) + 1
    print("Max time",num_bins)
    for t in all_event_times_sorted:
        bin_index = int(t)
        hist[bin_index] = hist.get(bin_index, 0) + 1

    counts_per_interval = [hist.get(i, 0) for i in range(num_bins)]
    freq = Counter(counts_per_interval)

    print("Count Per interval",counts_per_interval)
    print("Freq",freq.keys(),freq.values(),len(freq))
    print("MAx",max(freq.values()))

    sorted_event = sorted(freq.keys())
    print("Length",sorted_event)
   
    total = sum(freq.values())
    prob_exp = [freq[k] / total for k in sorted_event]
    print("EXP",prob_exp,total)

    lam_total = sum(lam_values)
    event_range = np.arange(0, max(sorted_event) + 1)

    
    p0 = math.exp(-lam_total)
    poisson.append(p0)
    for k in range(1, len(event_range)):
        pk = poisson[k-1] * lam_total / k
        poisson.append(pk)
    print("Poission",poisson)
    plt.bar(sorted_event, prob_exp, width=1.0,alpha=0.6, label="Experimental Probability")
    plt.plot(event_range, poisson, 'r-o', label="Theoretical Poisson")

    plt.xlabel("k = number of events per interval")
    plt.ylabel("Probability P(k)")
    plt.title(f"Poisson Process lamda:{lam_values}, sample:{sample}")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    lam_values = [5,9]
    # lam_values = [0.5, 1.0, 5.0, 10.0, 50.0]
    # lam_values = [50]
    sample = 500
    # different_lam(lam_values, sample)
    SuperpositionSimulation(lam_values, sample)
    # Test(5,500)
    # different_lam_same_plot(lam_values, sample)

if __name__ == "__main__":
    main()


