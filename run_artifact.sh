#! /bin/bash

if [ -z ${NUM_CORES+x} ]; then
	echo "Please set the environment variable NUM_CORES";
	exit 1;
fi

max_core_id=$((NUM_CORES - 1))
args=$@
for i in $( seq 0 $max_core_id )
do	
	tmux new-session -d -s artifact-core$i "taskset -c ${i} python3 run_artifact.py ${args} --num_cores ${NUM_CORES} --core_id ${i}"
done
