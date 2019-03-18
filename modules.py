import numpy as np
import random as rn
import csv
from multiprocessing import Queue
from subprocess import call

# Test value functions ###

def isValueBetweenOneAndFour(num):
	return True if (1 <= num <= 4) else False

def isValueBetweenZeroAndThousand(num):
	return True if (0.0 < num < 1000.0) else False

def isValueBetweenOneAndThousand(num):
	return True if (1.0 <= num < 1000.0) else False


def cleanInitialInputScheduleAlgorithm(scheduleAlgorithm):
	try:
		assert (isValueBetweenOneAndFour(int(scheduleAlgorithm))), "scheduleAlgorithm value should be an integer between 1 and 4"
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

def cleanInitialInputLmdaValues(num):
	try:
		assert (isValueBetweenOneAndThousand(float(num))), "Lambda value should be a float bigger than 1 and smaller than 1000"
	except:
		print("\nINPUT RANGE ERROR: \n Lambda selection should be a float bigger than 1 and smaller than 1000\n")
		while True:
			num = raw_input('Number bigger than 1 and smaller than 1000: ')
			try:
				num = float(num)
			except:
				print("\nPlease input a number")
				continue
			if (isValueBetweenOneAndThousand(num)):
				print("\nInput accepted :)\n")
				break
			else:
				print("\nNumber must be bigger than 1 and smaller than 1000")

	return float(num)

def cleanInitialInputFloatValues(num, name):
	try:
		assert (isValueBetweenZeroAndThousand(float(num))), name + " value should be a float bigger than 0 and smaller than 1000"
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
	poissonValue = (np.log(randomUniform))/(-num) # x = (-1/lmbda)*ln(y) or (-Ts)*ln(y)
	# print("Poisson Value: " + str(poissonValue))
	return poissonValue

def poissonStep2(num):
	return np.random.poisson(num)

class Process:
	def __init__(self, params):
		self.id = params.get('id')
		self.arrivalTime = params.get('arrivalTime')
		self.serviceTime = params.get('serviceTime')
		self.remainingTime = params.get('serviceTime')
		self.completionTime = 0

def createProcess(params):
	processParams = {
		"id" : params.get("id"),
		"arrivalTime" : params.get("clock") + poissonStep2(params.get("lmbda")),
		"serviceTime" : poissonStep2(params.get("mu"))
	}
	return Process(processParams)

class Event:
	def __init__(self, params):
		self.type = params.get('type')
		self.time = params.get('time')
		self.process = params.get('process')

def createArrivalEvent(processParams):
	newProcess = createProcess(processParams)
	eventParams = {
		"type" : "ARR",
		"time" : newProcess.arrivalTime,
		"process" : newProcess
	}
	return Event(eventParams)

def createDepartureEvent(process, time):
	eventParams = {
		"type" : "DEP",
		"time" : time + process.serviceTime,
		"process" : process
	}
	return Event(eventParams)

class RecordedData:
	def __init__(self, params):
		self.CPU_time = params.get('CPU_time')
		self.turnaround = params.get('turnaround')
		self.queueSize = params.get('queueSize')
		#self.throughput = params.get('throughput')

def newRecordedData(process, clock, queueSize):
	recordedDataParams = {
		"CPU_time" : process.serviceTime, 
		"turnaround" : clock - process.arrivalTime, 
		"queueSize" : queueSize
	}
	return RecordedData(recordedDataParams)

def interpretData(recordedDataList, processParams, numSamples):

	totalCPU_UtilizationTime = 0
	sumOfAllTurnaroundTimes = 0
	sumOfAllQueueSizes = 0
	totalThroughput = 0

	for data in recordedDataList:
		# print("CPU: " + str(data.CPU_time))
		# print("Turn: " + str(data.turnaround))
		# print("Queue: " + str(data.queueSize))
		totalCPU_UtilizationTime += data.CPU_time
		sumOfAllTurnaroundTimes += data.turnaround
		sumOfAllQueueSizes += data.queueSize

	clock = processParams.get("clock")
	CPU_Utilization = totalCPU_UtilizationTime/clock
	avgTurnaroundTime = sumOfAllTurnaroundTimes/numSamples
	avgQueueSize = sumOfAllQueueSizes/numSamples
	systemThroughput = numSamples/clock

	avgServiceTime = processParams.get("avgServiceTime")
	roundRobinQuantum = processParams.get("roundRobinQuantum")
	lmbda = processParams.get("lmbda")

	csvParams = {
		"CPU_Utilization": CPU_Utilization, 
		"avgTurnaroundTime": avgTurnaroundTime, 
		"avgQueueSize": avgQueueSize, 
		"systemThroughput" :systemThroughput,
		"avgServiceTime": avgServiceTime,
		"quantum": roundRobinQuantum,
		"line": int(lmbda)
	}

	return csvParams

def recordToCSV(params, dataType):
	# Following section records data to appropriate row in corresponding excel file
	excelList = []
	fileName = ''
	if(dataType == 1):
		fileName = 'FirstComeFirstServe.csv'
	elif(dataType == 2):
		fileName = 'ShortestTimeRemainingFirst.csv'
	elif(dataType == 3):
		fileName = 'HighestResponseRatioNext.csv'
	elif(dataType == 4):
		if(params.get("quantum") == .01):
			fileName = 'RoundRobin.csv'
		else:
			fileName = 'RoundRobin2.csv'
	else:
		fileName = 'ErrorFile.csv'

	# Read all data from the csv file.

	with open(fileName, 'rb') as b:
		excelFile = csv.reader(b)
		excelList.extend(excelFile)

	line = params.get("line")
	lmbda = line
	avgServiceTime = params.get("avgServiceTime")
	quantum = params.get("quantum")
	CPU_Utilization = params.get("CPU_Utilization")
	avgTurnaroundTime = params.get("avgTurnaroundTime")
	avgQueueSize = params.get("avgQueueSize")
	systemThroughput = params.get("systemThroughput")


	# data to override in the format {line_num_to_override:data_to_write}.
	# Lambda, Avg Service Time, Quantum, CPU Utilization, Avg Turnaround, Avg Queuesize, System Throughput,
	line_to_override = {line:[lmbda, avgServiceTime, quantum, CPU_Utilization, avgTurnaroundTime, avgQueueSize, systemThroughput]}

	# Write data to the csv file and replace the lines in the line_to_override dict.
	with open(fileName, 'wb') as b:
		writer = csv.writer(b)
		for line, row in enumerate(excelList):
			data = line_to_override.get(line, row)
			writer.writerow(data)


# def testFirstComeFirstServe(process1, process2):
# 	return process1.arrivalTime < process2.arrivalTime

# def testShortestTimeRemainingFirst(process1, process2):
# 	return process1.remainingTime < process2.remainingTime

# def testHighestResponseRatioNext(process1, process2, currentTime): #(W+S)/S
# 	waiting_1 = currentTime - process1.arrivalTime
# 	waiting_2 = currentTime - process2.arrivalTime
# 	return ((waiting_1/process1.serviceTime) + 1) > ((waiting_2/process2.arrivalTime) + 1)

def getEvent(event_PriorityQueue):
	print("ok")