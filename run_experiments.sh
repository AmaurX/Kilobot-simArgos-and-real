#!/bin/bash

for i in `seq 1 10`;
do
        argos3 -c simulation_config/kilobot_with_generic_controller.argos
done