import modules as md
import sys
import time
from multiprocessing import Queue
from Queue import Empty
from Queue import PriorityQueue

def sim(scheduleAlgorithm = 1, lmbda = 10.0, avgServiceTime = .6, roundRobinQuantum = .01):
	print("hello")
	scheduleAlgorithm = md.cleanInitialInputScheduleAlgorithm(scheduleAlgorithm)
	lmbda = md.cleanInitialInputFloatValues(lmbda, "Lambda")
	avgServiceTime = md.cleanInitialInputFloatValues(avgServiceTime, "Average Service Time")
	roundRobinQuantum = md.cleanInitialInputFloatValues(roundRobinQuantum, "Round Robin Quantum")

	timeout = time.time() + 60*5 # If process takes more than 5 minutes, it will terminate
	numSamples = 10
	recordedDataList = []
	processCounter = 0
	idCounter = 0
	clock = 0.0
	queueSize = 0
	CPU_iddle = 1
	processParams = {"id" : idCounter, "clock" : clock, "lmbda" : lmbda, "mu" : 1/avgServiceTime}
	idCounter += 1

	# departureEventParams = {"type" : "DEP", "time" : newProcess.arrivalTime + newProcess.serviceTime, "process" : newProcess}
	# departureEvent = md.Event(departureEventParams)
	# event_PriorityQueue.put((departureEvent.time, departureEvent))
	# STRF_PriorityQueue = PriorityQueue()
	# RoundRobin_Queue = Queue()

	if(scheduleAlgorithm == 1):
		# Create appropriate data structures for FCFS
		FCFS_Queue = Queue()
		event_PriorityQueue = PriorityQueue()

		# Create first process and place it as an arrival at time 0 in event_PriorityQueue
		newProcess = md.createProcess(processParams)
		arrivalEventParams = {"type" : "ARR", "time" : newProcess.arrivalTime, "process" : newProcess}
		arrivalEvent = md.Event(arrivalEventParams)
		event_PriorityQueue.put((arrivalEvent.time, arrivalEvent))

		while(processCounter < numSamples and time.time() < timeout):

			currentEvent = event_PriorityQueue.get()[1]
			clock = currentEvent.time
			print("Clock: " + str(clock))
			print("Sample: " + str(processCounter))

			if(currentEvent.type == "ARR"):
				if(CPU_iddle == 1):
					CPU_iddle = 0
					departureEventParams = {"type" : "DEP", "time" : clock + currentEvent.process.serviceTime, "process" : currentEvent.process}
					departureEvent = md.Event(departureEventParams)
					event_PriorityQueue.put((departureEvent.time, departureEvent))
				else:
					FCFS_Queue.put(currentEvent.process)
					queueSize += 1
				# Create a new process to arrive
				processParams.update({'id': idCounter})
				processParams.update({'clock': clock})
				newProcess = md.createProcess(processParams)
				arrivalEventParams = {"type" : "ARR", "time" : newProcess.arrivalTime, "process" : newProcess}
				arrivalEvent = md.Event(arrivalEventParams)
				event_PriorityQueue.put((arrivalEvent.time, arrivalEvent))
				idCounter += 1
			elif(currentEvent.type == "DEP"):
				recordedDataList.append(newRecordedData(currentEvent.process, clock, queueSize))
				processCounter += 1
				if(FCFS_Queue.empty()):
					CPU_iddle = 1
				else:
					currentEvent = FCFS_Queue.get()
					departureEventParams = {"type" : "DEP", "time" : clock + currentEvent.serviceTime, "process" : currentEvent}
					departureEvent = md.Event(departureEventParams)
					event_PriorityQueue.put((departureEvent.time, departureEvent))
					queueSize -= 1

	# Update clock to final value
	finalEvent = event_PriorityQueue.get()[1]
	clock = finalEvent.time

	# Time to save the data in a readable format
	totalCPU_UtilizationTime = 0
	sumOfAllTurnaroundTimes = 0
	sumOfAllQueueSizes = 0
	totalThroughput = 0

	for data in recordedDataList:
		print("CPU: " + str(data.CPU_time))
		print("Turn: " + str(data.turnaround))
		print("Queue: " + str(data.queueSize))
		totalCPU_UtilizationTime += data.CPU_time
		sumOfAllTurnaroundTimes += data.turnaround
		sumOfAllQueueSizes += data.queueSize

	print("CPU Utilization: " + str(clock/totalCPU_UtilizationTime))
	print("Average turnaround time: " + str(sumOfAllTurnaroundTimes/numSamples))
	print("Average Queue Size: " + str(sumOfAllQueueSizes/numSamples))
	print("System Throughput: " + str(numSamples/clock))
	print("goodbye")

def newRecordedData(process, clock, queueSize):
	recordedDataParams = {"CPU_time" : process.serviceTime, "turnaround" : clock - process.arrivalTime, "queueSize" : queueSize}
	return md.RecordedData(recordedDataParams)

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    sim(*sys.argv[1:])