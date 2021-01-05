#/bin/bash.sh

python3.8 -m src \
--border wrap \
--view-dist 31 \
-tr 50 -bv 5 \
--error 0:3 \
-ror 1 -roa 31 \
-roo-var 1:1:10 --roo-step-duration 200 \
--step-nb 200 \
--render \
--verbose
