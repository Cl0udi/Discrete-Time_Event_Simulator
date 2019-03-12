import modules as md
import sys

def sim(scheduleAlgorithm = 1, lmbda = 10, avgServiceTime = .6, roundRobinQuantum = .01):

	scheduleAlgorithm = md.cleanInitialInputScheduleAlgorithm(int(scheduleAlgorithm))
	lmbda = md.cleanInitialInputFloatValues(lmbda, "Lambda")
	avgServiceTime = md.cleanInitialInputFloatValues(avgServiceTime, "Average Service Time")
	roundRobinQuantum = md.cleanInitialInputFloatValues(roundRobinQuantum, "Round Robin Quantum")

	print(scheduleAlgorithm)
	print("goodbye")


if __name__ == '__main__':
    # Map command line arguments to function arguments.
    sim(*sys.argv[1:])