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

def getShortestRemainingTime(processList):
	organizedBySRTFQueue = PriorityQueue()

	for process in processList:
		organizedBySRTFQueue.put((process.remainingTime, process))

	highestPriorityProcess = organizedBySRTFQueue.get()[1]

	processList.remove(highestPriorityProcess)

	return highestPriorityProcess