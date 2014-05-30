#!/bin/bash

DIR=$(cd $(dirname $0) && pwd)
TG_DIR="tg"
LIMIT="5000"
STEP="100"

mkfifo tg_pipe
cd "$TG_DIR"
./telegram -W < $DIR/tg_pipe > $DIR/output &
cd "$DIR"

for i in $(seq $LIMIT -$STEP 0); do
	echo -n ".";
	cmd="history NappiGram $STEP $i";
	# echo $cmd;
	echo $cmd > tg_pipe;
	sleep 5;
done

echo "quit" > tg_pipe
rm tg_pipe
