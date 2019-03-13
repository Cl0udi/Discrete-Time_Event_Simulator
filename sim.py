import modules as md
import sys
from multiprocessing import Queue
from Queue import Empty
from Queue import PriorityQueue

def sim(scheduleAlgorithm = 1, lmbda = 10.0, avgServiceTime = .6, roundRobinQuantum = .01):
	print("hello")
	scheduleAlgorithm = md.cleanInitialInputScheduleAlgorithm(scheduleAlgorithm)
	lmbda = md.cleanInitialInputFloatValues(lmbda, "Lambda")
	avgServiceTime = md.cleanInitialInputFloatValues(avgServiceTime, "Average Service Time")
	roundRobinQuantum = md.cleanInitialInputFloatValues(roundRobinQuantum, "Round Robin Quantum")

	processCounter = 0
	idCounter = 0
	clock = 0.0
	CPU_iddle = 1
	event_PriorityQueue = PriorityQueue()
	FCFS_Queue = Queue()

	processParams = {"id" : idCounter, "clock" : clock, "lmbda" : lmbda, "mu" : 1/avgServiceTime}
	idCounter += 1
	newProcess = createProcess(processParams)
	arrivalEventParams = {"type" : "ARR", "time" : newProcess.arrivalTime, "process" : newProcess}
	arrivalEvent = Event(arrivalEventParams)
	departureEventParams = {"type" : "DEP", "time" : newProcess.arrivalTime + newProcess.serviceTime, "process" : newProcess}
	departureEvent = Event(departureEventParams)

	event_PriorityQueue.put((arrivalEvent.time, arrivalEvent))
	event_PriorityQueue.put((departureEvent.time, departureEvent))


	while(processCounter < 10000):
	#STRF_PriorityQueue = PriorityQueue()
	#RoundRobin_Queue = Queue()
	print("goodbye")


if __name__ == '__main__':
    # Map command line arguments to function arguments.
    sim(*sys.argv[1:])