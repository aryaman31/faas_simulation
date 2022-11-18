import heapq as hq
from numpy import random

def simulate(stopTime, arrival_rates, service_rates, alpha, mf, maxmemory):
    time = queueInitialFunctionRequests(arrival_rates) # store next time and function to issue 
    memory = addInitialToMemory(time, maxmemory, mf) # store function in memory with the time it becomes idle
    prints = False

    coldStartRatios = []
    lossrates = []
    times = []
    total = 0
    coldStarts = 0
    losses = 0
    minimumIdleTime = 2

    now = 0 
    while now < stopTime:
        now, f = hq.heappop(time)
        if prints: print(now)
        if prints: print(f"Request for function {f}")

        # Check if f is in memory, if it is, update the end time 
        mem_func_i = inMemory(f, memory)
        if mem_func_i != -1:
            if prints: print(f"Function {f} in memory")
            end_time, _ = memory[mem_func_i]
            if end_time + minimumIdleTime < now: # function is idle right now
                if prints: print(f"Function {f} is idle. New end time assigned")
                memory[mem_func_i] = (now + random.exponential(1 / service_rates[f - 1]), f) # set functions new end time to now + service time 
            else: # function not idle, so request is lost 
                losses += 1
                if prints: print(f"Function {f} is busy, cannot service request")
        else: # else remove oldest end time function and add f with new end time + load time 
            replace_i = earliestEndMemory(memory)
            if prints: print(f"Function {f} not in memory")
            if memory[replace_i][0] + minimumIdleTime < now: # can deallocate since function is idle 
                coldStarts += 1

                if prints: print(f"Function {f} added to memory succesfully")
                memory.pop(replace_i)
                memory.append((now + random.exponential(1/alpha) + random.exponential(1 / service_rates[f - 1]), f))
            else:
                losses += 1
                if prints: print(f"Function {f} is cannot be allocated on memory, no existing functions to remove")
        
        if prints: print()
        # add next function call
        hq.heappush(time, (now + random.exponential(1/arrival_rates[f - 1]), f))

        total += 1
        times.append(now)
        coldStartRatios.append(coldStarts / total)
        lossrates.append(losses / total)

    return times, coldStartRatios, lossrates

def queueInitialFunctionRequests(arrival_rates):
    time = []
    hq.heapify(time)
    for i, v in enumerate(arrival_rates):
        hq.heappush(time, (random.exponential(1/v), i + 1))
    return time

def addInitialToMemory(time, memory_size, mf):
    smallest = hq.nsmallest(memory_size // mf, time)
    return list(map((lambda x : (-1, x[1])), smallest)) 
        
def inMemory(f, memory): # returns the index of where function is stored in memory else -1
    for i, (_, fin) in enumerate(memory):
        if f == fin: 
            return i 
    return -1

def earliestEndMemory(memory):
    m = (0, memory[0][0])
    for i, (e, _) in enumerate(memory):
        if e < m[1]:
            m = (i, e)
    return m[0]