#! /bin/sh
cat /dev/random | head > /dev/null
REPETITIONS=35 EVENTS="-e r08:uk,r08:h,r09:uk,r09:h,r17:uk,r17:h" ./run_all.sh
REPETITIONS=35 EVENTS="-e r02:uk,r02:h,r05:uk,r05:h" ./run_all.sh
