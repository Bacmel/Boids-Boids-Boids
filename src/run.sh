#!/usr/bin/bash

python3.8 -m sim \
--border none \
-tr 50 -v 5 \
-d-sd 10 \
-ror 1 \
-roa 31 \
--blindspot-direction -180 --blindspot-opening 90 \
--step-nb 1600 \
-roo-var 1:0.25:2.25 \
--roo-step-duration 20
#--render
# -roo 16 \