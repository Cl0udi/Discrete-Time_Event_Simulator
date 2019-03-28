import numpy as np
import random as rn
import csv
import time
from subprocess import call
from multiprocessing import Queue
from Queue import Empty
from Queue import PriorityQueue
from collections import deque
import heapq

# Test input values functions ###

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

# End of test input values functions ###

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
		"arrivalTime" : float(params.get("clock") + poissonStep(params.get("lmbda"))),
		"serviceTime" : float(poissonStep(params.get("mu")))
	}
	# print("arrivalTime  " + str(processParams.get("arrivalTime")))
	# print("serviceTime  " + str(processParams.get("serviceTime")))
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
		"time" : time,
		"process" : process
	}
	return Event(eventParams)

def createRoundRobinEvent(process, time):
	eventParams = {
		"type" : "RR",
		"time" : time,
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
	# print("\n\nArrival: " + str(process.arrivalTime))
	# print("Clock: " + str(clock))
	# print("Turnaround: " + str(recordedDataParams.get("turnaround")))
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

	print("totalCPU_UtilizationTime: " + str(totalCPU_UtilizationTime))
	print("sumOfAllTurnaroundTimes: " + str(sumOfAllTurnaroundTimes))
	print("sumOfAllQueueSizes: " + str(sumOfAllQueueSizes))
	print("CPU_IddleTime: " + str(processParams.get("CPU_IddleTime")))

	clock = processParams.get("clock")
	# CPU_Utilization = float(100*totalCPU_UtilizationTime/clock)
	CPU_Utilization = 100*(clock - processParams.get("CPU_IddleTime"))/clock
	avgTurnaroundTime = float(sumOfAllTurnaroundTimes/numSamples)
	avgQueueSize = float(sumOfAllQueueSizes/numSamples)
	systemThroughput = float(numSamples/clock)

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

def removeDepartures_PriorityQueue(priority_Queue):
	queueObjectsList = []

	while(priority_Queue.empty() != True):
		queueObjectsList.append(priority_Queue.get()[1])

	for queueObject in queueObjectsList:
		if queueObject.type == "ARR":
			priority_Queue.put((queueObject.time, queueObject))

	return priority_Queue

def getShortestRemainingTime(processList):
	organizedBySRTFQueue = PriorityQueue()

	for process in processList:
		organizedBySRTFQueue.put((process.remainingTime, process))

	highestPriorityProcess = organizedBySRTFQueue.get()[1]

	processList.remove(highestPriorityProcess)

	return highestPriorityProcess

def getHighestResponseRatio(processList, clock):
	# organizedByHRRNQueue = PriorityQueue()

	# for process in processList:
	# 	waiting = clock - process.arrivalTime
	# 	responseRatio = -1*((waiting/process.serviceTime) + 1)
	# 	organizedByHRRNQueue.put((responseRatio, process))

	# highestPriorityProcess = organizedByHRRNQueue.get()[1]

	HighestResponseRatio = 0
	highestPriorityProcess = None

	for process in processList:
		waiting = clock - process.arrivalTime
		responseRatio = ((waiting/process.serviceTime) + 1)
		if(responseRatio > HighestResponseRatio):
			HighestResponseRatio = responseRatio
			highestPriorityProcess = process

	return highestPriorityProcess

def FCFS_Samples(processParams, numSamples):
	# Create appropriate data structures for FCFS
	FCFS_Queue = deque()
	event_PriorityQueue = PriorityQueue()

	# Create process counter to test end condition
	processCounter = 0

	# Queue Size to keep track of size of FCFS Queue
	queueSize = 0

	# To keep track of CPU being utilized
	CPU_iddle = 1
	lastCPU_UtilizationTime = 0
	totalCPU_IdleTime = 0

	# To store simulated information
	recordedDataList = []

	# If process takes more than 5 minutes, it will terminate
	timeout = time.time() + 60*5

	# Create first process and place it as an arrival at time 0 in event_PriorityQueue
	arrivalEvent = createArrivalEvent(processParams)
	processParams["id"] += 1
	event_PriorityQueue.put((arrivalEvent.time, arrivalEvent))

	while(processCounter < numSamples and time.time() < timeout):

		currentEvent = event_PriorityQueue.get()[1]
		clock = currentEvent.time
		currentProcess = currentEvent.process
		# print("clock:" + str(clock))
		# print("processCounter: " + str(processCounter))
		# print("Queue Size: " + str(queueSize))

		if(currentEvent.type == "ARR"):

			if(CPU_iddle == 1):
				CPU_iddle = 0
				totalCPU_IdleTime += clock - lastCPU_UtilizationTime
				departureEvent = createDepartureEvent(currentProcess, clock + currentProcess.serviceTime)
				event_PriorityQueue.put((departureEvent.time, departureEvent))
			else:
				queueSize += 1
				FCFS_Queue.appendleft(currentProcess)

			# Create a new process to arrive
			processParams.update({'clock': clock})
			arrivalEvent = createArrivalEvent(processParams)
			processParams["id"] += 1
			event_PriorityQueue.put((arrivalEvent.time, arrivalEvent))

		elif(currentEvent.type == "DEP"):

			if(len(FCFS_Queue) == 0):
				CPU_iddle = 1
				lastCPU_UtilizationTime = clock
			else:
				queueSize -= 1
				queuedProcess = FCFS_Queue.pop()
				departureEvent = createDepartureEvent(queuedProcess, clock + queuedProcess.serviceTime)
				event_PriorityQueue.put((departureEvent.time, departureEvent))

			# Record the data and add one to the process counter end condition
			recordedDataList.append(newRecordedData(currentProcess, clock, queueSize))
			processCounter += 1


	# Update clock to final value
	if(event_PriorityQueue.empty() == False):
		finalEvent = event_PriorityQueue.get()[1]
		clock = finalEvent.time + finalEvent.process.serviceTime
		processParams.update({'clock': clock})

	processParams.update({'CPU_IddleTime': totalCPU_IdleTime})

	return recordedDataList

def SRTF_Samples(processParams, numSamples):
	# Create appropriate data structures for SRTF
	processList = []
	event_PriorityQueue = PriorityQueue()

	# Create process counter to test end condition
	processCounter = 0

	# To keep track of CPU being utilized
	CPU_iddle = 1
	lastCPU_UtilizationTime = 0
	totalCPU_IdleTime = 0

	# To keep track of previous event times since SRTF is preemptive
	runningProcessStartTime = 0
	nextDepartureTime = 0
	runningProcess = []

	# To store simulated information
	recordedDataList = []

	# If process takes more than 5 minutes, it will terminate
	timeout = time.time() + 60*5

	# Create first process and place it as an arrival at time 0 in event_PriorityQueue
	arrivalEvent = createArrivalEvent(processParams)
	processParams["id"] += 1
	event_PriorityQueue.put((arrivalEvent.time, arrivalEvent))

	while(processCounter < numSamples and time.time() < timeout):

		currentEvent = event_PriorityQueue.get()[1]
		clock = currentEvent.time
		currentProcess = currentEvent.process

		if(currentEvent.type == "ARR"):

			# Add the current process to the list of considered processes that will be tested
			processList.append(currentProcess)

			# If CPU is iddle, run the process and create a departure event based on its service time
			if(CPU_iddle == 1):
				CPU_iddle = 0
				totalCPU_IdleTime += clock - lastCPU_UtilizationTime
				departureEvent = createDepartureEvent(currentProcess, clock + currentProcess.serviceTime)
				event_PriorityQueue.put((departureEvent.time, departureEvent))
				nextDepartureTime = clock + currentProcess.serviceTime
				runningProcess = currentProcess
				runningProcessStartTime = clock
			else:
				# If CPU is not iddle we need to check if this process should be running instead of the current one
				# otherwise place it in the process list
				if(nextDepartureTime > currentProcess.remainingTime + clock):
					for processObject in processList:
						if(processObject == runningProcess):
							processObject.serviceTime -= clock - runningProcessStartTime
					nextDepartureTime = clock + currentProcess.serviceTime
					runningProcess = currentProcess
					runningProcessStartTime = clock
					event_PriorityQueue = removeDepartures_PriorityQueue(event_PriorityQueue)
					departureEvent = createDepartureEvent(currentProcess, clock + currentProcess.serviceTime)
					event_PriorityQueue.put((departureEvent.time, departureEvent))
				else:
					pass

			# Create a new process to arrive
			processParams.update({'clock': clock})
			arrivalEvent = createArrivalEvent(processParams)
			processParams["id"] += 1
			event_PriorityQueue.put((arrivalEvent.time, arrivalEvent))

		elif(currentEvent.type == "DEP"):

			#processList.remove(currentProcess)

			for processObject in processList:
						if(processObject == runningProcess):
							processList.remove(processObject)

			if not processList:
				CPU_iddle = 1
				lastCPU_UtilizationTime = clock
				# Create a ridiculous departure time so that it gets overiden when a new process arrives
				nextDepartureTime = 1000000 + clock
				runningProcess = None
				runningProcessStartTime = 1000000 + clock
			else:
				queuedProcess = getShortestRemainingTime(processList)
				departureEvent = createDepartureEvent(queuedProcess, clock + queuedProcess.serviceTime)
				event_PriorityQueue.put((departureEvent.time, departureEvent))
				nextDepartureTime = departureEvent.time
				runningProcess = departureEvent
				runningProcessStartTime = clock

			# Record the data and add one to the process counter end condition
			recordedDataList.append(newRecordedData(currentProcess, clock, len(processList)))
			processCounter += 1


	# Update clock to final value
	if(event_PriorityQueue.empty() == False):
		finalEvent = event_PriorityQueue.get()[1]
		clock = finalEvent.time + finalEvent.process.serviceTime
		processParams.update({'clock': clock})

	processParams.update({'CPU_IddleTime': totalCPU_IdleTime})

	return recordedDataList

def HRRN_Samples(processParams, numSamples):
	# Create appropriate data structures for HRRN
	processList = []
	event_PriorityQueue = PriorityQueue()

	# Create process counter to test end condition
	processCounter = 0

	# To keep track of CPU being utilized
	CPU_iddle = 1
	lastCPU_UtilizationTime = 0
	totalCPU_IdleTime = 0

	# To keep track of running process
	runningProcess = None

	# To store simulated information
	recordedDataList = []

	# If process takes more than 20 minutes, it will terminate
	timeout = time.time() + 60*20

	# Create first process and place it as an arrival at time 0 in event_PriorityQueue
	arrivalEvent = createArrivalEvent(processParams)
	processParams["id"] += 1
	event_PriorityQueue.put((arrivalEvent.time, arrivalEvent))

	while(processCounter < numSamples and time.time() < timeout):

		currentEvent = event_PriorityQueue.get()[1]
		clock = currentEvent.time
		currentProcess = currentEvent.process

		if(currentEvent.type == "ARR"):
			# Add the current process to the list of considered processes that will be tested
			processList.append(currentProcess)

			# If CPU is iddle, run the process and create a departure event based on its service time
			if(CPU_iddle == 1):
				CPU_iddle = 0
				totalCPU_IdleTime += clock - lastCPU_UtilizationTime
				runningProcess = currentProcess
				departureEvent = createDepartureEvent(currentProcess, clock + currentProcess.serviceTime)
				event_PriorityQueue.put((departureEvent.time, departureEvent))
			else:
				pass

			# Create a new process to arrive
			processParams.update({'clock': clock})
			arrivalEvent = createArrivalEvent(processParams)
			processParams["id"] += 1
			event_PriorityQueue.put((arrivalEvent.time, arrivalEvent))

		elif(currentEvent.type == "DEP"):

			# Delete process from list since it is departing
			# for processObject in processList:
			# 			if(processObject == runningProcess):
			# 				processList.remove(processObject)

			if runningProcess in processList:
				processList.remove(runningProcess)

			if not processList:
				# If process list is empty, the CPU becomes iddle while waiting for next process
				CPU_iddle = 1
				lastCPU_UtilizationTime = clock
				runningProcess = None
			else:
				queuedProcess = getHighestResponseRatio(processList, clock)
				departureEvent = createDepartureEvent(queuedProcess, clock + queuedProcess.serviceTime)
				event_PriorityQueue.put((departureEvent.time, departureEvent))
				runningProcess = queuedProcess

			# Record the data and add one to the process counter end condition
			recordedDataList.append(newRecordedData(currentProcess, clock, len(processList)))
			processCounter += 1
			print("Processes left: " + str(numSamples - processCounter))


	# Update clock to final value
	if(event_PriorityQueue.empty() == False):
		finalEvent = event_PriorityQueue.get()[1]
		clock = finalEvent.time + finalEvent.process.serviceTime
		processParams.update({'clock': clock})

	processParams.update({'CPU_IddleTime': totalCPU_IdleTime})

	return recordedDataList

def RoundRobin_Samples(processParams, numSamples):
	# Create appropriate data structures for RoundRobin
	RoundRobin_Queue = deque()
	event_PriorityQueue = PriorityQueue()
	QUANTUM = processParams.get("roundRobinQuantum")
	nextQuantum = QUANTUM

	# Create process counter to test end condition
	processCounter = 0

	# Queue Size to keep track of size of FCFS Queue
	queueSize = 0

	# To keep track of CPU being utilized
	CPU_iddle = 1
	lastCPU_UtilizationTime = 0
	totalCPU_IdleTime = 0

	# To store simulated information
	recordedDataList = []

	# If process takes more than 10 minutes, it will terminate
	timeout = time.time() + 60*10

	# Create first process and place it as an arrival at a poisson generated time in event_PriorityQueue
	arrivalEvent = createArrivalEvent(processParams)
	arrivalEvent.arrivalTime = 0
	arrivalEvent.process.arrivalTime = 0
	processParams["id"] += 1
	event_PriorityQueue.put((arrivalEvent.time, arrivalEvent))

	while(processCounter < numSamples and time.time() < timeout):

		currentEvent = event_PriorityQueue.get()[1]
		clock = currentEvent.time
		currentProcess = currentEvent.process

		while(clock >= nextQuantum):
			nextQuantum += QUANTUM

		# print("NEXT QUANTUM: " + str(nextQuantum))
		# print("Process Counter: " + str(processCounter))
		# print("Queue Size: " + str(queueSize))
		# print("Clock: " + str(clock))
		# print("Current Process Arrival: " + str(currentProcess.arrivalTime))

		if(currentEvent.type == "ARR"):
			# print("ARR")

			if(CPU_iddle == 1):
				CPU_iddle = 0
				totalCPU_IdleTime += clock - lastCPU_UtilizationTime

				if(clock + currentProcess.remainingTime < nextQuantum):
					# If arriving process would finish in less than 1 Quantum, schedule a departure
					departureTime = clock + currentProcess.remainingTime
					departureEvent = createDepartureEvent(currentProcess, departureTime)
					event_PriorityQueue.put((departureEvent.time, departureEvent))
				else:
					# Otherwise schedule it for a Round Robin round
					roundRobinEvent = createRoundRobinEvent(currentProcess, nextQuantum)
					event_PriorityQueue.put((roundRobinEvent.time, roundRobinEvent))
			else:
				# IF CPU is busy, place it at the end of Round Robin Queue
				queueSize += 1
				RoundRobin_Queue.appendleft(currentProcess)

			# Create a new process to arrive
			processParams.update({'clock': clock})
			arrivalEvent = createArrivalEvent(processParams)
			processParams["id"] += 1
			event_PriorityQueue.put((arrivalEvent.time, arrivalEvent))

		elif(currentEvent.type == "DEP"):
			# print("DEP")
			if(len(RoundRobin_Queue) == 0):
				CPU_iddle = 1
				lastCPU_UtilizationTime = clock
			else:
				queuedProcess = RoundRobin_Queue.pop()
				if(clock + queuedProcess.remainingTime < nextQuantum):
					queueSize -= 1
					departureTime = clock + queuedProcess.remainingTime
					departureEvent = createDepartureEvent(queuedProcess, departureTime)
					event_PriorityQueue.put((departureEvent.time, departureEvent))
				else:
					roundRobinEvent = createRoundRobinEvent(queuedProcess, clock)
					event_PriorityQueue.put((roundRobinEvent.time, roundRobinEvent))

			# Record the data and add one to the process counter end condition
			recordedDataList.append(newRecordedData(currentProcess, clock, queueSize))
			processCounter += 1

		# Added a new type of event known as the round robin
		# If a process still has a few more cycles before being done it will feed itself into the queue
		# Processes are not terminated here so data is not recorded
		elif(currentEvent.type == "RR"):
			# print("Robin")
			# Remove the service time the CPU performed from the remaining time 
			currentProcess.remainingTime -= (nextQuantum - clock)

			if(len(RoundRobin_Queue) == 0):
				processOfInterest = currentProcess
			else:
				RoundRobin_Queue.appendleft(currentProcess)
				processOfInterest = RoundRobin_Queue.pop()

			if(clock + processOfInterest.remainingTime < nextQuantum):
				departureTime = clock + processOfInterest.remainingTime
				departureEvent = createDepartureEvent(processOfInterest, departureTime)
				event_PriorityQueue.put((departureEvent.time, departureEvent))
			else:
				roundRobinEvent = createRoundRobinEvent(processOfInterest, nextQuantum)
				event_PriorityQueue.put((roundRobinEvent.time, roundRobinEvent))



	# Update clock to final value
	if(event_PriorityQueue.empty() == False):
		finalEvent = event_PriorityQueue.get()[1]
		clock = finalEvent.time + finalEvent.process.serviceTime
		processParams.update({'clock': clock})

	processParams.update({'CPU_IddleTime': totalCPU_IdleTime})

	return recordedDataList


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