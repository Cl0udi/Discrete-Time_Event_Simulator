# Discrete-Time_Event_Simulator

Please make sure to include CSV FILES in the folder you run any of these programs. You can change the name of those files in modules.py->recordToCSV

3	HOW TO RUN
3.1	Python Files

The project is written in python. It includes to main files:

1.	‘sim.py’ used for running individual simulation tests. It takes 4 inputs in the following order:
1)	Schedule algorithm: a number from 1 to 4 specifying which scheduling algorithm to use. (1: FCFS, 2: SRTF, 3: HRRN and 4: RR)
2)	Lambda: accepting a value from 1 to 1000
3)	Avg Service Time: accepting a value from 0 to 1000
4)	Round Robin Quantum: accepting a value from 0 to 1000

2.	‘modules.py’ used for defining all of the functions and objects used in the simulator.

The example commands for running one test individually is as follows:

python sim.py or python sim.py 2 15 .06 .2

3.2	Batch Files
	The project also includes batch files in order to run. There is one batch file for each of the scheduling algorithms. The have the following file names:

1.	‘runSimFCFS.sh’: runs FCFS with lambda values from 1 to 30
2.	‘runSimSRTF.sh’: runs SRTF with lambda values from 1 to 30
3.	‘runSimHRRN.sh’: runs HRRN with lambda values from 1 to 30
4.	‘runSimRoundRobin.sh’: runs Round Robin with lambda values from 1 to 30 and Quantum values of 0.01 and 0.2

The example commands for running any of the batch files is as follows:

sh runSimFCFS.sh or sh runSimRoundRobin.sh

3.3	Other necessary files
	Please make sure to include all the existing csv files as they need to be overwritten. My program does not create new csv files and will simply say csv file not found if you attempt to run and save results without the file in the current folder.
