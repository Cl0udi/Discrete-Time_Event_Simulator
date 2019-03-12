import numpy as np
import random as rn

from Queue import PriorityQueue as pq
from subprocess import call

# Test value functions ###

def isValueBetweenOneAndFour(num):
	return True if (1 <= num <= 4) else False

def isValueBetweenZeroAndThousand(num):
	return True if (0 < num < 1000) else False

def testInputScheduleAlgorithm(num):
	print("hello")

def cleanInitialInputScheduleAlgorithm(scheduleAlgorithm):
	try:
		assert (isValueBetweenOneAndFour(scheduleAlgorithm)), "scheduleAlgorithm value should be an integer between 1 and 4"
	except:
		print("\nINPUT RANGE ERROR: \nscheduleAlgorithm selection should be an integer between 1 and 4\n")
		print("These are available options for Scheduling Algorthims:\n")
		print("1 - First Come First Serve")
		print("2 - Shortest Time Remaining First")
		print("3 - Highest Response Ratio Next")
		print("4 - Round Robin\n")
		while True:
			scheduleAlgorithm = raw_input('Number between 1 and 4:')
			try:
				scheduleAlgorithm = int(scheduleAlgorithm)
			except:
				print("\nPlease input a number")
				continue
			if (isValueBetweenOneAndFour(scheduleAlgorithm)):
				call("cowsay", "\nInput accepted :)\n")
				break
			else:
				print("\nNumber must be between 1 and 4")

	return int(scheduleAlgorithm)

def cleanInitialInputFloatValues(num, name):
	try:
		assert (isValueBetweenOneAndFour(scheduleAlgorithm)), name + " value should be a float bigger than 0 and smaller than 1000"
	except:
		print("\nINPUT RANGE ERROR: \n" + name +  " selection should be a float bigger than 0 and smaller than 1000\n")
		while True:
			num = raw_input('Number bigger than 0 and smaller than 1000:')
			try:
				num = float(num)
			except:
				print("\nPlease input a number")
				continue
			if (isValueBetweenZeroAndThousand(num)):
				print("\nInput accepted :)\n")
				break
			else:
				print("\nNumber must be bigger than 0 and smaller than 1000")

	return float(num)

# End of test value functions ###

def poissonStep(lmbda):
	return (np.log(rn.uniform(0, 1)))/(-lmbda) # x = (-1/lmbda)*ln(y)

class Process:
	def __init__(self, params):
		self.id = params.get('id')
		self.arrivalTime = params.get('arrivalTime')
		self.serviceTime = params.get('serviceTime')
		self.remainingTime = self.serviceTime - self.arrivalTime
		self.completionTime = 0