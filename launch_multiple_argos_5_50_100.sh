#!/bin/bash

for alpha in 1.0 1.2 1.4 1.6 1.8 2.0; do
	for rho in 0.00 0.15 0.30 0.45 0.60 0.75 0.90 0.95 0.99; do
		for n in 5 50 100; do
			for speed in 1.00; do
				argos3 -c simulation_config/generated_configs/kilobot_sim_${speed}_${n}_${alpha}_${rho}.argos
			done
		done
	done
done
