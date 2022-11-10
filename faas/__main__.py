import sys
import numpy as np

from .simulator import simulate
import matplotlib.pyplot as plt
import scipy.stats as st

# Constants 
alpha = 0.5 
mf = 100 
time = 30 * 24 * 60 * 60 # in seconds
stoptime = int(0.3 * 24 * 60 * 60)
maxmemory = 4000

def idealMemory(lambdas, service_rates, startMemory=100000):
    minimumMemory = 4000 
    mid = (startMemory + minimumMemory) // 2
    _, coldStartRatios, _ = simulate(stoptime, lambdas, service_rates, alpha, mf, mid)
    while pointEstimate(coldStartRatios) > 0.05: 
        minimumMemory = mid 
        mid = (startMemory + minimumMemory) // 2
        print(f"testing memory size= {mid}")
        _, coldStartRatios, _ = simulate(stoptime, lambdas, service_rates, alpha, mf, mid)
    return mid 

def pointEstimate(data, ignore=4000):
    return sum(data[ignore:]) / (len(data) - ignore)

def confidence_interval(data, ignore=4000):
    m = pointEstimate(data, ignore)
    return st.norm.interval(confidence=0.95, loc=m)

def results(times, coldStartRatios, lossRates): 
    print(f"Cold start ratio: {pointEstimate(coldStartRatios)}")
    print(f"95% confidence interval for Cold start ratio: {confidence_interval(coldStartRatios)}\n")
    print(f"loss rate: {pointEstimate(lossRates)}")
    print(f"95% confidence interval for loss rate: {confidence_interval(lossRates)}\n")

    plt.subplot(211)
    plt.plot(times, coldStartRatios, label='Cold Start Ratios', color='b')
    plt.ylabel('Cold Start Ratios')

    plt.subplot(212)
    plt.plot(times, lossRates, label='Loss Rates', color='r')
    plt.ylabel('Loss Rates')

    plt.xlabel('times')
    plt.show()

if __name__ == "__main__":
    data = np.loadtxt(sys.argv[1], skiprows=1, delimiter=',', dtype=int)

    lambdas = data[:, 2] / time 
    service_rates = 1000 / data[:,1]

    times, coldStartRatios, lossRates = simulate(stoptime, lambdas, service_rates, alpha, mf, maxmemory) 

    results(times, coldStartRatios, lossRates)

    # binary search to find optimal maxMemory
    idealmem = idealMemory(lambdas, service_rates, 65000)
    print(f"Ideal maxMemory: {idealmem}")

    # times, coldStartRatios, lossRates = simulate(stoptime, lambdas, service_rates, alpha, mf, idealmem) 
    # results(times, coldStartRatios, lossRates)

