#!/bin/bash

for alpha in 2.0; do
	for rho in 0.90; do
		for n in 10 20 30; do
			argos3 -c simulation_config/generated_configs/kilobot_sim_${n}_${alpha}_${rho}.argos
		done
	done
done
