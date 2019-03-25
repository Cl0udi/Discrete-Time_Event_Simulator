import modules as md
import sys
import time
# from signal import signal, SIGPIPE, SIG_DFL
# signal(SIGPIPE,SIG_DFL) 

def sim(scheduleAlgorithm = 1, lmbda = 10.0, avgServiceTime = 0.6, roundRobinQuantum = 0.01):
	print("\nhello\n")
	time.sleep(.1)

	scheduleAlgorithm = md.cleanInitialInputScheduleAlgorithm(scheduleAlgorithm)
	lmbda = md.cleanInitialInputLmdaValues(lmbda)
	avgServiceTime = md.cleanInitialInputFloatValues(avgServiceTime, "Average Service Time")
	roundRobinQuantum = md.cleanInitialInputFloatValues(roundRobinQuantum, "Round Robin Quantum")

	numSamples = 10000
	idCounter = 0
	clock = 0.0
	processParams = {
		"id" : idCounter, 
		"clock" : clock, 
		"lmbda" : lmbda,
		"avgServiceTime": avgServiceTime,
		"roundRobinQuantum": roundRobinQuantum,
		"mu" : 1/avgServiceTime
	}

	# departureEventParams = {"type" : "DEP", "time" : newProcess.arrivalTime + newProcess.serviceTime, "process" : newProcess}
	# departureEvent = md.Event(departureEventParams)
	# event_PriorityQueue.put((departureEvent.time, departureEvent))
	# STRF_PriorityQueue = PriorityQueue()
	# RoundRobin_Queue = Queue()

	if(scheduleAlgorithm == 1):
		recordedDataList = md.FCFS_Samples(processParams, numSamples)

	elif(scheduleAlgorithm == 2):
		recordedDataList = md.SRTF_Samples(processParams, numSamples)

	elif(scheduleAlgorithm == 3):
		recordedDataList = md.SRTF_Samples(processParams, numSamples)

	elif(scheduleAlgorithm == 4):
		recordedDataList = md.RoundRobin_Samples(processParams, numSamples)

	else:
		print("Variable scheduleAlgorithm not in range (1-4). TERMINATING to prevent faulty data")
		sys.exit()


	# Time to save the data in a readable format
	csvParams = md.interpretData(recordedDataList, processParams, numSamples)
	md.recordToCSV(csvParams, scheduleAlgorithm)

	print("Clock: " + str(processParams.get("clock")))
	print("CPU Utilization: " + str(csvParams.get("CPU_Utilization")))
	print("Average turnaround time: " + str(csvParams.get("avgTurnaroundTime")))
	print("Average Queue Size: " + str(csvParams.get("avgQueueSize")))
	print("System Throughput: " + str(csvParams.get("systemThroughput")))


	time.sleep(.1)
	print("\ngoodbye\n")

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    sim(*sys.argv[1:])