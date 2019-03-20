#!/bin/bash
simulations=1
while [ $simulations -le 30 ]
do
python sim.py 3 $simulations
((simulations++))
done
echo All done
