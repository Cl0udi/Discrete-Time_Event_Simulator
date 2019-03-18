import modules as md
import sys
import time
from multiprocessing import Queue
from Queue import Empty
from Queue import PriorityQueue
# from signal import signal, SIGPIPE, SIG_DFL
# signal(SIGPIPE,SIG_DFL) 

def sim(scheduleAlgorithm = 1, lmbda = 10.0, avgServiceTime = 0.6, roundRobinQuantum = 0.01):
	print("\nhello\n")
	time.sleep(.1)

	scheduleAlgorithm = md.cleanInitialInputScheduleAlgorithm(scheduleAlgorithm)
	lmbda = md.cleanInitialInputLmdaValues(lmbda)
	avgServiceTime = md.cleanInitialInputFloatValues(avgServiceTime, "Average Service Time")
	roundRobinQuantum = md.cleanInitialInputFloatValues(roundRobinQuantum, "Round Robin Quantum")

	timeout = time.time() + 60*5 # If process takes more than 5 minutes, it will terminate
	numSamples = 10000
	recordedDataList = []
	processCounter = 0
	idCounter = 0
	clock = 0.0
	queueSize = 0
	CPU_iddle = 1
	processParams = {
		"id" : idCounter, 
		"clock" : clock, 
		"lmbda" : lmbda,
		"avgServiceTime": avgServiceTime,
		"roundRobinQuantum": roundRobinQuantum,
		"mu" : 1/avgServiceTime
	}
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
		arrivalEvent = md.createArrivalEvent(processParams)
		processParams["id"] += 1
		event_PriorityQueue.put((arrivalEvent.time, arrivalEvent))

		while(processCounter < numSamples and time.time() < timeout):

			currentEvent = event_PriorityQueue.get()[1]
			clock = currentEvent.time
			currentProcess = currentEvent.process
			# print("Sample: " + str(processCounter) + "	Queue: " + str(queueSize) + "	Clock: " + str(clock))
			# print("IDDLE?: " + str(CPU_iddle) + "	Type: " + str(currentEvent.type))

			if(currentEvent.type == "ARR"):
				queueSize += 1

				if(CPU_iddle == 1):
					queueSize -= 1
					# print("AAAAAAAAA")
					CPU_iddle = 0
					departureEvent = md.createDepartureEvent(currentProcess, clock)
					event_PriorityQueue.put((departureEvent.time, departureEvent))
				else:
					# print("BBBBBBBBB")
					FCFS_Queue.put(currentProcess)

				# Create a new process to arrive
				processParams.update({'clock': clock})
				arrivalEvent = md.createArrivalEvent(processParams)
				processParams["id"] += 1
				event_PriorityQueue.put((arrivalEvent.time, arrivalEvent))

			elif(currentEvent.type == "DEP"):

				if(FCFS_Queue.empty() == True):
					# print("CCCCCCCCCC")
					CPU_iddle = 1
				else:
					# print("DDDDDDDDDD")
					queueSize -= 1
					queuedProcess = FCFS_Queue.get()
					departureEvent = md.createDepartureEvent(queuedProcess, clock)
					event_PriorityQueue.put((departureEvent.time, departureEvent))

				# Record the data and add one to the process counter end condition
				recordedDataList.append(md.newRecordedData(currentProcess, clock, queueSize))
				processCounter += 1


		# Update clock to final value
		finalEvent = event_PriorityQueue.get()[1]
		clock = finalEvent.time + finalEvent.process.serviceTime
		processParams.update({'clock': clock})


	# Time to save the data in a readable format
	csvParams = md.interpretData(recordedDataList, processParams, numSamples)
	md.recordToCSV(csvParams, scheduleAlgorithm)

	print("CPU Utilization: " + str(csvParams.get("CPU_Utilization")))
	print("Average turnaround time: " + str(csvParams.get("avgTurnaroundTime")))
	print("Average Queue Size: " + str(csvParams.get("avgQueueSize")))
	print("System Throughput: " + str(csvParams.get("systemThroughput")))


	time.sleep(.5)
	print("\ngoodbye\n")

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    sim(*sys.argv[1:])