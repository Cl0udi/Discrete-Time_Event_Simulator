#!/bin/bash
simulations=1
while [ $simulations -le 30 ]
do
python sim.py 4 $simulations
((simulations++))
done
simulations2=1
while [ $simulations2 -le 30 ]
do
python sim.py 4 $simulations2 .06 .2
((simulations2++))
done
echo All done
