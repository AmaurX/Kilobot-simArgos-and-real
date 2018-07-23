#!/bin/bash

for alpha in 2.0; do
	for rho in 0.90; do
		for n in 20; do
			for speed in 1.00; do
				argos3 -c simulation_config/generated_configs/kilobot_sim_${speed}_${n}_${alpha}_${rho}.argos
			done
		done
	done
done
