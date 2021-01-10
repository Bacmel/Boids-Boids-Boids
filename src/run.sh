#!/usr/bin/bash

python3.8 -m sim \
--border none \
-tr 50 -v 5 \
-d-sd 10 \
-ror 1 \
-roo 16 \
-roa 31 \
--blindspot-direction -180 --blindspot-opening 90 \
--step-nb 1000 \
#--render
# -roo 16 \
