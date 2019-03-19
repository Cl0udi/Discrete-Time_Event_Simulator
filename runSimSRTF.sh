#!/bin/bash
simulations=1
while [ $simulations -le 30 ]
do
python sim.py 2 $simulations
((simulations++))
done
echo All done
