import numpy as np
import random as rn

np.set_printoptions(precision=3)

count = 1000
lmbda = 10

def poissonStep(lmbda):
	return (np.log(rn.uniform(0, 1)))/(-lmbda) # x = (-1/lmbda)*ln(y)

intervals = []

for t in range(count):
    intervals.append(poissonStep(lmbda))
    
timestamps = []
timestamp = 0

for t in range(count):
    timestamp += intervals[t]
    timestamps.append(timestamp)

print('First 10 Steps:')
print(timestamps[:10])

print('\nAverage Lambda:')
print(np.average(intervals))

#print('yay' if md.isValueBetweenOneAndFour(scheduleAlgorithm) else 'boo')
