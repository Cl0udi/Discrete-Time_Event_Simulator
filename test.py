import numpy as np
import random as rn
import csv
import sys
from multiprocessing import Queue

# np.set_printoptions(precision=3)

# count = 1000
# lmbda = 10

# def poissonStep(lmbda):
# 	return (np.log(rn.uniform(0, 1)))/(-lmbda) # x = (-1/lmbda)*ln(y)

# intervals = []

# for t in range(count):
#     intervals.append(poissonStep(lmbda))
    
# timestamps = []
# timestamp = 0

# for t in range(count):
#     timestamp += intervals[t]
#     timestamps.append(timestamp)

# print('First 10 Steps:')
# print(timestamps[:10])

# print('\nAverage Lambda:')
# print(np.average(intervals))

# #print('yay' if md.isValueBetweenOneAndFour(scheduleAlgorithm) else 'boo')


# def poissonStep(num):
# 	randomUniform = rn.uniform(0, 1)
# 	while(randomUniform == 0 or randomUniform == 1):
# 		randomUniform = rn.uniform(0, 1)
# 	poissonValue = (np.log(randomUniform))/(-num) # x = (-1/lmbda)*ln(y) or (-Ts)*ln(y)
# 	# print("Poisson Value: " + str(poissonValue))
# 	return poissonValue

def test(lmba = 10, avgServiceTime = 0.06):
	
	bottle_list = []
	# Read all data from the csv file.
	with open('a.csv', 'rb') as b:
		bottles = csv.reader(b)
		bottle_list.extend(bottles)

	# data to override in the format {line_num_to_override:data_to_write}. 
	line_to_override = {1:['e', 'c', 'd'] }

	# Write data to the csv file and replace the lines in the line_to_override dict.
	with open('a.csv', 'wb') as b:
		writer = csv.writer(b)
		for line, row in enumerate(bottle_list):
			data = line_to_override.get(line, row)
			writer.writerow(data)


if __name__ == '__main__':
    # Map command line arguments to function arguments.
    test(*sys.argv[1:])