#!/usr/bin/bash

python3.8 -m sim \
--border none \
-tr 50 -v 5 \
-ror 1 \
-roo 11 \
-roa 22 \
--blindspot-direction -180 --blindspot-opening 90 \
--step-nb 500 \
-d-sd 0.05 \
--render
# --view-dist 31 \
# -roo 16 \
# 6 8 12
