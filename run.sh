#/bin/bash.sh

python3.8 -m src \
--border wrap \
--view-dist 31 \
-tr 50 -bv 5 \
--render \
--error 0:0 \
-ror 1 -roo 16 -roa 31 \
--step-nb 2000
