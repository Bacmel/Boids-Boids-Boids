#!/usr/bin/bash

python3.8 -m sim \
--border none \
-tr 50 -v 5 \
-ror 1 \
-roo 10 \
-roa 14 \
--blindspot-direction -122.5 122.5 --blindspot-opening 57.5 57.5 \
--step-nb 1000 \
-d-sd 0.05 \
--render
