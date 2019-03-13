import numpy as np
import random as rn

from multiprocessing import Queue
from subprocess import call

# Test value functions ###

def isValueBetweenOneAndFour(num):
	return True if (1 <= num <= 4) else False

def isValueBetweenZeroAndThousand(num):
	return True if (0.0 < num < 1000.0) else False


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
			scheduleAlgorithm = raw_input('Number between 1 and 4: ')
			try:
				scheduleAlgorithm = int(scheduleAlgorithm)
			except:
				print("\nPlease input a number")
				continue
			if (isValueBetweenOneAndFour(scheduleAlgorithm)):
				print("\nInput accepted :)\n")
				break
			else:
				print("\nNumber must be between 1 and 4")

	return int(scheduleAlgorithm)

def cleanInitialInputFloatValues(num, name):
	try:
		assert (isValueBetweenZeroAndThousand(num)), name + " value should be a float bigger than 0 and smaller than 1000"
	except:
		print("\nINPUT RANGE ERROR: \n" + name +  " selection should be a float bigger than 0 and smaller than 1000\n")
		while True:
			num = raw_input('Number bigger than 0 and smaller than 1000: ')
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

def poissonStep(num):
	randomUniform = rn.uniform(0, 1)
	while(randomUniform == 0 or randomUniform == 1):
		randomUniform = rn.uniform(0, 1)
	return (np.log(randomUniform))/(-num) # x = (-1/lmbda)*ln(y) or (-Ts)*ln(y)

class Process:
	def __init__(self, params):
		self.id = params.get('id')
		self.arrivalTime = params.get('arrivalTime')
		self.serviceTime = params.get('serviceTime')
		self.remainingTime = self.serviceTime - self.arrivalTime
		self.completionTime = 0

def createProcess(params):
	processParams = {
		"id" : params.get("id"),
		"arrivalTime" : params.get("clock") + poissonStep(params.get("lmbda")),
		"serviceTime" : poissonStep(params.get("mu"))
	}
	return Process(processParams)

class Event:
	def __init__(self, params):
		self.type = params.get('type')
		self.time = params.get('time')
		self.process = params.get('process')

def testFirstComeFirstServe(process1, process2):
	return process1.arrivalTime < process2.arrivalTime

def testShortestTimeRemainingFirst(process1, process2):
	return process1.remainingTime < process2.remainingTime

def testHighestResponseRatioNext(process1, process2, currentTime): #(W+S)/S
	waiting_1 = currentTime - process1.arrivalTime
	waiting_2 = currentTime - process2.arrivalTime
	return ((waiting_1/process1.serviceTime) + 1) > ((waiting_2/process2.arrivalTime) + 1)

def getEvent(event_PriorityQueue):


